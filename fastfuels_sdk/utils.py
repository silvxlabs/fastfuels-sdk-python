from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastfuels_sdk.client_library.models import ProcessingError


def format_processing_error(error: "ProcessingError") -> str:
    """
    Format a ProcessingError into a detailed error message.

    Parameters
    ----------
    error : ProcessingError
        The processing error object from the API response

    Returns
    -------
    str
        A formatted error message with code, message, details, and suggestions
    """
    parts = []

    # Get error code and message (main error line)
    code = getattr(error, "code", None)
    message = getattr(error, "message", None)

    if code and message:
        parts.append(f"{code}: {message}")
    elif code:
        parts.append(code)
    elif message:
        parts.append(message)

    # Add details if available
    details = getattr(error, "details", None)
    if details:
        parts.append(f"\n{details}")

    # Add suggestions if available
    suggestions = getattr(error, "suggestions", None)
    if suggestions:
        parts.append(f"\nTo resolve this issue: {suggestions}")

    return "\n".join(parts) if parts else ""


def parse_dict_items_to_pydantic_list(items, item_class):
    """Parse modifications or treatments into the correct format before sending to the API.

    Parameters
    ----------
    items : dict or list[dict] or None
        Raw items to parse. Each item should be a dictionary containing
        the required fields for the specified item_class.

    item_class : type
        Class to parse items into (e.g. TreeInventoryModification or TreeInventoryTreatment)

    Returns
    -------
    list or None
        Parsed items in the correct format, or None if input was None
    """
    if items is None:
        return None

    if isinstance(items, dict):
        items = [items]

    return [item_class.from_dict(item) for item in items]  # type: ignore
