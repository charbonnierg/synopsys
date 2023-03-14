from dataclasses import dataclass


@dataclass
class SubjectSyntax:
    """NATS subject syntax."""

    match_sep: str = "."
    """The character used to separate address tokens."""

    match_all: str = ">"
    """The character used to match all address tokens."""

    match_one: str = "*"
    """The character used to match a single address token."""
