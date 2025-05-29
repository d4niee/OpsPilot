from typing import Any, List, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class BoolValidator(BaseValidator):
    """Validiert Bool-Slots mit Yes/No und resettet Followups"""
    def validate(
        self,
        value: Any,
        slot_name: str,
        followups: List[str],
        dispatcher: CollectingDispatcher,
    ) -> Dict[str, Any]:
        if isinstance(value, str):
            val = value.strip().lower()
            if val in ["yes", "true"]:
                return {slot_name: True, **self.reset_followups(followups)}
            if val in ["no", "false"]:
                return {slot_name: False}
        if isinstance(value, bool):
            return {slot_name: value}
        dispatcher.utter_message(text="Please answer with 'yes' or 'no'.")
        return {slot_name: None}