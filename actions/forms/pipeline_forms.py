from typing import Any, Text, Dict, List
from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.validators.pipeline.bool_validator import BoolValidator
from actions.validators.pipeline.platform_validator import PlatformValidator
from actions.validators.pipeline.name_validator import NameValidator
from actions.validators.pipeline.url_validator import UrlValidator
from actions.validators.pipeline.path_validator import PathValidator
from actions.validators.pipeline.namespace_validator import NamespaceValidator

VALIDATORS = {
    "test_stage_enabled": BoolValidator("test_stage_enabled"),
    "security_scans_enabled": BoolValidator("security_scans_enabled"),
    "deploy_stage_enabled": BoolValidator("deploy_stage_enabled"),
    "use_helm": BoolValidator("use_helm"),
    "platform": PlatformValidator("platform"),
    "pipeline_name": NameValidator("pipeline_name"),
    "deployment_name": NameValidator("deployment_name"),
    "registry_url": UrlValidator("registry_url"),
    "registry_repository_url": UrlValidator("registry_repository_url"),
    "helm_path": PathValidator("helm_path"),
    "manifests_path": PathValidator("manifests_path"),
    "kubeconfig_path": PathValidator("kubeconfig_path"),
    "namespace": NamespaceValidator("namespace"),
}

class ValidateCICDForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_cicd_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Text]:
        required = [
            "platform",
            "pipeline_name",
            "test_stage_enabled",
            "security_scans_enabled",
            "deploy_stage_enabled",
        ]

        if tracker.get_slot("deploy_stage_enabled"):
            required.append("use_helm")
            use_helm = tracker.get_slot("use_helm")

            if use_helm is True:
                required.append("helm_path")
            elif use_helm is False:
                required.append("manifests_path")

            required += [
                "deployment_name",
                "kubeconfig_path",
                "kube_context",
                "namespace",
            ]

        required += [
            "registry_url",
            "registry_repository_url",
        ]

        return required


def create_validator(slot: str, validator_obj):
    async def validate_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if hasattr(validator_obj, "validate"):
            if hasattr(validator_obj, "slot_name"):
                return validator_obj.validate(slot_value, dispatcher)
            else:
                return validator_obj.validate(slot_value, slot, dispatcher)
        return {slot: slot_value}
    return validate_slot

for slot_name, validator in VALIDATORS.items():
    method = create_validator(slot_name, validator)
    setattr(ValidateCICDForm, f"validate_{slot_name}", method)
