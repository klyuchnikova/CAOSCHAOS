import sqlite3
from sqlite3 import Error

from telegram import Bot, Chat
from telegram.ext import CommandHandler
from telegram.ext import Updater, MessageHandler, Filters
import asyncio
import requests

bot = None
conn = None
cur = None