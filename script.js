document.getElementById('generate').addEventListener('click', async () => {
    const topic = document.getElementById('topic').value;
    const genre = document.getElementById('genre').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic, genre })
    });

    const data = await response.json();
    const outputDiv = document.getElementById('output');

    if (response.ok) {
        outputDiv.innerHTML = data.results.map(result => `<p>${result}</p>`).join('');
    } else {
        outputDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
    }
});
