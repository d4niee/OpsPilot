import os
import yaml
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, ActiveLoop
from jinja2 import Environment, FileSystemLoader

from actions.forms import ValidateDockerfileForm

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "docker_configs.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as cfg_file:
    docker_configs: Dict[str, Any] = yaml.safe_load(cfg_file)


class ActionGenerateDockerfile(Action):
    def name(self) -> Text:
        return "action_generate_dockerfile"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        language = tracker.get_slot("language") or "react"
        build_type = tracker.get_slot("build_type") or "basic"
        app_name = tracker.get_slot("app_name") or "demo-app"

        config = docker_configs.get(language, {}).get(build_type)
        if not config:
            dispatcher.utter_message(
                text=f"❌ Sorry, Dockerfiles für '{language}' mit Typ '{build_type}' sind noch in Arbeit."
            )
            return [
                SlotSet(slot, None)
                for slot in ["build_type", "language", "image_version",
                             "package_manager", "port", "app_name",
                             "build_tool", "jar_dest"]
            ]

        defaults = config["defaults"]
        image_version   = tracker.get_slot("image_version")   or defaults.get("image_version")
        package_manager = tracker.get_slot("package_manager") or defaults.get("package_manager")
        port            = tracker.get_slot("port")            or defaults.get("port")
        build_tool      = tracker.get_slot("build_tool")      or defaults.get("build_tool")
        jar_dest        = tracker.get_slot("jar_dest")        or defaults.get("jar_dest", "app.jar")
        entrypoint      = tracker.get_slot("entrypoint")      or defaults.get("entrypoint", "app.js")

        context = {
            "image_version":   image_version,
            "package_manager": package_manager,
            "port":            port,
            "app_name":        app_name,
            "build_tool":      build_tool,
            "jar_dest":        jar_dest,
            "entrypoint":      entrypoint
        }

        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template(config["template"])
        dockerfile = template.render(context).strip().replace("\n\n", "\n")

        dispatcher.utter_message(text="Finished! 🎉 Here is your Dockerfile for your application:")
        dispatcher.utter_message(text=f"*{dockerfile}*")

        return [AllSlotsReset(), ActiveLoop(None)]
