import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, ActiveLoop
from jinja2 import Environment, FileSystemLoader
import base64
import json

from actions.forms import ValidateKubernetesForm

def generate_dockerconfigjson(username, password, email, server):
    if not server.startswith("http"):
        server = server.rstrip('/')

    auth_str = f"{username}:{password}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    docker_config = {
        "auths": {
            server: {
                "username": username,
                "password": password,
                "email": email,
                "auth": auth_b64
            }
        }
    }
    docker_config_json = json.dumps(docker_config)
    print("GENERATED DOCKERCONFIG:", docker_config_json)
    encoded = base64.b64encode(docker_config_json.encode()).decode()
    print("📦 Base64 encoded .dockerconfigjson:\n", encoded)
    return encoded

class ActionGenerateKubernetesDeploymentDialoge(Action):
    def name(self) -> Text:
        return "action_generate_kubernetes_deployment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        def slot(name: str, default=None):
            return tracker.get_slot(name) or default

        app_name          = slot("kubernetes_app_name", "demo-app")
        image             = slot("kubernetes_image", "nginx")
        replicas          = slot("kubernetes_replicas", 1)
        container_port    = slot("kubernetes_container_port", 80)
        secret_name       = slot("kubernetes_secret_name", f"{app_name}-secret")

        raw_env           = slot("kubernetes_env_vars", "")
        env_vars: Dict[str, str] = {}
        if isinstance(raw_env, str):
            for pair in raw_env.split(","):
                if "=" in pair:
                    k, v = pair.strip().split("=", 1)
                    env_vars[k.strip()] = v.strip()
        elif isinstance(raw_env, dict):
            env_vars = raw_env

        tls_enabled       = slot("kubernetes_tls_enabled", False)
        tls_secret_name   = slot("kubernetes_tls_secret_name", f"{app_name}-tls")
        tls_issuer        = slot("kubernetes_tls_issuer", "letsencrypt-prod")
        domain_name       = slot("kubernetes_domain", f"{app_name}.example.com")

        ingress_enabled   = slot("kubernetes_ingress_enabled", False)
        ingress_paths     = slot("kubernetes_ingress_paths", [])
        ingress_class     = slot("ingress_class", "nginx")

        secret_enabled    = slot("kubernetes_secret_enabled", False)
        secretsraw           = slot("kubernetes_secrets", "")
        secrets = {secret_name: secretsraw}

        kubernetes_cpu_req     = slot("kubernetes_cpu_req", "250m")
        kubernetes_cpu_max     = slot("kubernetes_cpu_max", "500m")
        kubernetes_mem_req     = slot("kubernetes_mem_req", "256Mi")
        kubernetes_mem_max     = slot("kubernetes_mem_max", "512Mi")
        run_as_non_root        = slot("kubernetes_no_root_enabled", False)

        use_private_registry   = slot("use_private_registry", False)
        registry_server        = slot("docker_registry", "https://index.docker.io/v1/")
        registry_username      = slot("docker_username", "")
        registry_password      = slot("docker_password", "")
        registry_email         = slot("docker_email", "user@example.com")
        image_pull_secret_name = slot("image_pull_secret_name", f"{app_name}-pull-secret")

        dockerconfigjson = ""
        if use_private_registry:
            dockerconfigjson = generate_dockerconfigjson(
                username=registry_username,
                password=registry_password,
                email=registry_email,
                server=registry_server,
            )

        context = {
            "kubernetes_app_name": app_name,
            "image": image,
            "replicas": replicas,
            "container_port": container_port,
            "env_vars": env_vars,
            "tls_enabled": tls_enabled,
            "tls_secret_name": tls_secret_name,
            "tls_issuer": tls_issuer,
            "domain": domain_name,
            "ingress_enabled": ingress_enabled,
            "ingress_paths": ingress_paths,
            "ingress_class": ingress_class,
            "secret_enabled": secret_enabled,
            "secrets": secrets,
            "kubernetes_cpu_req": kubernetes_cpu_req,
            "kubernetes_cpu_max": kubernetes_cpu_max,
            "kubernetes_mem_req": kubernetes_mem_req,
            "kubernetes_mem_max": kubernetes_mem_max,
            "kubernetes_run_as_non_root": run_as_non_root,
            "use_private_registry": use_private_registry,
            "image_pull_secret_name": image_pull_secret_name,
            "dockerconfigjson": dockerconfigjson,
        }

        # Load templates from actions/templates/kubernetes/
        template_dir = os.path.join(os.path.dirname(__file__), "templates", "kubernetes")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Render function
        def render(template_name: str) -> str:
            return env.get_template(template_name).render(context).strip()

        rendered_parts: List[str] = []

        # Deployment manifest
        try:
            deployment_yaml = render("deployment.yaml.j2")
            rendered_parts.append(deployment_yaml)
        except Exception as e:
            dispatcher.utter_message(text=f"Could not render Deployment YAML: {e}")

        # Optional Secret manifest
        if secret_enabled:
            try:
                secret_yaml = render("secret.yaml.j2")
                rendered_parts.append(secret_yaml)
            except Exception as e:
                dispatcher.utter_message(text=f"Could not render Secret YAML: {e}")

        # Optional Ingress manifest
        if ingress_enabled:
            try:
                ingress_yaml = render("ingress.yaml.j2")
                rendered_parts.append(ingress_yaml)
            except Exception as e:
                dispatcher.utter_message(text=f"Could not render Ingress YAML: {e}")

        if use_private_registry:
            try:
                registry_secret = render("registry-secret.yaml.j2")
                rendered_parts.append(registry_secret)
            except Exception as e:
                dispatcher.utter_message(text=f"Could not render Registry Secret YAML: {e}")

        dispatcher.utter_message(text="Finished! Here are your Kubernetes manifests:")
        for yaml_text in rendered_parts:
            dispatcher.utter_message(text=f"*{yaml_text}*")

        dispatcher.utter_message(
            text="Now you can apply these with:\n")
        dispatcher.utter_message(
            text= "*kubectl apply -f deployment.yaml*")

        return [AllSlotsReset(), ActiveLoop(None)]