import discord
import requests
import asyncio
import os

TOKEN = os.environ["REALTOKEN"]
CHANNEL_ID = 1279592030120579085  # Replace with your channel ID

client = discord.Client(intents=discord.Intents.all())

# URL to check the Roblox client version
VERSION_URL = 'https://clientsettings.roblox.com/v2/client-version/WindowsPlayer'
CHECK_INTERVAL = 5  # Check every 60 seconds

# Store the latest version to compare with new ones
last_version = None

# Function to fetch the current Roblox version
async def get_roblox_version():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            version_info = response.json()
            return version_info.get("clientVersionUpload")
        else:
            print("Failed to get version:", response.status_code)
    except Exception as e:
        print("Error fetching version:", e)
    return None

# Function to check for version updates
async def check_for_updates():
    global last_version
    while True:
        new_version = await get_roblox_version()

        if new_version is not None and new_version != last_version:
            last_version = new_version

            # Send an embed message to Discord when a new version is detected
            channel = client.get_channel(CHANNEL_ID)

            # Create an embed for the update notification
            embed = discord.Embed(
                title="🚨 Roblox Update Detected!",
                description=f"A new Roblox client version has been released: **{new_version}**",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/roblox/images/1/14/Roblox_icon.png")  # Roblox Icon
            embed.add_field(name="Version", value=new_version, inline=False)
            embed.set_footer(text="Developed by hex000001")

            # Send the embed to the Discord channel
            await channel.send(embed=embed)
            print(f'Roblox updated to version: {new_version}')
        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await check_for_updates()

# Start the bot
client.run(TOKEN)
