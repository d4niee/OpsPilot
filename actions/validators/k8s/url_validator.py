import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class UrlValidator(BaseValidator):
    slot_name = "docker_registry"

    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        pattern = r"^https?://[\w\.-]+(?::\d+)?([/\w\-\./]*)?$"
        if isinstance(value, str) and re.fullmatch(pattern, value):
            return {self.slot_name: value}
        dispatcher.utter_message(response="utter_invalid_url")
        return {self.slot_name: None}