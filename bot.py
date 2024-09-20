# bot.py
import discord
import random
from config import TOKEN
from games.sudoku import SudokuGame
from discord.ext import commands
import asyncio
import aiohttp
import googlePhotosAPI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import aiohttp
from games.sudoku import sudoku10


# Scopes needed for Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.appendonly']

creds = None

## google api, getting the token.json for authentication ready.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # required to read messages

client = commands.Bot(command_prefix='s.', intents=intents, help_command=None)

# on ready, first executed when the bot goes online.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# On message for googlePhotosAPI, whenever a message is sent, this function checks if it is an image mentioned and whether to upload it or not.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.channel) == 'pictures':
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'heic', 'mov', 'mp4', 'avi')):
                    image_url = attachment.url
                    guild = message.guild
                    if guild.name == "Transfer Orientation 363":
                        await googlePhotosAPI.download_and_upload_to_google_photos(image_url, 'Orientation 2024')
                    elif guild.name == "Orientation Group 368":
                        await googlePhotosAPI.download_and_upload_to_google_photos(image_url, 'Freshman Orientation 2024')
                    else:
                        await googlePhotosAPI.download_and_upload_to_google_photos(image_url, 'Saiborg test')
                    response = "File has been uploaded to the album!"
                    embed = discord.Embed(title = response)
                    await message.channel.send(embed = embed)

    await client.process_commands(message)

@client.command()
async def link(ctx):
    #send them the album link
    guild = ctx.guild
    if guild.name == "Orientation Group 368":
        em = discord.Embed(title="Album link", description="https://photos.app.goo.gl/R4qjPTbT5VAqwgGq7")
    elif guild.name == "Trasfer Group 363":
        em = discord.Embed(title="Album link", description="https://photos.app.goo.gl/dCS4yWQ1ZZmKKwGS9")
    else:
        em = discord.Embed(title="Album link", description="https://photos.app.goo.gl/d2XZH2bSaU7M87tPA")
    
    await ctx.send(embed=em)



@client.command()
async def help(ctx):
    # display a help message with available commands.
    em = discord.Embed(title="Help", description="List of commands")
    commands_list = [
        ("s.help", "Shows this message"),
        ("s.link", "Sends the link to the shared pictures album"),
        ("s.singlesudoku", "Starts a single player 4x4 Sudoku game\nCommands: \ns.endsudoku: ends the game. \ns.placenum <row> <col> <number>: places a number on [row, col] of the board. \ns.removenum <row> <col>: removes the number on [row, col] of the board.\nThis is single player 4x4 sudoku game."),
        ("s.multisudoku", "Starts a 9x9 multiplayer Sudoku game\nCommands: \ns.end: ends the game. \ns.place <row> <col> <number>: places a number on [row, col] of the board. \ns.remove <row> <col>: removes the number on [row, col] of the board.\nThis is 9x9 multiplayer sudoku that requires teamwork and coordination! It is difficult but really interesting.")
    ]

    for command, desc in commands_list:
        em.add_field(name=command, value=f"```{desc}```", inline=False)

    em.set_footer(text="Created by Sai")
    await ctx.send(embed=em)

## GAME OF SUDOKU: (4X4) 
sudoku_game = SudokuGame(SudokuGame.load_initial_boards())

@client.command()
async def singlesudoku(ctx):
    response = await sudoku_game.start_game(ctx.author.id)
    if len(response) <= 256:
        embed = discord.Embed(title = response)
    else:
        embed = discord.Embed(description = response)
    await ctx.send(embed = embed)

@client.command()
async def endsudoku(ctx):
    response = await sudoku_game.end_game(ctx.author.id)
    embed = discord.Embed(title = response)
    await ctx.send(embed = embed)

@client.command()
async def placenum(ctx, row: int, col: int, number: int):
    response = await sudoku_game.placenum(ctx.author.id, row, col, number)
    if len(response) > 256:
        embed = discord.Embed(description=response)
    else:
        embed = discord.Embed(title=response)
    await ctx.send(embed = embed)

@client.command()
async def removenum(ctx, row: int, col: int):
    response = await sudoku_game.removenum(ctx.author.id, row, col)
    if len(response) > 256:
        embed = discord.Embed(description=response)
    else:
        embed = discord.Embed(title=response)
    await ctx.send(embed = embed)

# GAME OF SUDOKU 9x9
sudoku_9x9 = sudoku10(sudoku10.load_initial_boards_9())

@client.command()
async def multisudoku(ctx):
    response = await sudoku_9x9.start_game(ctx.channel.id)
    embed = discord.Embed(description = response)
    await ctx.send(embed = embed)

@client.command()
async def end(ctx):
    response = await sudoku_9x9.end_game(ctx.channel.id)
    embed = discord.Embed(description=response)
    await ctx.send(embed = embed)

@client.command()
async def place(ctx, row: int, col: int, number: int):
    response = await sudoku_9x9.placenum(ctx.channel.id, row, col, number)
    embed = discord.Embed(description=response)

    await ctx.send(embed = embed)

@client.command()
async def remove(ctx, row: int, col: int):
    response = await sudoku_9x9.removenum(ctx.channel.id, row, col)
    embed = discord.Embed(description=response)
    await ctx.send(embed = embed)

@client.event
async def on_command_error(ctx, error):
    response = f"{str(error)}\nType `s.help` for help."
    if len(response) > 256:
        embed = discord.Embed(description=response)
    else:
        embed = discord.Embed(title=response)
    await ctx.send(embed = embed)



client.run(TOKEN)