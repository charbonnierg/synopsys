from re import escape

import pytest
from typing_extensions import TypedDict

from synopsys.api import create_event


def test_event_empty_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        create_event("", "subject")


def test_event_empty_subject():
    with pytest.raises(ValueError, match="Subject cannot be empty"):
        create_event("name", "")


def test_event_repr():
    event = create_event("test", "test.event")
    assert repr(event) == "Event(name='test', subject='test.event', schema=NoneType)"

    class Foo:
        pass

    other_event = create_event("test", "test.event", schema=Foo)
    assert repr(other_event) == "Event(name='test', subject='test.event', schema=Foo)"


def test_event_missing_scope_annotations():
    class EventScope(TypedDict):
        """A typed dict without the 'device' key which is required by the event."""

        location: str

    # Not OK using a typed dict with missing field
    with pytest.raises(
        ValueError,
        match=escape(
            "Too many placeholders in subject or missing scope variables. Did not expect in subject: ['device']"
        ),
    ):
        create_event("test", "test.{device}.{location}", scope_schema=EventScope)


def test_event_extra_scope_annotations():
    class EventScope(TypedDict):
        """A typed dict with an additional key 'location' not present in event subject."""

        device: str
        location: str

    # Not OK using a typed dict with missing field
    with pytest.raises(
        ValueError,
        match=escape(
            "Not enough placeholders in subject or unexpected scope variable. Missing in subject: ['location']"
        ),
    ):
        create_event("test", "test.{device}", scope_schema=EventScope)


def test_event_proper_scope_annotations():
    class EventScope(TypedDict):
        """A typed dict with an additional key 'location' not present in event subject."""

        device: str
        location: str

    event = create_event("test", "test.{device}.{location}", scope_schema=EventScope)
    assert event.name == "test"
    assert event.scope_schema == EventScope
    assert event.subject == "test.{device}.{location}"
