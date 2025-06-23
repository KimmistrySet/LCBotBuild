async function sendMessage() {
    const message = document.getElementById("user_input").ariaValueMax;
    const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content_Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });
    const data = await response.json();
    document.getElementById("chatbot_response").innerText = data.response;
}

