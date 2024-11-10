document.getElementById('getEventsBtn').addEventListener('click', () => {
    axios.get('/api/events')
        .then(response => {
            const eventsDiv = document.getElementById('events');
            eventsDiv.innerHTML = '';
            response.data.forEach(event => {
                const p = document.createElement('p');
                p.textContent = `${event.name} - ${event.country} (${event.date})`;
                eventsDiv.appendChild(p);
            });
        })
        .catch(error => console.error(error));
});

document.getElementById('predictPitBtn').addEventListener('click', () => {
    const tireWear = parseFloat(document.getElementById('tireWear').value);
    const racePosition = parseFloat(document.getElementById('racePosition').value);
    const trackLength = parseFloat(document.getElementById('trackLength').value);

    axios.post('/api/get_pit_decision', {
        tire_wear: tireWear,
        race_position: racePosition,
        track_length: trackLength
    })
    .then(response => {
        document.getElementById('prediction').textContent = `Predicted Lap Time: ${response.data.predicted_lap_time.toFixed(2)}s - ${response.data.pit_decision} (Lap: ${response.data.current_lap})`;
    })
    .catch(error => console.error(error));
});
