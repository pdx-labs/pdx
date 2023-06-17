class PDXError(Exception):
    """Base class for all PDX Errors."""
    pass


class AgentError(PDXError):
    """Base class for all agent exceptions."""

    def __init__(self, message, value=None):
        self.message = message
        self.value = value

    def __str__(self):
        if self.value is None:
            return f"{self.message}"
        else:
            return f"{self.message}: {self.value}"


class PromptError(PDXError):
    """Base class for all prompt exceptions."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"


class ModelError(PDXError):
    """Base class for all model exceptions."""

    def __init__(self, status_code, message, prefix=None):
        self.status_code = status_code
        self.message = message
        self.prefix = prefix

    def __str__(self):
        if self.prefix:
            return f"{self.prefix}::{self.status_code}: {self.message}"
        else:
            return f"{self.status_code}: {self.message}"
