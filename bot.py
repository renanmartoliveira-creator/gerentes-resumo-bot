import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone, date

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Variáveis BOT_TOKEN ou OPENAI_API_KEY não definidas")

TZ = timezone(timedelta(hours=-3))
DB = "data.db"

client = OpenAI(api_key=OPENAI_API_KEY)

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        chat INTEGER,
        user TEXT,
        text TEXT,
        created TEXT
    )
    """)
    conn.commit()
    conn.close()

def save(chat, user, text):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO messages VALUES(?,?,?,?)",
        (chat, user, text, datetime.now(TZ).isoformat())
    )
    conn.commit()
    conn.close()

def parse_date(txt):
    m = re.search(r"(\d{2})[\/\-](\d{2})[\/\-](\d{4})", txt)
    if not m:
        return None
    d,mn,y = map(int,m.groups())
    return date(y,mn,d)

def fetch(d):
    start = datetime(d.year,d.month,d.day,tzinfo=TZ).isoformat()
    end = (datetime(d.year,d.month,d.day,tzinfo=TZ)+timedelta(days=1)).isoformat()

    conn = sqlite3.connect(DB)
    cur = conn.execute(
        "SELECT user,text FROM messages WHERE created BE
