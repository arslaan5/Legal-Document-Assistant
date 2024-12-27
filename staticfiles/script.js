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

function scrollToTop() {
  const chatHistory = document.getElementById("chatHistory");
  if (chatHistory) chatHistory.scrollTop = 0;
}

function scrollToElement(container, elementId) {
  const element = document.getElementById(elementId);
  if (container && element) {
    const elementPosition = element.offsetTop;
    container.scrollTop = elementPosition - container.offsetTop; // Scroll to the top of the element
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

// chatForm.addEventListener("submit", async (e) => {
//   e.preventDefault();
//   const loader = document.getElementById('loader');
//   if (loader) loader.style.display = "block";

//   const formData = new FormData(chatForm);
//   const csrfToken = formData.get("csrfmiddlewaretoken");

//   try {
//       const response = await fetch(chatForm.action, {
//       method: "POST",
//       headers: {
//         "X-Requested-With": "XMLHttpRequest",
//         "X-CSRFToken": csrfToken,
//       },
//       body: formData,
//     });

//     if (response.ok) {
//       const data = await response.json();

//       // Escape the HTML for safe rendering
//       const userMessage = escapeHtml(data.user_message.content);

//       chatHistory.innerHTML += `
//             <div class="mb-4 flex justify-between">
//                 <div class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
//                     <strong>User:</strong> ${userMessage}
//                 </div>
//             </div>`;
      
//       chatHistory.innerHTML += `
//             <div class="mb-4 flex justify-between">
//                 <div class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
//                     <strong>Assistant:</strong> ${data.assistant_message.content}
//                 </div>
//             </div>`;

//       toggleNoMessagesText();
//       queryInput.value = "";
//     } else {
//       alert("Failed to fetch a response. Please try again.");
//     }
//   } catch (error) {
//     console.error("Error:", error);
//     alert("An error occurred. Please try again.");
//   } finally {
//     if (loader) loader.style.display = "none";
//   }
// });


chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const loader = document.getElementById('loader');
  const queryInput = document.getElementById('queryInput');
  const chatHistory = document.getElementById("chatHistory");

  if (loader) loader.style.display = "block";

  // Append the user query immediately
  const userQuery = escapeHtml(queryInput.value);
  chatHistory.innerHTML += `
        <div class="mb-4 flex justify-between">
            <div id="userDiv" class="text-xs md:text-lg text-[#0A0A0A] p-2 sm:p-4 rounded-lg ml-auto max-w-xl sm:max-w-3xl">
                <strong>User:</strong> ${userQuery}
            </div>
        </div>`;
  scrollToBottom();

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

      chatHistory.innerHTML += `
            <div class="mb-4 flex justify-between">
                <div id="assistantDiv" class="text-xs md:text-base prose space-y-2 p-2 sm:p-4 rounded-lg text-[#001F54] my-2 ml-0 max-w-2xl sm:max-w-3xl">
                    <strong>Assistant:</strong> ${data.assistant_message.content}
                </div>
            </div>`;
      
      // Scroll to the top of the user query
      scrollToElement(chatHistory, "userDiv");

      toggleNoMessagesText();
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