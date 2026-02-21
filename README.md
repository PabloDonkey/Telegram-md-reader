# telegram_md_sender

A Python tool to send Markdown messages to Telegram using the `telegramify-markdown` library. Integrates with GitHub Copilot as a skill to send generated Markdown directly to your Telegram chat.

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Telegram credentials

#### Get your BOT_TOKEN
1. Open Telegram and search for **@BotFather**
2. Send `/start` to begin
3. Send `/newbot` to create a new bot
4. Follow the prompts to name your bot
5. Copy the bot token provided (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

#### Get your CHAT_ID
You can get your chat ID in several ways:

**Option A: Direct method**
1. Start a chat with your bot by sending `/start`
2. Go to: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
3. Replace `YOUR_BOT_TOKEN` with your actual token
4. Look for the `chat.id` field in the JSON response

**Option B: Using a test message**
1. Send a message to your bot
2. Run: `curl https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates | jq '.result[0].message.chat.id'`
3. Look for your chat ID in the output

#### Create .env file

Copy the example file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholders:

```env
BOT_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

## Usage

### Send Markdown from stdin

```bash
cat your_markdown_file.md | python3 send_to_telegram.py
```

### Send Markdown from a file

```bash
python3 send_to_telegram.py --file your_markdown_file.md
```

### Send Markdown as a direct argument

```bash
python3 send_to_telegram.py --text "# Hello\n\nThis is **bold** text."
```

## Message Splitting

The script automatically splits messages that exceed 2000 characters to ensure readability and avoid hitting Telegram's message size limits (4096 characters max). 

**Splitting strategy:**
1. First tries to split on paragraph boundaries (`\n\n`) to keep paragraphs intact
2. Falls back to splitting on line breaks (`\n`) if paragraphs are too long
3. As a last resort, hard-splits at the character limit if individual lines exceed 2000 chars

When a message is split, each chunk is sent as a separate message with a sequence indicator (e.g., "Message 1/3", "Message 2/3").

**Example:**
```bash
# This long markdown will be automatically split and sent as multiple messages
python3 send_to_telegram.py --file very_long_document.md
```

## Integration with GitHub Copilot

### Copy the skill file

If you have Copilot CLI installed and configured, copy the skill file to your skills directory:

```bash
mkdir -p ~/.copilot/skills
cp copilot-skill.yaml ~/.copilot/skills/send_to_telegram.yaml
```

### Use the skill

After Copilot generates Markdown output, send it to Telegram:

```bash
copilot skill send_to_telegram
```

Or pipe directly:

```bash
echo "# Generated Content\n\nSome markdown" | copilot skill send_to_telegram
```

## Markdown Formatting Support

The script uses `telegramify-markdown` to convert standard Markdown to Telegram's MarkdownV2 format. Supported formatting:

- **Bold**: `**text**` → `*text*`
- *Italic*: `*text*` → `_text_`
- `Code`: `` `code` `` → `` `code` ``
- Code blocks: `` ```code``` `` → `` ```code``` ``
- Links: `[text](url)` → `[text](url)`
- Headers: `# Header` → `*Header*`
- Lists and other Markdown elements

## Troubleshooting

### "BOT_TOKEN not set"
- Ensure `.env` file exists in the project directory
- Check that you've added your actual token to `.env`
- Run from the project directory

### "CHAT_ID not set"
- Follow the steps above to get your chat ID
- Add it to your `.env` file

### "Error sending message to Telegram"
- Verify your bot token is correct
- Verify your chat ID is correct
- Ensure your bot has permission to send messages
- Start a conversation with your bot first

### Message formatting issues
- Check that your Markdown is valid
- Some special characters may need escaping in MarkdownV2 format
- Try sending a simple test message first

## Requirements

- Python 3.7+
- python-telegram-bot
- telegramify-markdown
- python-dotenv

## License

MIT
