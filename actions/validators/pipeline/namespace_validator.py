import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class NamespaceValidator:
    pattern = re.compile(r"^[A-Za-z0-9_-]+$")

    def __init__(self, slot_name: str):
        self.slot_name = slot_name

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        ns = str(value).strip()
        if self.pattern.fullmatch(ns):
            return {self.slot_name: ns}
        dispatcher.utter_message(response="utter_invalid_namespace")
        return {self.slot_name: None}
