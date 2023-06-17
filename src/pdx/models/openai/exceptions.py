from pdx.exceptions import ModelError, PromptError
import json


def handle_openai_request_error(status_code: int, content: str) -> None:
    try:
        formatted_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        formatted_content = content

    status_code_messages = {
        401: "Unauthorized: Authententication error, maybe due to incorrect API key or API key not part of organization.",
        429: "Model API Error: Rate limit, quota exceeded, or engine overload.",
        500: "The server had an error while processing your request.",
    }

    if isinstance(formatted_content, dict) and "error" in formatted_content:
        if formatted_content["error"]["message"] != "":
            _message = formatted_content["error"]["message"]
            raise ModelError(status_code, _message, "OPENAI-API-ERROR")

    if status_code in status_code_messages:
        _message = status_code_messages[status_code]
    elif isinstance(formatted_content, str):
        _message = formatted_content
    else:
        _message = "An unknown error has occurred."

    raise ModelError(status_code, _message, "OPENAI-API-ERROR")


def handle_openai_prompt_validation(prompt: str) -> None:
    '''
    TODO: Check if the prompt is valid for the model and API.
    At the moment, this is handled intrinsically by the Library.
    TO accomplish, we need to find outliers.
    '''
    pass
