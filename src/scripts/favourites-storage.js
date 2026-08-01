// Local favourites storage — Phase 3a (.claude/plans/phase-3a-local-favourites.md §4).
//
// Session code -> ISO timestamp, in localStorage. Nothing else is stored: no
// titles, times or rooms. A favourite is a reference into the schedule, not a
// snapshot of it, so it can never go stale when the schedule flexes.
//
// No network, no sync, no auth. Phase 3b adds those on top of this shape.

export const STORAGE_KEY = "pyconau2026.favourites";
export const STORAGE_VERSION = 1;

/**
 * The empty document. `migratedToAccount` is reserved for Phase 3b's one-time
 * anonymous -> authenticated merge (§6): the flag has to exist from the first
 * version, or devices that already merged have no record of it and their
 * deliberately-deleted favourites get resurrected.
 */
function emptyStore() {
  return { version: STORAGE_VERSION, favourites: {}, migratedToAccount: false };
}

/**
 * In-memory fallback for when localStorage is unavailable — Safari private
 * browsing throws on access, and it can be disabled outright (§4.4).
 * Favourites then work for the session and evaporate. Deliberately silent: an
 * attendee who has locked their browser down doesn't need a warning.
 */
let memoryStore = null;

let storageAvailable;

function hasLocalStorage() {
  if (storageAvailable !== undefined) return storageAvailable;
  try {
    const probe = "__pyconau_probe__";
    window.localStorage.setItem(probe, probe);
    window.localStorage.removeItem(probe);
    storageAvailable = true;
  } catch {
    storageAvailable = false;
  }
  return storageAvailable;
}

/**
 * Read the stored document, treating everything in localStorage as untrusted
 * (§4.2). It is shared, user-editable and survives deploys, so anything
 * unexpected — unparseable JSON, a future version, a hand-edited shape —
 * resolves to empty rather than throwing on page load and taking the schedule
 * down with it. The bad value is left in place and overwritten on next write.
 */
export function read() {
  if (!hasLocalStorage()) {
    if (!memoryStore) memoryStore = emptyStore();
    return memoryStore;
  }

  let raw;
  try {
    raw = window.localStorage.getItem(STORAGE_KEY);
  } catch {
    return emptyStore();
  }

  if (!raw) return emptyStore();

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return emptyStore();
  }

  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    return emptyStore();
  }

  // An unknown version is not interpreted — guessing at what an older or newer
  // shape meant is how a migration goes wrong.
  if (parsed.version !== STORAGE_VERSION) return emptyStore();

  const source =
    parsed.favourites &&
    typeof parsed.favourites === "object" &&
    !Array.isArray(parsed.favourites)
      ? parsed.favourites
      : {};

  // Keep only code -> string pairs. A hand-edited object value or a null would
  // otherwise flow through to the merge in Phase 3b.
  const favourites = {};
  for (const [code, addedAt] of Object.entries(source)) {
    if (typeof code === "string" && code && typeof addedAt === "string") {
      favourites[code] = addedAt;
    }
  }

  return {
    version: STORAGE_VERSION,
    favourites,
    migratedToAccount: parsed.migratedToAccount === true,
  };
}

/**
 * Write synchronously — no debounce. The data is tiny, and losing a write
 * because someone closed the tab immediately is far worse than writing often
 * (§3.5). A quota or private-browsing failure falls back to memory rather than
 * throwing into a click handler.
 */
export function write(store) {
  if (!hasLocalStorage()) {
    memoryStore = store;
    return;
  }
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
  } catch {
    memoryStore = store;
  }
}

/** Is this session code favourited? */
export function has(code) {
  if (!code) return false;
  return Object.prototype.hasOwnProperty.call(read().favourites, code);
}

/** Every favourited session code. Order is not meaningful. */
export function list() {
  return Object.keys(read().favourites);
}

export function add(code) {
  if (!code) return false;
  const store = read();
  store.favourites[code] = new Date().toISOString();
  write(store);
  return true;
}

export function remove(code) {
  if (!code) return false;
  const store = read();
  delete store.favourites[code];
  write(store);
  return false;
}

/**
 * Toggle a favourite, returning the resulting state: true if it is now
 * favourited, false if it is not.
 */
export function toggle(code) {
  return has(code) ? remove(code) : add(code);
}
