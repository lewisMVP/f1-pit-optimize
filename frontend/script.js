async function getPitStopDecision() {
    const tire_health = parseFloat(document.getElementById('tire_health').value);
    const race_position = parseInt(document.getElementById('race_position').value);
    const current_lap = parseInt(document.getElementById('current_lap').value);  // Lấy current lap

    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_pit_decision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tire_health, race_position, current_lap })  // Gửi current lap
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const result = await response.json();
        document.getElementById('decision').innerText = `Predicted lap time: ${result.predicted_lap_time.toFixed(2)} seconds, Decision: ${result.pit_decision}, Current Lap: ${result.current_lap}`;
    } catch (error) {
        document.getElementById('decision').innerText = `Error: ${error.message}`;
    }
}
