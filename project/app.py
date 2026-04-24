from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get raw values
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')

        # 🔍 DEBUG PRINTS (check in terminal / Render logs)
        print("Location:", location)
        print("Date:", date)
        print("Time:", time)
        print("Latitude:", lat)
        print("Longitude:", lon)

        # ❌ Check empty values
        if not all([location, date, time, lat, lon]):
            return render_template('index.html',
                prediction_text="❌ Please fill all fields correctly.")

        # Convert safely
        latitude = float(lat)
        longitude = float(lon)

        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        time_obj = datetime.datetime.strptime(time, "%H:%M")

        hour = time_obj.hour

        # Simple prediction logic
        if 8 <= hour <= 10 or 17 <= hour <= 19:
            traffic = "High Traffic 🚗🚗🚗"
        elif 11 <= hour <= 16:
            traffic = "Moderate Traffic 🚗🚗"
        else:
            traffic = "Low Traffic 🚗"

        result = f"""
        📍 {location} <br>
        ⏰ {time} | 🗓 {date} <br>
        🌐 ({latitude}, {longitude}) <br><br>
        🚦 {traffic}
        """

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        print("ERROR:", e)
        return render_template('index.html',
            prediction_text=f"❌ Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
