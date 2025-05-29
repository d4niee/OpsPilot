from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from typing import Any, Dict, List
from .base_validator import BaseValidator, docker_configs

class LanguageValidator(BaseValidator):
    slot_name = "language"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        val = str(value).strip().lower()
        supported: List[str] = list(docker_configs.keys())
        if val in supported:
            return {self.slot_name: val}
        return self.reject(dispatcher, "utter_wrong_language")