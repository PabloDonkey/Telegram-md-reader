#!/usr/bin/env python3
"""
Send Markdown messages to Telegram bot.
Converts Markdown to Telegram-safe text and sends via bot API.
"""

import argparse
import sys
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from telegramify_markdown import markdownify

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def read_input(file_path=None):
    """Read Markdown text from file or stdin."""
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        return sys.stdin.read()


def convert_to_telegram_markdown(text):
    """Convert Markdown to Telegram-safe format."""
    try:
        converted = markdownify(text)
        return converted
    except Exception as e:
        print(f"Error converting Markdown: {e}", file=sys.stderr)
        sys.exit(1)


def send_to_telegram(text):
    """Send text to Telegram bot."""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set in environment or .env file.", file=sys.stderr)
        sys.exit(1)
    if not CHAT_ID:
        print("Error: CHAT_ID not set in environment or .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        bot = Bot(token=BOT_TOKEN)
        message = bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="MarkdownV2"
        )
        print(f"✓ Message sent successfully. Message ID: {message.message_id}")
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Send Markdown messages to Telegram bot."
    )
    parser.add_argument(
        "--file",
        help="Path to Markdown file to send",
        type=str,
        default=None
    )
    parser.add_argument(
        "--text",
        help="Markdown text to send directly",
        type=str,
        default=None
    )

    args = parser.parse_args()

    # Determine input source
    if args.text:
        markdown_text = args.text
    elif args.file:
        markdown_text = read_input(args.file)
    else:
        # Read from stdin
        markdown_text = read_input()

    if not markdown_text.strip():
        print("Error: No input provided.", file=sys.stderr)
        sys.exit(1)

    # Convert and send
    telegram_text = convert_to_telegram_markdown(markdown_text)
    send_to_telegram(telegram_text)


if __name__ == "__main__":
    main()
