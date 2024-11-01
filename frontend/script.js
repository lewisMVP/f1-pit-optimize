async function predict() {
    const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state: [1, 0.8, 10] })  // Ví dụ về trạng thái đầu vào
    });
    const data = await response.json();
    document.getElementById("result").innerText = `Pit Stop Decision: ${data.action}`;
}
