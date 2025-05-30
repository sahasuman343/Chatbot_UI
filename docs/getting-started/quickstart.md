# Quick Start Guide

This guide will help you get up and running with SCM Chatbot quickly.

## Basic Usage

### 1. Start the Application

```bash
streamlit run main.py
```

### 2. Access the Application

Open your web browser and navigate to:
```
http://localhost:8501
```

### 3. Login

#### Regular User
1. Enter any username (except "admin")
2. Click "Login"

#### Admin User
1. Check "Login as admin"
2. Enter username "admin"
3. Enter your password
4. Click "Login"

## Chat Interface

### Starting a New Chat
1. Click "🆕 Start New Chat" in the sidebar
2. Type your message in the chat input
3. Press Enter or click the send button

### Viewing Chat History
- Today's chats appear under "📅 Today"
- Past 7 days' chats appear under "🗓 Past 7 Days"
- Click any chat to view its history

### Providing Feedback
- Use thumbs up/down buttons to rate responses
- Feedback is automatically saved

## Admin Features

### Accessing Admin Dashboard
1. Login as admin
2. View feedback statistics in the sidebar
3. Click "Overall Feedback Summary" for general stats
4. Click individual sessions for detailed feedback

### Viewing Feedback
- Overall positive/negative feedback counts
- Session-wise feedback breakdown
- Chat history with feedback

## Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| `Enter` | Send message |
| `Ctrl + Enter` | New line in message |
| `Esc` | Clear input |

## Tips and Tricks

### 1. Session Management
- Each chat session has a unique ID
- Sessions are automatically saved
- Access past sessions from the sidebar

### 2. Feedback Collection
- Provide feedback for each response
- View feedback trends in admin dashboard
- Track user satisfaction over time

### 3. Best Practices
- Keep messages clear and concise
- Use appropriate feedback
- Log out after session completion

## Common Tasks

### Starting a New Session
```python
# The application automatically creates a new session
# when you click "Start New Chat"
```

### Saving Chat History
```python
# Chat history is automatically saved
# No manual saving required
```

### Viewing Feedback
```python
# Access feedback through the admin dashboard
# or view individual message feedback
```

## Next Steps

1. Read the [User Guide](../user-guide/chat-interface.md)
2. Learn about [Configuration](configuration.md)
3. Explore [Advanced Features](../user-guide/feedback-system.md)

## Need Help?

- Check the [User Guide](../user-guide/chat-interface.md)
- Visit our [GitHub Issues](https://github.com/yourusername/streamlit_app/issues)
- Contact the support team 