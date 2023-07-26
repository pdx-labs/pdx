from dataclasses import dataclass
from pdx.version import __version__


@dataclass
class PDXMetadata:
    version: str
