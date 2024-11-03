document.getElementById('getWeather').addEventListener('click', async function() {
    const track = document.getElementById('track').value;
    const weatherInfoDiv = document.getElementById('weatherInfo');

    try {
        const response = await fetch(`/api/weather?location=${track}`);
        const weatherData = await response.json();
        
        weatherInfoDiv.innerHTML = `
            <h2>Weather at ${track}</h2>
            <p>Temperature: ${weatherData.main.temp} °C</p>
            <p>Description: ${weatherData.weather[0].description}</p>
        `;
    } catch (error) {
        console.error('Error:', error);
    }
});

// Add a button to get pit stop decision
document.getElementById('predictPitTime').addEventListener('click', async function() {
    const tireWear = parseFloat(document.getElementById('tireWearInput').value); // From 0 to 1
    const speed = parseFloat(document.getElementById('speedInput').value); // Average speed
    
    try {
        const response = await fetch('/api/get_pit_decision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ tire_wear: tireWear, speed: speed }),
        });
        const data = await response.json();
        alert(`Predicted lap time: ${data.predicted_lap_time.toFixed(2)} seconds\nDecision: ${data.pit_decision}`);
    } catch (error) {
        console.error('Error:', error);
    }
});
