# Plan: Breaks from Schedule Data with Column Spanning

## Overview

Add support for schedule breaks (Morning Break, Lunch, Afternoon Break, etc.) from the Pretalx API, with intelligent column spanning for breaks that occur simultaneously across adjacent rooms.

## Current State

### API Data Available
The Pretalx `/slots/` endpoint returns break slots with:
```json
{
  "id": 1336251,
  "room": 4448,
  "start": "2025-09-12T10:30:00+10:00",
  "end": "2025-09-12T11:00:00+10:00",
  "submission": null,        // null indicates a break, not a talk
  "description": { "en": "Morning Break" },
  "duration": 30,
  "is_visible": true,
  "slot_type": "break"       // explicit break type
}
```

### Room Order (from Pretalx API position field)
| Position | Room ID | Room Name |
|----------|---------|-----------|
| 0 | 4448 | Ballroom 3 |
| 1 | 4449 | Ballroom 2 |
| 2 | 4450 | Ballroom 1 |
| - | 4711 | Junior Ballroom |
| - | 4716 | Stradbroke Room |

### Website Room Order (from `schedule.ts`)
```typescript
const roomOrder = ["Ballroom 1", "Ballroom 2", "Ballroom 3", "Stradbroke Room"];
```

**Note:** The website uses Ballroom 1, 2, 3 order (left to right), while Pretalx has position 0=Ballroom 3. The website order should be the source of truth for column spanning logic.

---

## Implementation Plan

### Step 1: Update `schedule_sync.py` to Fetch Breaks

Modify the sync script to:
1. Fetch all slots (already done)
2. Filter slots where `submission` is `null` AND `slot_type == "break"`
3. Create break session files with type `"break"`

**Changes to `schedule_sync.py`:**

```python
# After fetching slots_data, extract breaks
breaks_data = []
for slot in slots_data:
    if slot.get("submission") is None and slot.get("slot_type") == "break":
        room_id = slot.get("room")
        room_name = room_id_to_name.get(room_id, "") if isinstance(room_id, int) else ""

        description = slot.get("description", {})
        title = description.get("en", "Break") if isinstance(description, dict) else "Break"

        breaks_data.append({
            "code": f"BREAK-{slot['id']}",  # Synthetic code for breaks
            "title": title,
            "start": slot.get("start"),
            "end": slot.get("end"),
            "room": ROOM_LABELS.get(room_name, room_name),
            "type": "break",
            "speakers": [],
            "body": "",
        })
```

### Step 2: Define Break Session Schema

Update the sessions content collection schema in `src/content/config.ts`:

```typescript
// Ensure "break" is a valid session type
type: z.enum(["talk", "keynote", "plenary", "workshop", "lightning", "panel", "break"]),
```

### Step 3: Column Span Logic for Breaks

The key algorithm for merging adjacent breaks:

```typescript
interface MergedBreak {
  title: string;
  start: Date;
  end: Date;
  rooms: string[];      // Which rooms this break covers
  colSpan: number;      // How many columns to span
  startColumn: number;  // 0-indexed starting column position
}

function mergeAdjacentBreaks(breaks: Break[], roomOrder: string[]): MergedBreak[] {
  // Group breaks by (start, end, title)
  const groups = new Map<string, Break[]>();

  for (const brk of breaks) {
    const key = `${brk.start.getTime()}-${brk.end.getTime()}-${brk.title}`;
    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key)!.push(brk);
  }

  const merged: MergedBreak[] = [];

  for (const [key, groupBreaks] of groups) {
    // Get room indices in the defined order
    const roomIndices = groupBreaks
      .map(b => roomOrder.indexOf(b.room))
      .filter(i => i !== -1)
      .sort((a, b) => a - b);

    if (roomIndices.length === 0) continue;

    // Find contiguous ranges of adjacent rooms
    let rangeStart = roomIndices[0];
    let rangeEnd = roomIndices[0];

    for (let i = 1; i < roomIndices.length; i++) {
      if (roomIndices[i] === rangeEnd + 1) {
        // Adjacent, extend range
        rangeEnd = roomIndices[i];
      } else {
        // Gap - emit current range and start new one
        merged.push({
          title: groupBreaks[0].title,
          start: groupBreaks[0].start,
          end: groupBreaks[0].end,
          rooms: roomOrder.slice(rangeStart, rangeEnd + 1),
          colSpan: rangeEnd - rangeStart + 1,
          startColumn: rangeStart,
        });
        rangeStart = roomIndices[i];
        rangeEnd = roomIndices[i];
      }
    }

    // Emit final range
    merged.push({
      title: groupBreaks[0].title,
      start: groupBreaks[0].start,
      end: groupBreaks[0].end,
      rooms: roomOrder.slice(rangeStart, rangeEnd + 1),
      colSpan: rangeEnd - rangeStart + 1,
      startColumn: rangeStart,
    });
  }

  return merged;
}
```

### Step 4: Update `schedule.ts` Grid Logic

Modify `getScheduleForGrid()` to:

1. Fetch breaks alongside sessions
2. Merge adjacent breaks using the algorithm above
3. Include merged breaks in the schedule rows with `colSpan` info

**Key changes:**

```typescript
export interface PositionedSession {
  session: Session;
  topPercent: number;
  heightPx: number;
  showTrackHeader: boolean;
  isFullWidth: boolean;
  colSpan: number;
  startColumn: number;  // NEW: which column this starts at (for breaks)
  isBreak: boolean;     // NEW: flag to style differently
}
```

### Step 5: Update `[day].astro` Rendering

Handle breaks in the schedule grid:

```astro
{/* For breaks that span columns */}
{ps.isBreak && ps.colSpan > 1 && (
  <div
    class="schedule-break"
    style={`
      grid-column: span ${ps.colSpan};
      height: ${ps.heightPx}px;
    `}
  >
    <span class="break-title">{ps.session.data.title}</span>
    <span class="break-time">{timeStr}</span>
  </div>
)}
```

### Step 6: Add Break Styling

Add CSS for break styling (distinct from sessions):

```css
.schedule-break {
  background-color: #f5f5f5;
  border: 1px dashed #ccc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #666;
}

.break-title {
  font-weight: 500;
}

.break-time {
  font-size: 0.875rem;
  opacity: 0.7;
}
```

---

## Edge Cases to Handle

1. **Non-adjacent breaks at same time**: If Ballroom 1 and Ballroom 3 have breaks but Ballroom 2 doesn't, render as two separate breaks (no spanning across the gap)

2. **Breaks in rooms not in roomOrder**: Skip them or render as single-column

3. **Breaks with different titles at same time**: Keep them separate (e.g., "Morning Break" vs "Sponsor Meet & Greet")

4. **Breaks that span ALL rooms**: Similar to plenary, use `isFullWidth: true` pattern

---

## File Changes Summary

| File | Changes |
|------|---------|
| `scripts/schedule_sync.py` | Add break extraction from slots |
| `scripts/config.py` | Add ROOM_ORDER constant |
| `src/content/config.ts` | Add "break" to session type enum |
| `src/utils/schedule.ts` | Add break merging logic, update grid generation |
| `src/pages/program/[day].astro` | Add break rendering with colSpan |
| CSS (TBD) | Add `.schedule-break` styles |

---

## Testing Checklist

- [ ] Breaks appear in schedule grid
- [ ] Adjacent breaks (same time, adjacent rooms) merge correctly
- [ ] Non-adjacent breaks render separately
- [ ] Break styling is visually distinct from sessions
- [ ] Column spanning works correctly (1, 2, or 3 columns)
- [ ] Breaks with different titles at same time stay separate
- [ ] Room order is respected (Ballroom 1, 2, 3 left-to-right)
