import { defineCollection, z } from "astro:content";

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

const specialistTracks = defineCollection({
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

export const collections = {
  posts,
  sponsors,
  "specialist-tracks": specialistTracks,
};
