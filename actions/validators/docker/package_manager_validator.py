from typing import Any, List, Dict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from .base_validator import BaseValidator

class PackageManagerValidator(BaseValidator):
    slot_name = "package_manager"

    async def validate(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        val = str(value).strip().lower()
        supported = self._get_available(tracker, self.slot_name)
        if isinstance(supported, str):
            supported = [supported]
        if val in supported:
            return {self.slot_name: val}
        return self.reject(dispatcher, "utter_wrong_package_manager")