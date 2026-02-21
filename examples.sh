#!/bin/bash
# Example usage of telegram_md_sender

# This script demonstrates different ways to use the send_to_telegram tool

echo "telegram_md_sender Usage Examples"
echo "=================================="
echo ""

# Create a temporary markdown file for demo
cat > /tmp/demo.md << 'EOF'
# Demo: Markdown to Telegram

Here's an example of **bold text** and *italic text*.

## Features

- Send Markdown directly
- Convert special formatting
- Integrate with Copilot

### Code Example

```python
def hello():
    print("Hello, Telegram!")
```

[Learn more](https://example.com)
EOF

echo "1. From stdin (pipe a file):"
echo "   cat your_file.md | python3 send_to_telegram.py"
echo ""

echo "2. From a file argument:"
echo "   python3 send_to_telegram.py --file /path/to/file.md"
echo ""

echo "3. From direct text argument:"
echo "   python3 send_to_telegram.py --text '**Hello** World'"
echo ""

echo "Demo file created at: /tmp/demo.md"
echo ""
echo "To actually send messages, first:"
echo "  1. Copy .env.example to .env"
echo "  2. Add your BOT_TOKEN and CHAT_ID"
echo "  3. Run: cat /tmp/demo.md | python3 send_to_telegram.py"

rm /tmp/demo.md
