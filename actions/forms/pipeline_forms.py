from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


class ValidatePipelineForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pipeline_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Text]:
        return [
            "platform",
            "pipeline_name",
            "registry_url",
            "registry_username",
            "registry_password",
            "registry_repository_url",
            "deployment_name",
            "helm_path",
            "kubeconfig_path",
            "kube_context",
            "use_helm",
            "manifests_path",
            "namespace",
        ]

    async def validate_platform(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        val = str(slot_value).strip().lower()
        if val in ("github", "gitlab"):
            return {"platform": val}
        dispatcher.utter_message(response="utter_wrong_platform")
        return {"platform": None}

    async def validate_use_helm(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        val = str(slot_value).strip().lower()
        if val in ("yes", "y", "true", "1"):
            return {"use_helm": True}
        if val in ("no", "n", "false", "0"):
            return {"use_helm": False}
        dispatcher.utter_message(response="utter_wrong_use_helm")
        return {"use_helm": None}
