import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
from discord import opus
import random
import json

intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

bot = commands.Bot(command_prefix=':', intents=intents)

# Music-related variables
song_queue = []
current_playlist = {}  # To store custom playlists

# Load Opus library (update path if necessary)
opus.load_opus("/opt/homebrew/Cellar/opus/1.5.2/lib/libopus.0.dylib")


# Helper function to add a song to the queue
async def add_to_queue(url, ctx):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        song = {
            'title': info['title'],
            'url': info['url']
        }
    song_queue.append(song)
    return song


# Join VC Command
@bot.command()
async def join(ctx, *, channel_name: str = "music"):
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
    if channel:
        await channel.connect()
        await ctx.send(f"Joined the '{channel.name}' voice channel!")
    else:
        await ctx.send(f"Could not find a voice channel named '{channel_name}'. Please make sure it exists.")


# Play music from SoundCloud link
@bot.command()
async def play(ctx, url: str):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel. Use :join <channel_name> first!")
        return

    song = await add_to_queue(url, ctx)

    # Play the audio with FFmpeg
    voice_client = ctx.voice_client
    voice_client.play(discord.FFmpegPCMAudio(song['url']))
    await ctx.send(f"Now playing: {song['title']}")


# Pause music
@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("No music is currently playing.")


# Resume music
@bot.command()
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Music resumed.")
    else:
        await ctx.send("No music is paused.")


# Skip to next track (or stop if no queue)
@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipping current track.")
    else:
        await ctx.send("No music is currently playing.")


# Skip to a specific track command
@bot.command()
async def skipto(ctx, index: int):
    if 0 < index <= len(song_queue):
        song = song_queue.pop(index - 1)
        voice_client = ctx.voice_client
        voice_client.stop()
        await ctx.send(f"Skipped to: {song['title']}")
    else:
        await ctx.send("Invalid track index.")


# View current song queue
@bot.command()
async def queue(ctx):
    if not song_queue:
        await ctx.send("The queue is currently empty.")
    else:
        queue_message = "Current queue:\n"
        for idx, song in enumerate(song_queue):
            queue_message += f"{idx + 1}. {song['title']}\n"
        await ctx.send(queue_message)

# Clear the queue
@bot.command()
async def clearqueue(ctx):
    song_queue.clear()
    await ctx.send("The queue has been cleared.")


# Set volume control
@bot.command()
async def volume(ctx, level: float):
    if 0.0 <= level <= 1.0:
        voice_client = ctx.voice_client
        voice_client.source.volume = level
        await ctx.send(f"Volume set to {level * 100}%")
    else:
        await ctx.send("Volume must be between 0.0 and 1.0.")


# Seek to specific time
@bot.command()
async def seek(ctx, time: str):
    try:
        minutes, seconds = map(int, time.split(":"))
        total_seconds = minutes * 60 + seconds
        voice_client = ctx.voice_client
        voice_client.play(discord.FFmpegPCMAudio(song_queue[0]['url'], options=f'-ss {total_seconds}'))
        await ctx.send(f"Jumped to {time}.")
    except ValueError:
        await ctx.send("Invalid time format. Use mm:ss.")


# Song info command
@bot.command()
async def songinfo(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await ctx.send("No music is currently playing.")
    else:
        song = song_queue[0]
        await ctx.send(f"Now playing: {song['title']}")


# Search for music
# Search for music on SoundCloud
@bot.command()
async def search(ctx, *, query: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'noplaylist': True,
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Search SoundCloud for the query
        info = ydl.extract_info(f"scsearch:{query}", download=False)
        if 'entries' in info:
            song = info['entries'][0]
            url2 = song['url']
            await add_to_queue(url2, ctx)
            await ctx.send(f"Added {song['title']} to the queue.")
        else:
            await ctx.send("No results found on SoundCloud.")


# Shuffle the queue
@bot.command()
async def shuffle(ctx):
    if not song_queue:
        await ctx.send("The queue is empty.")
    else:
        random.shuffle(song_queue)
        await ctx.send("The queue has been shuffled.")


# Create a custom playlist
@bot.command()
async def createplaylist(ctx, playlist_name: str):
    if playlist_name not in current_playlist:
        current_playlist[playlist_name] = []
        await ctx.send(f"Playlist '{playlist_name}' has been created.")
    else:
        await ctx.send(f"Playlist '{playlist_name}' already exists.")


# Add a song to a custom playlist
@bot.command()
async def addtoplaylist(ctx, playlist_name: str, url: str):
    if playlist_name not in current_playlist:
        await ctx.send(f"Playlist '{playlist_name}' does not exist.")
    else:
        song = await add_to_queue(url, ctx)
        current_playlist[playlist_name].append(song)
        await ctx.send(f"Added {song['title']} to playlist '{playlist_name}'.")


# Play a custom playlist
@bot.command()
async def playplaylist(ctx, playlist_name: str):
    if playlist_name not in current_playlist:
        await ctx.send(f"Playlist '{playlist_name}' does not exist.")
    else:
        for song in current_playlist[playlist_name]:
            song_queue.append(song)
        await ctx.send(f"Now playing playlist: '{playlist_name}'.")


# Leave VC
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

# Play songs in the queue
@bot.command()
async def playqueue(ctx):
    if not song_queue:
        await ctx.send("The queue is empty.")
        return

    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel. Use :join <channel_name> first!")
        return

    voice_client = ctx.voice_client

    # Play the first song
    song = song_queue.pop(0)
    voice_client.play(discord.FFmpegPCMAudio(song['url']), after=lambda e: play_next_song(ctx))

    # Send a message indicating the song is playing
    await ctx.send(f"Now playing: {song['title']}")

# Helper function to play the next song in the queue
def play_next_song(ctx):
    if song_queue:
        next_song = song_queue.pop(0)
        ctx.voice_client.play(discord.FFmpegPCMAudio(next_song['url']), after=lambda e: play_next_song(ctx))
        ctx.send(f"Now playing: {next_song['title']}")
    else:
        ctx.send("The queue is empty.")


# Run the bot
bot.run('TOKEN_HERE')  # Replace with your actual bot token
