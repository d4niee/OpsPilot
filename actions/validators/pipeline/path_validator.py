import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class PathValidator:
    pattern = re.compile(r"^(\./)?[\w\-/]+$")

    def __init__(self, slot_name: str):
        self.slot_name = slot_name

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        path = str(value).strip()
        if self.pattern.fullmatch(path):
            return {self.slot_name: path}
        dispatcher.utter_message(response="utter_invalid_path")
        return {self.slot_name: None}
