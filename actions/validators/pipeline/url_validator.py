import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher

class UrlValidator:
    """Validiert HTTP/HTTPS-URLs"""
    def __init__(self, slot_name: str):
        self.slot_name = slot_name
        # erlaubt optional Pfad mit ':' für repository URL
        self.pattern = re.compile(r"^https?://[\w\.-]+(?::\d+)?(/[\w\-\./:]*)?$")

    def validate(self, value: Any, dispatcher: CollectingDispatcher) -> Dict[str, Any]:
        url = str(value).strip()
        if self.pattern.fullmatch(url):
            return {self.slot_name: url}
        dispatcher.utter_message(response="utter_invalid_registry_url")
        return {self.slot_name: None}