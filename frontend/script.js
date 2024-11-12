// Global variable to store circuit data
let circuitData = {};

// Function to dynamically load circuit data from API
async function loadCircuitData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_circuit_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})  // Empty object since we want all circuits
        });

        // Check if response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        circuitData = data; // Store circuit data globally

        // Get the select element
        const circuitSelect = document.getElementById('circuit');
        
        // Clear existing options
        circuitSelect.innerHTML = '<option value="">--Select a Circuit--</option>';

        // Add new options
        Object.keys(circuitData).forEach(circuitName => {
            const option = document.createElement('option');
            option.value = circuitName;
            option.textContent = circuitName;
            circuitSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading circuit data:', error);
        alert('Failed to load circuit data. Please check the API connection.');
    }
}

// Function to update track length when circuit is selected
function updateTrackLength() {
    const circuitSelect = document.getElementById('circuit');
    const trackLengthInput = document.getElementById('track_length');
    
    const selectedCircuit = circuitSelect.value;
    if (selectedCircuit && circuitData[selectedCircuit]) {
        // Convert km to meters
        trackLengthInput.value = circuitData[selectedCircuit]['Track Length (km)'] * 1000;
    } else {
        trackLengthInput.value = '';
    }
}

// Function to get pit stop decision
async function getPitStopDecision() {
    const circuit = document.getElementById('circuit').value;
    const tireHealth = parseFloat(document.getElementById('tire_health').value);
    const racePosition = parseInt(document.getElementById('race_position').value);
    const currentLap = parseInt(document.getElementById('current_lap').value);
    const weather = document.getElementById('weather').value;

    if (!circuit || isNaN(tireHealth) || isNaN(racePosition) || isNaN(currentLap)) {
        alert('Please fill in all required fields');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_pit_decision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                circuit_name: circuit,
                tire_wear: 1 - tireHealth, // Convert health to wear
                race_position: racePosition,
                current_lap: currentLap,
                weather: weather
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const resultElement = document.getElementById('result');
        resultElement.innerHTML = `
            <h3>Analysis Result:</h3>
            <p>Predicted Lap Time: ${data.predicted_lap_time.toFixed(2)} seconds</p>
            <p>Decision: ${data.pit_decision}</p>
            <p>Track Type: ${data.track_type}</p>
            <p>Average Wear Rate: ${data.average_wear_rate}</p>
        `;
    } catch (error) {
        console.error('Error getting pit stop decision:', error);
        alert('Failed to get pit stop decision. Please try again.');
    }
}

// Load circuit data when the page loads
document.addEventListener('DOMContentLoaded', loadCircuitData);