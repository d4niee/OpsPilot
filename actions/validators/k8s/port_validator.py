from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class PortValidator(BaseValidator):
    slot_name = "kubernetes_container_port"

    def validate(self, value: Any, slot_name: str, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        try:
            port = int(value)
            if 1 <= port <= 65535:
                return {slot_name: port}
        except (ValueError, TypeError):
            pass
        dispatcher.utter_message(response="utter_invalid_port")
        return {slot_name: None}