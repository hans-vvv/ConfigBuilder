import os
from pathlib import Path

from dotenv import load_dotenv

# Resolve project root (…/MerakiParser)
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env", override=False)  # load once for the whole app

def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Set it in your OS env or in {ROOT / '.env'}"
        )
    return val

# Exported constants you can import anywhere
OPENAI_API_KEY: str = _require("OPENAI_API_KEY")
MERAKI_API_KEY: str = _require("MERAKI_API_KEY")
