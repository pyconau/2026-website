# Schedule & Program Feature Implementation Plan

This document outlines the plan for implementing the schedule/program feature for the PyCon AU 2026 website. The feature synchronises session and speaker data from Pretalx and renders it using the new 2026 design.

## Overview

### Goals
1. Sync session and speaker data from Pretalx API to local markdown files
2. Render schedule, session, and speaker pages using the 2026 design
3. Support specialist tracks with their own landing pages and session lists
4. Build in phases: 2025 data first, then mock 2026 data, then production 2026 data

### URL Structure
| Page | URL | Design Template |
|------|-----|-----------------|
| Program landing | `/program` | TBD (simple list for now) |
| Specialist tracks index | `/program/specialist-tracks` | `session-landing.html` |
| Individual specialist track | `/program/specialist-tracks/[track-slug]` | `session-index.html` |
| Track shortcut | `/[track-slug]` | Redirect to above |
| Day schedule | `/program/[day]` | `schedule-hardcoded.html` |
| Session detail | `/program/[code]` | `session-post-alt.html` |

---

## Phase 1: Data Sync Scripts

### 1.1 Script Structure

Create `scripts/` directory with:

```
scripts/
├── pyproject.toml          # Poetry dependencies
├── poetry.lock
├── schedule_sync.py        # Main sync script
├── pretalx_questions.py    # Helper to discover question IDs
└── config.py               # Configuration constants
```

### 1.2 Dependencies

Same as 2025 script:
- `requests` - HTTP client for Pretalx API
- `ruamel.yaml` - YAML parsing (for reading existing files)
- `python-dateutil` - Timezone handling
- `Pillow` - Image processing for speaker avatars

### 1.3 Configuration (`config.py`)

```python
# Pretalx API
PRETALX_EVENT_SLUG = "pycon-au-2025"  # Phase 1: 2025 data
EVENT_TIMEZONE = "Australia/Melbourne"

# Question IDs (discovered via pretalx_questions.py)
CONTENT_WARNING_QUESTION_ID = 5326
PRONOUNS_QUESTION_ID = 5332
BLUESKY_QUESTION_ID = 5329
FEDIVERSE_QUESTION_ID = 5328

# Room labels (optional display name overrides)
# If a room from the API is not listed here, the API name is used as-is
ROOM_LABELS = {
    "Ballroom 1": "Ballroom 1",
    "Ballroom 2": "Ballroom 2",
    "Ballroom 3": "Ballroom 3",
    # "Junior Ballroom": "Junior Ballroom",  # Example: uncomment to override
}

# Plenary rooms (combined ballrooms for keynotes)
# Sessions marked as keynote/plenary span all these rooms
PLENARY_ROOMS = ["Ballroom 1", "Ballroom 2", "Ballroom 3"]
```

**Note:** Track mappings are NOT hardcoded. Instead, tracks are derived from local `src/content/specialist-tracks/*.md` files via their `pretalxTrack` frontmatter field. See section 1.6.

### 1.4 Question Discovery Script (`pretalx_questions.py`)

A helper script that queries the Pretalx questions API and outputs a list of question IDs and their titles. This helps identify the correct question IDs for content warnings, pronouns, social handles, etc.

Usage:
```bash
cd scripts && poetry run python pretalx_questions.py
```

### 1.5 Main Sync Script (`schedule_sync.py`)

Adapted from 2025 script with these changes:

**Input:** Pretalx API (sessions, speakers, answers)

**Output:** Markdown files with frontmatter

**Sessions** → `src/content/sessions/[code].md`
```yaml
---
title: "Session Title"
code: "ABC123"
start: 2025-09-05T09:00:00+10:00
end: 2025-09-05T10:00:00+10:00
room: "Ballroom 1"  # Room name from API (or label if configured)
track: data-and-ai  # null for Main Conference
type: talk  # talk, keynote, break, workshop, etc.
speakers:
  - speaker-code-1
  - speaker-code-2
sponsor: "Acme Corporation"  # Optional: sponsoring company name
contentWarning: "Optional content warning"
youtubeSlug: "video-id"  # Added post-conference
---

Session abstract/description in Markdown (from Pretalx API)
```

**Speakers** → `src/content/people/[code].md`
```yaml
---
name: "Speaker Name"
code: "SPEAKER123"
pronouns: "they/them"
bluesky: "@speaker.bsky.social"
fediverse: "@speaker@fosstodon.org"
hasAvatar: true
---

Speaker biography in Markdown (from Pretalx API)
```

**Speaker Avatars** → `public/images/people/[code].jpg`
- Downloaded from Pretalx
- Resized to 225×225 pixels
- Optimised as JPEG (95% quality)
- Uses HTTP ETag caching to avoid redundant downloads

### 1.6 Specialist Track Updates

The sync script derives track mappings from local filesystem, not hardcoded config. Each `src/content/specialist-tracks/*.md` file includes a `pretalxTrack` frontmatter key:

```yaml
---
title: "Data & AI"
pretalxTrack: "Data & AI"  # Exact track name from Pretalx API
shortDescription: "..."
organisers: [...]
---
```

**How it works:**

1. The sync script reads all `src/content/specialist-tracks/*.md` files at startup
2. It builds a mapping of `pretalxTrack` → `file slug` (e.g., `"Data & AI"` → `"data-and-ai"`)
3. When processing sessions, it looks up the track name in this mapping
4. Sessions with tracks not in the mapping get `track: null` (Main Conference)

**Benefits:**
- Track configuration lives with track content, not in a separate config
- Adding a new specialist track only requires creating the markdown file
- Phase 1→2→3 transitions only require updating `pretalxTrack` values

**Example mappings for Phase 1 (2025 data):**

| File | `pretalxTrack` value | Notes |
|------|---------------------|-------|
| `data-and-ai.md` | `"Data & AI"` | Direct match |
| `education.md` | `"Education"` | Direct match |
| `cybersecurity.md` | `"Security"` | 2025 used different name |
| `devrel.md` | `null` | No 2025 equivalent, skip for Phase 1 |
| `platform-engineering.md` | `null` | No 2025 equivalent, skip for Phase 1 |
| `research-software-engineering.md` | `"Scientific Python"` | Map to closest 2025 track |

---

## Phase 2: Content Collections & Schema

### 2.1 Update Content Config

Update `src/content/config.ts` to add new collections:

```typescript
const sessions = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    code: z.string(),
    start: z.coerce.date(),
    end: z.coerce.date(),
    room: z.string(),
    track: z.string().nullable(),
    type: z.enum(["talk", "keynote", "break", "workshop", "lightning", "panel"]).default("talk"),
    speakers: z.array(z.string()).default([]),
    sponsor: z.string().optional(),
    contentWarning: z.string().optional(),
    youtubeSlug: z.string().optional(),
  }),
});

const people = defineCollection({
  type: "content",
  schema: z.object({
    name: z.string(),
    code: z.string(),
    pronouns: z.string().optional(),
    bluesky: z.string().optional(),
    fediverse: z.string().optional(),
    hasAvatar: z.boolean().default(false),
  }),
});

// Update specialist-tracks to include pretalxTrack
const specialistTracks = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    pretalxTrack: z.string().optional(),  // NEW: maps to Pretalx track name
    shortDescription: z.string(),
    organisers: z.array(...).optional().default([]),
  }),
});
```

---

## Phase 3: Page Templates

### 3.1 Specialist Tracks Index (`/program/specialist-tracks`)

**File:** `src/pages/program/specialist-tracks/index.astro`

**Based on:** `static/session-landing.html`

**Data:**
- All specialist tracks from `specialist-tracks` collection
- Session counts per track (from `sessions` collection)

### 3.2 Individual Specialist Track (`/program/specialist-tracks/[slug]`)

**File:** `src/pages/program/specialist-tracks/[...slug].astro`

**Based on:** `static/session-index.html`

**Data:**
- Track metadata from `specialist-tracks` collection
- Sessions matching `track` field, ordered by `start` time
- Speaker data for each session

**Note:** Each specialist track runs on a single day, in a single room.

### 3.3 Track Shortcuts

**File:** `astro.config.mjs` (redirects)

Add redirects for each specialist track slug:
```javascript
redirects: {
  '/data-and-ai': '/program/specialist-tracks/data-and-ai',
  '/education': '/program/specialist-tracks/education',
  '/cybersecurity': '/program/specialist-tracks/cybersecurity',
  '/devrel': '/program/specialist-tracks/devrel',
  '/platform-engineering': '/program/specialist-tracks/platform-engineering',
  '/research-software-engineering': '/program/specialist-tracks/research-software-engineering',
  // ... existing redirects
}
```

### 3.4 Day Schedule (`/program/[day]`)

**File:** `src/pages/program/[day].astro`

**Based on:** `static/schedule-hardcoded.html`

**Data:**
- Sessions filtered by day (derived from `start` date)
- Grouped by room and time slot
- Links to individual session pages

**Days:** wednesday, thursday, friday, saturday (derived from session data)

**Special Layout Scenarios:**

1. **Keynotes/Plenaries:** Sessions with `type: "keynote"` or `type: "plenary"` span the full width across all plenary rooms (configured in `PLENARY_ROOMS`). The ballrooms are combined into one large room for these sessions, so visually they should span columns.

2. **Breaks:** Sessions with `type: "break"` (morning tea, lunch, afternoon tea) are displayed in the schedule grid but are NOT clickable. They may have text/detail but don't expand to a session detail page. Breaks may run in some rooms while regular sessions run in others (e.g., a workshop continues through a break).

### 3.5 Session Detail (`/program/[code]`)

**File:** `src/pages/program/[code].astro`

**Based on:** `static/session-post-alt.html`

**Data:**
- Session from `sessions` collection
- Speakers from `people` collection (using speaker codes)
- Track metadata (if specialist track)

**Features:**
- Breadcrumb: Home > Specialist Tracks > [Track Name] (or Home > Program)
- Session title, time, room, track
- Full session description
- Speaker cards with photos, bios, pronouns, social links

### 3.6 Program Landing (`/program`)

**File:** `src/pages/program/index.astro`

**Design:** TBD - Simple placeholder for now

**Data:**
- List of days with session counts
- Links to `/program/[day]`
- Link to specialist tracks index

---

## Phase 4: Components

### 4.1 New Components Needed

| Component | Purpose | Based On |
|-----------|---------|----------|
| `SessionCard.astro` | Session preview card (title, time, speakers) | `session-index.html` cards |
| `SpeakerCard.astro` | Speaker bio card with photo | `session-post-alt.html` speaker section |
| `SponsorBadge.astro` | "Sponsored by X" indicator for sponsored talks | `session-post-alt.html` sponsor line |
| `ScheduleGrid.astro` | Time/room grid for day view | `schedule-hardcoded.html` schedule |
| `ScheduleSlot.astro` | Individual slot in schedule (session or break) | `schedule-hardcoded.html` cells |
| `ScheduleBreak.astro` | Non-clickable break slot (morning tea, lunch) | `schedule-hardcoded.html` break cells |
| `ScheduleKeynote.astro` | Full-width keynote/plenary slot | `schedule-hardcoded.html` keynote row |
| `DayTabs.astro` | Day navigation tabs | `schedule-hardcoded.html` tabs |
| `TrackBadge.astro` | Coloured track indicator | Existing track badges |

### 4.2 Shared Utilities

**File:** `src/utils/schedule.ts`

```typescript
// Get sessions for a specific day
export function getSessionsByDay(sessions, day: string)

// Get sessions for a specific track
export function getSessionsByTrack(sessions, trackSlug: string)

// Group sessions by room and time slot
export function groupSessionsForSchedule(sessions)

// Get unique days from session data
export function getConferenceDays(sessions): string[]

// Format session time
export function formatSessionTime(start: Date, end: Date): string
```

---

## Implementation Order

### Step 1: Scripts Setup
1. Create `scripts/` directory structure
2. Copy and adapt `schedule_sync.py` from 2025
3. Create `pretalx_questions.py` helper
4. Test sync against pycon-au-2025 event

### Step 2: Content Collections
1. Update `src/content/config.ts` with new schemas
2. Add `pretalxTrack` to specialist track files
3. Run sync to populate `sessions` and `people` collections
4. Verify data structure

### Step 3: Session Detail Page
1. Create `src/pages/program/[code].astro`
2. Build `SpeakerCard.astro` component
3. Style based on `session-post-alt.html`

### Step 4: Specialist Track Pages
1. Create `SessionCard.astro` component
2. Create `src/pages/program/specialist-tracks/index.astro`
3. Create `src/pages/program/specialist-tracks/[...slug].astro`
4. Add track shortcut redirects

### Step 5: Schedule Pages
1. Create `ScheduleGrid.astro` and `DayTabs.astro`
2. Create `src/pages/program/[day].astro`
3. Create `src/pages/program/index.astro` (simple version)

### Step 6: Navigation Updates
1. Update header navigation with Program menu
2. Add day nav bubble links

---

## Testing Phases

### Phase 1: 2025 Data
- Use `pycon-au-2025` Pretalx event
- Map 2025 tracks to 2026 specialist tracks
- Verify all pages render correctly

### Phase 2: Mock 2026 Data
- Switch to `pycon-au-2026` event slug
- Create test sessions in Pretalx
- Verify track mapping works correctly

### Phase 3: Production 2026 Data
- Final track name mapping
- Room mapping updates if venues change
- Question ID updates if Pretalx form changes

---

## Environment Variables

```bash
# Required
PRETALX_TOKEN=your-api-token

# Optional (for switching between events)
PRETALX_EVENT=pycon-au-2025
```

---

## Open Questions / Future Work

1. **YouTube integration:** How/when are video slugs added post-conference?
2. **Sprint day:** Custom layout for Sunday sprints (not from Pretalx)
3. **Session types:** Keynotes, workshops, lightning talks - different styling?
4. **Search:** Session/speaker search functionality
5. **Favourites:** Personal schedule builder (localStorage or account-based)

---

## File Changes Summary

### New Files
- `scripts/pyproject.toml`
- `scripts/schedule_sync.py`
- `scripts/pretalx_questions.py`
- `scripts/config.py`
- `src/content/sessions/*.md` (generated)
- `src/content/people/*.md` (generated)
- `public/images/people/*.jpg` (generated)
- `src/pages/program/index.astro`
- `src/pages/program/[day].astro`
- `src/pages/program/[code].astro`
- `src/pages/program/specialist-tracks/index.astro`
- `src/pages/program/specialist-tracks/[...slug].astro`
- `src/components/schedule/SessionCard.astro`
- `src/components/schedule/SpeakerCard.astro`
- `src/components/schedule/ScheduleGrid.astro`
- `src/components/schedule/DayTabs.astro`
- `src/components/schedule/TrackBadge.astro`
- `src/components/schedule/SponsorBadge.astro`
- `src/components/schedule/ScheduleSlot.astro`
- `src/components/schedule/ScheduleBreak.astro`
- `src/components/schedule/ScheduleKeynote.astro`
- `src/utils/schedule.ts`

### Modified Files
- `src/content/config.ts` - Add sessions, people collections
- `src/content/specialist-tracks/*.md` - Add `pretalxTrack` field
- `astro.config.mjs` - Add track shortcut redirects
- `src/components/Header.astro` - Update navigation

---

## Acceptance Criteria

- [ ] Running `poetry run python schedule_sync.py` populates session and speaker content
- [ ] Sync script reads track mappings from `specialist-tracks/*.md` files (not hardcoded)
- [ ] Speaker avatars are downloaded and optimised
- [ ] All session pages render at `/program/[code]`
- [ ] Specialist track pages list their sessions ordered by time
- [ ] Track shortcut URLs redirect correctly
- [ ] Schedule grid shows sessions organised by room and time
- [ ] Keynote/plenary sessions span full width across plenary rooms
- [ ] Break slots are displayed but not clickable
- [ ] Sponsored talks display sponsor badge
- [ ] Speaker cards display with photos, bios, and social links
- [ ] Content warning displays when present
- [ ] Mobile-responsive layout matches designs
