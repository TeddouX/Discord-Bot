from discord.ext import commands
import discord
import functools
import typing
import youtube_dl
import os

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './downloadedsongs/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

async def check_reaction(message: discord.message.Message, reactions: list) -> bool:
    updated_message = await message.channel.fetch_message(message.id)
    has_reacted = False
    for i in updated_message.reactions:
        if i.count >= 2 and i.emoji in reactions:
            has_reacted = True
            return has_reacted
        else:
            return has_reacted

async def play_music(voice: discord.VoiceProtocol, name: str, volume: int):
    voice.play(discord.FFmpegPCMAudio(executable='./_FFmpeg/bin/ffmpeg.exe', source=f"./downloadedsongs/{name}.mp3"))
    print(f'{name} is now playing')
    voice.volume = volume
    voice.is_playing()

def check_if_music_exists(name: str) -> bool:
    return os.path.exists(f'./downloadedsongs/{name}.mp3')

def check_music_title(url: str):
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return info['title']

def download_mp3_from_youtube_url(url: str) -> None:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def run_blocking(bot: commands.bot.Bot, blocking_func: typing.AsyncGenerator, *args, **kwargs) -> None:
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await bot.loop.run_in_executor(None, func)
