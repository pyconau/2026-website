import { defineCollection, z } from "astro:content"

const posts = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    published: z.coerce.date(),
    category: z.enum(["news", "directors-desk", "uncategorised"]).default("uncategorised"),
  }),
})

export const collections = {
  posts,
}
