from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from typing import Any, List, Dict
import os, yaml

CONFIG_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "docker_configs.yaml"
    )
)

with open(CONFIG_PATH, encoding="utf-8") as f:
    docker_configs: Dict[str, Any] = yaml.safe_load(f)

class BaseValidator:
    """
    Stellt get_available() zur Verfügung und Hilfsmethoden.
    """
    def _get_available(self, tracker: Tracker, field: str) -> List[str]:
        lang = tracker.get_slot("language")
        build_type = tracker.get_slot("build_type")
        return (
            docker_configs
            .get(lang, {})
            .get(build_type, {})
            .get("available", {})
            .get(field, [])
        )

    def reject(self, dispatcher: CollectingDispatcher, response: str) -> Dict[str, Any]:
        dispatcher.utter_message(response=response)
        return {self.slot_name: None}