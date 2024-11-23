const chatForm = document.getElementById('chatForm');
const chatHistory = document.getElementById('chatHistory');
const queryInput = document.getElementById('queryInput');
const loader = document.getElementById("loader");

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {

    e.preventDefault(); // Prevent default form submission
    loader.style.display = "block"; // Show the loader

    const formData = new FormData(chatForm);
    const csrfToken = formData.get('csrfmiddlewaretoken');

    // Send AJAX request
    try {
        const response = await fetch(chatForm.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();

            // Append user query
            chatHistory.innerHTML += `
                <div class="mb-4 flex">
                    <div class="text-xs md:text-base bg-red-50 p-2 sm:p-4 rounded-lg text-gray-800 ml-auto max-w-3xl">
                        <strong>User:</strong> ${data.user_message.content}
                    </div>
                </div>`;

            // Append assistant response
            chatHistory.innerHTML += `
                <div class="mb-4 flex">
                    <div class="text-xs md:text-base prose space-y-2 bg-blue-50 p-2 sm:p-4 rounded-lg text-gray-800 my-2 ml-0 max-w-4xl">
                        <strong>Assistant:</strong> ${data.assistant_message.content}
                    </div> 
                </div>`;

            scrollToBottom();

            // Clear input
            queryInput.value = '';
        } else {
            alert('Failed to fetch a response. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } 
    loader.style.display = "none";
});

// Scroll to the latest message after page load
scrollToBottom();


// function scrollToBottom() {
//     chatHistory.scrollTop = chatHistory.scrollHeight;
//   }

// chatForm.addEventListener('submit', async (e) => {

//     e.preventDefault(); // Prevent default form submission
//     loader.style.display = "block"; // Show the loader

//     const formData = new FormData(chatForm);
//     const csrfToken = formData.get('csrfmiddlewaretoken');

//     // Send AJAX request
//     try {
//         const response = await fetch(chatForm.action, {
//             method: 'POST',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'X-CSRFToken': csrfToken,
//             },
//             body: formData,
//         });

//         if (response.ok) {
//             const data = await response.json();

//             // Append user query
//             chatHistory.innerHTML += 
//                 <div class="mb-4">
//                     <div class="bg-blue-100 p-3 rounded-lg text-gray-800">
//                         <strong>User:</strong> ${data.user_message.content}
//                     </div>
//                 </div>;

//             // Append assistant response
//             chatHistory.innerHTML += 
//                 <div class="mb-4">
//                     <div class="bg-gray-100 p-3 rounded-lg text-gray-800 mt-2">
//                         <strong>Assistant:</strong> ${data.assistant_message.content}
//                     </div>
//                 </div>;

//             scrollToBottom();

//             // Clear input
//             queryInput.value = '';
//         } else {
//             alert('Failed to fetch a response. Please try again.');
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//     } 
//     loader.style.display = "none"
// });

// Scroll to the latest message
scrollToBottom();

// const loader = document.getElementById("loader");
// const form = document.getElementById("chatForm");

// form.addEventListener("submit", async (event) => {
//     event.preventDefault(); // Prevent form from reloading the page
//     loader.style.display = "block"; // Show the loader

//     const formData = new FormData(form);

//     try {
//         // Send the form data via fetch API
//         const response = await fetch(form.action, {
//             method: "POST",
//             body: formData,
//         });

//         if (!response.ok) {
//             throw new Error('Failed to fetch a response');
//         }

//         const html = await response.text();

//         // Update the chat history with the response HTML
//         document.body.innerHTML = html;
//         scrollToBottom();
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//     } finally {
//         loader.style.display = "none"; // Hide the loader
//     }
//     scrollToBottom();
// });
