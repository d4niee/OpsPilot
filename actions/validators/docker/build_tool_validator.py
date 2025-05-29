from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class BuildToolValidator(BaseValidator):
    slot_name = "build_tool"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        val = str(value).strip().lower()
        available = self._get_available(tracker, self.slot_name)
        if val in available:
            return {self.slot_name: val}
        return self.reject(dispatcher, "utter_invalid_build_tool")