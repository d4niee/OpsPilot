from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import os
import yaml
import re

CONFIG_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "docker_configs.yaml"
    )
)

with open(CONFIG_PATH, "r", encoding="utf-8") as cfg_file:
    docker_configs: Dict[str, Any] = yaml.safe_load(cfg_file)

class ValidateDockerfileForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_dockerfile_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Text]:
        lang = tracker.get_slot("language")
        slots: List[Text] = [
            "build_type",
            "language",
            "image_version",
            "app_name",
            "port",
        ]
        if lang == "react":
            slots.append("package_manager")
        elif lang == "springboot":
            slots.extend(["build_tool", "jar_dest"])
        elif lang == "nodejs":
            slots.append("entrypoint")
        return slots
    
    def _get_available(self, tracker: Tracker, field: str) -> List[str]:
        lang       = tracker.get_slot("language")
        build_type = tracker.get_slot("build_type")
        return docker_configs \
            .get(lang, {}) \
            .get(build_type, {}) \
            .get("available", {}) \
            .get(field, [])

    async def validate_package_manager(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = str(slot_value).strip().lower()
        lang = tracker.get_slot("language")
        build_type = tracker.get_slot("build_type")
        supported = docker_configs \
                        .get(lang, {}) \
                        .get(build_type, {}) \
                        .get("available", {}) \
                        .get("package_manager", [])
        if isinstance(supported, str):
            supported = [supported]
        if val in supported:
            return {"package_manager": val}
        dispatcher.utter_message(response="utter_wrong_package_manager")
        return {"package_manager": None}
    
    async def validate_app_name(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        name = str(slot_value).strip()
        if re.fullmatch(r"[A-Za-z0-9_-]+", name):
            return {"app_name": name}
        dispatcher.utter_message(response="utter_invalid_app_name")
        return {"app_name": None}


    async def validate_image_version(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        val = str(slot_value).strip()
        avail = self._get_available(tracker, "image_version")
        if avail:
            if val in avail:
                return {"image_version": val}
            dispatcher.utter_message(response="utter_invalid_app_name")
            return {"image_version": None}
        if re.fullmatch(r"[A-Za-z0-9._-]+", val):
            return {"image_version": val}
        dispatcher.utter_message(response="utter_invalid_image_version")
        return {"image_version": None}
    

    async def validate_build_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = str(slot_value).strip().lower()
        if val in ["basic", "multi-stage", "multistage"]:
            normalized = "multi-stage" if val in ["multi-stage", "multistage"] else "basic"
            return {"build_type": normalized}
        dispatcher.utter_message(response="utter_wrong_dockerfile_type")
        return {"build_type": None}
    
    async def validate_build_tool(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val   = str(slot_value).strip().lower()
        avail = self._get_available(tracker, "build_tool")
        if val in avail:
            return {"build_tool": val}
        dispatcher.utter_message(response="utter_invalid_build_tool")
        return {"build_tool": None}
    
    async def validate_language(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = str(slot_value).strip().lower()
        supported = list(docker_configs.keys())

        if val in supported:
            return {"language": val}
        # Antwort, wenn die Sprache nicht unterstützt wird
        dispatcher.utter_message(response="utter_wrong_language")
        return {"language": None}

    async def validate_port(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if isinstance(slot_value, str) and slot_value.isdigit():
            port = int(slot_value)
            if 1 <= port <= 65535:
                return {"port": port}
        dispatcher.utter_message(response="utter_invalid_port")
        return {"port": None}
