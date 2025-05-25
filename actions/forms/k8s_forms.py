from typing import Any, Text, Dict, List
import re
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


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
            "use_private_registry",
            "kubernetes_replicas",
            "kubernetes_container_port",
            "kubernetes_env_vars",
            "kubernetes_secret_enabled",
            "kubernetes_ingress_enabled",
        ]
        if tracker.get_slot("use_private_registry"):
            required += [
                "image_pull_secret_name",
                "docker_registry",
                "docker_username",
                "docker_password",
                "docker_email",
            ]
        if tracker.get_slot("kubernetes_tls_enabled"):
            required += ["kubernetes_tls_secret_name", "kubernetes_tls_issuer"]
        if tracker.get_slot("kubernetes_secret_enabled"):
            required += ["kubernetes_secret_name", "kubernetes_secrets"]
        if tracker.get_slot("kubernetes_ingress_enabled"):
            required += [
                "ingress_class",
                "kubernetes_domain",
                "kubernetes_ingress_paths",
            ]
            if tracker.get_slot("kubernetes_tls_enabled"):
                required += ["kubernetes_tls_secret_name", "kubernetes_tls_issuer"]
        required += [
            "kubernetes_cpu_req",
            "kubernetes_cpu_max",
            "kubernetes_mem_req",
            "kubernetes_mem_max",
            "kubernetes_no_root_enabled",
        ]
        return required

    def _validate_bool_and_reset_followups(
        self,
        value: Any,
        slot_name: str,
        followups: List[str],
        dispatcher: CollectingDispatcher,
    ) -> Dict[Text, Any]:
        if isinstance(value, str):
            val = value.strip().lower()
            if val in ["yes", "true"]:
                return {slot_name: True, **{slot: None for slot in followups}}
            if val in ["no", "false"]:
                return {slot_name: False}
        if isinstance(value, bool):
            return {slot_name: value}
        dispatcher.utter_message(text="Please answer with 'yes' or 'no'.")
        return {slot_name: None}

    def _validate_cpu(
        self,
        value: Any,
        slot_key: str,
        dispatcher: CollectingDispatcher,
    ) -> Dict[Text, Any]:
        if isinstance(value, str) and re.fullmatch(r"\d+m", value):
            return {slot_key: value}
        dispatcher.utter_message(response="utter_invalid_cpu_req_or_max")
        return {slot_key: None}

    def _validate_mem(
        self,
        value: Any,
        slot_key: str,
        dispatcher: CollectingDispatcher,
    ) -> Dict[Text, Any]:
        if isinstance(value, str) and re.fullmatch(r"\d+Mi", value):
            return {slot_key: value}
        dispatcher.utter_message(response="utter_invalid_mem_req_or_max")
        return {slot_key: None}

    def _validate_secret_name(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
    ) -> Dict[Text, Any]:
        pattern = r"^[A-Za-z0-9_-]+$"
        slot_key = tracker.get_slot("requested_slot")
        if isinstance(value, str) and re.fullmatch(pattern, value):
            return {slot_key: value}
        dispatcher.utter_message(response="utter_invalid_secret_name")
        return {slot_key: None}

    def validate_kubernetes_replicas(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if isinstance(value, str) and value.isdigit() and int(value) > 0:
            return {"kubernetes_replicas": int(value)}
        dispatcher.utter_message(response="utter_invalid_replicas")
        return {"kubernetes_replicas": None}

    def validate_kubernetes_container_port(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            port = int(value)
            if 1 <= port <= 65535:
                return {"kubernetes_container_port": port}
        except (ValueError, TypeError):
            pass
        dispatcher.utter_message(response="utter_invalid_port")
        return {"kubernetes_container_port": None}

    validate_kubernetes_cpu_req = lambda self, value, dispatcher, tracker, domain: self._validate_cpu(value, "kubernetes_cpu_req", dispatcher)
    validate_kubernetes_cpu_max = lambda self, value, dispatcher, tracker, domain: self._validate_cpu(value, "kubernetes_cpu_max", dispatcher)
    validate_kubernetes_mem_req = lambda self, value, dispatcher, tracker, domain: self._validate_mem(value, "kubernetes_mem_req", dispatcher)
    validate_kubernetes_mem_max = lambda self, value, dispatcher, tracker, domain: self._validate_mem(value, "kubernetes_mem_max", dispatcher)

    def validate_docker_registry(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        pattern = r"^https?://[\w\.-]+(?::\d+)?(/[\w\-\./]*)?$"
        if isinstance(value, str) and re.fullmatch(pattern, value):
            return {"docker_registry": value}
        dispatcher.utter_message(response="utter_invalid_url")
        return {"docker_registry": None}

    def validate_docker_email(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if isinstance(value, str) and re.fullmatch(email_pattern, value):
            return {"docker_email": value}
        dispatcher.utter_message(response="utter_invalid_email")
        return {"docker_email": None}

    # Secret name validators
    validate_kubernetes_app_name = lambda self, value, dispatcher, tracker, domain: self._validate_secret_name(value, dispatcher, tracker)
    validate_image_pull_secret_name = lambda self, value, dispatcher, tracker, domain: self._validate_secret_name(value, dispatcher, tracker)
    validate_kubernetes_tls_secret_name = lambda self, value, dispatcher, tracker, domain: self._validate_secret_name(value, dispatcher, tracker)
    validate_kubernetes_secret_name = lambda self, value, dispatcher, tracker, domain: self._validate_secret_name(value, dispatcher, tracker)

    validate_kubernetes_tls_enabled = lambda self, value, dispatcher, tracker, domain: self._validate_bool_and_reset_followups(value, "kubernetes_tls_enabled", ["kubernetes_tls_secret_name", "kubernetes_tls_issuer"], dispatcher)
    validate_kubernetes_secret_enabled = lambda self, value, dispatcher, tracker, domain: self._validate_bool_and_reset_followups(value, "kubernetes_secret_enabled", ["kubernetes_secret_name", "kubernetes_secrets"], dispatcher)
    validate_kubernetes_ingress_enabled = lambda self, value, dispatcher, tracker, domain: self._validate_bool_and_reset_followups(value, "kubernetes_ingress_enabled", ["ingress_class", "kubernetes_domain", "kubernetes_ingress_paths"], dispatcher)
    validate_kubernetes_no_root_enabled = lambda self, value, dispatcher, tracker, domain: self._validate_bool_and_reset_followups(value, "kubernetes_no_root_enabled", [], dispatcher)
    validate_use_private_registry = lambda self, value, dispatcher, tracker, domain: self._validate_bool_and_reset_followups(value, "use_private_registry", ["docker_registry", "docker_username", "docker_password", "docker_email", "image_pull_secret_name"], dispatcher)
