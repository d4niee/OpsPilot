import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class EntrypointValidator(BaseValidator):
    """
    Validator for the 'entrypoint' slot, ensuring the filename ends with a valid extension
    based on the chosen language (e.g., .py for Flask, .js for Node.js).
    """
    slot_name = "entrypoint"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        val = str(value).strip()
        language = tracker.get_slot("language") or ""
        ext_map = {
            "flask": ".py",
            "nodejs": ".js",
            "springboot": ".jar",
        }
        expected_ext = ext_map.get(language.lower()) if isinstance(language, str) else None

        if expected_ext and val.lower().endswith(expected_ext):
            return {self.slot_name: val}

        if not expected_ext and re.fullmatch(r"[^\s]+\.[A-Za-z0-9]+", val):
            return {self.slot_name: val}

        dispatcher.utter_message(response="utter_invalid_entrypoint")
        return {self.slot_name: None}