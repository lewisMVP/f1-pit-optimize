async function predict() {
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ state: [1, 0.8, 10] })  // Ví dụ về trạng thái đầu vào
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const pitStopDecision = data.action === 1 ? "Pit this lap" : "No Box";
        document.getElementById("result").innerText = pitStopDecision;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        document.getElementById("result").innerText = 'Error fetching prediction';
    }
}
