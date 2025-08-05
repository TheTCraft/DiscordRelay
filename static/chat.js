const messagesDiv = document.getElementById('messages');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');

async function fetchMessages() {
  try {
    const res = await fetch('/api/get_messages');
    const data = await res.json();
    messagesDiv.innerHTML = '';
    data.forEach(msg => {
      const msgDiv = document.createElement('div');
      const usernameSpan = document.createElement('span');
      usernameSpan.className = 'username';
      usernameSpan.textContent = `[${msg.username}]: `;
      msgDiv.appendChild(usernameSpan);
      msgDiv.appendChild(document.createTextNode(msg.content));
      messagesDiv.appendChild(msgDiv);
    });
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  } catch (e) {
    console.error('Failed to load messages', e);
  }
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const content = messageInput.value.trim();
  if (!content) return;

  try {
    await fetch('/api/send_message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: USERNAME, content })
    });
    messageInput.value = '';
    fetchMessages();
  } catch (e) {
    console.error('Failed to send message', e);
  }
});

// Fetch messages every 2 seconds
setInterval(fetchMessages, 2000);
fetchMessages();