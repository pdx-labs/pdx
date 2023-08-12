from pdx.exceptions import ModelError, PromptError
import json


def handle_elevenlabs_prompt_validation(prompt: str) -> None:
    pass


def handle_elevenlabs_request_error(status_code: int, content: str) -> None:
    try:
        formatted_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        formatted_content = content

    status_code_messages = {
        400: "Bad request: there was an issue with the format or content of your request.",
        401: "Unauthorized: there's an issue with your API key.",
        498: "Your request has been blocked.",
        500: "An unexpected error has occurred internal to Eleben Labs' systems.",
    }

    if status_code in status_code_messages:
        _message = status_code_messages[status_code]
    elif isinstance(formatted_content, dict) and "error" in formatted_content:
        _message = formatted_content["error"]
    elif isinstance(formatted_content, str):
        _message = formatted_content
    else:
        _message = "An unknown error has occurred."

    raise ModelError(status_code, _message, "ELEVENLABS-API-ERROR")
