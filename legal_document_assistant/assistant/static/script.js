document.addEventListener('DOMContentLoaded', () => {
  const loader = document.getElementById('loader');
  const chatHistory = document.getElementById("chatHistory");

  toggleNoMessagesText();
  scrollToBottom();

  if (loader) loader.style.display = "none";

});

function scrollToBottom() {
  const chatHistory = document.getElementById("chatHistory");
  if (chatHistory) chatHistory.scrollTop = chatHistory.scrollHeight;
}

function toggleNoMessagesText() {
  const chatHistory = document.getElementById('chatHistory');
  const noMessagesText = document.getElementById('noMessagesText');
  if (chatHistory && noMessagesText) {
    noMessagesText.style.display = chatHistory.children.length > 0 ? "none" : "block";
  }
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const loader = document.getElementById('loader');
  if (loader) loader.style.display = "block";

  const formData = new FormData(chatForm);
  const csrfToken = formData.get("csrfmiddlewaretoken");

  try {
    const response = await fetch(chatForm.action, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      const userMessage = escapeHtml(data.user_message.content);
      const assistantMessage = escapeHtml(data.assistant_message.content);

      chatHistory.innerHTML += `
            <div class="mb-4 flex justify-between">
                <div class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
                    <strong>User:</strong> ${userMessage}
                </div>
            </div>`;
      
      chatHistory.innerHTML += `
            <div class="mb-4 flex justify-between">
                <div class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
                    <strong>Assistant:</strong> ${assistantMessage}
                </div>
            </div>`;

      toggleNoMessagesText();
      scrollToBottom();
      queryInput.value = "";
    } else {
      alert("Failed to fetch a response. Please try again.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  } finally {
    if (loader) loader.style.display = "none";
  }
});

function escapeHtml(unsafe) {
  const div = document.createElement('div');
  div.textContent = unsafe;
  return div.innerHTML;
}
