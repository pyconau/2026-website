import { getCollection } from "astro:content";
import type { CollectionEntry } from "astro:content";

// ============================================================================
// Configuration
// ============================================================================

/**
 * Conference timezone - used for all date/time formatting and calculations.
 * Change this when setting up a conference in a different location.
 */
export const CONFERENCE_TIMEZONE = "Australia/Melbourne";

// ============================================================================
// Types
// ============================================================================

export type Session = CollectionEntry<"sessions">;
export type Person = CollectionEntry<"people">;
export type SpecialistTrack = CollectionEntry<"specialist-tracks">;

/**
 * Get all sessions for a specific track slug
 */
export async function getSessionsByTrack(trackSlug: string): Promise<Session[]> {
  const sessions = await getCollection("sessions");
  return sessions
    .filter((session) => session.data.track === trackSlug)
    .sort((a, b) => {
      const aStart = a.data.start?.getTime() ?? 0;
      const bStart = b.data.start?.getTime() ?? 0;
      return aStart - bStart;
    });
}

/**
 * Check if a date is valid (not null, undefined, or Unix epoch from invalid parsing)
 */
function isValidSessionDate(date: Date | null | undefined): date is Date {
  if (!date) return false;
  // Check for Unix epoch (invalid date parsing) - year 1970
  if (date.getFullYear() < 2000) return false;
  return !isNaN(date.getTime());
}

/**
 * Get sessions for a specific day
 */
export async function getSessionsByDay(dayName: string): Promise<Session[]> {
  const sessions = await getCollection("sessions");
  return sessions
    .filter((session) => {
      if (!isValidSessionDate(session.data.start)) return false;
      const day = session.data.start.toLocaleDateString("en-AU", {
        weekday: "long",
        timeZone: CONFERENCE_TIMEZONE,
      });
      return day.toLowerCase() === dayName.toLowerCase();
    })
    .sort((a, b) => {
      const aStart = a.data.start?.getTime() ?? 0;
      const bStart = b.data.start?.getTime() ?? 0;
      return aStart - bStart;
    });
}

/**
 * Get unique conference days from session data, sorted by actual date.
 * Only returns days that have sessions scheduled.
 */
export async function getConferenceDays(): Promise<string[]> {
  const sessions = await getCollection("sessions");

  // Map day names to their earliest date for sorting
  const dayDates = new Map<string, Date>();

  sessions.forEach((session) => {
    if (isValidSessionDate(session.data.start)) {
      const day = session.data.start.toLocaleDateString("en-AU", {
        weekday: "long",
        timeZone: CONFERENCE_TIMEZONE,
      }).toLowerCase();

      // Keep track of the earliest date for each day name
      const existingDate = dayDates.get(day);
      if (!existingDate || session.data.start < existingDate) {
        dayDates.set(day, session.data.start);
      }
    }
  });

  // Sort by actual date order
  return Array.from(dayDates.entries())
    .sort((a, b) => a[1].getTime() - b[1].getTime())
    .map(([dayName]) => dayName);
}

/**
 * Format session time range
 */
export function formatSessionTime(start: Date, end: Date): string {
  const options: Intl.DateTimeFormatOptions = {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
    timeZone: CONFERENCE_TIMEZONE,
  };

  const startTime = start.toLocaleTimeString("en-AU", options);
  const endTime = end.toLocaleTimeString("en-AU", options);

  return `${startTime} - ${endTime}`;
}

/**
 * Format session day and date
 */
export function formatSessionDate(date: Date): string {
  return date.toLocaleDateString("en-AU", {
    weekday: "long",
    day: "numeric",
    month: "long",
    timeZone: CONFERENCE_TIMEZONE,
  });
}

/**
 * Get a speaker/person by their code
 */
export async function getPersonByCode(code: string): Promise<Person | undefined> {
  const people = await getCollection("people");
  return people.find((person) => person.data.code === code);
}

/**
 * Get multiple speakers by their codes
 */
export async function getPeopleByCode(codes: string[]): Promise<Person[]> {
  const people = await getCollection("people");
  return codes
    .map((code) => people.find((person) => person.data.code === code))
    .filter((person): person is Person => person !== undefined);
}

/**
 * Get track metadata by slug
 */
export async function getTrackBySlug(
  slug: string
): Promise<SpecialistTrack | undefined> {
  const tracks = await getCollection("specialist-tracks");
  return tracks.find((track) => track.slug === slug);
}

/**
 * Get sessions that belong to a specialist track based on its pretalxTrack mapping
 */
export async function getSessionsForSpecialistTrack(
  track: SpecialistTrack
): Promise<Session[]> {
  const pretalxTrack = track.data.pretalxTrack;
  if (!pretalxTrack) return [];

  // Find the slug that maps from this pretalxTrack
  // Sessions use the slug, not the pretalxTrack name
  const allTracks = await getCollection("specialist-tracks");
  const matchingSlugs = allTracks
    .filter((t) => t.data.pretalxTrack === pretalxTrack)
    .map((t) => t.slug);

  const sessions = await getCollection("sessions");
  return sessions
    .filter((session) => matchingSlugs.includes(session.data.track ?? ""))
    .sort((a, b) => {
      const aStart = a.data.start?.getTime() ?? 0;
      const bStart = b.data.start?.getTime() ?? 0;
      return aStart - bStart;
    });
}

/**
 * Track color configuration
 */
export const trackColors: Record<string, { bg: string; text: string }> = {
  "data-and-ai": { bg: "#F2BF36", text: "#282828" },
  "research-software-engineering": { bg: "#511FE5", text: "#FFFFFF" },
  education: { bg: "#EF553C", text: "#FFFFFF" },
  cybersecurity: { bg: "#10B981", text: "#FFFFFF" },
  devrel: { bg: "#8B5CF6", text: "#FFFFFF" },
  "platform-engineering": { bg: "#F97316", text: "#FFFFFF" },
  default: { bg: "#FFFFFF", text: "#282828" },
};

/**
 * Get track color configuration
 */
export function getTrackColor(trackSlug: string | null): {
  bg: string;
  text: string;
} {
  if (!trackSlug) return trackColors.default;
  return trackColors[trackSlug] || trackColors.default;
}

/**
 * Get unique rooms from sessions for a given day
 */
export async function getRoomsForDay(dayName: string): Promise<string[]> {
  const sessions = await getSessionsByDay(dayName);
  const rooms = new Set<string>();

  sessions.forEach((session) => {
    if (session.data.room) {
      rooms.add(session.data.room);
    }
  });

  // Sort rooms by common conference room naming
  const roomOrder = [
    "Ballroom 1",
    "Ballroom 2",
    "Ballroom 3",
    "Stradbroke Room",
    "Junior Ballroom",
  ];
  return Array.from(rooms).sort((a, b) => {
    const aIdx = roomOrder.indexOf(a);
    const bIdx = roomOrder.indexOf(b);
    if (aIdx === -1 && bIdx === -1) return a.localeCompare(b);
    if (aIdx === -1) return 1;
    if (bIdx === -1) return -1;
    return aIdx - bIdx;
  });
}

/**
 * Time slot for schedule grid
 */
export interface TimeSlot {
  time: Date;
  label: string;
}

/**
 * Generate time slots for a day (30-minute intervals)
 */
export async function getTimeSlotsForDay(dayName: string): Promise<TimeSlot[]> {
  const sessions = await getSessionsByDay(dayName);
  if (sessions.length === 0) return [];

  // Find earliest and latest times
  let earliest: Date | null = null;
  let latest: Date | null = null;

  sessions.forEach((session) => {
    if (session.data.start) {
      if (!earliest || session.data.start < earliest) {
        earliest = session.data.start;
      }
    }
    if (session.data.end) {
      if (!latest || session.data.end > latest) {
        latest = session.data.end;
      }
    }
  });

  if (!earliest || !latest) return [];

  // Round down to nearest 30 minutes for start
  const startTime = new Date(earliest);
  startTime.setMinutes(Math.floor(startTime.getMinutes() / 30) * 30, 0, 0);

  // Round up to nearest 30 minutes for end
  const endTime = new Date(latest);
  endTime.setMinutes(Math.ceil(endTime.getMinutes() / 30) * 30, 0, 0);

  const slots: TimeSlot[] = [];
  const current = new Date(startTime);

  while (current <= endTime) {
    slots.push({
      time: new Date(current),
      label: current.toLocaleTimeString("en-AU", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
        timeZone: CONFERENCE_TIMEZONE,
      }),
    });
    current.setMinutes(current.getMinutes() + 30);
  }

  return slots;
}

// Layout constants
const PX_PER_MINUTE = 3; // pixels per minute of session duration

/**
 * Session prepared for flex layout
 */
export interface FlexSession {
  session: Session;
  heightPx: number; // Height based on duration
  showTrackHeader: boolean; // Whether to show the track header above this session
  isFullWidth: boolean; // True for keynotes and plenaries that span all rooms
}

/**
 * A time block is a group of sessions that happen at the same time.
 * It can be either a full-width session or parallel sessions across rooms.
 */
export interface TimeBlock {
  type: "fullwidth" | "parallel";
  startTime: number;
  endTime: number;
  heightPx: number;
  fullWidthSession?: FlexSession; // For fullwidth blocks
  sessionsByRoom?: Map<string, FlexSession[]>; // For parallel blocks
}

/**
 * Get sessions organized into time blocks for flex-based schedule display
 */
export async function getSessionsForFlexSchedule(
  dayName: string
): Promise<{
  rooms: string[];
  timeBlocks: TimeBlock[];
  allSessionsSorted: FlexSession[];
}> {
  const sessions = await getSessionsByDay(dayName);
  const rooms = await getRoomsForDay(dayName);

  // Create flex sessions
  const allFlexSessions: FlexSession[] = [];

  sessions.forEach((session) => {
    if (!session.data.start || !session.data.end || !session.data.room) return;

    const startTime = session.data.start.getTime();
    const endTime = session.data.end.getTime();
    const durationMinutes = (endTime - startTime) / (1000 * 60);

    const sessionType = session.data.type;
    const isFullWidth = sessionType === "keynote" || sessionType === "plenary";

    const heightPx = durationMinutes * PX_PER_MINUTE;

    const flexSession: FlexSession = {
      session,
      heightPx,
      showTrackHeader: false,
      isFullWidth,
    };

    allFlexSessions.push(flexSession);
  });

  // Sort all sessions by start time
  allFlexSessions.sort((a, b) => {
    const aStart = a.session.data.start?.getTime() ?? 0;
    const bStart = b.session.data.start?.getTime() ?? 0;
    return aStart - bStart;
  });

  // Determine which sessions show track headers
  allFlexSessions.forEach((fs) => {
    const room = fs.session.data.room;
    const startTime = fs.session.data.start?.getTime();
    if (!room || !startTime) return;

    const hasPrecedingSession = allFlexSessions.some((other) => {
      if (other === fs) return false;
      if (other.session.data.room !== room) return false;
      const otherEndTime = other.session.data.end?.getTime();
      return otherEndTime === startTime;
    });

    const trackName = fs.session.data.trackName;
    const isSpecialistTrack = !!trackName && trackName !== "Main Conference";
    fs.showTrackHeader = isSpecialistTrack && !hasPrecedingSession;
  });

  // Group sessions into time blocks
  // A full-width session creates its own block
  // Regular sessions that overlap go into a parallel block
  const timeBlocks: TimeBlock[] = [];
  let currentParallelBlock: TimeBlock | null = null;

  for (const fs of allFlexSessions) {
    const startTime = fs.session.data.start?.getTime() ?? 0;
    const endTime = fs.session.data.end?.getTime() ?? 0;
    const room = fs.session.data.room ?? "";

    if (fs.isFullWidth) {
      // Close any current parallel block
      if (currentParallelBlock) {
        timeBlocks.push(currentParallelBlock);
        currentParallelBlock = null;
      }

      // Add full-width block
      timeBlocks.push({
        type: "fullwidth",
        startTime,
        endTime,
        heightPx: fs.heightPx,
        fullWidthSession: fs,
      });
    } else {
      // Check if this session fits in the current parallel block
      // Sessions fit if they start at or before the current block ends
      if (currentParallelBlock && startTime < currentParallelBlock.endTime) {
        // Add to current block
        if (!currentParallelBlock.sessionsByRoom!.has(room)) {
          currentParallelBlock.sessionsByRoom!.set(room, []);
        }
        currentParallelBlock.sessionsByRoom!.get(room)!.push(fs);
        // Extend end time if needed
        currentParallelBlock.endTime = Math.max(currentParallelBlock.endTime, endTime);
        // Update height to match the longest duration
        const blockDuration = (currentParallelBlock.endTime - currentParallelBlock.startTime) / (1000 * 60);
        currentParallelBlock.heightPx = blockDuration * PX_PER_MINUTE;
      } else {
        // Close current block and start new one
        if (currentParallelBlock) {
          timeBlocks.push(currentParallelBlock);
        }

        const sessionsByRoom = new Map<string, FlexSession[]>();
        rooms.forEach((r) => sessionsByRoom.set(r, []));
        sessionsByRoom.get(room)?.push(fs);

        currentParallelBlock = {
          type: "parallel",
          startTime,
          endTime,
          heightPx: fs.heightPx,
          sessionsByRoom,
        };
      }
    }
  }

  // Don't forget the last parallel block
  if (currentParallelBlock) {
    timeBlocks.push(currentParallelBlock);
  }

  return { rooms, timeBlocks, allSessionsSorted: allFlexSessions };
}

/**
 * Get formatted date for day page
 */
export async function getDayDate(dayName: string): Promise<string | null> {
  const sessions = await getSessionsByDay(dayName);
  if (sessions.length === 0) return null;

  const firstSession = sessions.find((s) => s.data.start);
  if (!firstSession?.data.start) return null;

  return firstSession.data.start.toLocaleDateString("en-AU", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: CONFERENCE_TIMEZONE,
  });
}

// ============================================================================
// Grid-based schedule layout (matching static template structure)
// ============================================================================

/**
 * Schedule layout types:
 * - "detailed": 30-minute slots, 160px height - for busy days with many sessions
 * - "simple": 60-minute slots, 100px height - for quieter days with longer sessions
 */
export type ScheduleLayout = "detailed" | "simple";

// Layout configuration
const LAYOUT_CONFIG = {
  detailed: {
    slotMinutes: 30,
    slotHeightPx: 160,
  },
  simple: {
    slotMinutes: 60,
    slotHeightPx: 100,
  },
} as const;

/**
 * Get the recommended layout for a given day
 */
export function getScheduleLayout(dayName: string): ScheduleLayout {
  // Monday uses simple layout (fewer, longer sessions)
  if (dayName.toLowerCase() === "monday") {
    return "simple";
  }
  // Friday, Saturday, Sunday use detailed layout
  return "detailed";
}

// Room order for column spanning logic
const ROOM_ORDER = ["Ballroom 1", "Ballroom 2", "Ballroom 3", "Stradbroke Room", "Junior Ballroom"];

/**
 * Internal type for session data before positioning
 */
interface SessionDataItem {
  session: Session;
  slotIndex: number;
  topPercent: number;
  heightPx: number;
  room: string;
  showTrackHeader: boolean;
  isFullWidth: boolean;
  colSpan: number;
  startColumn: number;
  isBreak: boolean;
}

/**
 * Merge adjacent breaks that occur at the same time.
 * Breaks with the same start/end time and title in adjacent rooms are merged
 * into a single entry that spans multiple columns.
 */
function mergeAdjacentBreaks(
  sessionData: SessionDataItem[],
  rooms: string[]
): SessionDataItem[] {
  const breaks = sessionData.filter((s) => s.isBreak);
  if (breaks.length === 0) return [];

  // Group breaks by (start time, end time, title)
  const groups = new Map<string, SessionDataItem[]>();

  for (const brk of breaks) {
    const startTime = brk.session.data.start?.getTime() ?? 0;
    const endTime = brk.session.data.end?.getTime() ?? 0;
    const title = brk.session.data.title;
    const key = `${startTime}-${endTime}-${title}`;

    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key)!.push(brk);
  }

  const merged: SessionDataItem[] = [];

  for (const [, groupBreaks] of groups) {
    // Get room indices in the defined order
    const roomIndices = groupBreaks
      .map((b) => rooms.indexOf(b.room))
      .filter((i) => i !== -1)
      .sort((a, b) => a - b);

    if (roomIndices.length === 0) continue;

    // Find contiguous ranges of adjacent rooms
    let rangeStart = roomIndices[0];
    let rangeEnd = roomIndices[0];

    const emitRange = () => {
      // Find a break from this range to use as template
      const templateBreak = groupBreaks.find(
        (b) => rooms.indexOf(b.room) >= rangeStart && rooms.indexOf(b.room) <= rangeEnd
      );
      if (!templateBreak) return;

      merged.push({
        ...templateBreak,
        colSpan: rangeEnd - rangeStart + 1,
        startColumn: rangeStart,
      });
    };

    for (let i = 1; i < roomIndices.length; i++) {
      if (roomIndices[i] === rangeEnd + 1) {
        // Adjacent, extend range
        rangeEnd = roomIndices[i];
      } else {
        // Gap - emit current range and start new one
        emitRange();
        rangeStart = roomIndices[i];
        rangeEnd = roomIndices[i];
      }
    }

    // Emit final range
    emitRange();
  }

  return merged;
}

/**
 * A positioned session within a time slot
 */
export interface PositionedSession {
  session: Session;
  topPercent: number; // Position within slot as percentage (0-100)
  heightPx: number; // Height in pixels based on duration
  showTrackHeader: boolean;
  isFullWidth: boolean;
  colSpan: number; // Number of room columns to span
  startColumn: number; // 0-indexed starting column position (for breaks)
  isBreak: boolean; // Flag to style breaks differently
}

/**
 * A 30-minute time slot row in the schedule
 */
export interface ScheduleRow {
  time: Date;
  label: string;
  sessionsByRoom: Map<string, PositionedSession[]>;
}

/**
 * Get schedule data organized for the static template layout
 */
export async function getScheduleForGrid(
  dayName: string,
  layout?: ScheduleLayout
): Promise<{
  rooms: string[];
  rows: ScheduleRow[];
  layout: ScheduleLayout;
}> {
  const sessions = await getSessionsByDay(dayName);
  const rooms = await getRoomsForDay(dayName);
  const scheduleLayout = layout ?? getScheduleLayout(dayName);
  const { slotMinutes, slotHeightPx } = LAYOUT_CONFIG[scheduleLayout];

  if (sessions.length === 0) {
    return { rooms: [], rows: [], layout: scheduleLayout };
  }

  // Find earliest and latest times
  let earliest: Date | null = null;
  let latest: Date | null = null;

  sessions.forEach((session) => {
    if (session.data.start && (!earliest || session.data.start < earliest)) {
      earliest = session.data.start;
    }
    if (session.data.end && (!latest || session.data.end > latest)) {
      latest = session.data.end;
    }
  });

  if (!earliest || !latest) {
    return { rooms: [], rows: [], layout: scheduleLayout };
  }

  // Round down to nearest slot boundary for start
  const gridStart = new Date(earliest);
  gridStart.setMinutes(Math.floor(gridStart.getMinutes() / slotMinutes) * slotMinutes, 0, 0);

  // Round up to nearest slot boundary for end
  const gridEnd = new Date(latest);
  if (gridEnd.getMinutes() % slotMinutes !== 0) {
    gridEnd.setMinutes(Math.ceil(gridEnd.getMinutes() / slotMinutes) * slotMinutes, 0, 0);
  }

  const gridStartTime = gridStart.getTime();

  // Track which non-break sessions have a preceding non-break session in the same room
  // Breaks don't count as "preceding" for track header display purposes
  const nonBreakEndTimes = new Map<string, number[]>();

  // Process sessions and assign to slots
  const sessionData: SessionDataItem[] = [];

  sessions.forEach((session) => {
    if (!session.data.start || !session.data.end || !session.data.room) return;

    const startTime = session.data.start.getTime();
    const endTime = session.data.end.getTime();
    const durationMinutes = (endTime - startTime) / (1000 * 60);
    const room = session.data.room;

    // Calculate which slot this session starts in
    const minutesFromStart = (startTime - gridStartTime) / (1000 * 60);
    const slotIndex = Math.floor(minutesFromStart / slotMinutes);

    // Calculate position within the slot as percentage
    const minutesIntoSlot = minutesFromStart % slotMinutes;
    // Add 1% top offset for vertical gap between sessions
    const topPercentRaw = (minutesIntoSlot / slotMinutes) * 100 + 1;

    // Calculate height based on duration (2% shorter for 1% top + 1% bottom gap)
    const heightPx = (durationMinutes / slotMinutes) * slotHeightPx * 0.98;

    const sessionType = session.data.type;
    const isFullWidth = sessionType === "keynote" || sessionType === "plenary";
    const colSpan = isFullWidth ? rooms.length : 1;
    const isBreak = sessionType === "break";

    // Check for track header display and back-to-back sessions
    // Only non-break sessions count as "preceding" - sessions after breaks should show track headers
    const roomEndTimes = nonBreakEndTimes.get(room) || [];
    const hasPrecedingSession = !isBreak && roomEndTimes.includes(startTime);
    const trackName = session.data.trackName;
    const isSpecialistTrack = !!trackName && trackName !== "Main Conference";
    const showTrackHeader = isSpecialistTrack && !hasPrecedingSession;

    // Track headers are absolutely positioned above session cards (top: -24px),
    // so they don't affect vertical spacing. No gap compensation needed.
    const topPercent = Math.round(topPercentRaw * 100) / 100;

    // Record this session's end time (only for non-break sessions)
    if (!isBreak) {
      if (!nonBreakEndTimes.has(room)) {
        nonBreakEndTimes.set(room, []);
      }
      nonBreakEndTimes.get(room)!.push(endTime);
    }

    const roomIndex = rooms.indexOf(room);
    const startColumn = roomIndex >= 0 ? roomIndex : 0;

    sessionData.push({
      session,
      slotIndex,
      topPercent,
      heightPx,
      room,
      showTrackHeader,
      isFullWidth,
      colSpan,
      startColumn,
      isBreak,
    });
  });

  // Merge adjacent breaks that occur at the same time
  // Group breaks by (start time, end time, title) and find contiguous room ranges
  const mergedBreaks = mergeAdjacentBreaks(sessionData, rooms);

  // Replace individual break entries with merged versions
  const nonBreakSessions = sessionData.filter((s) => !s.isBreak);
  const finalSessionData = [...nonBreakSessions, ...mergedBreaks];

  // Generate time slots
  const rows: ScheduleRow[] = [];
  const current = new Date(gridStart);
  let slotIndex = 0;

  while (current < gridEnd) {
    const sessionsByRoom = new Map<string, PositionedSession[]>();
    rooms.forEach((room) => sessionsByRoom.set(room, []));

    // Find sessions that start in this slot
    const slotSessions = finalSessionData.filter((s) => s.slotIndex === slotIndex);

    slotSessions.forEach((s) => {
      const positioned: PositionedSession = {
        session: s.session,
        topPercent: s.topPercent,
        heightPx: s.heightPx,
        showTrackHeader: s.showTrackHeader,
        isFullWidth: s.isFullWidth,
        colSpan: s.colSpan,
        startColumn: s.startColumn,
        isBreak: s.isBreak,
      };

      // For full-width sessions, add to first room only (rendering will handle colspan)
      if (s.isFullWidth) {
        sessionsByRoom.get(rooms[0])?.push(positioned);
      } else if (s.isBreak && s.colSpan > 1) {
        // For merged breaks, add to the first room in their span
        const startRoom = rooms[s.startColumn];
        if (startRoom) {
          sessionsByRoom.get(startRoom)?.push(positioned);
        }
      } else {
        sessionsByRoom.get(s.room)?.push(positioned);
      }
    });

    rows.push({
      time: new Date(current),
      label: current.toLocaleTimeString("en-AU", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
        timeZone: CONFERENCE_TIMEZONE,
      }),
      sessionsByRoom,
    });

    current.setMinutes(current.getMinutes() + slotMinutes);
    slotIndex++;
  }

  return { rooms, rows, layout: scheduleLayout };
}
