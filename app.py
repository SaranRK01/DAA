from flask import Flask, request, jsonify, render_template

import time  # Import the time module to measure execution time

app = Flask(__name__)

def find_odd_ball_divide_and_conquer(balls):
    comparisons = 0  # Track the number of comparisons

    def divide_and_conquer(balls, start, end):
        nonlocal comparisons

        # Base case: If only one ball remains, it is the odd one
        if start == end:
            return {"position": start, "condition": "Odd"}  # Return zero-based index

        # Divide the balls into three groups
        total_balls = end - start + 1
        mid = total_balls // 3
        group1 = balls[start:start + mid]
        group2 = balls[start + mid:start + 2 * mid]
        remaining = balls[start + 2 * mid:end + 1]

        weight1 = sum(group1)
        weight2 = sum(group2)
        comparisons += 1  # Increment comparisons for each weight comparison

        if weight1 == weight2:
            # If weights are equal, the odd ball is in the remaining group
            if remaining:
                return divide_and_conquer(balls, start + 2 * mid, end)
            else:
                return {"position": -1, "condition": "Not Found"}  # Handle edge case
        elif weight1 != weight2:
            # Odd ball is in the heavier or lighter group
            if weight1 > weight2:
                return divide_and_conquer(balls, start, start + mid - 1)
            else:
                return divide_and_conquer(balls, start + mid, start + 2 * mid - 1)

    start_time = time.time()  # Start the timer
    result = divide_and_conquer(balls, 0, len(balls) - 1)
    end_time = time.time()  # End the timer

    execution_time = end_time - start_time  # Calculate execution time
    result["executionTime"] = f"{execution_time:.6f} seconds"
    result["timeComplexity"] = f"O(log n), Comparisons: {comparisons}"
    result["index"] = result["position"]  # Add zero-based index explicitly
    return result

def find_odd_ball_brute_force(balls):
    start_time = time.time()  # Start the timer
    for i in range(1, len(balls)):  # Start from index 1 to compare with the first ball
        if balls[i] != balls[0]:
            end_time = time.time()  # End the timer
            execution_time = end_time - start_time
            return {
                "position": i,
                "condition": "Odd",
                "executionTime": f"{execution_time:.6f} seconds",
                "timeComplexity": f"O(n), Comparisons: {i + 1}",
                "index": i
            }
    end_time = time.time()  # End the timer
    execution_time = end_time - start_time
    return {
        "position": 0,  # If no mismatch is found, the first ball is the odd one
        "condition": "Odd",
        "executionTime": f"{execution_time:.6f} seconds",
        "timeComplexity": "O(n), Comparisons: n",
        "index": 0
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    balls = data.get('balls', [])

    if not balls or len(balls) < 3:
        return jsonify({"error": "Please provide at least 3 balls"}), 400

    # Compute results for both approaches
    divide_and_conquer_result = find_odd_ball_divide_and_conquer(balls)
    brute_force_result = find_odd_ball_brute_force(balls)

    # Return both results in the response
    return jsonify({
        "divide_and_conquer": divide_and_conquer_result,
        "brute_force": brute_force_result
    })

if __name__ == '__main__':
    app.run(debug=True)