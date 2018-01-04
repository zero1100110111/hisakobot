import asyncio
import datetime
import operator
import random
import sys
import time
import urllib.request, json

import discord
from discord.ext import commands

description = '''contact @Ameyuri#9271 for help'''

# specifies what extensions to load when the bot starts up
startup_extensions = ['waralert']

bot = commands.Bot(command_prefix = "\\", description = description)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game = discord.Game(name = 'with Ame'))

@bot.command(pass_context = True)
async def shh(ctx):
    '''Kill switch.'''
    if ctx.message.author.id != "250785445087150080":
        await bot.say("Insufficient permissions.")
        return
    await bot.say('`[ hisako is going to sleep ]`')
    await bot.logout()
    sys.exit()

@bot.command(pass_context = True)
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("**{}** loaded.".format(extension_name))

@bot.command(pass_context = True)
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("**{}** unloaded.".format(extension_name))

@bot.command(pass_context = True)
async def reload(ctx, extension_name : str):
    """Reloads an extension."""
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("**{}** reloaded.".format(extension_name))

#-----------------------------------------

@bot.event
async def on_member_join(member):
    embed = discord.Embed(description = member.mention + " " + member.name + "#" + str(member.discriminator), timestamp = datetime.datetime.now(), color = discord.Colour.green())
    embed.set_author(name = 'Member joined!', icon_url = member.avatar_url)
    await bot.send_message(discord.Object(id = "354837682653757440"), embed = embed)

#-----------------------------------------

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    with open('bottoken.txt', 'r') as f:
        token = f.read()
        bot.run(token)
