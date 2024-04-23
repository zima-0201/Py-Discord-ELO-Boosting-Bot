import os
import json
import nextcord
import gspread
import stripe
from nextcord.ext import commands
from nextcord import Interaction, Embed, SlashOption
from dotenv import load_dotenv
from multiprocessing import Process, freeze_support
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build