# ============================================================
# app.py — Flask Backend
# ============================================================
# Only ONE change from before:
#   schedule_fixtures() now returns a dict with
#   fixtures + stats instead of just a list
# ============================================================

from flask import Flask, render_template, request, jsonify
from scheduler import schedule_fixtures

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/schedule", methods=["POST"])
def schedule():
    """
    Accepts: { "teams": ["Team A", "Team B", ...] }

    Returns:
        success → fixtures + stats (placements, backtracks,
                  cache_hits, cache_misses, memo_size)
        failure → error message
    """
    data = request.get_json()

    if not data or "teams" not in data:
        return jsonify({"success": False,
                        "message": "No teams provided."}), 400

    teams = data["teams"]

    if len(teams) < 2:
        return jsonify({"success": False,
                        "message": "Need at least 2 teams."}), 400

    if len(teams) > 8:
        return jsonify({"success": False,
                        "message": "Maximum 8 teams allowed."}), 400

    # Clean team names
    teams = list(set([t.strip() for t in teams if t.strip()]))

    # Run Backtracking + DP scheduler
    result = schedule_fixtures(teams)

    if result is None:
        return jsonify({"success": False,
                        "message": "Could not find a valid schedule."}), 500

    # Build summary stats for frontend
    fixtures = result["fixtures"]
    dp_stats = result["stats"]

    summary = {
        "teams_count":      len(teams),
        "total_matches":    len(fixtures),
        "total_days":       max(f["day"] for f in fixtures),
        "matches_per_team": (len(teams) - 1) * 2,
    }

    return jsonify({
        "success":   True,
        "fixtures":  fixtures,
        "stats":     summary,
        "dp_stats":  dp_stats,        # ← NEW: DP proof stats
        "memo_size": result["memo_size"]  # ← NEW: cache size
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)