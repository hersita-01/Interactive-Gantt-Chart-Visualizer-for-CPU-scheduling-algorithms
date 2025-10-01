# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduling_logic import ALGORITHM_REGISTRY
import traceback
import logging

app = Flask(__name__)
CORS(app)

# basic request logging to help debug method/path issues
logging.basicConfig(level=logging.INFO)



@app.route("/api/schedule", methods=["POST"])
def schedule():
    """
    POST /api/schedule
    Expected JSON:
    {
        "algorithm": "FCFS" | "SJF" | "SRTF" | "RR",
        "processes": [
            {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 0},
            ...
        ],
        "quantum": 2   # required if algorithm == "RR"
    }
    Response:
    {
        "gantt_data": [{"pid":"P1","start":0,"end":4,"color":"#..."}, ...],
        "metrics": [{"pid":"P1","completion_time":4,"turnaround_time":4,"waiting_time":0}, ...],
        "averages": {"awt": <float>, "att": <float>}
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        algorithm = data.get("algorithm")
        processes = data.get("processes", [])
        quantum = data.get("quantum", None)

        if not algorithm or algorithm not in ALGORITHM_REGISTRY:
            return jsonify({"error": f"Unsupported or missing algorithm. Supported algorithms: {list(ALGORITHM_REGISTRY.keys())}"}), 400

        # normalize and validate processes
        normalized = []
        for p in processes:
            try:
                pid = str(p.get("pid"))
                arrival = int(p.get("arrival_time", 0))
                burst = int(p.get("burst_time", 0))
                priority = int(p.get("priority", 0)) if p.get("priority") is not None else 0
                tq = int(p.get("time_quantum", 0)) if p.get("time_quantum") is not None else 0
            except Exception:
                return jsonify({"error": "Invalid process format. Fields pid (string), arrival_time (int), burst_time (int) required."}), 400

            if burst < 0 or arrival < 0:
                return jsonify({"error": "arrival_time and burst_time must be >= 0"}), 400

            normalized.append({
                "pid": pid,
                "arrival_time": arrival,
                "burst_time": burst,
                "priority": priority,
                "time_quantum": tq
            })

        func = ALGORITHM_REGISTRY[algorithm]
        if algorithm == "RR":
            if quantum is None:
                return jsonify({"error": "Round Robin requires 'quantum' parameter."}), 400
            try:
                q = int(quantum)
            except Exception:
                return jsonify({"error": "'quantum' must be an integer."}), 400
            gantt, metrics, averages = func(normalized, q)
        else:
            gantt, metrics, averages = func(normalized)

        response = {
            "gantt_data": gantt,
            "metrics": metrics,
            "averages": averages
        }
        return jsonify(response)
    except Exception as e:
        # log stack trace to server console for debugging
        traceback.print_exc()
        return jsonify({"error": "Server error", "message": str(e)}), 500


@app.route("/api/schedule", methods=["GET"])
def schedule_info():
    """Return simple instructions for callers using the wrong method (helps avoid 405 when opening the URL in a browser)
    """
    logging.info(f"Received info request from {request.remote_addr}")
    return jsonify({
        "message": "POST JSON to this endpoint with algorithm and processes. See /backend/app.py docstring for the expected format.",
        "supported_methods": ["POST"]
    }), 200


if __name__ == "__main__":
    # App runs on port 5001 to avoid conflicts; set debug=False in production
    app.run(host="0.0.0.0", port=5001, debug=True)
