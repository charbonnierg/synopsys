import typing as t
from re import escape

import pytest

from synopsys.api import Event, create_event


@pytest.mark.parametrize(
    "subject,event,result",
    [
        ("test", create_event("test", "test", scope_schema=None), None),
        ("test", create_event("test", "test", scope_schema=dict), dict()),
        (
            "test.someid",
            create_event("test", "test.{id}", scope_schema=dict),
            {"id": "someid"},
        ),
        (
            "test.someid.westus",
            create_event("test", "test.{device}.{location}", scope_schema=dict),
            {"device": "someid", "location": "westus"},
        ),
    ],
)
def test_extract_subject_placeholders(
    subject: str, event: Event[t.Any, t.Any, t.Any, t.Any], result: t.Dict[str, str]
):
    assert event.extract_scope(subject) == result


def test_extract_subject_placeholders_missing():
    event = create_event("test", "test.{device}")
    with pytest.raises(
        ValueError,
        match=escape("Invalid subject. Missing placeholder: device (index: 1)"),
    ):
        event.extract_scope("test")

    other_event = create_event("other", "other.{device}.{location}")
    with pytest.raises(
        ValueError,
        match=escape("Invalid subject. Missing placeholder: location (index: 2)"),
    ):
        other_event.extract_scope("other.device")
