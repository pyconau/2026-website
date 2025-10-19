import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const blog = await getCollection('blog');

  // Filter for news and announcements only, and sort by date descending
  const newsAndAnnouncements = blog
    .filter(post => post.data.category === 'news')
    .sort((a, b) => b.data.published.valueOf() - a.data.published.valueOf());

  return rss({
    title: 'PyCon AU 2026 News & Announcements',
    description: 'Latest news and announcements from PyCon AU 2026',
    site: context.site || 'https://2026.pycon.org.au',
    items: newsAndAnnouncements.map((post) => ({
      title: post.data.title,
      pubDate: post.data.published,
      link: `/blog/${post.slug}/`,
    })),
    customData: `<language>en-au</language>`,
  });
}
