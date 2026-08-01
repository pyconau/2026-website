// Curated exceptions to ordinary favouriting.
//
// Both lists are hardcoded by session code rather than derived from session
// type, because neither rule actually follows from type. "Always favourited"
// is not all plenaries - the lightning talks and the opening keynote talks are
// plenaries an attendee may well want to opt out of. And "cannot be
// favourited" is a registration question, not a scheduling one.
//
// Codes are stable Pretalx identifiers, so this list survives a retitle. It
// does not survive a session being recreated upstream, which is the known cost
// of hardcoding; a code that no longer exists is simply inert.

/**
 * Sessions everybody is at. These render as favourited and cannot be
 * unfavourited - the bookmark is shown filled and inert, as a statement rather
 * than a control.
 *
 * Conference welcome for each day, the keynotes now that they are public, and
 * the closing address.
 */
export const ALWAYS_FAVOURITED = new Set<string>([
  // Conference welcome - Thursday, Friday, Saturday
  "3FQZVE",
  "VQD3SG",
  "9PXVYP",

  // Keynotes
  "NDWRBS", // Thursday - 30 to 70 PRs a day
  "BYLBNB", // Friday - Why Australians don't trust AI
  "X79GWF", // Saturday - The Care of Software

  // Conference close
  "TGQGWT", // Closing address
]);

/**
 * Sessions ticketed separately from the conference. Favouriting is disabled on
 * these for now: an attendee who has not registered would otherwise save a
 * session they cannot attend, and one who has does not need to.
 *
 * This is a placeholder treatment. The intended UX is a control that reflects
 * registration rather than one that is simply switched off.
 */
export const NOT_FAVOURITABLE = new Set<string>([
  // Workshops. Sprints belong here in principle, but they are not sessions -
  // they live on their own hand-built page and are included with a contributor
  // ticket - so there is no card to disable and nothing to list.
  "H33RW8", // Build a cross-platform GUI app with Python
  "GGCEE9", // Typed Python: from Zero to Hero
  "PZPG8U", // Building Durable AI Agents with AWS Strands, MCP, and Temporal
]);

/** Is this session pinned as always-favourited? */
export function isAlwaysFavourited(code: string): boolean {
  return ALWAYS_FAVOURITED.has(code);
}

/** Is favouriting disabled for this session? */
export function isNotFavouritable(code: string): boolean {
  return NOT_FAVOURITABLE.has(code);
}
