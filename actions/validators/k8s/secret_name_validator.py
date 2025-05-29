import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class SecretNameValidator(BaseValidator):
    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]+", value):
            return {slot_name: value}
        dispatcher.utter_message(response="utter_invalid_secret_name")
        return {slot_name: None}