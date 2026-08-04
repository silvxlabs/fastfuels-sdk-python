"""Builders for grid-compose operations."""

from collections.abc import Iterable

from fastfuels_sdk.v2.client_library.models import (
    ComposeAttributeCondition,
    ComposeComparisonOperator,
    ComposeCompute,
    ComposeLiteral,
    ComposeOperator,
    ComposeSelect,
    GridFeatureSpatialCondition,
    GridGeometrySpatialCondition,
    InlineCompute,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = ["select", "compute", "condition", "literal", "inline_compute"]

_VARIADIC_OPERATORS = {
    ComposeOperator.ADD,
    ComposeOperator.AVERAGE,
    ComposeOperator.MAX,
    ComposeOperator.MIN,
    ComposeOperator.MULTIPLY,
}
_ORDERING_OPERATORS = {
    ComposeComparisonOperator.GE,
    ComposeComparisonOperator.GT,
    ComposeComparisonOperator.LE,
    ComposeComparisonOperator.LT,
}
_CONDITION_TYPES = (
    ComposeAttributeCondition,
    GridFeatureSpatialCondition,
    GridGeometrySpatialCondition,
)
_ELSE_TYPES = (ComposeLiteral, InlineCompute, int, float, str)


def select(
    output: str,
    from_: str,
    *,
    conditions: Iterable | None = None,
    else_=None,
    name: str | None = None,
    description: str | None = None,
) -> ComposeSelect:
    """Build an operation that copies an input band into the output grid.

    Parameters
    ----------
    output : str
        Key for the output band.
    from_ : str
        Alias-qualified source band, such as ``"base.fbfm"``.
    conditions : iterable, optional
        Attribute or spatial conditions, all of which must match. Attribute
        conditions can be built with :func:`condition`.
    else_ : optional
        Fallback band reference, number, typed :func:`literal`, fuel-model
        label, or :func:`inline_compute`. Required when conditions are given.
    name, description : str, optional
        Display metadata for the output band.

    Returns
    -------
    ComposeSelect
        A select operation for
        :func:`fastfuels_sdk.v2.grids.create_grid_from_compose`.
    """
    _require_text(output, "output")
    _require_band_reference(from_, "from_")
    condition_list = _condition_list(conditions)
    _validate_conditional_fallback(condition_list, else_)
    return ComposeSelect(
        output=output,
        from_=from_,
        conditions=condition_list,
        else_=_else_value(else_),
        name=_optional(name),
        description=_optional(description),
    )


def compute(
    output: str,
    operator,
    operands: Iterable,
    *,
    conditions: Iterable | None = None,
    else_=None,
    unit: str | None = None,
    name: str | None = None,
    description: str | None = None,
) -> ComposeCompute:
    """Build an operation that computes an output band.

    Parameters
    ----------
    output : str
        Key for the output band.
    operator : str or ComposeOperator
        ``"add"``, ``"subtract"``, ``"multiply"``, ``"divide"``,
        ``"min"``, ``"max"``, or ``"average"``.
    operands : iterable
        Alias-qualified band references, bare numbers, or typed literals.
        At least one operand must be a band reference.
    conditions : iterable, optional
        Attribute or spatial conditions, all of which must match.
    else_ : optional
        Fallback value. Required when conditions are given.
    unit : str, optional
        Canonical unit in which to express the computed output.
    name, description : str, optional
        Display metadata for the output band.

    Returns
    -------
    ComposeCompute
        A compute operation for
        :func:`fastfuels_sdk.v2.grids.create_grid_from_compose`.
    """
    _require_text(output, "output")
    operator = _operator(operator)
    operand_list = _operands(operator, operands)
    condition_list = _condition_list(conditions)
    _validate_conditional_fallback(condition_list, else_)
    return ComposeCompute(
        output=output,
        operator=operator,
        operands=operand_list,
        conditions=condition_list,
        else_=_else_value(else_),
        unit=_optional(unit),
        name=_optional(name),
        description=_optional(description),
    )


def condition(band: str, operator, value) -> ComposeAttributeCondition:
    """Build an attribute condition for a compose operation.

    Parameters
    ----------
    band : str
        Alias-qualified input band to test.
    operator : str or ComposeComparisonOperator
        ``"eq"``, ``"ne"``, ``"gt"``, ``"lt"``, ``"ge"``, ``"le"``,
        or ``"in"``.
    value : int, float, str, or list
        Comparison value. ``"in"`` requires a list; ordering comparisons
        require a scalar.

    Returns
    -------
    ComposeAttributeCondition
        A condition for :func:`select` or :func:`compute`.
    """
    _require_band_reference(band, "band")
    try:
        operator = ComposeComparisonOperator(operator)
    except (TypeError, ValueError):
        choices = [item.value for item in ComposeComparisonOperator]
        raise ValueError(
            f"Unknown compose comparison operator {operator!r}. Use one of {choices}."
        ) from None

    is_list = isinstance(value, list)
    values = value if is_list else [value]
    if not all(_is_scalar(item) for item in values):
        raise TypeError("Compose condition values must be numbers or strings.")
    if operator == ComposeComparisonOperator.IN and not is_list:
        raise ValueError("The 'in' compose condition requires a list value.")
    if operator in _ORDERING_OPERATORS and is_list:
        raise ValueError(f"The {operator.value!r} condition requires a scalar value.")
    return ComposeAttributeCondition(band=band, operator=operator, value=value)


def literal(value, unit: str | None = None) -> ComposeLiteral:
    """Build a typed literal for a compose operand or fallback.

    Parameters
    ----------
    value : int, float, or str
        Literal value.
    unit : str, optional
        Canonical unit for a numeric literal. String literals are unitless.

    Returns
    -------
    ComposeLiteral
        A typed compose literal.
    """
    if not _is_scalar(value):
        raise TypeError("Compose literal values must be numbers or strings.")
    if isinstance(value, str) and unit is not None:
        raise ValueError("String compose literals cannot carry a unit.")
    if unit is not None and not isinstance(unit, str):
        raise TypeError("unit must be a string or None.")
    return ComposeLiteral(value=value, unit=_optional(unit))


def inline_compute(operator, operands: Iterable) -> InlineCompute:
    """Build a computation for the fallback branch of a compose operation.

    Parameters
    ----------
    operator : str or ComposeOperator
        Arithmetic operator.
    operands : iterable
        Alias-qualified band references, bare numbers, or typed literals.

    Returns
    -------
    InlineCompute
        A computed fallback for ``else_=``.
    """
    operator = _operator(operator)
    return InlineCompute(operator=operator, operands=_operands(operator, operands))


def _optional(value):
    return UNSET if value is None else value


def _require_text(value, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{name} must be a nonempty string.")


def _require_band_reference(value, name: str) -> None:
    _require_text(value, name)
    alias, separator, band = value.partition(".")
    if not separator or not alias or not band:
        raise ValueError(
            f"{name} must be an alias-qualified band reference such as "
            "'base.fuel_load.1hr'."
        )


def _operator(value) -> ComposeOperator:
    try:
        return ComposeOperator(value)
    except (TypeError, ValueError):
        choices = [item.value for item in ComposeOperator]
        raise ValueError(
            f"Unknown compose operator {value!r}. Use one of {choices}."
        ) from None


def _operands(operator: ComposeOperator, values: Iterable) -> list:
    if isinstance(values, (str, bytes)):
        raise TypeError("operands must be an iterable of compose operands.")
    try:
        operands = list(values)
    except TypeError:
        raise TypeError("operands must be an iterable of compose operands.") from None

    expected = "at least two" if operator in _VARIADIC_OPERATORS else "exactly two"
    valid_arity = (
        len(operands) >= 2 if operator in _VARIADIC_OPERATORS else len(operands) == 2
    )
    if not valid_arity:
        raise ValueError(
            f"The {operator.value!r} operator requires {expected} operands."
        )
    for operand in operands:
        if isinstance(operand, str):
            _require_band_reference(operand, "operand")
        elif isinstance(operand, ComposeLiteral):
            if isinstance(operand.value, str):
                raise ValueError("String literals are not valid compute operands.")
        elif not _is_number(operand):
            raise TypeError(
                "Compose operands must be band references, numbers, or typed literals."
            )
    if not any(isinstance(operand, str) for operand in operands):
        raise ValueError("A compute operation must include at least one band operand.")
    return operands


def _condition_list(values: Iterable | None):
    if values is None:
        return UNSET
    if isinstance(values, _CONDITION_TYPES):
        raise TypeError("conditions must be an iterable of compose conditions.")
    try:
        conditions = list(values)
    except TypeError:
        raise TypeError(
            "conditions must be an iterable of compose conditions."
        ) from None
    if not all(isinstance(item, _CONDITION_TYPES) for item in conditions):
        raise TypeError(
            "conditions must contain compose attribute or grid spatial conditions."
        )
    return conditions


def _validate_conditional_fallback(conditions, else_) -> None:
    has_conditions = conditions is not UNSET and bool(conditions)
    if has_conditions and else_ is None:
        raise ValueError("else_ is required when compose conditions are provided.")
    if not has_conditions and else_ is not None:
        raise ValueError("else_ requires at least one compose condition.")


def _else_value(value):
    if value is None:
        return UNSET
    if isinstance(value, bool) or not isinstance(value, _ELSE_TYPES):
        raise TypeError(
            "else_ must be a band reference, number, fuel-model label, typed "
            "literal, or inline compute."
        )
    return value


def _is_number(value) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float))


def _is_scalar(value) -> bool:
    return _is_number(value) or isinstance(value, str)
