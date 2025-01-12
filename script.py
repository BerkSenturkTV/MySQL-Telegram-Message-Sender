
import requests
import mysql.connector
import time
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_db():
    """Connect to the database using credentials from the .env file."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def send_message(chat_id, message):
    """Send a message using the Telegram bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=payload, timeout=10)
    return response

def main():
    admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))

    print("What do you want to do?")
    print("1. Send Message")
    choice = input("Make your choice (1): ").strip()

    if choice == "1":
        message_base = input("Enter the message to send: ")
        user_ids = input("Enter the UIDs of the users to send messages to, separated by commas: ").split(',')
        message_delay = int(input("Enter the message delay time (in seconds): "))

        db = connect_to_db()
        cursor = db.cursor()

        total_users = len(user_ids)
        sent_messages = 0
        blocked_users = []
        deactivated_users = []
        timeout_users = []
        failed_users = []
        not_found_users = []
        all_sent_users = []

        for user_id in user_ids:
            user_id = user_id.strip()
            if not user_id.isdigit():
                print(f"Invalid UID entered: {user_id}. Please enter a number.")
                continue

            try:
                cursor.execute("SELECT uID, userName FROM alluser WHERE uID = %s", (user_id,))
                result = cursor.fetchone()

                if result:
                    chat_id = result[0]
                    username = result[1]
                    random_suffix = f"W{random.randint(1, 999):03d}"
                    message = f"{message_base} {random_suffix}"

                    print(f"Waiting to send a message to UID {user_id}...")

                    try:
                        response = send_message(chat_id, message)

                        if response.status_code == 200:
                            sent_messages += 1
                            all_sent_users.append(f"{username} [{user_id}]")
                            print(f"Message successfully sent to UID {user_id}.")
                        else:
                            error_description = response.json().get('description', 'Unknown error')
                            if "bot was blocked by the user" in error_description:
                                blocked_users.append(f"{username} [{user_id}]")
                                print(f"Message could not be sent to UID {user_id}. Reason: Blocked.")
                            elif "user is deactivated" in error_description:
                                deactivated_users.append(f"{username} [{user_id}]")
                                print(f"Message could not be sent to UID {user_id}. Reason: Deactivated.")
                            else:
                                failed_users.append(user_id)
                                print(f"Message could not be sent to UID {user_id}. Error: {error_description}")
                    except requests.exceptions.Timeout:
                        timeout_users.append(f"{username} [{user_id}]")
                        failed_users.append(user_id)
                        print(f"Message request to UID {user_id} timed out. Continuing...")
                else:
                    not_found_users.append(user_id)
                    print(f"UID {user_id} not found in the database.")
            except mysql.connector.Error as db_err:
                print(f"Database error: {db_err}")
                db = connect_to_db()
                cursor = db.cursor()
                continue

            time.sleep(message_delay)

        final_report = (
            f"Message sending process completed.
"
            f"Total messages sent: {sent_messages}
"
            f"Remaining messages: {total_users - sent_messages - len(not_found_users)}
"
            f"Blocked users: {', '.join(blocked_users) if blocked_users else 'None'}
"
            f"Deactivated users: {', '.join(deactivated_users) if deactivated_users else 'None'}
"
            f"Timeout users: {', '.join(timeout_users) if timeout_users else 'None'}
"
            f"Failed message deliveries: {', '.join(map(str, failed_users)) if failed_users else 'None'}
"
            f"Users not found in the database: {', '.join(map(str, not_found_users)) if not_found_users else 'None'}
"
            f"All users who received messages:
{chr(10).join(all_sent_users) if all_sent_users else 'None'}"
        )

        # Send report to admin
        response = send_message(admin_chat_id, final_report)
        if response.status_code == 200:
            print("Message successfully sent to the admin.")
        else:
            print(f"Message could not be sent to the admin. Error: {response.status_code}")
            print(response.json())

        cursor.close()
        db.close()
    else:
        print("Invalid choice. Program is terminating.")

if __name__ == "__main__":
    main()
