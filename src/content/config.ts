import { defineCollection, z } from "astro:content";

const sessions = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    code: z.string(),
    start: z.coerce.date(),
    end: z.coerce.date(),
    room: z.string(),
    track: z.string().nullable().optional(), // Local slug for linking
    trackName: z.string().optional(), // Original Pretalx track name for display
    type: z
      .enum(["talk", "break", "workshop", "plenary", "poster", "other"])
      .default("talk"),
    speakers: z.array(z.string()).default([]),
    sponsor: z.string().optional(),
    contentWarning: z.string().optional(),
    youtubeSlug: z.string().optional(),
    layout: z.string().optional(), // Graphics layout variant (layout_1, layout_2, etc)
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

const posts = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    published: z.coerce.date(),
    category: z
      .enum(["news", "directors-desk", "uncategorised"])
      .default("uncategorised"),
    previewText: z.string(),
  }),
});

const sponsors = defineCollection({
  type: "content",
  schema: z.object({
    name: z.string(),
    tier: z.enum(["diamond", "platinum", "gold", "standard", "digital", "in-kind", "supporting"]),
    logo: z.string(),
    website: z.string().url().optional(),
  }),
});

const cfpSpecialistTracks = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    shortDescription: z.string(),
    organisers: z
      .array(
        z.object({
          name: z.string(),
          title: z.string(),
          pronouns: z.string().optional(),
          photo: z.string(),
          social: z.record(z.string(), z.string()).optional(),
        })
      )
      .optional()
      .default([]),
  }),
});

const scheduleSpecialistTracks = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    shortDescription: z.string(),
    pretalxTrack: z.string().optional(),
    date: z.coerce.date().optional(),
  }),
});

export const collections = {
  sessions,
  people,
  posts,
  sponsors,
  "cfp-specialist-tracks": cfpSpecialistTracks,
  "schedule-specialist-tracks": scheduleSpecialistTracks,
};
