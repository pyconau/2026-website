#!/usr/bin/env python3
"""
Discover Pretalx question IDs and submission types.

This helper script queries the Pretalx API and outputs:
- Question IDs and their titles (for content warnings, pronouns, social handles, etc.)
- Submission type IDs and names (for mapping to session types)

Usage:
    cd scripts && uv run python pretalx_questions.py
"""

import sys

import requests

from config import PRETALX_BASE_URL, PRETALX_EVENT_SLUG, PRETALX_TOKEN


def get_questions() -> list[dict]:
    """Fetch all questions from Pretalx API."""
    if not PRETALX_TOKEN:
        print("Error: PRETALX_TOKEN environment variable not set")
        sys.exit(1)

    url = f"{PRETALX_BASE_URL}/{PRETALX_EVENT_SLUG}/questions/"
    headers = {"Authorization": f"Token {PRETALX_TOKEN}"}

    questions = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        questions.extend(data["results"])
        url = data.get("next")

    return questions


def get_submission_types() -> list[dict]:
    """Fetch all submission types from Pretalx API."""
    if not PRETALX_TOKEN:
        print("Error: PRETALX_TOKEN environment variable not set")
        sys.exit(1)

    url = f"{PRETALX_BASE_URL}/{PRETALX_EVENT_SLUG}/submission-types/"
    headers = {"Authorization": f"Token {PRETALX_TOKEN}"}

    types = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        types.extend(data["results"])
        url = data.get("next")

    return types


def main():
    print(f"Fetching data for event: {PRETALX_EVENT_SLUG}")
    print("=" * 60)

    # Fetch and display submission types
    submission_types = get_submission_types()

    if submission_types:
        print("\nSUBMISSION TYPES:")
        print("-" * 40)
        for st in sorted(submission_types, key=lambda x: x["id"]):
            name = st.get("name", {})
            if isinstance(name, dict):
                name = name.get("en", str(name))
            print(f"  ID: {st['id']:5d}  |  {name}")

        # Generate proposed mapping
        print("\n" + "-" * 40)
        print("Proposed SUBMISSION_TYPE_MAPPING for config.py:")
        print("-" * 40)
        print("SUBMISSION_TYPE_MAPPING: dict[int, str] = {")
        for st in sorted(submission_types, key=lambda x: x["id"]):
            name = st.get("name", {})
            if isinstance(name, dict):
                name = name.get("en", str(name))
            name_lower = name.lower()

            # Propose a mapping
            if "keynote" in name_lower:
                session_type = "keynote"
            elif "workshop" in name_lower:
                session_type = "workshop"
            elif "lightning" in name_lower:
                session_type = "lightning"
            elif "panel" in name_lower:
                session_type = "panel"
            elif "break" in name_lower:
                session_type = "break"
            else:
                session_type = "talk"

            print(f'    {st["id"]}: "{session_type}",  # {name}')
        print("}")

    # Fetch and display questions
    questions = get_questions()

    if questions:
        # Group by target (submission vs speaker)
        submission_questions = []
        speaker_questions = []

        for q in questions:
            if q.get("target") == "submission":
                submission_questions.append(q)
            else:
                speaker_questions.append(q)

        if speaker_questions:
            print("\n" + "=" * 60)
            print("\nSPEAKER QUESTIONS:")
            print("-" * 40)
            for q in sorted(speaker_questions, key=lambda x: x["id"]):
                question_text = q.get("question", {})
                # Handle localized question text
                if isinstance(question_text, dict):
                    text = question_text.get("en", str(question_text))
                else:
                    text = str(question_text)
                print(f"  ID: {q['id']:5d}  |  {text[:50]}")

        if submission_questions:
            print("\nSUBMISSION QUESTIONS:")
            print("-" * 40)
            for q in sorted(submission_questions, key=lambda x: x["id"]):
                question_text = q.get("question", {})
                if isinstance(question_text, dict):
                    text = question_text.get("en", str(question_text))
                else:
                    text = str(question_text)
                print(f"  ID: {q['id']:5d}  |  {text[:50]}")

    print("\n" + "=" * 60)
    print(f"Total: {len(submission_types)} submission types, {len(questions)} questions")
    print("\nUpdate config.py with the IDs and mappings above.")


if __name__ == "__main__":
    main()
