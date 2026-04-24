from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))

        # Convert date & time
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        time_obj = datetime.datetime.strptime(time, "%H:%M")

        day = date_obj.day
        month = date_obj.month
        hour = time_obj.hour

        # 👉 Dummy logic (replace with ML model later)
        if hour in range(8, 11) or hour in range(17, 20):
            traffic = "High Traffic 🚗🚗🚗"
        elif hour in range(11, 17):
            traffic = "Moderate Traffic 🚗🚗"
        else:
            traffic = "Low Traffic 🚗"

        # Output message
        result = f"""
        📍 Location: {location} <br>
        🗓 Date: {date} <br>
        ⏰ Time: {time} <br>
        🌐 Lat: {latitude}, Lon: {longitude} <br><br>
        🚦 Prediction: {traffic}
        """

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        print("ERROR:", e)
        return render_template(
            'index.html',
            prediction_text="❌ Error processing prediction. Please check inputs."
        )


# Run app
if __name__ == "__main__":
    app.run(debug=True)
