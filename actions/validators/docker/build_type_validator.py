from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator
from typing import Dict, Any

class BuildTypeValidator(BaseValidator):
    slot_name = "build_type"

    async def validate(self,
                       value: Any,
                       dispatcher: CollectingDispatcher,
                       tracker: Tracker,
                       domain: Dict[str, Any]
                       ) -> Dict[str, Any]:
        val = str(value).strip().lower()
        if val in ["basic", "multi-stage", "multistage"]:
            norm = "multi-stage" if val in ["multi-stage", "multistage"] else "basic"
            return {self.slot_name: norm}
        return self.reject(dispatcher, "utter_wrong_dockerfile_type")