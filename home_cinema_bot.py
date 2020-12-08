from discord.ext import commands
import discord
from os import listdir
from os.path import isfile, join
import time, random, sys

pass_file = open("pass.pass", "r")

TOKEN = ""

for line in pass_file:
    TOKEN = line

bot = commands.Bot(command_prefix='$')

scripts_path = "movie_scripts"

movie_scripts = [f for f in listdir(scripts_path) if isfile(join(scripts_path, f))]

scripts = {}

scripts_running = {}

spamming_emotes = {}

emotes = ["kekw", "pepega", "sadge", "peepohappy", "monkaW", "ELIMINAR",
          "pufavo", "pogchamp", "weirdchamp", "homies", "FeelsStrongMan",
          "5head", "bruh", "caragomeu", "ehehe", "mds", "facho"]


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="fuckyou", help="fuck you")
async def fuck_you(ctx):
    print("running: fuckyou")
    await ctx.send("thats why")


@bot.command(name="yomamasofat", help="lol")
async def yomamasofat(ctx):
    print("running: yomamasofat")
    await ctx.send("lol, no u")


@bot.command(name="poke", help="be a annoying prick, poke a member >:)")
async def poke(ctx, member: discord.Member):
    print("running: poke")
   
    the_message = ctx.message

    await ctx.send(member.mention)

    if(the_message):
        await the_message.delete()


@bot.command(name="clear", help="clears the last 10 messages", hidden=True)
async def clear(ctx, the_limit=100):
    print("running: clear")
    the_message: discord.Message = ctx.message

    if(the_message):
        await the_message.delete()

    the_channel = ctx.channel

    the_commands = list(map(lambda x: bot.command_prefix + x.name, bot.commands))

    if(the_channel):
        async for message in the_channel.history(limit=the_limit):
            if message.author.name == "Spam Bot" or message.content in the_commands:
                await message.delete()
            else:
                for command in the_commands:
                    if(message.content.startswith(command)):
                        await message.delete()
                        break


@bot.command(name="spam_emote", help="Spams emotes continualsy (or a specified number of times) or one particular emote specified by the user")
async def spam_emote(ctx, emote_name: str = "no emote", num_times: int = -1):
    print("running: spam_emote")
    the_message: discord.Message = ctx.message

    if(the_message):
        await the_message.delete()

    the_guild = ctx.guild

    if(the_guild):
        if(the_guild not in spamming_emotes or not spamming_emotes[the_guild]):
            spamming_emotes[the_guild] = True
        else:
            if(spamming_emotes[the_guild]):
                await ctx.send(f"***Already spamming emotes {ctx.author.mention}!***")
                return

    if(num_times <= -1):
        while spamming_emotes[the_guild]:
            emote = emote_name
            if(emote_name == "no emote"):
                emote = random.choice(emotes)
            else:
                pass

            emoji = discord.utils.get(bot.emojis, name=emote)
            await ctx.send(str(emoji) if emoji else f"No emote with name {emote} found")
    else:
        for i in range(num_times):
            emote = emote_name
            if(emote_name == "no emote"):
                emote = random.choice(emotes)
            else:
                pass

            emoji = discord.utils.get(bot.emojis, name=emote)
            await ctx.send(str(emoji) if emoji is not None else f"No emote with name {emote} found")
            spamming_emotes[the_guild] = False


@bot.command(name='read_movie', help="Starts writing the movie script, line by line")
async def read_movie(ctx, movie_name: str):
    print("running: read_movie")
    the_guild = ctx.guild

    if(the_guild):
        if(the_guild not in scripts_running or not scripts_running[the_guild]):
            scripts_running[the_guild] = True
        else:
            if(scripts_running[the_guild]):
                await ctx.send(f"***Already writing movie script {ctx.author.mention}!***")
                return

    print("Not currently writing movie in guild, beginning to do so!")

    if(movie_name == ""):
        await ctx.send("You need to provide a movie to display!!")
        scripts_running[the_guild] = False
        return

    movie = (movie_name + ".txt")

    if(movie not in movie_scripts):
        await ctx.send("You need to provide an existing movie to display!!")
        scripts_running[the_guild] = False
        return

    print("Valid movie name given")

    movie_file = open("movie_scripts/" + movie, "r")

    script = []

    num_lines_read = 0
    for line in movie_file:
        num_lines_read += 1
        script.append(line)

    print("Read", num_lines_read, "lines")

    print("Finished reading movie file!")

    if(the_guild):
        if(the_guild not in scripts):
            scripts[the_guild] = script

    print("Putting movie in scripts dict, beginning to write lines")

    if(len(script) > 0):
        if(the_guild):
            for line in scripts[the_guild]:
                if(line != ""):
                    await ctx.send(line)
                    time.sleep(1)
    else:
    	print("No movie read!!!!")
            
    print("Finnished writing movie!")
            
    scripts_running[the_guild] = False


@bot.command(name="speak_movie", help="NOT WORKING-Joins a voice channel and starts reading the given movie")
async def speak_movie(ctx, movie_name: str):
    print("running: speak_movie")
    if(True):
        await ctx.send("NOT CURRENTLY WORKING")
        return

    the_guild = ctx.guild

    if(the_guild):
        if(the_guild not in scripts_running.keys):
            scripts_running[the_guild] = True
        else:
            if(scripts_running[the_guild]):
                await ctx.send(f"***Already writing movie script {ctx.author.mention}!***")
                return

    if(movie_name == ""):
        await ctx.send("You need to provide a movie to speak!!")
        return

    connected = ctx.author.voice

    if not connected:
        await ctx.send("You need to be connected in a voice channel to use this command!")
        return

    vc = await connected.channel.connect()

    movie = (movie_name + ".txt")

    if(movie not in movie_scripts):
        await ctx.send("You need to provide an existing movie to speak!!")
        return

    movie_file = open("movie_scripts/" + movie, "r")

    script = []

    for line in movie_file:
        script.append(line)

    for line in script:
        await ctx.send(line)
        time.sleep(1)

    await vc.disconnect()


@bot.command(name="stop", help="Stops the bot from reading the movie script or spamming emotes, defaults to movies")
async def stop(ctx, spam_type="movie"):
    print("running: stop")
    the_guild = ctx.guild

    if(the_guild):
        if(spam_type == "movie"):
            if(the_guild not in scripts_running or not scripts_running[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(scripts_running[the_guild]):
                    scripts[the_guild].clear()
                    await ctx.send("Stoping movie script playback")
                    scripts_running[the_guild] = False
                    del scripts[the_guild]
        elif(spam_type == "emote"):
            if(the_guild not in spamming_emotes or not spamming_emotes[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(spamming_emotes[the_guild]):
                    await ctx.send("Stoping emote spam playback")
                    spamming_emotes[the_guild] = False


@bot.event
async def on_command_error(ctx, error):
    print("ERROR", error, type(error))
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command doesn't currently exist!")

bot.run(TOKEN)
