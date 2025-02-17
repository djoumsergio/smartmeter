from flask import Flask, jsonify, render_template
import random
import time
import threading
import smartmeter

app = Flask(__name__)

# Simulated power consumption data
data = {"timestamp": time.time(), "power_consumption": random.randint(200, 300)}

def update_data():
    """Updates power consumption data every second."""
    global data
    while True:
        time.sleep(60)
        power = smartmeter.get_power(smartmeter.get_data())
        smartmeter.save_to_json(power)
        data = power
        print(power)

# Start background thread
data_thread = threading.Thread(target=update_data, daemon=True)
data_thread.start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)