from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class ReplicasValidator(BaseValidator):
    slot_name = "kubernetes_replicas"

    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        if isinstance(value, str) and value.isdigit() and int(value) > 0:
            return {slot_name: int(value)}
        dispatcher.utter_message(response="utter_invalid_replicas")
        return {slot_name: None}