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
    tier: z.enum(["diamond", "platinum", "gold", "standard", "digital", "in-kind"]),
    logo: z.string(),
    website: z.string().url().optional(),
  }),
});

export const collections = {
  posts,
  sponsors,
};
