# ============================================================
# scheduler.py — Football Fixture Scheduler using Backtracking
# ============================================================
# CORE IDEA:
#   Given N teams, we schedule every pair to play TWICE
#   (home & away). Each match is assigned to a (day, slot).
#
#   CONSTRAINT 1 → No team plays on consecutive days
#   CONSTRAINT 2 → Each team plays at most once per day
#   CONSTRAINT 3 → Every team plays home AND away vs each opponent
#
#   BACKTRACKING: place a match → check constraints →
#   if fail → backtrack and try next day/slot.
# ============================================================

from itertools import combinations


def generate_matches(teams):
    """
    Generate all match pairs: each pair plays HOME and AWAY.
    Example: [A, B, C] → (A vs B), (B vs A), (A vs C), etc.
    Returns a list of {home, away} dicts.
    """
    matches = []
    for home, away in combinations(teams, 2):
        matches.append({"home": home, "away": away})   # First leg
        matches.append({"home": away, "away": home})   # Return leg
    return matches


def is_valid(schedule, match, day, slot):
    """
    Check constraints before placing a match on a given day/slot.

    CONSTRAINT 1: Neither team played the day before OR after.
    CONSTRAINT 2: Each team appears at most once on this day.
    CONSTRAINT 3: This slot on this day is not already taken.
    """
    home_team = match["home"]
    away_team = match["away"]

    # --- CONSTRAINT 1: No consecutive days ---
    for adj in [day - 1, day + 1]:
        if adj in schedule:
            for m in schedule[adj]:
                if home_team in (m["home"], m["away"]):
                    return False
                if away_team in (m["home"], m["away"]):
                    return False

    # --- CONSTRAINT 2: Each team plays at most once per day ---
    if day in schedule:
        for m in schedule[day]:
            if home_team in (m["home"], m["away"]):
                return False
            if away_team in (m["home"], m["away"]):
                return False

    # --- CONSTRAINT 3: Slot on this day must be free ---
    if day in schedule:
        used_slots = [m["slot"] for m in schedule[day]]
        if slot in used_slots:
            return False

    return True  # ✅ All constraints passed


def backtrack(matches, index, schedule, max_days, slots_per_day):
    """
    Recursive Backtracking Function.

    Tries to place matches[index] into a valid (day, slot).
    If placed → recurse for next match.
    If no valid placement found → return False (backtrack).
    """

    # BASE CASE: All matches placed successfully!
    if index == len(matches):
        return True

    match = matches[index]

    # Try every day and every slot
    for day in range(1, max_days + 1):
        for slot in range(1, slots_per_day + 1):

            if is_valid(schedule, match, day, slot):

                # ✅ PLACE the match
                if day not in schedule:
                    schedule[day] = []
                schedule[day].append({**match, "slot": slot})

                # 🔁 RECURSE for next match
                if backtrack(matches, index + 1, schedule, max_days, slots_per_day):
                    return True  # Solution found!

                # ❌ BACKTRACK — undo placement
                schedule[day].remove({**match, "slot": slot})
                if not schedule[day]:
                    del schedule[day]

    return False  # No valid placement for this match


def schedule_fixtures(teams):
    """
    Main entry point.
    Generates all matches and runs backtracking.

    Returns a sorted list of scheduled matches, or None on failure.
    """
    matches = generate_matches(teams)

    n = len(teams)
    total_matches = len(matches)            # n*(n-1) total matches

    # Allow enough days — generous buffer so backtracking has room
    slots_per_day = max(1, n // 2)          # parallel matches per day
    max_days = total_matches * 3            # generous upper bound

    schedule = {}

    success = backtrack(matches, 0, schedule, max_days, slots_per_day)

    if not success:
        return None

    # Flatten into sorted list
    result = []
    for day in sorted(schedule.keys()):
        for match in sorted(schedule[day], key=lambda m: m["slot"]):
            result.append({
                "day": day,
                "slot": match["slot"],
                "home": match["home"],
                "away": match["away"]
            })

    return result