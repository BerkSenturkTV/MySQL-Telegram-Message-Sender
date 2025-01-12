
# Telegram Message Sending Script

This project is a Python-based solution to send personalized messages to specific users via Telegram. It integrates with a MySQL database to fetch user information and automates the message delivery process with error handling and reporting.

## Features
- Secure integration with a MySQL database to retrieve user details.
- Automated message delivery via Telegram API.
- Supports custom delays between messages to avoid rate limiting.
- Generates detailed reports for sent, blocked, deactivated, and failed messages.
- Admin notification of the final report.

## Requirements
- Python 3.7 or higher
- Libraries:
  - `mysql-connector-python`
  - `python-dotenv`
  - `requests`
- A MySQL database with a `alluser` table that includes `uID` and `userName` columns.
- A Telegram bot token and admin chat ID.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-message-script.git
   cd telegram-message-script
   ```

2. Create a `.env` file in the project directory and add your credentials:
   ```env
   DB_HOST=your-database-host
   DB_PORT=3306
   DB_USER=your-database-username
   DB_PASSWORD=your-database-password
   DB_NAME=your-database-name
   TELEGRAM_TOKEN=your-telegram-bot-token
   ADMIN_CHAT_ID=your-admin-chat-id
   ```

3. Install the required libraries:
   ```bash
   pip install mysql-connector-python python-dotenv requests
   ```

4. Run the script:
   ```bash
   python script.py
   ```

## Notes
- Ensure your database credentials and Telegram token are correct.
- Use secure credentials and avoid exposing sensitive information.

## License
This project is licensed under the MIT License.
