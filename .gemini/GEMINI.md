
#  Code Assistant Workspace Context

`.gemini/01_development_docs`配下を参考にして作成してほしい。

## About This Project

This project is a LINE Bot application built with Python and Flask. It's designed to provide interactive experiences, including puzzles and games, to LINE users. The bot can handle various types of user interactions, such as text messages, audio messages (with speech-to-text capabilities), and postback events from rich menus. It manages user state and interacts with Firebase for data handling. The bot's behavior is configured through JSON files in the `lib` directory.

## Key Technologies

- **Backend:** Python, Flask
- **LINE Integration:** `line-bot-sdk-python`
- **WSGI Server:** Gunicorn
- **Speech Recognition:** Vosk
- **Dependency Management:** pip, `requirements.txt`
- **Environment Variables:** `python-dotenv`
- **Database:** Firebase (Firestore)

## Project Structure

- **`app.py`**: The main Flask application file.
- **`src/`**: Contains the core application logic.
  - **`managers/`**: Manages user state and Firebase interactions.
  - **`services/`**: Handles different types of LINE events (message, postback, etc.).
  - **`messages/`**: Defines the bot's responses to user messages.
  - **`commonclass/`**: Common classes used across the application.
- **`lib/`**: Contains JSON files that define the bot's configuration, messages, and postback actions. See `[.gemini/01_development_docs/03_lib_definition_files.md](.gemini/01_development_docs/03_lib_definition_files.md)` for more details.
- **`templates/`**: HTML templates for the web interface.
- **`resources/`**: Static assets like images.
- **`.gemini/`**: Contains documentation for the Gemini assistant.

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
