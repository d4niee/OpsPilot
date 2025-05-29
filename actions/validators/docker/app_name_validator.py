import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class AppNameValidator(BaseValidator):
    slot_name = "app_name"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        name = str(value).strip()
        if re.fullmatch(r"[A-Za-z0-9_-]+", name):
            return {self.slot_name: name}
        return self.reject(dispatcher, "utter_invalid_app_name")