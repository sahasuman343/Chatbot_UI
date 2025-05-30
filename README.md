# Chatbot UI

A Streamlit-based generic chatbot application with user authentication, chat history, and feedback collection features for quick poc showcase.

## Features

- 🔐 User Authentication
  - Regular user login
  - Admin access with password protection
- 💬 Chat Interface
  - Real-time chat with simulated responses
  - Message history tracking
  - Session management
- 📊 Feedback System
  - Thumbs up/down feedback for responses
  - Feedback analytics for admins
- 📱 User Experience
  - Clean, modern interface
  - Session history view
  - Easy navigation

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd streamlit_app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the application in your web browser at `http://localhost:8501`

3. Login:
   - Regular users: Enter any username (except "admin")
   - Admin: Use username "admin" and the configured password

## Project Structure

```
streamlit_app/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── users.json          # User credentials
└── chat_logs/          # Directory for chat session logs
```

## Features in Detail

### User Authentication
- Regular users can login with any username
- Admin access requires password authentication
- Session management with unique session IDs

### Chat Interface
- Real-time chat with simulated responses
- Message history tracking per session
- Persistent chat logs in JSON format

### Admin Dashboard
- View overall feedback statistics
- Access session-wise feedback
- Monitor user interactions

### Data Persistence
- Chat sessions are saved in JSON format
- User feedback is tracked and stored
- Session history is maintained for 7 days

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.
