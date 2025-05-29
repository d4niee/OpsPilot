import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class EmailValidator(BaseValidator):
    slot_name = "docker_email"

    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if isinstance(value, str) and re.fullmatch(pattern, value):
            return {self.slot_name: value}
        dispatcher.utter_message(response="utter_invalid_email")
        return {self.slot_name: None}