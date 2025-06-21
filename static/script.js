const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send message on Enter
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendQuickQuestion(question) {
    // Hide welcome message
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
    
    messageInput.value = question;
    sendMessage();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Hide welcome message if it exists
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }

    // Disable send button and input
    sendBtn.disabled = true;
    messageInput.disabled = true;

    // Add user message
    addMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send message to Flask backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add AI response
        addMessage(data.response, 'bot');
        
        // Show feedback options
        showFeedbackOptions();

    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        // Re-enable send button and input
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function showFeedbackOptions() {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'feedback-container';
    feedbackDiv.style.display = 'block';
    feedbackDiv.innerHTML = `
        <p><strong>Was this answer helpful?</strong></p>
        <div class="feedback-buttons">
            <button class="feedback-btn" onclick="submitFeedback('yes', this)">
                <i class="fas fa-thumbs-up"></i> Yes
            </button>
            <button class="feedback-btn" onclick="submitFeedback('no', this)">
                <i class="fas fa-thumbs-down"></i> No
            </button>
        </div>
    `;
    
    const lastMessage = chatMessages.lastElementChild;
    lastMessage.appendChild(feedbackDiv);
}

async function submitFeedback(feedback, button) {
    const feedbackContainer = button.closest('.feedback-container');
    const lastBotMessage = feedbackContainer.closest('.message').querySelector('.message-content').textContent;
    
    try {
        // Send feedback to Flask backend
        await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                feedback: feedback,
                message: lastBotMessage
            })
        });
        
        feedbackContainer.innerHTML = `
            <p style="color: #059669;">
                <i class="fas fa-check-circle"></i> 
                Thank you for your feedback! It helps us improve our service.
            </p>
        `;
    } catch (error) {
        console.error('Error submitting feedback:', error);
        feedbackContainer.innerHTML = `
            <p style="color: #ef4444;">
                <i class="fas fa-exclamation-circle"></i> 
                Unable to submit feedback. Please try again.
            </p>
        `;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    messageInput.focus();
});