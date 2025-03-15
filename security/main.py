import discord
from discord.ext import commands
import asyncio
import json
from collections import deque

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    BOT_TOKEN = config["TOKEN"]

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

channel_activity = {}
THRESHOLD = 3  
TIME_WINDOW = 5  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.guilds)} guilds"))

async def check_mass_action(guild, user, action_type, log_action):
    if not user or user == guild.owner:  
        return

    if guild.id not in channel_activity:
        channel_activity[guild.id] = {"deleted": deque(maxlen=THRESHOLD), "created": deque(maxlen=THRESHOLD)}
    
    channel_activity[guild.id][action_type].append(asyncio.get_event_loop().time())

    timestamps = list(channel_activity[guild.id][action_type])
    if len(timestamps) >= THRESHOLD and (timestamps[-1] - timestamps[0]) <= TIME_WINDOW:
        try:
            await guild.ban(user, reason=f"Mass channel {action_type} detected")
            print(f"Banned {user} for mass channel {action_type}.")

            async for log in guild.audit_logs(limit=50, action=log_action):  
                if log.user == user:
                    try:
                        await log.target.delete()
                        print(f"Deleted channel {log.target.name} created by {user}.")
                    except discord.Forbidden:
                        print(f"Bot lacks permission to delete channel {log.target.name}.")
                    except discord.HTTPException:
                        print(f"Failed to delete channel {log.target.name}.")
        except discord.Forbidden:
            print("Bot lacks permission to ban members.")
        except discord.HTTPException:
            print("Failed to ban member.")

@bot.event
async def on_guild_channel_delete(channel):
    async for log in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        if log:
            await check_mass_action(channel.guild, log.user, "deleted", discord.AuditLogAction.channel_create)

@bot.event
async def on_guild_channel_create(channel):
    async for log in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
        if log:
            await check_mass_action(channel.guild, log.user, "created", discord.AuditLogAction.channel_create)

bot.run(BOT_TOKEN)
