from __future__ import annotations

import os

import logfire
from dotenv import load_dotenv


def configure_logfire() -> None:
    """
    Configure Logfire + environment for Pydantic-AI & Gemini.

    - Loads .env from the repo root.
    - Mirrors GEMINI_API_KEY → GOOGLE_API_KEY (required by Pydantic-AI's Gemini model).
    - Calls logfire.configure() and logfire.instrument_pydantic_ai().
    """
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and not os.getenv("GOOGLE_API_KEY"):
        # Required by pydantic-ai's GoogleModel
        os.environ["GOOGLE_API_KEY"] = gemini_key

    # Logfire reads the write token from .logfire/ created by:
    #   logfire auth
    #   logfire projects use agentic-ai
    logfire.configure()
    logfire.instrument_pydantic_ai()
