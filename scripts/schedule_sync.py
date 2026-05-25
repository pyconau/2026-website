#!/usr/bin/env python3
"""
Sync Pretalx schedule data to PyCon AU website.

This script fetches session and speaker data from the Pretalx API and generates
markdown files with frontmatter for Astro content collections.

Usage:
    cd scripts && uv run python schedule_sync.py

Environment variables:
    PRETALX_TOKEN - API token for Pretalx (required)
    PRETALX_EVENT - Event slug (default: pycon-au-2025)
"""

import hashlib
import io
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dateutil import parser as dateparser
from PIL import Image
from ruamel.yaml import YAML

from config import (
    AVATAR_QUALITY,
    AVATAR_SIZE,
    AVATARS_OUTPUT_DIR,
    BLUESKY_QUESTION_ID,
    CONTENT_WARNING_QUESTION_ID,
    EVENT_TIMEZONE,
    FEDIVERSE_QUESTION_ID,
    PEOPLE_OUTPUT_DIR,
    PLENARY_ROOMS,
    PLENARY_SESSION_CODES,
    PRETALX_BASE_URL,
    PRETALX_EVENT_SLUG,
    PRETALX_TOKEN,
    PRONOUNS_QUESTION_ID,
    ROOM_LABELS,
    ROOM_ORDER,
    SESSIONS_OUTPUT_DIR,
    SPECIALIST_TRACKS_DIR,
    SUBMISSION_TYPE_MAPPING,
)

# Initialize YAML with round-trip mode for preserving formatting
yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False


def get_project_root() -> Path:
    """Get the project root directory (parent of scripts/)."""
    return Path(__file__).parent.parent


def api_request(endpoint: str, params: dict | None = None) -> dict:
    """Make an authenticated request to the Pretalx API."""
    if not PRETALX_TOKEN:
        print("Error: PRETALX_TOKEN environment variable not set")
        sys.exit(1)

    url = f"{PRETALX_BASE_URL}/{PRETALX_EVENT_SLUG}/{endpoint}"
    headers = {"Authorization": f"Token {PRETALX_TOKEN}"}

    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def paginate_api(endpoint: str, params: dict | None = None) -> list[dict]:
    """Fetch all pages from a paginated Pretalx API endpoint."""
    results = []
    url = f"{PRETALX_BASE_URL}/{PRETALX_EVENT_SLUG}/{endpoint}"
    headers = {"Authorization": f"Token {PRETALX_TOKEN}"}

    while url:
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        results.extend(data.get("results", []))
        url = data.get("next")
        params = None  # URL already includes params for next page

    return results


def load_track_mappings() -> dict[str, str]:
    """
    Load track mappings from schedule-specialist-tracks markdown files.

    Returns a dict mapping Pretalx track names to file slugs.
    e.g., {"Data & AI": "data-and-ai", "Education": "education"}
    """
    tracks_dir = get_project_root() / "src/content/schedule-specialist-tracks"
    mappings = {}

    if not tracks_dir.exists():
        print(f"Warning: Specialist tracks directory not found: {tracks_dir}")
        return mappings

    for md_file in tracks_dir.glob("*.md"):
        slug = md_file.stem  # filename without extension

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.load(parts[1])
                pretalx_track = frontmatter.get("pretalxTrack")
                if pretalx_track:
                    mappings[pretalx_track] = slug
                    print(f"  Track mapping: '{pretalx_track}' -> '{slug}'")

    return mappings


def get_answer_for_question(answers: list[dict], question_id: int) -> str | None:
    """Extract answer text for a specific question ID."""
    for answer in answers:
        question = answer.get("question")
        # question can be an int (ID) or a dict with 'id' key
        if isinstance(question, int):
            qid = question
        elif isinstance(question, dict):
            qid = question.get("id")
        else:
            continue

        if qid == question_id:
            return answer.get("answer", "").strip() or None
    return None


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def determine_session_type(submission: dict) -> str:
    """Determine session type from Pretalx submission data.

    Uses the static SUBMISSION_TYPE_MAPPING from config.py, with special
    handling for plenary sessions (conference openings/closings).
    """
    code = submission.get("code", "")

    # Check if this is a plenary session (conference opening/closing)
    if code in PLENARY_SESSION_CODES:
        return "plenary"

    # Look up the submission type ID in the static mapping
    submission_type = submission.get("submission_type")
    submission_type_id = submission_type

    # submission_type can be an int or a dict with an 'id' field
    if isinstance(submission_type, dict):
        submission_type_id = submission_type.get("id")

    if isinstance(submission_type_id, int):
        return SUBMISSION_TYPE_MAPPING.get(submission_type_id, "talk")

    return "talk"


def process_breaks(
    slots_data: list[dict],
    room_id_to_name: dict[int, str],
) -> list[dict]:
    """Process Pretalx slots to extract break data, deduplicating by start/end/title/room."""
    breaks = []
    seen_breaks = set()

    for slot in slots_data:
        # Breaks have no submission and slot_type == "break"
        if slot.get("submission") is not None:
            continue
        if slot.get("slot_type") != "break":
            continue

        room_id = slot.get("room")
        room_name = room_id_to_name.get(room_id, "") if isinstance(room_id, int) else ""

        # Apply room label override if configured
        room_display = ROOM_LABELS.get(room_name, room_name)

        # Skip breaks in rooms we don't display
        if room_display not in ROOM_ORDER:
            continue

        # Get break title from description
        description = slot.get("description", {})
        title = description.get("en", "Break") if isinstance(description, dict) else "Break"

        # Deduplicate: use (start, end, title, room) as unique key
        break_key = (slot.get("start"), slot.get("end"), title, room_display)
        if break_key in seen_breaks:
            continue
        seen_breaks.add(break_key)

        break_data = {
            "code": f"BREAK-{slot['id']}",  # Synthetic code for breaks
            "title": title,
            "start": slot.get("start"),
            "end": slot.get("end"),
            "room": room_display,
            "track": None,  # Breaks don't have tracks
            "type": "break",
            "speakers": [],
            "body": "",
        }

        breaks.append(break_data)

    return breaks


def process_sessions(
    submissions: list[dict],
    track_mappings: dict[str, str],
    track_id_to_name: dict[int, str],
    slots_by_submission: dict[str, dict],
    answers_by_submission: dict[str, list[dict]],
    verbose: bool = True,
) -> list[dict]:
    """Process Pretalx submissions into session data."""
    sessions = []

    for i, sub in enumerate(submissions):
        code = sub.get("code", "")
        if not code:
            continue

        # Get localized strings
        title = sub.get("title", "")
        if isinstance(title, dict):
            title = title.get("en", str(title))

        abstract = sub.get("abstract", "") or ""
        if isinstance(abstract, dict):
            abstract = abstract.get("en", str(abstract))

        description = sub.get("description", "") or ""
        if isinstance(description, dict):
            description = description.get("en", str(description))

        # Abstract goes to frontmatter; description-only content goes to body
        body = description if description and description != abstract else ""

        # Get schedule slot from slots lookup (not from submission directly)
        slot = slots_by_submission.get(code, {})
        start = slot.get("start")
        end = slot.get("end")
        room_name = slot.get("room", "")

        # Apply room label override if configured
        room_display = ROOM_LABELS.get(room_name, room_name)

        # Map track (track field is an ID, look up name)
        track_id = sub.get("track")
        track_name = ""
        if isinstance(track_id, int):
            track_name = track_id_to_name.get(track_id, "")
        elif isinstance(track_id, dict):
            track_name = track_id.get("en", "")

        track_slug = track_mappings.get(track_name) if track_name else None

        # Get speaker codes (may be list of objects or list of strings)
        raw_speakers = sub.get("speakers", [])
        speakers = []
        for s in raw_speakers:
            if isinstance(s, dict):
                if s.get("code"):
                    speakers.append(s["code"])
            elif isinstance(s, str):
                speakers.append(s)

        # Determine session type
        session_type = determine_session_type(sub)

        # Get content warning from answers (using answers grouped by submission code)
        submission_answers = answers_by_submission.get(code, [])
        content_warning = get_answer_for_question(submission_answers, CONTENT_WARNING_QUESTION_ID)

        session = {
            "code": code,
            "title": title,
            "start": start,
            "end": end,
            "room": room_display,
            "track": track_slug,
            "trackName": track_name if track_name else None,
            "type": session_type,
            "speakers": speakers,
            "abstract": abstract if abstract else None,
            "contentWarning": content_warning,
            "body": body,
            "layout": "layout_1",  # Default layout for graphics generation
        }

        if verbose and (i + 1) % 10 == 0:
            print(f"    Processed {i + 1}/{len(submissions)} sessions...")

        sessions.append(session)

    return sessions


def process_speakers(speakers_data: list[dict], answers_by_speaker: dict[str, list[dict]]) -> list[dict]:
    """Process Pretalx speakers into people data."""
    people = []

    for speaker in speakers_data:
        code = speaker.get("code", "")
        if not code:
            continue

        name = speaker.get("name", "")
        biography = speaker.get("biography", "") or ""
        if isinstance(biography, dict):
            biography = biography.get("en", str(biography))

        avatar_url = speaker.get("avatar_url")

        # Get answers for this speaker
        answers = answers_by_speaker.get(code, [])

        pronouns = get_answer_for_question(answers, PRONOUNS_QUESTION_ID)
        bluesky = get_answer_for_question(answers, BLUESKY_QUESTION_ID)
        fediverse = get_answer_for_question(answers, FEDIVERSE_QUESTION_ID)

        person = {
            "code": code,
            "name": name,
            "pronouns": pronouns,
            "bluesky": bluesky,
            "fediverse": fediverse,
            "avatar_url": avatar_url,
            "biography": biography,
        }

        people.append(person)

    return people


def download_avatar(url: str, output_path: Path) -> bool:
    """
    Download and process a speaker avatar.

    Returns True if avatar was downloaded/updated, False otherwise.
    """
    if not url:
        return False

    # Check if we already have this avatar (using ETag or simple existence check)
    headers = {}
    etag_file = output_path.with_suffix(".etag")

    if etag_file.exists() and output_path.exists():
        with open(etag_file, "r") as f:
            headers["If-None-Match"] = f.read().strip()

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 304:
            # Not modified, skip
            return False

        response.raise_for_status()

        # Save ETag for future requests
        if "ETag" in response.headers:
            etag_file.parent.mkdir(parents=True, exist_ok=True)
            with open(etag_file, "w") as f:
                f.write(response.headers["ETag"])

        # Process image
        img = Image.open(io.BytesIO(response.content))

        # Convert to RGB if necessary (for JPEG output)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize to target size
        img = img.resize(AVATAR_SIZE, Image.Resampling.LANCZOS)

        # Save as JPEG
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, "JPEG", quality=AVATAR_QUALITY)

        return True

    except Exception as e:
        print(f"  Warning: Failed to download avatar from {url}: {e}")
        return False


def write_session_file(session: dict, output_dir: Path) -> None:
    """Write a session markdown file with frontmatter."""
    code = session["code"]
    output_path = output_dir / f"{code}.md"

    # Load existing frontmatter to preserve custom fields like layout
    existing_layout = "layout_2"  # default layout
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                if match:
                    existing_frontmatter = yaml.load(match.group(1)) or {}
                    if "layout" in existing_frontmatter:
                        existing_layout = existing_frontmatter["layout"]
        except Exception:
            pass  # If we can't read the file, just use the default layout

    frontmatter = {
        "title": session["title"],
        "code": session["code"],
        "start": session["start"],
        "end": session["end"],
        "room": session["room"],
        "track": session["track"],
        "type": session["type"],
        "speakers": session["speakers"],
        "layout": existing_layout,
    }

    # Add optional fields only if present
    if session.get("trackName"):
        frontmatter["trackName"] = session["trackName"]
    if session.get("abstract"):
        frontmatter["abstract"] = session["abstract"]
    if session.get("contentWarning"):
        frontmatter["contentWarning"] = session["contentWarning"]
    if session.get("sponsor"):
        frontmatter["sponsor"] = session["sponsor"]

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f)
        f.write("---\n\n")
        f.write(session.get("body", "").strip())
        f.write("\n")


def write_person_file(person: dict, output_dir: Path, has_avatar: bool) -> None:
    """Write a speaker/person markdown file with frontmatter."""
    code = person["code"]
    output_path = output_dir / f"{code}.md"

    frontmatter = {
        "name": person["name"],
        "code": person["code"],
        "hasAvatar": has_avatar,
    }

    # Add optional fields only if present
    if person.get("pronouns"):
        frontmatter["pronouns"] = person["pronouns"]
    if person.get("bluesky"):
        frontmatter["bluesky"] = person["bluesky"]
    if person.get("fediverse"):
        frontmatter["fediverse"] = person["fediverse"]

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f)
        f.write("---\n\n")
        f.write(person.get("biography", "").strip())
        f.write("\n")


def main():
    print(f"PyCon AU Schedule Sync")
    print(f"Event: {PRETALX_EVENT_SLUG}")
    print("=" * 60)

    project_root = get_project_root()

    # Load track mappings from specialist-tracks files
    print("\nLoading track mappings...")
    track_mappings = load_track_mappings()
    print(f"  Found {len(track_mappings)} track mappings")

    # Fetch data from Pretalx
    print("\nFetching tracks from Pretalx...")
    tracks_data = paginate_api("tracks/")
    track_id_to_name: dict[int, str] = {}
    for track in tracks_data:
        track_name = track.get("name", {})
        if isinstance(track_name, dict):
            track_name = track_name.get("en", "")
        track_id_to_name[track["id"]] = track_name
    print(f"  Found {len(track_id_to_name)} tracks")

    print("\nFetching submission types from Pretalx...")
    submission_types_data = paginate_api("submission-types/")
    submission_types: dict[int, str] = {}
    for st in submission_types_data:
        st_name = st.get("name", {})
        if isinstance(st_name, dict):
            st_name = st_name.get("en", "")
        submission_types[st["id"]] = st_name
    print(f"  Found {len(submission_types)} submission types")

    print("\nFetching submissions from Pretalx...")
    submissions = paginate_api("submissions/", params={"state": "confirmed"})
    print(f"  Found {len(submissions)} confirmed submissions")

    print("\nFetching rooms from Pretalx...")
    rooms_data = paginate_api("rooms/")
    room_id_to_name: dict[int, str] = {}
    for room in rooms_data:
        room_name = room.get("name", {})
        if isinstance(room_name, dict):
            room_name = room_name.get("en", "")
        room_id_to_name[room["id"]] = room_name
    print(f"  Found {len(room_id_to_name)} rooms")

    print("\nFetching schedule slots from Pretalx...")
    slots_data = paginate_api("slots/")
    # Build a lookup from submission code to slot data
    slots_by_submission: dict[str, dict] = {}
    for slot in slots_data:
        submission_code = slot.get("submission")
        if submission_code:
            # Resolve room ID to name
            room_id = slot.get("room")
            room_name = room_id_to_name.get(room_id, "") if isinstance(room_id, int) else ""
            slots_by_submission[submission_code] = {
                "start": slot.get("start"),
                "end": slot.get("end"),
                "room": room_name,
            }
    print(f"  Found {len(slots_by_submission)} scheduled sessions")

    print("\nFetching speakers from Pretalx...")
    speakers = paginate_api("speakers/")
    print(f"  Found {len(speakers)} speakers")

    print("\nFetching answers from Pretalx...")
    answers = paginate_api("answers/")
    print(f"  Found {len(answers)} answers")

    # Build set of speaker codes from confirmed submissions
    confirmed_speaker_codes: set[str] = set()
    for sub in submissions:
        raw_speakers = sub.get("speakers", [])
        for s in raw_speakers:
            # Speakers may be objects with 'code' field or strings
            speaker_code = s.get("code") if isinstance(s, dict) else s
            if speaker_code:
                confirmed_speaker_codes.add(speaker_code)

    # Group answers by speaker code and submission code
    answers_by_speaker: dict[str, list[dict]] = {}
    answers_by_submission: dict[str, list[dict]] = {}
    for answer in answers:
        person = answer.get("person")
        if person:
            if person not in answers_by_speaker:
                answers_by_speaker[person] = []
            answers_by_speaker[person].append(answer)

        submission = answer.get("submission")
        if submission:
            if submission not in answers_by_submission:
                answers_by_submission[submission] = []
            answers_by_submission[submission].append(answer)

    print(f"  Grouped into {len(answers_by_speaker)} speakers, {len(answers_by_submission)} submissions")

    # Process data
    print("\nProcessing sessions...")
    sessions = process_sessions(submissions, track_mappings, track_id_to_name, slots_by_submission, answers_by_submission)
    print(f"  Processed {len(sessions)} sessions")

    print("\nProcessing breaks...")
    breaks = process_breaks(slots_data, room_id_to_name)
    print(f"  Processed {len(breaks)} breaks")

    print("\nProcessing speakers...")
    # Only process speakers who are associated with confirmed submissions
    confirmed_speakers = [s for s in speakers if s.get("code") in confirmed_speaker_codes]
    people = process_speakers(confirmed_speakers, answers_by_speaker)
    print(f"  Processed {len(people)} speakers (filtered from {len(speakers)} total)")

    # Write session files (sessions + breaks)
    sessions_dir = project_root / SESSIONS_OUTPUT_DIR
    all_sessions = sessions + breaks

    # Clean up old session files before writing new ones
    print(f"\nCleaning up old session files in {sessions_dir}...")
    if sessions_dir.exists():
        for old_file in sessions_dir.glob("*.md"):
            old_file.unlink()

    print(f"Writing session files to {sessions_dir}...")
    for i, session in enumerate(all_sessions):
        write_session_file(session, sessions_dir)
        if (i + 1) % 20 == 0:
            print(f"    Wrote {i + 1}/{len(all_sessions)} session files...")
    print(f"  Wrote {len(all_sessions)} session files ({len(sessions)} sessions + {len(breaks)} breaks)")

    # Download avatars and write speaker files
    people_dir = project_root / PEOPLE_OUTPUT_DIR
    avatars_dir = project_root / AVATARS_OUTPUT_DIR

    # Clean up old people files
    print(f"\nCleaning up old speaker files in {people_dir}...")
    if people_dir.exists():
        for old_file in people_dir.glob("*.md"):
            old_file.unlink()

    # Clean up old avatar files
    print(f"Cleaning up old avatar files in {avatars_dir}...")
    if avatars_dir.exists():
        for old_file in avatars_dir.glob("*"):
            if old_file.is_file():
                old_file.unlink()

    print(f"\nProcessing speaker avatars and writing files...")

    avatar_count = 0
    for i, person in enumerate(people):
        avatar_path = avatars_dir / f"{person['code']}.jpg"
        has_avatar = avatar_path.exists()

        # Try to download/update avatar
        if person.get("avatar_url"):
            if download_avatar(person["avatar_url"], avatar_path):
                avatar_count += 1
                has_avatar = True

        write_person_file(person, people_dir, has_avatar)

        if (i + 1) % 25 == 0:
            print(f"    Processed {i + 1}/{len(people)} speakers...")

    print(f"  Downloaded {avatar_count} new/updated avatars")
    print(f"  Wrote {len(people)} speaker files")

    print("\n" + "=" * 60)
    print("Sync complete!")
    print(f"  Sessions: {len(sessions)}")
    print(f"  Breaks: {len(breaks)}")
    print(f"  Speakers: {len(people)}")


if __name__ == "__main__":
    main()
