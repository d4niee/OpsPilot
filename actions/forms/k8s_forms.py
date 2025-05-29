from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

from actions.validators.k8s.bool_validator import BoolValidator
from actions.validators.k8s.cpu_validator import CpuValidator
from actions.validators.k8s.mem_validator import MemValidator
from actions.validators.k8s.secret_name_validator import SecretNameValidator
from actions.validators.k8s.replicas_validator import ReplicasValidator
from actions.validators.k8s.port_validator import PortValidator
from actions.validators.k8s.url_validator import UrlValidator
from actions.validators.k8s.email_validator import EmailValidator
from actions.validators.k8s.env_vars_validator import EnvVarsValidator
from actions.validators.k8s.container_image_validator import ContainerImageValidator

# Mapping Slotname → Validator-Funktion
VALIDATORS = {
    # Bool
    "use_private_registry": BoolValidator(),
    "kubernetes_tls_enabled": BoolValidator(),
    "kubernetes_secret_enabled": BoolValidator(),
    "kubernetes_ingress_enabled": BoolValidator(),
    "kubernetes_no_root_enabled": BoolValidator(),

    # CPU / Memory
    "kubernetes_cpu_req": CpuValidator(),
    "kubernetes_cpu_max": CpuValidator(),
    "kubernetes_mem_req": MemValidator(),
    "kubernetes_mem_max": MemValidator(),

    # Secret-Namen
    "kubernetes_app_name": SecretNameValidator(),
    "image_pull_secret_name": SecretNameValidator(),
    "kubernetes_tls_secret_name": SecretNameValidator(),
    "kubernetes_secret_name": SecretNameValidator(),

    # Replicas / Port / URL / Email
    "kubernetes_replicas": ReplicasValidator(),
    "kubernetes_container_port": PortValidator(),
    "docker_registry": UrlValidator(),
    "docker_email": EmailValidator(),
    "kubernetes_env_vars": EnvVarsValidator(),
    "kubernetes_image": ContainerImageValidator(),

}

# Optionale Follow-ups bei TRUE-Slots
FOLLOWUPS = {
    "use_private_registry": [
        "docker_registry", "docker_username", "docker_password", "docker_email", "image_pull_secret_name"
    ],
    "kubernetes_tls_enabled": ["kubernetes_tls_secret_name", "kubernetes_tls_issuer"],
    "kubernetes_secret_enabled": ["kubernetes_secret_name", "kubernetes_secrets"],
    "kubernetes_ingress_enabled": [
        "ingress_class", "kubernetes_domain", "kubernetes_ingress_paths"
    ],
}

class ValidateKubernetesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_kubernetes_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Text]:
        required: List[Text] = [
            "kubernetes_app_name",
            "kubernetes_image",
            "use_private_registry",  # zuerst die Registry-Entscheidung
        ]

        # Wenn private Registry → sofort die Details abfragen
        if tracker.get_slot("use_private_registry"):
            required += [
                "docker_registry",
                "docker_username",
                "docker_password",
                "docker_email",
                "image_pull_secret_name",
            ]

        # danach die allgemeinen Deployment-Parameter
        required += [
            "kubernetes_replicas",
            "kubernetes_container_port",
            "kubernetes_env_vars",
            "kubernetes_secret_enabled",   # Frage nach Secret-Erstellung
        ]

        # Wenn Secret erstellt werden soll → sofort Name + Werte
        if tracker.get_slot("kubernetes_secret_enabled"):
            required += [
                "kubernetes_secret_name",
                "kubernetes_secrets",
            ]

        # weiter mit Ressourcen-Limits
        required += [
            "kubernetes_cpu_req",
            "kubernetes_cpu_max",
            "kubernetes_mem_req",
            "kubernetes_mem_max",
            "kubernetes_no_root_enabled",
            "kubernetes_ingress_enabled",  # Frage nach Ingress
        ]

        # Wenn Ingress erwünscht → direkt Ingress-Details
        if tracker.get_slot("kubernetes_ingress_enabled"):
            required += [
                "ingress_class",
                "kubernetes_domain",
                "kubernetes_ingress_paths",
            ]
            # optional TLS direkt anschließend
            if tracker.get_slot("kubernetes_tls_enabled"):
                required += [
                    "kubernetes_tls_secret_name",
                    "kubernetes_tls_issuer",
                ]

        return required

# Dynamisch Validatoren zuweisen
def create_validator(slot: str, validator_obj):
    async def validate_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # Spezialfall Bool mit Follow-ups
        if isinstance(validator_obj, BoolValidator):
            followup = FOLLOWUPS.get(slot, [])
            return validator_obj.validate(slot_value, slot, followup, dispatcher)
        # Andere: CPU, MEM etc.
        return validator_obj.validate(slot_value, slot, dispatcher)
    return validate_slot

# Methoden zur Klasse hinzufügen
for slot_name, validator in VALIDATORS.items():
    method = create_validator(slot_name, validator)
    setattr(ValidateKubernetesForm, f"validate_{slot_name}", method)