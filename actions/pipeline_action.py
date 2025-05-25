import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, ActiveLoop
from jinja2 import Environment, FileSystemLoader

from actions.forms import ValidatePipelineForm

class ActionGeneratePipelineManifest(Action):
    def name(self) -> Text:
        return "action_generate_cicd"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # All required slots have already been validated by ValidatePipelineForm
        platform              = tracker.get_slot("platform")             # 'github' or 'gitlab'
        pipeline_name         = tracker.get_slot("pipeline_name") or "default-pipeline"
        registry_url          = tracker.get_slot("registry_url")
        registry_username     = tracker.get_slot("registry_username")
        registry_password     = tracker.get_slot("registry_password")
        registry_repository_url = tracker.get_slot("registry_repository_url")
        deployment_name       = tracker.get_slot("deployment_name")
        helm_path             = tracker.get_slot("helm_path")
        kubeconfig_path       = tracker.get_slot("kubeconfig_path")
        kube_context          = tracker.get_slot("kube_context")
        use_helm              = tracker.get_slot("use_helm") or False
        manifests_path        = tracker.get_slot("manifests_path")
        namespace             = tracker.get_slot("namespace")

        # Build context for Jinja
        context = {
            "platform": platform,
            "pipeline_name": pipeline_name,
            "registry_url": registry_url,
            "registry_username": registry_username,
            "registry_password": registry_password,
            "registry_repository_url": registry_repository_url,
            "deployment_name": deployment_name,
            "helm_path": helm_path,
            "kubeconfig_path": kubeconfig_path,
            "kube_context": kube_context,
            "use_helm": use_helm,
            "manifests_path": manifests_path,
            "namespace": namespace,
        }

        # Load and render the appropriate template
        template_dir = os.path.join(os.path.dirname(__file__), "templates", "pipeline-templates")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        if platform.lower() == "github":
            template = env.get_template("github_actions.yml.j2")
        else:  # gitlab
            template = env.get_template("gitlab-ci.yml.j2")

        rendered = template.render(context).strip().replace("\n\n", "\n")

        # Send the final manifest
        dispatcher.utter_message(text="Here is your final CI/CD manifest:")
        dispatcher.utter_message(text=f"*{rendered}*")

        # Reset all slots and end the form
        return [AllSlotsReset(), ActiveLoop(None)]
