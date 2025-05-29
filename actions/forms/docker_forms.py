from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

from actions.validators.docker.build_type_validator import BuildTypeValidator
from actions.validators.docker.language_validator import LanguageValidator
from actions.validators.docker.package_manager_validator import PackageManagerValidator
from actions.validators.docker.app_name_validator import AppNameValidator
from actions.validators.docker.image_version_validator import ImageVersionValidator
from actions.validators.docker.build_tool_validator import BuildToolValidator
from actions.validators.docker.port_validator import PortValidator
from actions.validators.docker.entrypoint_validator import EntrypointValidator

VALIDATORS = {
    "build_type": BuildTypeValidator(),
    "language": LanguageValidator(),
    "package_manager": PackageManagerValidator(),
    "app_name": AppNameValidator(),
    "image_version": ImageVersionValidator(),
    "build_tool": BuildToolValidator(),
    "port": PortValidator(),
    "entrypoint": EntrypointValidator(),
}

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
        required = [
            "build_type",
            "language",
            "image_version",
            "app_name",
            "port",
        ]
        lang = tracker.get_slot("language")
        if lang == "react":
            required.append("package_manager")
        elif lang == "springboot":
            required.extend(["build_tool", "jar_dest"])
        elif lang in ["nodejs", "flask"]:
            required.append("entrypoint")
        return required

def create_slot_validator(slot_name, validator):
    async def validate_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return await validator.validate(slot_value, dispatcher, tracker, domain)
    return validate_slot

for slot, validator in VALIDATORS.items():
    method = create_slot_validator(slot, validator)
    setattr(ValidateDockerfileForm, f"validate_{slot}", method)
