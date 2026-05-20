# Specialist Tracks Implementation Plan

## Overview

Create a data-driven specialist tracks system using Astro content collections, allowing track information to be managed via markdown files with YAML frontmatter.

## File Structure

```
src/
  content/
    specialist-tracks/          # New directory for track markdown files
      example-track.md          # Example track file
    config.ts                   # Update to add specialistTracks collection
  components/
    cfp/
      TrackOrganiser.astro      # New component (based on our-team profile style)
      SpecialistTrack.astro     # New component to render a track section
  pages/
    cfp/
      specialist-tracks.astro   # Update to use new data-driven approach
public/
  images/
    specialist-tracks/          # New directory for track organiser photos
```

## 1. Content Collection Schema

Add to `src/content/config.ts`:

```typescript
const specialistTracks = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    shortDescription: z.string(),
    organisers: z.array(z.object({
      name: z.string(),
      title: z.string(),
      pronouns: z.string().optional(),
      photo: z.string(),
      social: z.record(z.string(), z.string()).optional(),  // {"LinkedIn": "url", "Bluesky": "url", "Mastodon": "url"}
    })).optional().default([]),
  }),
});
```

## 2. Example Track Markdown File

`src/content/specialist-tracks/example-track.md`:

```markdown
---
title: Example Track
shortDescription: A one-sentence description of what this track is about.
organisers:
  - name: Jane Doe
    title: Software Engineer
    pronouns: She/Her
    photo: /images/specialist-tracks/jane-doe.jpg
    social:
      LinkedIn: https://linkedin.com/in/janedoe
      Bluesky: https://bsky.app/profile/janedoe
  - name: John Smith
    title: Data Scientist
    photo: /images/specialist-tracks/john-smith.jpg
    social:
      Mastodon: https://mastodon.social/@johnsmith
---

This is the first paragraph of the longer description. It provides more context about what the track covers and who might be interested in submitting proposals.

This is the second paragraph. It could include specific topics of interest, the format of sessions, or any other relevant details for potential speakers.
```

## 3. TrackOrganiser Component

New file: `src/components/cfp/TrackOrganiser.astro`

Based on the commented-out profile cards in `our-team.astro` (lines 153-506), using the emerald card style with:
- Profile photo
- Name (text-stone)
- Title (text-lime)
- Pronouns (text-stone/50, optional)
- Social links (rendered dynamically from the `social` object keys)

## 4. SpecialistTrack Component

New file: `src/components/cfp/SpecialistTrack.astro`

Props:
- `title`: string
- `shortDescription`: string
- `content`: rendered markdown (the longer description)
- `organisers`: array of organiser objects

Structure:
- H2 with track title (styled consistently with site)
- Short description paragraph
- Rendered markdown content for longer description
- Grid of TrackOrganiser cards (if organisers exist)

## 5. Updated specialist-tracks.astro Page

- Import and query the `specialistTracks` collection
- Loop through tracks and render each using `SpecialistTrack` component
- Maintain existing page header, navigation, and footer

## 6. Photo Directory

Create: `public/images/specialist-tracks/`

Upload track organiser photos here with consistent naming (e.g., `firstname-lastname.jpg`).

## Implementation Notes

- Social links use flexible key-based approach: the key becomes the link text (e.g., "LinkedIn", "Bluesky", "Mastodon")
- Tracks can have zero organisers (the organisers section simply won't render)
- The emerald card style from the our-team mockup provides visual consistency
- Each track markdown file = one track section on the page
