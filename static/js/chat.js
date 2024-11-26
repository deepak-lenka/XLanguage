document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const loadingIndicator = document.getElementById('loading');
    const languagePanel = document.getElementById('languagePanel');
    const selectedLanguageDiv = document.querySelector('.selected-language');
    
    let isProcessing = false;
    let currentLanguage = 'English';
    let isPanelOpen = false;

    // Language Panel Toggle
    window.toggleLanguagePanel = function(event) {
        event.stopPropagation(); // Prevent event bubbling
        isPanelOpen = !isPanelOpen;
        
        // Toggle panel visibility
        languagePanel.classList.toggle('active');
        selectedLanguageDiv.classList.toggle('active');
        
        // Add/remove click outside listener
        if (isPanelOpen) {
            document.addEventListener('click', handleClickOutside);
        } else {
            document.removeEventListener('click', handleClickOutside);
        }
    };

    // Tab Switching
    window.switchTab = function(tabId, event) {
        event.stopPropagation(); // Prevent event bubbling
        
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab-button').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Add active class to clicked tab and its content
        event.currentTarget.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    };

    // Language Selection
    window.selectLanguage = function(language, event) {
        event.stopPropagation(); // Prevent event bubbling
        
        // Update current language
        currentLanguage = language;
        document.getElementById('current-language').textContent = language;

        // Update visual selection
        document.querySelectorAll('.language-grid button').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedButton = event.currentTarget;
        selectedButton.classList.add('selected');

        // Add visual feedback
        const ripple = document.createElement('div');
        ripple.classList.add('ripple');
        selectedButton.appendChild(ripple);

        // Close panel with slight delay for visual feedback
        setTimeout(() => {
            ripple.remove();
            closeLanguagePanel();
        }, 200);
    };

    // Handle click outside
    function handleClickOutside(event) {
        if (!languagePanel.contains(event.target) && 
            !selectedLanguageDiv.contains(event.target)) {
            closeLanguagePanel();
        }
    }

    // Close language panel
    function closeLanguagePanel() {
        isPanelOpen = false;
        languagePanel.classList.remove('active');
        selectedLanguageDiv.classList.remove('active');
        document.removeEventListener('click', handleClickOutside);
    }

    // Add message to chat
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Add typing effect for bot messages
        if (!isUser) {
            typeMessage(messageDiv, text);
        } else {
            messageDiv.textContent = text;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Typing effect for bot messages
    function typeMessage(element, text) {
        let index = 0;
        element.textContent = '';
        
        function type() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                scrollToBottom();
                setTimeout(type, 20);
            }
        }
        
        type();
    }

    // Scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show/hide loading indicator
    function showLoading(show) {
        loadingIndicator.classList.toggle('active', show);
    }

    // Send message
    async function sendMessage() {
        if (isProcessing) return;

        const message = messageInput.value.trim();
        if (!message) return;

        try {
            isProcessing = true;
            showLoading(true);
            
            // Add user message to chat
            addMessage(message, true);
            messageInput.value = '';

            // Disable input while processing
            messageInput.disabled = true;
            sendButton.disabled = true;

            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    target_language: currentLanguage
                })
            });

            const data = await response.json();

            if (data.error) {
                addMessage(`Error: ${data.error}`, false);
            } else if (data.choices && data.choices[0].message.content) {
                addMessage(data.choices[0].message.content, false);
            } else {
                addMessage(data.response || 'Sorry, I could not process your request.', false);
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong. Please try again.', false);
        } finally {
            isProcessing = false;
            showLoading(false);
            
            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Close panel on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isPanelOpen) {
            closeLanguagePanel();
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768 && isPanelOpen) {
            closeLanguagePanel();
        }
    });

    // Initialize focus
    messageInput.focus();

    // Prevent panel close when clicking inside
    languagePanel.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // Add touch events for mobile
    let touchStartY = 0;
    languagePanel.addEventListener('touchstart', function(e) {
        touchStartY = e.touches[0].clientY;
    });

    languagePanel.addEventListener('touchmove', function(e) {
        const touchY = e.touches[0].clientY;
        const diff = touchStartY - touchY;

        if (Math.abs(diff) > 50) {
            closeLanguagePanel();
        }
    });
});
