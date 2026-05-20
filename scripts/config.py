"""Configuration constants for Pretalx schedule sync."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from scripts directory
load_dotenv(Path(__file__).parent / ".env")

# Pretalx API
PRETALX_EVENT_SLUG = os.environ.get("PRETALX_EVENT", "pycon-au-2025")
PRETALX_TOKEN = os.environ.get("PRETALX_TOKEN", "")
PRETALX_BASE_URL = "https://pretalx.com/api/events"

# Event timezone
EVENT_TIMEZONE = "Australia/Melbourne"

# Question IDs (discovered via pretalx_questions.py)
# These may change between events - run pretalx_questions.py to discover
CONTENT_WARNING_QUESTION_ID = 5326
PRONOUNS_QUESTION_ID = 5332
BLUESKY_QUESTION_ID = 5329
FEDIVERSE_QUESTION_ID = 5328

# Submission type ID to session type mapping (discovered via pretalx_questions.py)
# Maps Pretalx submission type IDs to our session types:
#   talk, workshop, plenary, poster, other
# Updated for PyCon AU 2026 event
SUBMISSION_TYPE_MAPPING: dict[int, str] = {
    7192: "other",      # Flash talk
    7193: "plenary",    # Opening/Closing (conference-level, spans all ballrooms)
    7194: "talk",       # Education Keynote
    7195: "other",      # Backup
    7196: "other",      # Waitlist
    7197: "talk",       # Talk
    7198: "talk",       # Sponsored talk
    7199: "other",      # Other
    7200: "plenary",    # Keynote
    7201: "plenary",    # Lightning talks
    7202: "talk",       # Education Showcase
    7203: "workshop",   # Workshop (2h)
    7204: "workshop",   # Workshop (3h)
    7205: "other",      # Sprints
    7240: "poster",     # Poster Session
    7264: "workshop",   # Workshop
}

# Session codes that should be marked as plenary (full-width in schedule)
# These are conference-level openings/closings that span all rooms
PLENARY_SESSION_CODES: set[str] = {
    "VQD3SG",  # Conference welcome & keynote (Thursday)
    "3FQZVE",  # Keynote (Friday)
    "9PXVYP",  # Keynote (Saturday)
    "TGQGWT",  # Conference Closing (Saturday)
}

# Room labels (optional display name overrides)
# If a room from the API is not listed here, the API name is used as-is
ROOM_LABELS: dict[str, str] = {
    "Ballroom 1": "Ballroom 1",
    "Ballroom 2": "Ballroom 2",
    "Ballroom 3": "Ballroom 3",
}

# Plenary rooms (combined ballrooms for keynotes)
# Sessions marked as keynote/plenary span all these rooms
PLENARY_ROOMS = ["Ballroom 1", "Ballroom 2", "Ballroom 3"]

# Room order for schedule display and break column spanning
# Breaks that occur simultaneously in adjacent rooms will be merged
ROOM_ORDER = ["Ballroom 1", "Ballroom 2", "Ballroom 3", "Lyon"]

# Output paths (relative to project root)
SESSIONS_OUTPUT_DIR = "src/content/sessions"
PEOPLE_OUTPUT_DIR = "src/content/people"
AVATARS_OUTPUT_DIR = "public/images/people"
SPECIALIST_TRACKS_DIR = "src/content/specialist-tracks"

# Avatar image settings
AVATAR_SIZE = (225, 225)
AVATAR_QUALITY = 95
