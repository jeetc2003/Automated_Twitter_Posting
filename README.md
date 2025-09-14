# Automated Twitter Posting Assistant
## Overview

This project automates the workflow of generating and posting tweets while keeping a human in the loop for quality control. The system integrates multiple APIs and services to reduce the daily effort of creating engaging Twitter content, while still ensuring that every post reflects human approval.

## Workflow

**Seed Data:** Collects inspiration from a Google Sheet of previously liked or highly rated posts.

**Context Gathering:** Fetches recent technology news headlines via the GNews API.

**Post Generation:** Uses the Gemini LLM to generate a candidate tweet, combining the seed posts and current news.

## Approval Step:

Sends the generated post to a Telegram bot for human approval.

If rejected, the system regenerates a new post with feedback until approval is given.

If approved, the system requests a rating (1–10).

**Storage:** Saves the approved post and rating back into Google Sheets.

**Publishing:** Posts the approved tweet to Twitter using the Twitter API.

## Project Structure

**head.py** – Main orchestration script tying together the workflow.

**post_gen.py** – Fetches recent posts/news and generates new candidate tweets via Gemini.

**telegram_approval.py** – Handles human approval and rating collection using a Telegram bot.

**post_tweet.py** – Posts the approved tweet to Twitter.

## Current Capabilities

Modular integration of Google Sheets, GNews API, Gemini API, Telegram Bot API, and Twitter API.

**Human-in-the-loop** approval system with feedback and rating collection.

Iterative generation loop until satisfactory content is approved.

Storage of approved posts with metadata for future reuse.

## Future Plans

Add automation for scheduled posting (daily or user-defined frequency).

Allow users to specify preferred topics or domains for post generation.

Integrate support for images, videos, or other media in tweets.

Develop a user-friendly interface (Telegram or WhatsApp) where users can define preferences and approve posts in a single channel.

Build a deployable web or mobile application for broader usability.
