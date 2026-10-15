
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


def schedule_jobs(jobs):
    jobs = sorted(
        jobs, key=lambda x: int(x["profit"]), reverse=True
    )

    n = len(jobs)
    slots = [False] * n
    result = [None] * n
    total = 0

    for job in jobs:
        deadline = int(job["deadline"])
        profit = int(job["profit"])

        for j in range(min(n, deadline) - 1, -1, -1):
            if not slots[j]:
                slots[j] = True
                result[j] = job["id"]
                total += profit
                break

    return [job for job in result if job is not None], total


@app.route("/schedule", methods=["POST"])
def schedule():
    jobs = request.get_json(silent=True)

    if not isinstance(jobs, list):
        return jsonify({"error": "Expected a list of jobs"}), 400

    try:
        scheduled, profit = schedule_jobs(jobs)
        return jsonify({"jobs": scheduled, "profit": profit})
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid job data"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

