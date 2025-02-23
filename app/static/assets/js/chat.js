document.addEventListener("DOMContentLoaded", function () {
  const msgerForm = get(".msger-inputarea");
  const msgerInput = get(".msger-input");
  const msgerChat = get(".msger-chat");

  function getCurrentTime() {
    const now = new Date();
    return `${String(now.getHours()).padStart(
      2,
      "0"
    )}:${String(now.getMinutes()).padStart(2, "0")}`;
  }

  function addWelcomeMessage() {
    const welcomeMsg = `Selamat datang di layanan chatbot Pusat Konsultasi dan Pelaporan Kekerasan Seksual.
    Saya siap membantu Anda dengan informasi seputar pencegahan dan penanganan kekerasan seksual, 
    serta menerima laporan kasus jika Anda membutuhkan.`;
    appendMessage("left", welcomeMsg, getCurrentTime());
  }

  addWelcomeMessage();

  msgerForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage("right", msgText);
    msgerInput.value = "";

    botResponse(msgText);
  });

  function appendMessage(side, text) {
    const msgHTML = `
            <div class="msg ${side}-msg">
                <div class="msg-bubble">
                    <div class="msg-text">${text}</div>
                    <div class="msg-info-time">${formatDate(new Date())}</div>
                </div>
            </div>
        `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }

  function botResponse(userMessage) {
    // Send the user message to the Flask server
    fetch("/chat/send", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    })
      .then((response) => response.json())
      .then((data) => {
        const combinedResponse = data
          .map((response) => {
            let cleanText = response.text.trim();
            cleanText = cleanText.replace(/\n/g, '<br>');
            return `<div class='bot-message'>${cleanText}</div>`;
          })
          .join("");
        setTimeout(() => {
          appendMessage("left", combinedResponse);
        }, 1000); // Delay the bot response by 1 second
      })
      .catch((error) => {
        console.error("Error:", error);
        appendMessage(
          "left",
          "Sorry, I'm having trouble understanding right now. Could you try again?"
        );
      });
  }
  function appendMessage(side, text) {
    const msgHTML = `
    <div class="msg ${side}-msg">
        <div class="msg-bubble">
            ${text}
        </div>
    </div>
    `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }

  // Utils
  function get(selector, root = document) {
    return root.querySelector(selector);
  }

  function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
  }
});