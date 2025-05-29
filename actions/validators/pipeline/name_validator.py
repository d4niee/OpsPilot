import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class NameValidator:
    """Validiert alphanumerische Namen mit Unterstrich/Bindestrich"""
    def __init__(self, slot_name: str):
        self.slot_name = slot_name
        self.pattern = re.compile(r"^[A-Za-z0-9_-]+$")

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        name = str(value).strip()
        if self.pattern.fullmatch(name):
            return {self.slot_name: name}
        dispatcher.utter_message(response="utter_invalid_pipeline_or_deployment_name")
        return {self.slot_name: None}