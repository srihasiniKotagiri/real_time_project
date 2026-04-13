function predictTraffic() {
    let location = document.getElementById("location").value.toLowerCase();
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;

    if (!location || !date || !time) {
        alert("Please fill all fields");
        return;
    }

    let hour = parseInt(time.split(":")[0]);

    let trafficLevel;
    let condition;
    let status;

    // Busy city keywords (simulate real-world)
    let busyAreas = ["new york", "mumbai", "delhi", "london", "tokyo"];

    let isBusyLocation = busyAreas.some(area => location.includes(area));

    // Prediction logic
    if ((hour >= 8 && hour <= 11) || (hour >= 17 && hour <= 21)) {
        trafficLevel = isBusyLocation ? 90 : 75;
        condition = "High Traffic 🚗🚗🚗";
        status = "⚠️ Peak Hour Congestion";
    } 
    else if (hour >= 12 && hour <= 16) {
        trafficLevel = isBusyLocation ? 70 : 55;
        condition = "Moderate Traffic 🚗🚗";
        status = "Normal Flow";
    } 
    else {
        trafficLevel = isBusyLocation ? 50 : 25;
        condition = "Low Traffic 🚗";
        status = "Smooth Road";
    }

    // Random accident simulation
    if (Math.random() > 0.85) {
        status = "🚨 Accident Reported!";
    }

    document.getElementById("level").innerText = trafficLevel;
    document.getElementById("condition").innerText = condition;
    document.getElementById("status").innerText = status;
}