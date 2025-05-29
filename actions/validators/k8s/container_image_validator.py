import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class ContainerImageValidator(BaseValidator):
    """
    Validator für den Slot 'kubernetes_image'.
    Erlaubt entweder:
      - offizielle Docker-Hub-Images (z.B. nginx:latest)
      - Registry-URLs (z.B. registry.example.com/repo/image:tag)
    """
    slot_name = "kubernetes_image"

    def validate(
        self,
        value: Any,
        slot_name: str,
        dispatcher: CollectingDispatcher,
    ) -> Dict[str, Any]:
        val = str(value).strip()
        # Muster für Docker Hub Image: name[:tag]
        official_pattern = r'^[a-z0-9]+(?:[._-][a-z0-9]+)*(?::[A-Za-z0-9._-]+)?$'
        # Muster für Registry-URL: domain[:port]/path/image[:tag]
        registry_pattern = (
            r'^(?:[A-Za-z0-9.-]+(?::\d+)?)/(?:[A-Za-z0-9._-]+/)*'
            r'[A-Za-z0-9._-]+(?::[A-Za-z0-9._-]+)?$'
        )

        if re.fullmatch(official_pattern, val) or re.fullmatch(registry_pattern, val):
            return {self.slot_name: val}

        dispatcher.utter_message(response="utter_invalid_container_image")
        return {self.slot_name: None}