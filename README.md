# discordMusicPlayer
# Discord Music Bot

A custom Discord music bot built using Python, `discord.py`, and `yt-dlp`. The bot allows users to play music, manage queues, control volume, and more—all through easy-to-use commands.

## Features:
- **Play music** from SoundCloud links.
- **Queue system** to add and play songs sequentially.
- **Volume control** to adjust audio levels.
- **Pause, resume, skip** commands for managing playback.
- **Search for songs** on SoundCloud and add them to the queue.
- **Display the current song queue** with song names.

## Installation

Follow these steps to get the bot up and running:

### Prerequisites:
1. **Python 3.8+**: Make sure you have Python 3.8 or higher installed.
2. **Dependencies**: The bot uses the following Python libraries:
   - `discord.py` (for interacting with Discord)
   - `yt-dlp` (for downloading audio from SoundCloud)
   - `ffmpeg` (for handling audio playback)
### downloading the bot
    go to the releases page and download the main python file.
    see the steps under ehre to set it up
    
### Setting up Your Discord Bot:

1. **Create a new bot on Discord**:
    - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
    - Click **New Application**.
    - Give your application a name (e.g., `Discord Music Bot`).
    - Click **Create**.
    
2. **Create a Bot User**:
    - In the left sidebar, click on **Bot**.
    - Click **Add Bot** and confirm by clicking **Yes, do it!**.
    - Under the **TOKEN** section, click **Copy** to copy your bot's token. You'll need this to connect the bot to your Discord server. **Keep it secret** and do not share it publicly.

3. **Enable Intents**:
    Your bot needs specific intents to read messages and join/leave voice channels. Follow these steps to enable the necessary intents:

    - In the Discord Developer Portal, go to your application and click on **Bot** in the left sidebar.
    - Scroll down to the **Privileged Gateway Intents** section.
    - Enable the following intents:
        - **MESSAGE CONTENT INTENT** – Required to read the contents of messages (important for music commands).
        - **SERVER MEMBERS INTENT** – If you want your bot to know when users join or leave the server.
        - **PRESENCE INTENT** – If you need the bot to track user presence (e.g., when they are streaming music).
    - Save changes after enabling the intents.

4. **Invite the Bot to Your Server**:
    - In the left sidebar, click on **OAuth2**.
    - Under **OAuth2 URL Generator**, select `bot` in the **SCOPES** section.
    - In the **BOT PERMISSIONS** section, select the following permissions to allow the bot to perform its music functions:
        - **Read Messages** – Required to read messages in the text channels.
        - **Send Messages** – Required to send messages in text channels.
        - **Connect** – Required to connect to voice channels.
        - **Speak** – Required to play audio in voice channels.
        - **Use Voice Activity** – Allows the bot to listen to voice activity and interact with the channel.
    - Copy the generated URL, paste it in your browser, and select the server you want to invite the bot to.

5. **Add the Token to Your Bot's Code**:
     open the code file.
     scroll to the bottom of the code where you see TOKEN_HERE. remove the text and place your bot token there that you got from the discord developer portal
