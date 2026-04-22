# ============================================================
# app.py — Flask Backend for Football Fixture Scheduler
# ============================================================
# This file:
#   - Serves the main HTML page (index.html)
#   - Accepts a list of team names from the frontend (POST)
#   - Calls the backtracking scheduler
#   - Returns the fixture schedule as JSON
# ============================================================

from flask import Flask, render_template, request, jsonify
from scheduler import schedule_fixtures

# Initialize Flask app
app = Flask(__name__)


# ── ROUTE 1: Serve the main page ──────────────────────────
@app.route("/")
def index():
    """Render the homepage — the main fixture scheduler UI."""
    return render_template("index.html")


# ── ROUTE 2: Schedule fixtures via POST ───────────────────
@app.route("/schedule", methods=["POST"])
def schedule():
    """
    Accepts JSON: { "teams": ["Team A", "Team B", ...] }
    Runs backtracking algorithm and returns scheduled fixtures.

    Returns JSON:
        On success → { "success": true, "fixtures": [...], "stats": {...} }
        On failure → { "success": false, "message": "..." }
    """

    data = request.get_json()

    # --- Validate input ---
    if not data or "teams" not in data:
        return jsonify({"success": False, "message": "No teams provided."}), 400

    teams = data["teams"]

    # Need at least 2 teams to schedule a match
    if len(teams) < 2:
        return jsonify({"success": False, "message": "Please enter at least 2 teams."}), 400

    # Cap at 8 teams to keep backtracking fast in demo
    if len(teams) > 8:
        return jsonify({"success": False, "message": "Maximum 8 teams allowed."}), 400

    # Remove duplicates and empty names
    teams = list(set([t.strip() for t in teams if t.strip()]))

    # --- Run the backtracking scheduler ---
    fixtures = schedule_fixtures(teams)

    if fixtures is None:
        return jsonify({
            "success": False,
            "message": "Could not find a valid schedule. Try fewer teams."
        }), 500

    # --- Build stats summary ---
    total_matches = len(fixtures)
    total_days = max(f["day"] for f in fixtures)
    teams_count = len(teams)

    stats = {
        "total_matches": total_matches,
        "total_days": total_days,
        "teams_count": teams_count,
        "matches_per_team": (teams_count - 1) * 2  # Each team plays every other team twice
    }

    return jsonify({
        "success": True,
        "fixtures": fixtures,
        "stats": stats,
        "teams": teams
    })


# ── Run the app ───────────────────────────────────────────
if __name__ == "__main__":
    # debug=True → auto-reloads on code changes (dev mode)
    app.run(debug=True, port=5000)