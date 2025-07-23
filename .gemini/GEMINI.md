
#  Code Assistant Workspace Context

## About This Project

This project is a LINE Bot application built with Python and Flask. It's designed to provide interactive experiences, including puzzles and games, to LINE users. The bot can handle various types of user interactions, such as text messages, audio messages (with speech-to-text capabilities), and postback events from rich menus. It manages user state and interacts with external services like Google Apps Script (GAS) for data handling.

## Key Technologies

- **Backend:** Python, Flask
- **LINE Integration:** `line-bot-sdk-python`
- **WSGI Server:** Gunicorn
- **Speech Recognition:** Vosk
- **Dependency Management:** pip, `requirements.txt`
- **Environment Variables:** `python-dotenv`
- **Database:** Firebase (Firestore)

## Database (Firestore) Structure

With the transition to Firebase, the following Firestore collection structure is proposed to replace the existing GAS-based data management:

// Firestore構造（構造定義の記述）

Collection: users
├── Document ID: <line_user_id>
    ├── name: string        // 例: "山田太郎"
    ├── mode: string        // 例: "easy"
    ├── games: array        // ゲーム履歴の配列
        ├── title: string   // ゲームタイトル
        ├── score: number   // スコア
        ├── start: timestamp // 開始時刻
        ├── end: timestamp   // 終了時刻



The project is organized into several directories, each with a specific responsibility:

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

## How to Run

1.  **Set up the environment:**
    - Ensure you have Python installed.
    - Create a virtual environment: `python -m venv .venv`
    - Activate it: `.venv\Scripts\activate` (on Windows)
    - Install dependencies: `pip install -r requirements.txt`

2.  **Configure environment variables:**
    - Create a `.env` file in the root directory.
    - Add the necessary variables:
      ```
      CHANNEL_ACCESS_TOKEN="your_line_channel_access_token"
      CHANNEL_SECRET="your_line_channel_secret"
      FIREBASE_CREDENTIALS_PATH="path/to/your/firebase-credentials.json"
      ```

      *Note: The `GAS_API_URL` will no longer be needed after the migration.*

3.  **Run the development server:**
    ```bash
    python app.py
    ```
    The application will be running at `http://127.0.0.1:8000`.

4.  **Run in production (example):**
    The project includes `gunicorn`, so you can run it using a WSGI server:
    ```bash
    gunicorn --bind 0.0.0.0:8000 app:app
    ```

## How to Test

The project is configured to use `pytest` for testing, as indicated by the `.vscode/settings.json` file.

- **Run tests:**
  ```bash
  pytest
  ```
*(Note: No specific test files were found in the project structure, but the configuration is in place.)*

## Code Formatting

The project uses `black` for code formatting. To format the code, run:
```bash
black .
```
