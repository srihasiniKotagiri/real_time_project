import os
from flask import Flask, render_template, request
import pickle
from datetime import datetime

app = Flask(__name__)

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "model.pkl")
model = pickle.load(open(model_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    lat = float(request.form["lat"])
    lng = float(request.form["lng"])
    date = request.form["date"]
    time_input = request.form["time"]

    hour = int(time_input.split(":")[0])
    day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1

    # You can include lat/lng later in model (advanced)
    prediction = model.predict([[hour, day]])
    output = int(prediction[0])

    if output < 150:
        condition = "🟢 Low Traffic"
    elif output < 300:
        condition = "🟡 Medium Traffic"
    else:
        condition = "🔴 High Traffic"

    result = f"{output} vehicles | {condition} | Location: ({lat:.2f}, {lng:.2f})"

    return render_template("index.html", prediction_text=result)

if __name__ == "__main__":
    # Use the port assigned by Render, or default to 10000 locally
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
