from flask import Flask, render_template, request
import pickle
from datetime import datetime
import os

app = Flask(__name__)

# --- ROBUST MODEL LOADING ---
# This ensures we find the 690kb file inside the 'project' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "traffic_model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✅ SUCCESS: traffic_model.pkl (690kb) loaded correctly.")
except FileNotFoundError:
    print(f"❌ ERROR: {model_path} not found. Check your GitHub folder.")
    model = None
except Exception as e:
    print(f"❌ ERROR: Failed to unpickle model. {e}")
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template("index.html", prediction_text="Server Error: Model file missing or corrupt.")

    try:
        # Get data from form
        lat = float(request.form["lat"])
        lng = float(request.form["lng"])
        date = request.form["date"]
        time_input = request.form["time"]

        # Convert inputs to model features
        hour = int(time_input.split(":")[0])
        day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1

        # Predict
        prediction = model.predict([[hour, day]])
        output = int(prediction[0])

        # Define traffic labels
        if output < 150:
            condition = "🟢 Low Traffic"
        elif output < 300:
            condition = "🟡 Medium Traffic"
        else:
            condition = "🔴 High Traffic"

        result = f"{output} vehicles | {condition} | Location: ({lat:.2f}, {lng:.2f})"
        return render_template("index.html", prediction_text=result)

    except Exception as e:
        print(f"Prediction Error: {e}")
        return render_template("index.html", prediction_text="Error processing prediction. Check input formats.")

if __name__ == "__main__":
    # Render dynamic port assignment
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
