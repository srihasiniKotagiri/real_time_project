from flask import Flask, render_template, request
import pickle
from datetime import datetime
import os

app = Flask(__name__)

# --- MODEL LOADING LOGIC ---
# This ensures Render finds the files inside the 'project' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# If you have two models, load them both here. 
# I'm using 'model.pkl' as the primary. 
# Change the filename if 'traffic_model.pkl' is the one you actually need.
model_path = os.path.join(BASE_DIR, "model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find {model_path}")
    model = None
except Exception as e:
    print(f"❌ ERROR loading pickle: {e}")
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template("index.html", prediction_text="Error: Model not loaded on server.")

    try:
        lat = float(request.form["lat"])
        lng = float(request.form["lng"])
        date = request.form["date"]
        time_input = request.form["time"]

        # Processing inputs
        hour = int(time_input.split(":")[0])
        day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1

        # Prediction
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

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error during prediction: {e}")

if __name__ == "__main__":
    # Render requires the app to listen on a specific port provided via environment variables
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
