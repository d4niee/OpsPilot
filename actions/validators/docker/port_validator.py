from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class PortValidator(BaseValidator):
    slot_name = "port"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        if isinstance(value, str) and value.isdigit():
            port = int(value)
            if 1 <= port <= 65535:
                return {self.slot_name: port}
        return self.reject(dispatcher, "utter_invalid_port")