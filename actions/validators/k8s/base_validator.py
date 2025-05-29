from rasa_sdk.executor import CollectingDispatcher
from typing import List, Any, Dict

class BaseValidator:
    """
    Basisklasse mit Helfern für Followup-Reset.
    """
    slot_name: str

    def reject(self, dispatcher: CollectingDispatcher, response: str) -> Dict[str, Any]:
        dispatcher.utter_message(response=response)
        return {self.slot_name: None}

    def reset_followups(self, followups: List[str]) -> Dict[str, Any]:
        # setzt alle Followup-Slots auf None
        return {slot: None for slot in followups}