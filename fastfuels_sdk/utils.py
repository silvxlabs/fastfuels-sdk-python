from __future__ import annotations


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
