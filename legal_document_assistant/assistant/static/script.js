// Ensure placeholder visibility on page load
document.addEventListener('DOMContentLoaded', () => {
  toggleNoMessagesText(); // Initial check
  scrollToBottom(); // Scroll to the latest message
  const loader = document.getElementById('loader');
  if (loader) loader.style.display = "none"; // Hide loader initially
});

const chatForm = document.getElementById("chatForm");
const chatHistory = document.getElementById("chatHistory");
const queryInput = document.getElementById("queryInput");
const loader = document.getElementById("loader");

function scrollToBottom() {
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Function to toggle the placeholder text
function toggleNoMessagesText() {
  const chatHistory = document.getElementById('chatHistory');
  const noMessagesText = document.getElementById('noMessagesText');

  if (!chatHistory || !noMessagesText) return; // Exit if elements are missing

  const hasMessages = chatHistory.children.length > 0;

  if (hasMessages) {
    noMessagesText.style.display = "none"; // Hide placeholder
  } else {
    noMessagesText.style.display = "block"; // Show placeholder
  }
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent default form submission
  loader.style.display = "block"; // Show the loader

  const formData = new FormData(chatForm);
  const csrfToken = formData.get("csrfmiddlewaretoken");

  // Send AJAX request
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

      // Append user query
      chatHistory.innerHTML += `
            <div class="mb-4 flex justify-between">
                <div class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
                    <strong>User:</strong> ${data.user_message.content}
                </div>
            </div>`;
          console.log(chatHistory.innerHTML); // Debugging: Check current chat content

      // Append assistant response
      chatHistory.innerHTML += `
            <div class="mb-4 flex justify-between">
                <div class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
                    <strong>Assistant:</strong> ${data.assistant_message.content}
                </div>
            </div>`;
          console.log(chatHistory.innerHTML); // Debugging: Check after assistant's response

      // Update placeholder visibility
      toggleNoMessagesText();

      scrollToBottom();

      // Clear input
      queryInput.value = "";
    } else {
      alert("Failed to fetch a response. Please try again.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  } finally {
    loader.style.display = "none";
  }
});

// Scroll to the latest message after page load
scrollToBottom();