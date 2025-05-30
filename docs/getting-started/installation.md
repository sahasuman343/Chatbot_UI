# Installation Guide

This guide will help you set up the SCM Chatbot application on your system.

## Prerequisites

Before installing SCM Chatbot, ensure you have:

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/streamlit_app.git
cd streamlit_app
```

### 2. Create a Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following variables:

```env
# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key

# Database Settings (if applicable)
DATABASE_URL=your-database-url
```

### 5. Initialize the Application

```bash
# Create necessary directories
mkdir -p chat_logs
```

### 6. Verify Installation

Run the application:

```bash
streamlit run main.py
```

Visit `http://localhost:8501` in your web browser to verify the installation.

## Troubleshooting

### Common Issues

#### 1. Package Installation Errors

If you encounter errors during package installation:

```bash
# Update pip
python -m pip install --upgrade pip

# Try installing packages individually
pip install streamlit
pip install numpy
# ... etc.
```

#### 2. Port Already in Use

If port 8501 is already in use:

```bash
# Kill the process using the port
# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :8501
kill -9 <PID>
```

#### 3. Virtual Environment Issues

If you have issues with the virtual environment:

```bash
# Remove existing environment
rm -rf venv

# Create new environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Next Steps

After successful installation:

1. Read the [Quick Start Guide](quickstart.md)
2. Configure the application in [Configuration](configuration.md)
3. Learn about the [Chat Interface](../user-guide/chat-interface.md)

## Additional Resources

- [Python Installation Guide](https://www.python.org/downloads/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Virtual Environment Guide](https://docs.python.org/3/library/venv.html) 