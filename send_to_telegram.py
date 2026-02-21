#!/usr/bin/env python3
"""
Send Markdown messages to Telegram bot.
Converts Markdown to Telegram-safe text and sends via bot API.
"""

import argparse
import sys
import os
import asyncio
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


def split_message(text, limit=2000):
    """
    Split message intelligently at paragraph boundaries.
    
    Args:
        text: The message text to split
        limit: Character limit per message (default: 2000)
    
    Returns:
        List of message chunks
    """
    if len(text) <= limit:
        return [text]
    
    messages = []
    
    # Try splitting on paragraph boundaries (double newline)
    paragraphs = text.split('\n\n')
    current_message = ""
    
    for paragraph in paragraphs:
        # Check if adding this paragraph exceeds limit
        test_message = current_message + ('\n\n' if current_message else '') + paragraph
        
        if len(test_message) <= limit:
            current_message = test_message
        else:
            # Paragraph itself is too long, try splitting by lines
            if current_message:
                messages.append(current_message)
                current_message = ""
            
            # Split paragraph by lines
            lines = paragraph.split('\n')
            for line in lines:
                test_message = current_message + ('\n' if current_message else '') + line
                
                if len(test_message) <= limit:
                    current_message = test_message
                else:
                    # Line itself is too long, hard split it
                    if current_message:
                        messages.append(current_message)
                        current_message = ""
                    
                    # Hard split the long line
                    while len(line) > limit:
                        messages.append(line[:limit])
                        line = line[limit:]
                    
                    current_message = line
    
    if current_message:
        messages.append(current_message)
    
    return messages


def send_to_telegram(text):
    """Send text to Telegram bot, splitting into multiple messages if needed."""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set in environment or .env file.", file=sys.stderr)
        sys.exit(1)
    if not CHAT_ID:
        print("Error: CHAT_ID not set in environment or .env file.", file=sys.stderr)
        sys.exit(1)

    messages = split_message(text)

    async def send():
        try:
            bot = Bot(token=BOT_TOKEN)
            message_ids = []
            
            for i, msg in enumerate(messages, 1):
                message = await bot.send_message(
                    chat_id=CHAT_ID,
                    text=msg,
                    parse_mode="MarkdownV2"
                )
                message_ids.append(message.message_id)
                if len(messages) > 1:
                    print(f"✓ Message {i}/{len(messages)} sent successfully. Message ID: {message.message_id}")
                else:
                    print(f"✓ Message sent successfully. Message ID: {message.message_id}")
            
            if len(messages) > 1:
                print(f"✓ All {len(messages)} messages sent successfully.")
        except TelegramError as e:
            print(f"Error sending message to Telegram: {e}", file=sys.stderr)
            sys.exit(1)

    asyncio.run(send())


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
