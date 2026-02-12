#!/usr/bin/env python3
import os
import logging
from datetime import datetime, time
from telethon import TelegramClient, events, functions
from telethon.tl.types import Message
import asyncio
import requests
from collections import defaultdict

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API_ID = int(os.getenv('API_ID', '12345'))
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
GROUP_SOURCE_ID = int(os.getenv('GROUP_SOURCE_ID', '-1001234567890'))
GROUP_RESUME_ID = int(os.getenv('GROUP_RESUME_ID', '-1001234567890'))
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')

# Telegram client
client = TelegramClient('bot_session', API_ID, API_HASH)

# Store messages by topic
messages_by_topic = defaultdict(list)

async def summarize_with_perplexity(text):
    """Summarize text using Perplexity API"""
    if not PERPLEXITY_API_KEY:
        return f"[Resumo automático desabilitado]\n{text[:500]}..."
    
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-2-70b-chat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Faça um resumo conciso em português desta conversa:\n\n{text}"
                }
            ]
        }
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error summarizing with Perplexity: {e}")
    
    return text[:1000]

@client.on(events.NewMessage(chats=GROUP_SOURCE_ID))
async def handle_new_message(event):
    """Handle new messages from source group"""
    try:
        message = event.message
        topic_id = message.reply_to.topic_id if message.reply_to else 0
        
        # Store message
        msg_data = {
            'id': message.id,
            'text': message.text or '',
            'sender': message.sender_id,
            'date': message.date,
            'topic_id': topic_id
        }
        messages_by_topic[topic_id].append(msg_data)
        logger.info(f"Message stored for topic {topic_id}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")

@client.on(events.Raw)
async def handle_command(event):
    """Handle bot commands"""
    if not hasattr(event, 'message'):
        return
    
    message = event.message
    if not message.text or not message.text.startswith('/'):
        return
    
    if '/resumo_dia' in message.text:
        await send_daily_summary()
    elif '/relatorio_pessoa' in message.text:
        await send_person_report(event)
    elif '/contagem_msgs' in message.text:
        await send_message_count(event)

async def send_daily_summary():
    """Send daily summary of all topics"""
    try:
        for topic_id, messages in messages_by_topic.items():
            if not messages:
                continue
            
            # Compile messages for this topic
            topic_text = f"Resumo do Tópico ({topic_id}):\n\n"
            for msg in messages:
                topic_text += f"- {msg['text'][:100]}...\n"
            
            # Summarize
            summary = await summarize_with_perplexity(topic_text)
            
            # Send to resume group
            await client.send_message(
                GROUP_RESUME_ID,
                f"📊 **Resumo do Dia - Tópico #{topic_id}**\n\n{summary}",
                parse_mode='markdown',
                reply_to=topic_id
            )
            
            logger.info(f"Summary sent for topic {topic_id}")
    except Exception as e:
        logger.error(f"Error sending daily summary: {e}")

async def send_person_report(event):
    """Send report for a specific person"""
    logger.info("Person report feature not yet implemented")

async def send_message_count(event):
    """Send message count statistics"""
    logger.info("Message count feature not yet implemented")

async def schedule_daily_summary():
    """Schedule daily summary at 23:59"""
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(23, 59))
        
        if now > target_time:
            target_time = datetime.combine(now.date() + timedelta(days=1), time(23, 59))
        
        sleep_seconds = (target_time - now).total_seconds()
        logger.info(f"Waiting {sleep_seconds} seconds for daily summary")
        
        await asyncio.sleep(sleep_seconds)
        await send_daily_summary()
        
        # Clear messages for next day
        messages_by_topic.clear()

async def main():
    """Main bot function"""
    await client.start(bot_token=BOT_TOKEN)
    logger.info("Bot started")
    
    # Schedule daily summary
    asyncio.create_task(schedule_daily_summary())
    
    # Keep bot running
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
