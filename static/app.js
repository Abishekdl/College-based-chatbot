class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.chatbox__footer button'),
            messageInput: document.querySelector('.chatbox__footer input'),
            messagesContainer: document.querySelector('.chatbox__messages')
        }

        this.state = false;
        this.messages = [];
        this.userPhoto = ""; // Added to store user's photo URL
        this.botPhoto = ""; // Added to store bot's photo URL
    }

    display() {
        const { openButton, chatBox, sendButton, messageInput } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        messageInput.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hide the box
        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text1 = textField.value;
        if (text1 === "") {
            return;
        }

        const msg1 = { name: "User", message: text1, photo: this.userPhoto };
        this.messages.push(msg1);

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            const userQuery = r.user.query;
            const botResponse = r.bot.response;
            const userPhoto = r.user.photo;
            const botPhoto = r.bot.photo;

            // Store user's and bot's photo URLs
            this.userPhoto = userPhoto;
            this.botPhoto = botPhoto;

            // Display user's query and photo on the left side
            this.displayMessage(userQuery, userPhoto, true);

            // Display bot's response and photo on the right side
            this.displayMessage(botResponse, botPhoto, false);

            textField.value = '';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    displayMessage(message, photoUrl, isUser) {
        const { messagesContainer } = this.args;
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
    
        if (isUser) {
            messageElement.classList.add('user-message');
        } else {
            messageElement.classList.add('bot-message');
        }
    
        const imageElement = document.createElement('img');
        imageElement.src = photoUrl;
        imageElement.alt = isUser ? "Your Photo" : "Bot Photo";
        imageElement.classList.add('chatbot-image');
    
        const textElement = document.createElement('div');
        textElement.textContent = message;
    
        messageElement.appendChild(textElement); // Move text before image
    
        if (isUser) {
            messageElement.appendChild(imageElement); // Add image after text for user messages
        } else {
            const imageWrapper = document.createElement('div'); // Create a wrapper for bot messages
            imageWrapper.appendChild(imageElement);
            imageWrapper.classList.add('message-photo-wrapper');
            messageElement.insertBefore(imageWrapper, messageElement.firstChild); // Insert wrapper before text
        }
    
        if (!isUser) {
            messageElement.classList.add('user-message-left');
        }
    
        messagesContainer.insertBefore(messageElement, messagesContainer.firstChild);
    }
    
}

const chatbox = new Chatbox();
chatbox.display();
