export function slugFromId(id: string): string {
  return id.replace(/\.(md|mdx)$/i, "").replace(/\/index$/i, "");
}
