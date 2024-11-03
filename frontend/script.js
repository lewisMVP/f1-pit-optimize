async function getPitStopDecision() {
    const tire_health = parseFloat(document.getElementById('tire_health').value);
    const race_position = parseInt(document.getElementById('race_position').value);

    const response = await fetch('/api/get_pit_decision', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tire_health, race_position })
    });

    const result = await response.json();
    
    if (response.ok) {
        document.getElementById('decision').innerText = `Predicted lap time: ${result.predicted_lap_time.toFixed(2)} seconds, Decision: ${result.pit_decision}`;
    } else {
        document.getElementById('decision').innerText = `Error: ${result.error}`;
    }
}
