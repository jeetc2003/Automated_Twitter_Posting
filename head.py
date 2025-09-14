
import gspread
from google.oauth2.service_account import Credentials
import datetime

def connect_to_gsheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load creds.json file (use the one you pasted earlier)
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    client = gspread.authorize(creds)

    # Open Google Sheet by name
    sheet = client.open("likedPosts")

    # Create worksheet if it doesn't exist
    try:
        worksheet = sheet.worksheet("Sheet1")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Sheet1", rows="1000", cols="4")
        worksheet.append_row(
            [
                "Date",
                "Post",
                "Selection",
                "Ratings",
            ]
        )

    return worksheet

        # ✅ Test the connection
if __name__ == "__main__":
    
    
    from telegram_approval import get_telegram_approval
    get_telegram_approval()

    print()
    print('New post idea text generated and Approved by user using telegram')
    print()

    #  After approval ends, post to Twitter
    from post_tweet import tweet_last_approved_post
    tweet_last_approved_post()

    print('Now twitter posting is done and i can rest')
