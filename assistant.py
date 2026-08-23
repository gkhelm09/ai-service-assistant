"""AI assistant for biomedical field service troubleshooting.

Calls the OpenAI API and returns structured troubleshooting guidance.
"""

from __future__ import annotations

import json
import os
import re

from dotenv import load_dotenv
from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIError,
)
class MissingAPIKeyError(Exception):
    """Raised when OPENAI_API_KEY is not configured."""

load_dotenv()

EQUIPMENT_TYPES = (
    "X-ray",
    "CT",
    "MRI",
    "Ultrasound",
    "General Medical Equipment",
)

MODEL_NAME = "gpt-5-mini"

SYSTEM_PROMPT = """
You are AI BioMed Assistant, supporting a qualified medical equipment service
professional who is troubleshooting biomedical devices in the field.

Audience:
- Assume the user is a trained biomedical / field service engineer.
- Provide practical, equipment-focused troubleshooting guidance.
- Do not give clinical diagnosis or patient-care instructions.

Safety rules (mandatory):
- Do not provide instructions that bypass, defeat, or override safety systems,
  interlocks, emergency stops, radiation barriers, magnetic-field controls,
  lockout/tagout (LOTO), or manufacturer service procedures.
- Do not suggest operating equipment in an unsafe or unapproved mode.
- Prefer manufacturer-approved diagnostics, service manuals, and qualified
  procedures. If a step requires manufacturer-specific data, say so.
- Include relevant radiation, electrical, mechanical, MRI zone, infection
  control, and patient-environment precautions for the selected equipment type.

Response format:
- Return ONLY valid JSON with these exact keys:
  - "possible_cause" (2-4 likely root causes, concise)
  - "troubleshooting_steps" (5-8 numbered steps maximum, brief and actionable)
  - "safety_considerations" (2-4 key safety points only)
- troubleshooting_steps must be a numbered list in a single string, with
  each step on its own line. Each step should be 1-2 sentences.
- Keep guidance concise, specific, and useful for on-site service work.
""".strip()


def _normalize_equipment_type(equipment_type: str) -> str:
    if equipment_type in EQUIPMENT_TYPES:
        return equipment_type
    return "General Medical Equipment"


def _empty_response(equipment_type: str) -> dict[str, str]:
    return {
        "category": "Input required",
        "equipment_type": equipment_type,
        "possible_cause": "No problem description was provided.",
        "troubleshooting_steps": "Enter a description of the equipment issue and submit again.",
        "safety_considerations": "Always follow your site safety procedures before inspecting equipment.",
    }


def _error_response(equipment_type: str, message: str) -> dict[str, str]:
    return {
        "category": "API error",
        "equipment_type": equipment_type,
        "possible_cause": message,
        "troubleshooting_steps": (
            "1. Confirm a .env file exists in the project folder with OPENAI_API_KEY set.\n"
            "2. Restart the Streamlit app after changing environment variables.\n"
            "3. Check your network connection and OpenAI account status.\n"
            "4. Try submitting the problem description again."
        ),
        "safety_considerations": (
            "Do not attempt unsafe workarounds while the assistant is unavailable. "
            "Follow manufacturer procedures and site safety rules."
        ),
        "error": message,
    }


def _parse_model_output(text: str) -> dict[str, str] | None:
    payload = text.strip()
    if payload.startswith("```"):
        payload = re.sub(r"^```(?:json)?\s*", "", payload)
        payload = re.sub(r"\s*```$", "", payload)

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None

    required = ("possible_cause", "troubleshooting_steps", "safety_considerations")
    
    # Check that all required keys exist
    for key in required:
        if key not in data:
            return None
    
    # Convert and validate each field
    result = {}
    for key in required:
        value = data[key]
        
        # Handle string values
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            result[key] = stripped
        
        # Handle list values
        elif isinstance(value, list):
            if not value:  # Empty list is invalid
                return None
            # Check all items are strings
            if not all(isinstance(item, str) for item in value):
                return None
            # Convert list to numbered string format
            result[key] = "\n".join(f"{i + 1}. {item.strip()}" for i, item in enumerate(value) if item.strip())
            # If conversion resulted in empty string, return None
            if not result[key]:
                return None
        
        # Handle any other type
        else:
            return None
    
    return result


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise AuthenticationError(
            "OPENAI_API_KEY is missing. Add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def generate_response(
    problem_description: str,
    equipment_type: str = "General Medical Equipment",
) -> dict[str, str]:
    """Return troubleshooting guidance from the OpenAI API."""
    equipment_type = _normalize_equipment_type(equipment_type)
    problem = problem_description.strip()

    if not problem:
        return _empty_response(equipment_type)

    user_prompt = (
        f"Equipment category: {equipment_type}\n\n"
        f"Problem description:\n{problem}\n\n"
        "Provide likely causes, recommended troubleshooting steps, and safety "
        "considerations for this equipment category. Stay within manufacturer-"
        "approved service practice and do not suggest bypassing safety systems."
    )

    try:
        client = _get_client()
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        content = completion.choices[0].message.content or ""
        parsed = _parse_model_output(content)
        if parsed is None:
            return _error_response(
                equipment_type,
                "The assistant returned an unexpected response format. Please try again.",
            )
        return {
            "category": "AI troubleshooting",
            "equipment_type": equipment_type,
            **parsed,
        }
    except AuthenticationError:
        return _error_response(
            equipment_type,
            "Could not authenticate with OpenAI. Check that OPENAI_API_KEY is set in your .env file.",
        )
    except RateLimitError:
        return _error_response(
            equipment_type,
            "The OpenAI API rate limit was reached. Wait a moment and try again.",
        )
    except APIConnectionError:
        return _error_response(
            equipment_type,
            "Could not connect to the OpenAI API. Check your network connection and try again.",
        )
    except APIError:
        return _error_response(
            equipment_type,
            "The OpenAI API returned an error. Please try again in a moment.",
        )
    except Exception:
        return _error_response(
            equipment_type,
            "An unexpected error occurred while requesting troubleshooting guidance. Please try again.",
        )
