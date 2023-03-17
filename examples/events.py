import typing as t
from dataclasses import dataclass

from synopsys import create_event, create_flow
from synopsys.entities import Flow


@dataclass
class Page:
    """Page entity.
    A page is a namespace for a single page web application.
    Once a page is created, it is possible to create versions for the page.
    Versions are created by publishing a directory containing an index.html file, but page entities
    do not require any content to be created.
    A page entity may indicate a reference to its latest version available.
    """

    id: str
    """The page ID. Unique, generated automatically."""

    name: str
    """The page name. Unique. Only '-' and alphanumerical characters are allowed."""

    title: str
    """A human friendly title for the page."""

    description: str
    """A short description of the page application."""

    latest_version: t.Optional[str]
    """The latest version available for this page.
    This field always reference an existing page version.
    """


@dataclass
class Version:
    """Page version entity.
    A page version is a reference to a single page application (where a single page application
    is a directory containing at least a file named `index.html`).
    Several versions may exist for a single page.
    A single version at a time is considered the latest version.
    Note that the concept of latest version is not defined on version
    entities, instead it is defined on page entities.
    """

    page_id: str
    """The version page ID. All versions of a single page share the same page ID."""

    page_name: str
    """The version page name. All versions of a single page share the same page name."""

    page_version: str
    """The page version. Unique."""

    checksum: str
    """The page archive checksum. Note that archive are compressed using gzip and gzip checksums are not deterministic.
    Thus, compressing the same directory twice will produce a different checksum.
    """

    created_timestamp: int
    """The timestamp at which page version was fist published."""


@dataclass
class PageCreated:
    """Paylaod of a page-created event."""

    document: Page


@dataclass
class PageDeleted:
    """Payload of a page-deleted event."""

    page_id: str
    page_name: str


@dataclass
class VersionCreated:
    """Payload of version-created event."""

    document: Version
    content: str
    latest: bool


@dataclass
class VersionUploaded:
    """Payload of version-uploaded event."""

    page_id: str
    page_name: str
    page_version: str
    is_latest: bool


@dataclass
class VersionDeleted:
    """Payload of version-deleted event."""

    page_id: str
    page_name: str
    page_version: str


PAGE_CREATED = create_event(
    name="page-created",
    subject="page.created",
    schema=PageCreated,
    description="Event triggered when a page is successfully created",
)


PAGE_DELETED = create_event(
    name="page-deleted",
    subject="page.deleted",
    schema=PageDeleted,
    description="Event triggered when a page is successfully deleted",
)


VERSION_CREATED = create_event(
    name="version-created",
    subject="pages.created",
    schema=VersionCreated,
    description=(
        "Event triggered when a version is successfully created. "
        "Control plane must react to this event and upload the version to blob storage."
    ),
)


VERSION_UPLOADED = create_event(
    name="version-uploaded",
    subject="pages.versions.uploaded",
    schema=VersionUploaded,
    description=(
        "Event triggered when a version is successfully uploaded to blob storage. "
        "Page fileservers must react to this event and download version from blob storage."
    ),
)


VERSION_DELETED = create_event(
    name="version-deleted",
    subject="pages.versions.deleted",
    schema=VersionDeleted,
    description=(
        "Event triggered when a version is successfully deleted. "
        "Page fileservers must react to this event and remove the "
        "version from their cache."
    ),
)


FLOWS: t.List[Flow] = [
    create_flow("fileserver-cache-init", event=PAGE_CREATED),
    create_flow("fileserver-cache-purge", event=PAGE_DELETED),
    create_flow("fileserver-cache-delete", event=VERSION_DELETED),
    create_flow("fileserver-cache-update", event=VERSION_UPLOADED),
]
