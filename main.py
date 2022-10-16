from game import Game
from utils import *

from discord.ext import commands
import discord

TOKEN = 'your_token_goes_here'
command_prefix = '%'

bot = commands.Bot(command_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='argstest', help='I used this to test getting arguments from command')
async def argstest(ctx: commands.context.Context, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

@bot.command(name='rungame', help='Launches a dungeon game')
async def rungame(ctx: commands.context.Context):
    game = Game()
    await game.start(ctx)

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx: commands.context.Context):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx: commands.context.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Plays music from youtube url')
async def play(ctx: commands.context.Context, url: str, volume: str):
    await ctx.send("Getting everything ready")
    print("Someone wants to play music let me get that ready for them...")

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    music_title = check_music_title(url)
    music_exists = check_if_music_exists(music_title)

    if not music_exists:
        message = await ctx.send('The song that you want to play isn\'t downloaded yet. Do you want to download it?')
        await message.add_reaction('✅')
        await message.add_reaction('❎')
        
        has_reacted = False
        while not has_reacted:
            try:
                has_reacted = await check_reaction(message, reactions=['✅', '❎'])
            except discord.NotFound or discord.HTTPException:
                await ctx.send('An error occured and we can\'t continue, sorry')
        
        await message.delete()
        await ctx.send('The download started. The time that it takes will depend on the lenght of the video')

        await run_blocking(bot, download_mp3_from_youtube_url, url=url)

        await ctx.send('The download finished.')
    
    await ctx.send('Now playing music. If the bot isn\'t playing any music please report it to the mods')
    
    await play_music(voice, music_title, int(volume))

@bot.command(name='stop', help='Stops the song')
async def stop(ctx: commands.context.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

if __name__ == '__main__':
    bot.run(TOKEN)

# Invite link
# https://discord.com/api/oauth2/authorize?client_id=1025819101324640417&permissions=8&scope=bot
