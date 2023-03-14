import pytest

from synopsys.defaults import DEFAULT_SYNTAX
from synopsys.operations.subjects import match_subject


@pytest.mark.parametrize(
    "subject,filter,match",
    [
        ("a", "a", True),
        ("ab", "*", True),
        ("ab", ">", True),
        ("ab.a", "ab.a", True),
        ("ab.a", "ab.*", True),
        ("a.b.c", "*.b.c", True),
        ("a.b.c", "a.*.c", True),
        ("a.b.c", "a.b.*", True),
        ("ab.a", ">", True),
        ("ab.a", "ab.>", True),
        ("a", "b", False),
        ("a.b", "*", False),
        ("a.a", "a.b", False),
        ("a.b.c", "a.*", False),
        ("a", "a.b", False),
        ("a", "a.*", False),
        ("a", "a.>", False),
    ],
)
def test_match_subject(subject: str, filter: str, match: bool):
    assert match_subject(filter, subject, DEFAULT_SYNTAX) is match


def test_match_subject_error_filter_subject_cannot_be_empty():
    with pytest.raises(ValueError, match="Filter subject cannot be empty"):
        match_subject("", "subject", DEFAULT_SYNTAX)


def test_match_subject_error_subject_cannot_be_empty():
    with pytest.raises(ValueError, match="Subject cannot be empty"):
        match_subject("filter", "", DEFAULT_SYNTAX)
