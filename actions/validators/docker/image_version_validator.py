import re
from typing import Any, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class ImageVersionValidator(BaseValidator):
    slot_name = "image_version"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        val = str(value).strip()
        available: List[str] = self._get_available(tracker, self.slot_name)
        if available:
            if val in available:
                return {self.slot_name: val}
            return self.reject(dispatcher, "utter_invalid_image_version")
        if re.fullmatch(r"[A-Za-z0-9._-]+", val):
            return {self.slot_name: val}
        return self.reject(dispatcher, "utter_invalid_image_version")