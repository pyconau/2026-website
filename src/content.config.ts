import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const sessions = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/sessions" }),
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
    abstract: z.string().optional(),
    contentWarning: z.string().optional(),
    youtubeSlug: z.string().optional(),
    tags: z.array(z.string()).default([]),
    graphicsLayout: z.enum(["left", "right"]).optional(), // Graphics panel layout (left or right)
    theme: z.string().optional(), // Graphics theme (e.g. accent_coral, charcoal)
  }),
});

const people = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/people" }),
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
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/posts" }),
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
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/sponsors" }),
  schema: z.object({
    name: z.string(),
    tier: z.enum(["diamond", "platinum", "gold", "standard", "industry", "digital", "in-kind", "supporting"]),
    logo: z.string(),
    website: z.string().url().optional(),
  }),
});

const cfpSpecialistTracks = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/cfp-specialist-tracks" }),
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
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/schedule-specialist-tracks" }),
  schema: z.object({
    title: z.string(),
    shortDescription: z.string(),
    pretalxTrack: z.string().optional(),
    date: z.coerce.date().optional(),
    sponsor: z.string().optional(), // Sponsor slug matching a file in sponsors/
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