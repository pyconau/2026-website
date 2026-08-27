// Current-time line on the schedule day pages.
//
// Dependency-free vanilla JS, matching the rest of src/scripts. The grid only:
// the mobile agenda (< 768px) deliberately has no equivalent. Its groups are
// start times, not slots, so a line there can only sit between two groups and
// stay parked there for the length of a talk - which reads as a position on a
// time axis the agenda does not have.
//
// The grid is not a single time axis - it is a CSS grid of slot rows x room
// columns, with each session absolutely positioned inside its own slot cell.
// So rather than recomputing the layout maths from src/utils/schedule.ts, this
// measures the row box the browser actually laid out (offsetTop/offsetHeight)
// and interpolates within it. That stays correct across both slot lengths
// (30 min / 160px and 60 min / 130px), every breakpoint, and any future change
// to those numbers.
//
// All comparisons are between absolute instants. Date#toISOString() writes each
// row's start in UTC, and Date.parse() reads it back to the same instant, so a
// visitor in any timezone gets the right answer without converting anything and
// no timezone has to be named here.

/** How often the line is repositioned while the page is open. */
const TICK_MS = 30_000;

/**
 * The current instant, overridable with ?now=<ISO> so the indicator can be
 * seen and reviewed outside the conference week, e.g.
 * ?now=2026-08-27T14:05:00+10:00. An unparseable value is ignored rather than
 * pinning the line to the epoch.
 */
function currentTime() {
  const override = new URLSearchParams(window.location.search).get("now");
  if (override) {
    const parsed = Date.parse(override);
    if (!Number.isNaN(parsed)) return parsed;
  }
  return Date.now();
}

/**
 * Place the grid's line. Each row's time cell carries the row's absolute start;
 * the row that contains "now" gets the line at the matching fraction of its
 * height. No such row - a different day, or before/after the day's sessions -
 * means no line at all.
 */
function updateGrid(grid, marker, now) {
  const slotMs = Number(grid.dataset.slotMinutes) * 60_000;
  if (!Number.isFinite(slotMs) || slotMs <= 0) {
    marker.hidden = true;
    return;
  }

  for (const row of grid.querySelectorAll(".time[data-slot-start]")) {
    const start = Date.parse(row.dataset.slotStart);
    if (Number.isNaN(start)) continue;
    if (now < start || now >= start + slotMs) continue;

    // Below 768px the grid is display: none and every row measures zero. There
    // is no position to be had from a box that was never laid out.
    if (row.offsetHeight === 0) break;

    // offsetTop is relative to .schedule, which is position: relative for
    // exactly this reason.
    const top = row.offsetTop + ((now - start) / slotMs) * row.offsetHeight;
    marker.style.top = `${top}px`;
    marker.hidden = false;
    return;
  }

  marker.hidden = true;
}

function init() {
  const grid = document.querySelector(".schedule[data-slot-minutes]");
  const marker = document.querySelector("[data-schedule-now]");

  // Harmless anywhere else this module is ever included.
  if (!grid || !marker) return;

  const update = () => updateGrid(grid, marker, currentTime());

  // At most one update per frame, however many things ask for one.
  let pending = false;
  const scheduleUpdate = () => {
    if (pending) return;
    pending = true;
    window.requestAnimationFrame(() => {
      pending = false;
      update();
    });
  };

  update();

  window.setInterval(update, TICK_MS);

  // Anything that changes the grid's box invalidates the line's position: the
  // 768px layout swap, a window resize, a font landing after first paint, and
  // in dev the stylesheet itself, which arrives as a module after
  // DOMContentLoaded and so lands after the first measurement. Watching the
  // grid covers all of them, where a list of individual events would not - and
  // the line cannot feed back into it, being absolutely positioned and
  // zero-height.
  if (window.ResizeObserver) {
    new ResizeObserver(scheduleUpdate).observe(grid);
  }
  window.addEventListener("resize", scheduleUpdate);

  // A phone put in a pocket during a talk suspends timers; the line must be
  // right again the moment the screen comes back, not up to TICK_MS later.
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) update();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
