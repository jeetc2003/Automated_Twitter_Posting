import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# ------------------------------------------
# Fetch recent post
# ------------------------------------------

def get_recent_posts( limit=100):
    from head import connect_to_gsheets
    worksheet = connect_to_gsheets()
    rows = worksheet.get_all_records()  
    recent = rows[-limit:] if len(rows) >= limit else rows
    return [
        {"post": r["Post"], "selected": r["Selected"], "rating": r["Rating"]}
        for r in recent
    ]

# -------------------------------------------
# Get recent news
# -------------------------------------------
def get_recent_news(Field3net):
    import urllib.request

    apikey = os.getenv('NEWS_API_KEY')
    # url1 = f"https://gnews.io/api/v4/top-headlines?category={Field3net[0]}&lang=en&country=in&max=3&apikey={apikey}"
    url2 = f"https://gnews.io/api/v4/top-headlines?category={Field3net}&lang=en&country=in&max=5&apikey={apikey}"
    # url3 = f"https://gnews.io/api/v4/top-headlines?category={Field3net[2]}&lang=en&country=in&max=5&apikey={apikey}"

        # world news
    # with urllib.request.urlopen(url1) as response:
    #     data = json.loads(response.read().decode("utf-8"))
    #     world = data["articles"]
        # Tech news
    with urllib.request.urlopen(url2) as response:
        data = json.loads(response.read().decode("utf-8"))
        tech = data["articles"]
        # Science news
    # with urllib.request.urlopen(url3) as response:
    #     data = json.loads(response.read().decode("utf-8"))
    #     science = data["articles"]
        
    merged_news=[]
    # for i in range(3):
    #     merged_news.append(world[i]['description'])

    for i in range(5):
        merged_news.append(tech[i]['description'])

    # for i in range(5):
    #     merged_news.append(science[i]['description'])
    return merged_news

# -------------------------------------------
# Prompt engineering
# -------------------------------------------

def build_prompt(posts, headlines, tone="informative", max_chars=240):
    PROMPT_TEMPLATE = """You are a professional microblog copywriter.
Constraints:
- Tone: {tone}
- Max characters: {max_chars}
- Keep it original and not verbatim from examples.
- No private info, no defamation, no disallowed content.

Examples (seed posts):
{examples}

Current context / headlines:
{headlines}

Produce 1 tweet-like post (<= {max_chars} chars). Output only the tweet text and nothing else.
"""
    examples = "\n".join(
        [p["post"] for p in posts if (p["selected"] == "yes") and ((p["rating"]) >= 7)]
    )
    return PROMPT_TEMPLATE.format(
        tone=tone,
        max_chars=max_chars,
        examples=examples,
        headlines=headlines
    )

# --------------------------------------------
# Generate generate_post_with_gemini
# --------------------------------------------

def generate_post_with_gemini(prompt: str) -> str:
    API_KEY = "AIzaSyCNS6PjuBXFfmTltfbjvpq9CoMnXXLyJNU"
    GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code} {response.text}")

    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "⚠️ Could not parse Gemini response: " + str(result)



# ---------------------------------------------
# Final Work
# ---------------------------------------------


def final_work(feedback=""):
    posts=get_recent_posts()
    news=get_recent_news(['Technology'])
    prompt = build_prompt(posts=posts, headlines=news,max_chars=275,tone='witty')
    new_post=generate_post_with_gemini(prompt=prompt+feedback)
    return new_post