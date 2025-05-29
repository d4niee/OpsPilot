import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class MemValidator(BaseValidator):
    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        if isinstance(value, str) and re.fullmatch(r"\d+Mi", value):
            return {slot_name: value}
        dispatcher.utter_message(response="utter_invalid_mem_req_or_max")
        return {slot_name: None}