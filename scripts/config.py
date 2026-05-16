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
#   talk, keynote, plenary, workshop, lightning, panel, break
SUBMISSION_TYPE_MAPPING: dict[int, str] = {
    5931: "talk",      # Waitlist
    5932: "talk",      # Talk
    5933: "talk",      # Opening/Closing (track openings - NOT plenary)
    5934: "keynote",   # Education Keynote
    5935: "keynote",   # Keynote
    5936: "talk",      # Backup
    5937: "talk",      # Sprints
    5938: "workshop",  # Workshop (3h)
    5939: "workshop",  # Workshop (2h)
    5940: "talk",      # Sponsored talk
    5941: "talk",      # Flash talk
    5942: "talk",      # Education Showcase
    5943: "lightning", # Lightning talks
    6032: "talk",      # Other
}

# Session codes that should be marked as plenary (full-width in schedule)
# These are conference-level openings/closings that span all rooms
PLENARY_SESSION_CODES: set[str] = {
    "W7W3VR",  # Conference Opening (Saturday)
    "AMLK87",  # Conference Closing (Sunday)
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
ROOM_ORDER = ["Ballroom 1", "Ballroom 2", "Ballroom 3", "Stradbroke Room"]

# Output paths (relative to project root)
SESSIONS_OUTPUT_DIR = "src/content/sessions"
PEOPLE_OUTPUT_DIR = "src/content/people"
AVATARS_OUTPUT_DIR = "public/images/people"
SPECIALIST_TRACKS_DIR = "src/content/specialist-tracks"

# Avatar image settings
AVATAR_SIZE = (225, 225)
AVATAR_QUALITY = 95
