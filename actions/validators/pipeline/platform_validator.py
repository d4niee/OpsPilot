from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class PlatformValidator:
    def __init__(self, slot_name: str = "platform"):
        self.slot_name = slot_name

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        val = str(value).strip().lower()
        if val in ("github", "gitlab"):
            return {self.slot_name: val}
        dispatcher.utter_message(response="utter_invalid_platform")
        return {self.slot_name: None}
