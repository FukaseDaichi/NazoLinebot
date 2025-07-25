# Architecture_design

```
NazoLinebot/
├── app.py                  # Main application file (Flask routes, LINE event handlers)
├── requirements.txt        # Python dependencies
├── .gitignore
├── README.md
├── .venv/                  # Python virtual environment
├── lib/                    # Configuration files (JSON), and other libraries like the Vosk model
│   ├── config.json
│   ├── messages.json
│   └── model/
├── resources/              # Static assets like images
├── src/                    # Main source code
│   ├── commonclass/        # Utility classes
│   ├── managers/           # Handles user state and external API (GAS) interactions
│   ├── messages/           # Modules for creating different types of LINE messages
│   └── services/           # Business logic for handling LINE webhook events
└── templates/              # HTML templates for Flask
```

- **`app.py`**: The entry point of the application. It initializes the Flask app, sets up LINE Bot SDK handlers, and defines the main webhook endpoint (`/callback`).
- **`src/services`**: Contains modules that handle the core logic for different event types (e.g., `handle_message_service.py`, `handle_postback_service.py`).
- **`src/managers`**: Manages the user's state (e.g., `user_state_manager.py`) and communication with external APIs like Google Apps Script (`gas_manager.py`).
- **`src/messages`**: Responsible for constructing the various kinds of reply messages sent to the user.
- **`lib/`**: Stores configuration data in JSON files and contains the Vosk model for speech recognition.
- **`templates/`**: Contains the `index.html` file served at the root URL.