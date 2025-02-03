document.addEventListener('DOMContentLoaded', () => {
  const loader = document.getElementById('loader');
  const chatHistory = document.getElementById("chatHistory");
  const noMessagesText = document.getElementById('noMessagesText');
  const queryInput = document.getElementById('queryInput');
  const chatForm = document.getElementById('chatForm');

  toggleNoMessagesText();
  scrollToBottom();

  if (loader) loader.style.display = "none";

  chatForm.addEventListener("submit", handleFormSubmit);
});

function scrollToBottom() {
  const chatHistory = document.getElementById("chatHistory");
  if (chatHistory) {
    chatHistory.scrollTo({
      top: chatHistory.scrollHeight,
      behavior: "smooth"
    });
  }
}

function scrollToTop() {
  const chatHistory = document.getElementById("chatHistory");
  if (chatHistory) chatHistory.scrollTop = 0;
}

function scrollToElement(container, elementId) {
  const element = document.getElementById(elementId);
  if (container && element) {
    const elementPosition = element.offsetTop;
    container.scrollTop = elementPosition - container.offsetTop;
  }
}

function toggleNoMessagesText() {
  const chatHistory = document.getElementById('chatHistory');
  const noMessagesText = document.getElementById('noMessagesText');
  if (chatHistory && noMessagesText) {
    noMessagesText.style.display = chatHistory.children.length > 0 ? "none" : "block";
  }
}

function escapeHtml(unsafe) {
  const div = document.createElement('div');
  div.textContent = unsafe;
  return div.innerHTML;
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const loader = document.getElementById('loader');
  const queryInput = document.getElementById('queryInput');
  const chatHistory = document.getElementById("chatHistory");

  if (loader) loader.style.display = "block";

  const userQuery = escapeHtml(queryInput.value);
  appendUserMessage(userQuery);
  scrollToBottom();

  try {
    const response = await sendRequest();
    if (response.ok) {
      const data = await response.json();
      appendAssistantMessage(data.assistant_message.content);
      scrollToElement(chatHistory, "userDiv");
      toggleNoMessagesText();
      queryInput.value = "";
    } else {
      alert("Failed to fetch a response. Please try again.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert(`An error occurred: ${error.message}. Please try again.`);
  } finally {
    if (loader) loader.style.display = "none";
  }
}

function appendUserMessage(message) {
  const chatHistory = document.getElementById("chatHistory");
  chatHistory.innerHTML += `
    <div class="mb-4 flex justify-between">
      <div id="userDiv" class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
        <strong>User:</strong> ${message}
      </div>
    </div>`;
}

function appendAssistantMessage(message) {
  const chatHistory = document.getElementById("chatHistory");
  chatHistory.innerHTML += `
    <div class="mb-4 flex justify-between">
      <div id="assistantDiv" class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
        <strong>Assistant:</strong> ${message}
      </div>
    </div>`;
}

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
