from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def schedule_jobs(jobs):
    jobs = sorted(jobs, key=lambda x: x['profit'], reverse=True)

    n = len(jobs)
    slot = [False]*n
    result = [None]*n
    total = 0

    for i in range(n):
        for j in range(min(n, int(jobs[i]['deadline']))-1, -1, -1):
            if not slot[j]:
                slot[j] = True
                result[j] = jobs[i]['id']
                total += int(jobs[i]['profit'])
                break

    scheduled = [r for r in result if r]
    return scheduled, total

@app.route('/schedule', methods=['POST'])
def schedule():
    jobs = request.json
    jobs, profit = schedule_jobs(jobs)
    return jsonify({"jobs": jobs, "profit": profit})

if __name__ == '__main__':
    app.run(debug=True)
