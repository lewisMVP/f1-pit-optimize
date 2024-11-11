// Function to dynamically load circuit data from API
async function loadCircuitData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_circuit_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // Bạn có thể gửi thêm thông tin nếu cần, ví dụ như circuit_name
                circuit_name: "Some Circuit Name" // Ví dụ
            })
        });

        // Check if response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        circuitData = data; // Store circuit data globally

        const circuitSelect = document.getElementById('circuit');
        for (const [circuitName, circuitDetails] of Object.entries(circuitData)) {
            const option = document.createElement('option');
            option.value = circuitName;
            option.textContent = circuitName;
            circuitSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Error loading circuit data:', error);
        alert('Failed to load circuit data. Please check the API.');
    }
}
