document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatArea = document.getElementById('chat-area');

    // Function to append messages to the chat area
    function appendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender);
        messageElement.textContent = message;
        chatArea.appendChild(messageElement);
        chatArea.scrollTop = chatArea.scrollHeight; // Scroll to the bottom
    }

    // Handle send button click
    sendButton.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (message) {
            appendMessage(message, 'user');
            userInput.value = '';

            // Send the message to the server and get the response
            try {
                const response = await fetch('/api/check-symptoms', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ symptoms: message })
                });

                const data = await response.json();
                appendMessage(data.response || 'Error: Unable to process request', 'bot');
            } catch (error) {
                console.error('Error:', error);
                appendMessage('Error: Unable to process request', 'bot');
            }
        }
    });

    // Handle Enter key press
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});
