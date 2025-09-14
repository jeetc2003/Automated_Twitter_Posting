import tweepy
from head import connect_to_gsheets
from dotenv import load_dotenv
import os
load_dotenv()


def get_last_post_from_gsheet():
    worksheet = connect_to_gsheets()
    values = worksheet.get_all_values()
    last_row = values[-1]  # last row
    return last_row[1]    


def post_to_twitter(tweet: str):
    # ! OAuth 2
    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_KEY_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
        )

    print("Tweeting:", tweet)
    response = client.create_tweet(text=tweet)
    print("✅ Tweet posted! ID:", response.data["id"])


def tweet_last_approved_post():
    post = get_last_post_from_gsheet()
    post_to_twitter(post)


if __name__=='__main__':
    tweet_last_approved_post()