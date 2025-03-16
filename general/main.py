import discord
import json
import os
import subprocess
import colorama
from flask import Flask
from threading import Thread
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"
os.environ["PATH"] += os.pathsep + "/usr/local/bin"


def run():
    app.run(host="0.0.0.0", port=5000)

Thread(target=run).start()

with open('config.json') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]

colorama.init()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=intents)

ALLOWED_USER_ID = 1344966239667224604

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help"))

@bot.tree.command(name="help", description="Help with commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", color=0xaf1aff)
    embed.add_field(name="/ban", value="Bans a user", inline=False)
    embed.add_field(name="/kick", value="Kicks a user", inline=False)
    embed.add_field(name="/mute", value="Mutes a user", inline=False)
    embed.add_field(name="/unmute", value="Unmutes a user", inline=False)
    embed.add_field(name="/purge", value="Clears messages", inline=False)
    embed.add_field(name="/dm", value="DMs a user", inline=False)
    embed.add_field(name="/unban", value="Unbans a user", inline=False)
    embed.add_field9(name="/serverinfo", value="Shows server details", inline=False)
    embed.add_field(name="/userinfo", value="Shows user info", inline=False)
    embed.add_field(name="/role", value="Assigns a role to a user", inline=False)
    embed.add_field(name="/removerole", value="Removes a role from a user", inline=False)
    embed.add_field(name="/coinflip", value="Flips a coin", inline=False)
    embed.add_field(name="/roll", value="Rolls a dice", inline=False)
    embed.add_field(name=".nmap {ip}", value="get basic info about an ip", inline=False)
    embed.add_field(name=".ports {ip} {port1} {port2}", value="get info about ports within a range",inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Shows server details")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, color=0xaf1aff)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="Shows user details")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}'s Info", color=0xaf1aff)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles]), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="role", description="Assigns a role to a user")
@commands.has_permissions(manage_roles=True)
async def role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await interaction.response.send_message(f"{member.name} has been given the role {role.name}.")

@bot.tree.command(name="removerole", description="Removes a role from a user")
@commands.has_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f"{role.name} role has been removed from {member.name}.")

@bot.tree.command(name="coinflip", description="Flips a coin")
async def coinflip(interaction: discord.Interaction):
    import random
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"The coin landed on: {result}")

@bot.tree.command(name="roll", description="Rolls a dice")
async def roll(interaction: discord.Interaction, sides: int = 6):
    import random
    result = random.randint(1, sides)
    await interaction.response.send_message(f"You rolled a {result} on a {sides}-sided dice.")



@bot.tree.command(name="ban", description="Bans a user")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    embed = discord.Embed(title="User Banned", color=0xaf1aff)
    embed.add_field(name=f"{member}", value=f"Banned for {reason}", inline=False)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="unban", description="Unbans a user")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, member_name: str):
    async for ban_entry in interaction.guild.bans():
        user = ban_entry.user
        if user.name.lower() == member_name.lower():
            await interaction.guild.unban(user)
            embed = discord.Embed(title="User Unbanned", color=0xaf1aff)
            embed.add_field(name=f"{member_name}", value="Unbanned", inline=False)
            await interaction.response.send_message(embed=embed)
            return
    await interaction.response.send_message(f"❌ Cannot find `{member_name}` in the ban list.")



@bot.tree.command(name="kick", description="Kicks a user")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=reason)
    embed = discord.Embed(title="User Kicked", color=0xaf1aff)
    embed.add_field(name=f"{member}", value=f"Kicked for {reason}", inline=False)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="mute", description="Mutes a user")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    duration_seconds = duration * 60  
    timeout_until = discord.utils.utcnow() + timedelta(seconds=duration_seconds)
    await member.timeout(timeout_until, reason=reason)
    embed = discord.Embed(title="User Muted", color=0xaf1aff)
    embed.add_field(name=f"{member}", value=f"Muted for {duration} minutes. Reason: {reason}", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="unmute", description="Unmutes a user")
@app_commands.checks.has_permissions(moderate_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)  
    embed = discord.Embed(title="User Unmuted", color=0xaf1aff)
    embed.add_field(name=f"{member}", value="Unmuted successfully.", inline=False)
    await interaction.response.send_message(embed=embed)





@bot.tree.command(name="purge", description="Clears messages")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{amount} messages deleted successfully", ephemeral=True)
    




@bot.tree.command(name="dm", description="DMs a user")
@app_commands.checks.has_permissions(manage_messages=True)
async def dm(interaction: discord.Interaction, user: discord.Member, message: str):
    await user.send(message)
    await interaction.response.send_message(f"Sent message to {user.name}", ephemeral=True)






bot.run(TOKEN)
