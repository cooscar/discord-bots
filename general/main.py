from discord import Permissions
import discord, random, time
import json
from discord.ext import commands
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
    app.run(host="0.0.0.0", port=8080)


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
    print(f"{Fore.LIGHTCYAN_EX}Bot is online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.guilds)} guilds"))



@bot.command(pass_context=True)
async def help(ctx):
    embed = Embed(title="Help", color=0xaf1aff)
    embed.add_field(name=".ban", value="Bans a user", inline=False)
    embed.add_field(name=".kick", value="Kicks a user", inline=False)
    embed.add_field(name=".mute", value="Mutes a user", inline=False)
    embed.add_field(name=".unmute", value="Unmutes a user", inline=False)
    embed.add_field(name=".purge", value="Clears messages", inline=False)
    embed.add_field(name=".dm", value="DMs a user", inline=False)
    embed.add_field(name=".unban", value="Unbans a user", inline=False)
    embed.add_field(name=".nmap {ip}", value="get very basic info about an ip")
    embed.add_field(name=".ports {ip} {port1} {port2}", value="get info about ports within a range")
    await ctx.send(embed=embed)







@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        embed1 = Embed(title="User banned", color=0xaf1aff)
        embed1.add_field(name=f"{member}", value=f"banned for {reason}", inline=False)
        await ctx.send(embed=embed1)
        await member.send(embed=embed1)
        print(f"{member} has been banned for {reason}")
        await member.ban(reason=reason)
    except discord.Forbidden:
        await ctx.send("❌ You can not perform this command.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")




@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: str):
    async for ban_entry in ctx.guild.bans():
        try:
                
            user = ban_entry.user
            if user.name.lower() == member.lower():  
                await ctx.guild.unban(user)
                embed1 = Embed(title="User unbanned", color=0xaf1aff)
                embed1.add_field(name=f"{member}", value=f"unbanned", inline=False)
                await ctx.send(embed=embed1)
                print(f"{member} has been unbanned")
                return
                await ctx.send(f"❌ Cannot find `{member}` in the ban list.")
        except discord.Forbidden:
            await ctx.send("❌ You can not perform this command.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")






@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def dm(ctx, user:discord.Member, *, message=None):
    try:    
        await user.send(message)

    except discord.Forbidden:
        await ctx.send("❌ You can not perform this command.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")






@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        embed2 = Embed(title="User kicked", color=0xaf1aff)
        embed2.add_field(name=f"{member}", value=f"kicked for {reason}", inline=False)
        await ctx.send(embed=embed2)
        print(f"{member} has been kicked for {reason}")
        await member.send(embed=embed2)
        await member.kick(reason=reason)

    except discord.Forbidden:
        await ctx.send("❌ You can not perform this command.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")





@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    try:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        embed3 = Embed(title="User muted", color=0xaf1aff)
        embed3.add_field(name=f"{member}", value=f"muted for {reason}", inline=False)
        await ctx.send(embed=embed3)
        print(f"{member} has been muted for {reason}")
        await member.send(embed=embed3)
    except:
        await ctx.send("Muted role not found, creating one now")
        await ctx.guild.create_role(name="Muted")
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        embed3 = Embed(title="User muted", color=0xaf1aff)
        embed3.add_field(name=f"{member}", value=f"muted for {reason}", inline=False)
        await ctx.send(embed=embed3)
        print(f"{member} has been muted for {reason}")
        await member.send(embed=embed3)
        







@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    try:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        embed4 = Embed(title="User unmuted", color=0xaf1aff)
        embed4.add_field(name=f"{member}", value=f"unmuted", inline=False)
        await ctx.send(embed=embed4)
        print(f"{member} has been unmuted")
        await member.send(embed=embed4)
    except discord.Forbidden:
        await ctx.send("❌ You can not perform this command.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")



@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    try:
        await ctx.channel.purge(limit=amount)
        print(f"{amount} messages have been cleared")
        
    except discord.Forbidden:
        await ctx.send("❌ I cannot send messages to this user.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command()
async def nmap(ctx, arg):
    if ctx.author.id == ALLOWED_USER_ID:
        '''
        Used for port scanning just type .nmap with ip address which you want for example .nmap 127.0.0.1
        '''
        os_level_command_for_nmap = subprocess.run(["nmap", "-sV", "-oN", "prety.txt", f"{arg}"], capture_output=True, text=True)
    
        if os_level_command_for_nmap.returncode == 0:
            await ctx.send("Your result: \n")
            await ctx.send(file=discord.File("prety.txt"))
            print("sent")
        else:
            await ctx.send("An error occurred while running nmap.")
            print("Error running nmap:", os_level_command_for_nmap.stderr)\


#This command is credit to another repo


@bot.command()
async def ports(ctx, arg, port1, port2):
    os_level_command_for_nmap = subprocess.run(["nmap", "-p", f"{port1}-{port2}", "-oN", "Ports.txt", f"{arg}"], capture_output=True, text=True)

    if os_level_command_for_nmap.returncode == 0:
        await ctx.send("Your results: \n")
        await ctx.send(file=discord.File("Ports.txt"))
        print("Port sent")

    else:
        await ctx.send("An error occurred while searching for ports")
        print("Error", os_level_command_for_nmap)






bot.run(token)






