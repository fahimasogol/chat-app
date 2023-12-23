// app.js

// Function to get the value of a cookie by name (for CSRF token)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken'); // CSRF token for POST requests

// Fetch chat rooms
fetch('/api/chatrooms/')
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Process and display data
    })
    .catch(error => console.error('Error:', error));

// Post a message to a chat room
function postMessage(roomId, message) {
    fetch(`/chat/chatmessages/room/${roomId}/`, {  // Updated URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ message: message })  // Assuming you only need to send the message
    })
    .then(response => response.json())
    .then(data => {
        console.log('Message sent:', data);
    })
    .catch(error => console.error('Error:', error));
}

// WebSocket connection logic
let chatSocket;
function connect() {
    const roomName = '1'; // Replace with the actual room name or ID
    // Determine whether to use ws:// or wss://
    const wsStart = window.location.protocol === "https:" ? 'wss://' : 'ws://';
    chatSocket = new WebSocket(
        wsStart + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        displayMessage(data.message); // Process incoming message
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        setTimeout(function() {
            connect(); // Attempt to reconnect
        }, 1000); // Reconnect after 1 second
    };
}

connect(); // Call this function on page load

// Display a message in the chat log
function displayMessage(message) {
    const chatLog = document.getElementById('chat-log');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
}

// Form submission to send a message
document.getElementById('chat-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInput = document.getElementById('chat-message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInput.value = '';
};
