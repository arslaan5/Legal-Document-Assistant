document.addEventListener('DOMContentLoaded', () => {
  const loader = document.getElementById('loader');
  const chatHistory = document.getElementById("chatHistory");
  const noMessagesText = document.getElementById('noMessagesText');
  const queryInput = document.getElementById('queryInput');
  const chatForm = document.getElementById('chatForm');

  // Initialize chat
  toggleNoMessagesText();
  scrollToBottom();
  if (loader) loader.style.display = "none";

  // Load any existing messages from server
  loadInitialMessages();

  chatForm.addEventListener("submit", handleFormSubmit);
});

// Scroll to bottom of chat container
function scrollToBottom() {
  const chatHistory = document.getElementById("chatHistory");
  if (chatHistory) {
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }
}

// Toggle "no messages" text visibility
function toggleNoMessagesText() {
  const chatHistory = document.getElementById('chatHistory');
  const noMessagesText = document.getElementById('noMessagesText');
  if (chatHistory && noMessagesText) {
    noMessagesText.style.display = chatHistory.children.length > 0 ? "none" : "block";
  }
}

// Escape HTML to prevent XSS
function escapeHtml(unsafe) {
  const div = document.createElement('div');
  div.textContent = unsafe;
  return div.innerHTML;
}

// Load initial messages from server
async function loadInitialMessages() {
  try {
    const response = await fetch('/get-conversation/', {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      renderConversation(data.conversation);
      scrollToBottom();
    }
  } catch (error) {
    console.error("Error loading initial messages:", error);
  }
}

// Render entire conversation
function renderConversation(conversation) {
  const chatHistory = document.getElementById("chatHistory");
  if (!chatHistory) return;

  chatHistory.innerHTML = '';
  
  conversation.forEach(message => {
    if (message.role === 'user') {
      appendUserMessage(message.content, false);
    } else {
      appendAssistantMessage(message.content, false);
    }
  });
  
  toggleNoMessagesText();
}

// Handle form submission
async function handleFormSubmit(e) {
  e.preventDefault();
  const loader = document.getElementById('loader');
  const queryInput = document.getElementById('queryInput');

  if (!queryInput.value.trim()) return;

  if (loader) loader.style.display = "block";
  
  const userQuery = escapeHtml(queryInput.value.trim());
  appendUserMessage(userQuery, true);

  try {
    const response = await sendRequest();
    if (response.ok) {
      const data = await response.json();
      appendAssistantMessage(data.assistant_message.content, true);
      queryInput.value = "";
    } else {
      appendAssistantMessage("Failed to fetch a response. Please try again.", true);
    }
  } catch (error) {
    console.error("Error:", error);
    appendAssistantMessage(`An error occurred: ${error.message}. Please try again.`, true);
  } finally {
    if (loader) loader.style.display = "none";
    queryInput.focus();
  }
}

// Append user message to chat
function appendUserMessage(message, shouldScroll = true) {
  const chatHistory = document.getElementById("chatHistory");
  if (!chatHistory) return;

  const messageDiv = document.createElement('div');
  messageDiv.className = 'mb-4 flex justify-between user-message';
  messageDiv.innerHTML = `
    <div class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
      <strong>User:</strong> ${message}
    </div>
  `;
  
  chatHistory.appendChild(messageDiv);
  toggleNoMessagesText();
  
  if (shouldScroll) {
    scrollToBottom();
  }
}

// Append assistant message to chat
function appendAssistantMessage(message, shouldScroll = true) {
  const chatHistory = document.getElementById("chatHistory");
  if (!chatHistory) return;

  const messageDiv = document.createElement('div');
  messageDiv.className = 'mb-4 flex justify-between assistant-message';
  messageDiv.innerHTML = `
    <div class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
      <strong>Assistant:</strong> ${message}
    </div>
  `;
  
  chatHistory.appendChild(messageDiv);
  toggleNoMessagesText();
  
  if (shouldScroll) {
    scrollToBottom();
  }
}

// Send AJAX request
async function sendRequest() {
  const chatForm = document.getElementById('chatForm');
  const formData = new FormData(chatForm);
  const csrfToken = formData.get("csrfmiddlewaretoken");

  return await fetch(chatForm.action, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  });
}