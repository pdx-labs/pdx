from pdx.exceptions import ModelError, PromptError
from pdx.models.anthropic import constants
import json


def handle_anthropic_prompt_validation(prompt: str) -> None:    
    if not prompt.startswith(constants.HUMAN_PROMPT):
        raise PromptError(
            f"Prompt must start with anthropic.HUMAN_PROMPT ({repr(constants.HUMAN_PROMPT)})"
        )
    if constants.AI_PROMPT not in prompt:
        raise PromptError(
            f"Prompt must contain anthropic.AI_PROMPT ({repr(constants.AI_PROMPT)})"
        )
    if prompt.endswith(" "):
        raise PromptError(f"Prompt must not end with a space character")


def handle_anthropic_request_error(status_code: int, content: str) -> None:
    try:
        formatted_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        formatted_content = content

    status_code_messages = {
        400: "Invalid request: there was an issue with the format or content of your request.",
        401: "Unauthorized: there's an issue with your API key.",
        403: "Forbidden: your API key does not have permission to use the specified resource.",
        429: "Your account has hit a rate limit.",
        500: "An unexpected error has occurred internal to Anthropic's systems.",
    }

    if status_code in status_code_messages:
        _message = status_code_messages[status_code]
    elif isinstance(formatted_content, dict) and "error" in formatted_content:
        _message = formatted_content["error"]
    elif isinstance(formatted_content, str):
        _message = formatted_content
    else:
        _message = "An unknown error has occurred."

    raise ModelError(status_code, _message, "ANTHROPIC-API-ERROR")
