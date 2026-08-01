// Favourite bookmarks — Phase 3a (.claude/plans/phase-3a-local-favourites.md).
//
// Dependency-free vanilla JS, matching the rest of src/scripts. One delegated
// listener at the document level rather than one per card: a 37-session
// Saturday means 37 buttons, and delegation is both cheaper and survives any
// future re-render of the list.

import { has, toggle } from "./favourites-storage.js";

const BUTTON_SELECTOR = ".bookmark-btn";

/** How long the bookmark_added confirmation shows before settling to filled. */
const TRANSIENT_MS = 1200;

/**
 * Pending confirmation timers, keyed by the button they belong to. Tracked so a
 * second tap inside the window can cancel one — the transient must never
 * swallow or queue behind a tap — and so a timer can be cleared before it fires
 * against an element that has gone away.
 */
const transientTimers = new WeakMap();

function clearTransient(button) {
  const timer = transientTimers.get(button);
  if (timer !== undefined) {
    window.clearTimeout(timer);
    transientTimers.delete(button);
  }
  button.classList.remove("is-just-added");
}

/**
 * Put a button into its settled state. Hydration and un-favouriting both land
 * here directly, never by way of the confirmation transient (§9).
 */
function applyState(button, favourited) {
  button.setAttribute("aria-pressed", favourited ? "true" : "false");

  // The label follows the action the button will perform, not the state it is
  // in — aria-pressed already carries the state.
  const title = button.dataset.sessionTitle;
  if (title) {
    button.setAttribute(
      "aria-label",
      `${favourited ? "Remove from saved" : "Save"}: ${title}`
    );
  }
}

function onToggle(button) {
  const code = button.dataset.sessionCode;
  if (!code) return;

  // A tap during the confirmation window is a real un-favourite, so cancel the
  // pending settle first and let the toggle below decide the new state.
  clearTransient(button);

  const favourited = toggle(code);
  applyState(button, favourited);

  // Confirmation on add only. Removal needs none — the bookmark visibly
  // disappearing is the feedback. Storage is synchronous, so this is a
  // confirmation and not a loading state.
  if (favourited) {
    button.classList.add("is-just-added");
    const timer = window.setTimeout(() => {
      transientTimers.delete(button);
      button.classList.remove("is-just-added");
    }, TRANSIENT_MS);
    transientTimers.set(button, timer);
  }
}

/**
 * Reflect stored state onto every rendered control. The site is pre-rendered,
 * so every card ships from the CDN unfavourited and is corrected here — kept
 * early and cheap (one storage read, one attribute per button) to keep the
 * flash of unfavourited bookmarks short.
 */
function hydrate() {
  const buttons = document.querySelectorAll(BUTTON_SELECTOR);
  if (buttons.length === 0) return;

  for (const button of buttons) {
    const code = button.dataset.sessionCode;
    // A stored code that isn't in this build's schedule — a cancelled session,
    // or a stale entry — simply has no button here. It is skipped, not
    // deleted: the schedule regenerates from Pretalx and a session can
    // plausibly disappear and come back (§4.3).
    applyState(button, code ? has(code) : false);
  }
}

function init() {
  hydrate();

  // Every bookmark sits inside a card that is itself a link to the session
  // page, so the click must be stopped dead: without both calls, favouriting
  // navigates away every single time.
  document.addEventListener("click", (event) => {
    const button = event.target.closest?.(BUTTON_SELECTOR);
    if (!button) return;

    event.preventDefault();
    event.stopPropagation();

    onToggle(button);
  });

  // Clear any pending confirmation before the page goes away, so a timer never
  // fires against a detached element.
  window.addEventListener("pagehide", () => {
    for (const button of document.querySelectorAll(BUTTON_SELECTOR)) {
      clearTransient(button);
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init, { once: true });
} else {
  init();
}
