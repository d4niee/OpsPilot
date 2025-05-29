from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class BoolValidator:
    """Validiert Slots auf True/False aus Yes/No-Antworten"""

    def __init__(self, slot_name: str):
        self.slot_name = slot_name

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        val = str(value).strip().lower() if isinstance(value, str) else None
        if val in ("yes", "y", "true", "1"):
            return {self.slot_name: True}
        if val in ("no", "n", "false", "0"):
            return {self.slot_name: False}
        dispatcher.utter_message(response="utter_invalid_boolean")
        return {self.slot_name: None}
