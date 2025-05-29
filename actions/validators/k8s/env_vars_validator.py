import re
from typing import Any, Dict
from rasa_sdk.executor import CollectingDispatcher
from .base_validator import BaseValidator

class EnvVarsValidator(BaseValidator):
    """
    Validator für den Slot 'kubernetes_env_vars'.
    Akzeptiert entweder:
      - Eine kommaseparierte Liste key=value-Paare
      - Den Wert 'skip', um diesen Schritt zu überspringen
    """
    slot_name = "kubernetes_env_vars"

    def validate(
        self,
        value: Any,
        slot_name: str,
        dispatcher: CollectingDispatcher,
    ) -> Dict[str, Any]:
        # Skip-Fall: einfach übernehmen
        if isinstance(value, str) and value.strip().lower() == "skip" or "no" or "n" or "cancel":
            return {self.slot_name: "skip"}

        pattern = r"^[A-Za-z_][A-Za-z0-9_]*=[^=,]+(,[A-Za-z_][A-Za-z0-9_]*=[^=,]+)*$"
        if isinstance(value, str) and re.fullmatch(pattern, value.strip()):
            return {self.slot_name: value.strip()}

        dispatcher.utter_message(response="utter_invalid_env_vars")
        return {self.slot_name: None}
