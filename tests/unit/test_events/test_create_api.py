from synopsys.api import NULL, create_event


def test_create_minimal_event():
    evt = create_event("test-event", "test")
    assert evt.schema is NULL
    assert evt.scope_schema is NULL
    assert evt.metadata_schema is NULL
    assert evt.reply_schema is NULL


def test_create_event_with_schema():
    evt = create_event("test-event", "test", schema=int)
    assert evt.schema is int
    assert evt.scope_schema is NULL
    assert evt.metadata_schema is NULL
    assert evt.reply_schema is NULL


def test_create_event_with_schema_explicit_none():
    evt = create_event("test-event", "test", schema=None)
    assert evt.schema is NULL
    assert evt.scope_schema is NULL
    assert evt.metadata_schema is NULL
    assert evt.reply_schema is NULL


def test_create_event_with_reply_schema():
    evt = create_event("test-event", "test", reply_schema=int)
    assert evt.reply_schema is int
    assert evt.schema is NULL
    assert evt.scope_schema is NULL
    assert evt.metadata_schema is NULL


def test_create_event_with_reply_schema_explicit_none():
    evt = create_event("test-event", "test", reply_schema=None)
    assert evt.reply_schema is NULL
    assert evt.schema is NULL
    assert evt.scope_schema is NULL
    assert evt.metadata_schema is NULL


def test_create_event_with_metadata_schema():
    evt = create_event("test-event", "test", metadata_schema=dict)
    assert evt.metadata_schema is dict
    assert evt.schema is NULL
    assert evt.reply_schema is NULL
    assert evt.scope_schema is NULL


def test_create_event_with_metadata_schema_explicit_none():
    evt = create_event("test-event", "test", metadata_schema=None)
    assert evt.metadata_schema is NULL
    assert evt.schema is NULL
    assert evt.reply_schema is NULL
    assert evt.scope_schema is NULL


def test_create_event_with_scope_schema():
    evt = create_event("test-event", "test", scope_schema=dict)
    assert evt.scope_schema is dict
    assert evt.schema is NULL
    assert evt.reply_schema is NULL
    assert evt.metadata_schema is NULL


def test_create_event_with_scope_schema_explicit_null():
    evt = create_event("test-event", "test", scope_schema=None)
    assert evt.scope_schema is NULL
    assert evt.schema is NULL
    assert evt.reply_schema is NULL
    assert evt.metadata_schema is NULL
