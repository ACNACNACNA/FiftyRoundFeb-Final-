import discord as discord
import os
from discord.ext import commands
import prompts
import aiofile
import aiohttp
from bs4 import BeautifulSoup
import visualize

unfinished = 'Host Malone has not completed this part of me. You are free to harass him for this until I am ready.'
responseData = []
voteData = []
bot = commands.Bot(command_prefix=",")

@bot.event
async def on_ready():
    print('The image is sentient. Take caution.')

@bot.command(
    help="Use this command to look at the prompts:"
    + "\n\t    ,prompt all: Shows all the prompts. 2 hour cooldown."
    + "\n\t    ,prompt 39: Shows prompt # 39. Applies to all other prompts as well.",
    brief='This month\'s prompts'
)
async def prompt(ctx, arg1 = None):
    if arg1 == "all":
        await ctx.channel.send(file = discord.File('prompttext.txt'))
    else:
        listy = prompts.openFile("csvtest.csv")
        try:
            num = int(arg1)
            await ctx.channel.send(prompts.getPrompt(num, listy))
        except:
            await ctx.channel.send("https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
            await ctx.channel.send("Choose an actual number")


@bot.command(
    help='Use this command to respond to FRF! DM the bot the command!'
        + "\n\t ,response [number] [response]: Used to respond to Round [number]."
        + "\n\t ,response all: Coming soon. Basically get a txt file of all 50 responses in order and get em here.",
    brief='Used to respond for the month (must be used in DM\'s)'
)
async def response(ctx, arg = None, *, args=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        if arg != None:
            try:
                arg = int(arg)
                if args != None:
                    alert = []
                    alert = await prompts.getResponse(args, arg, ctx.message.author.name, str(ctx.message.author.id), "responses.csv")
                    for i in alert:
                        await ctx.channel.send(i)
                else:
                    await ctx.channel.send(
                        "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
                    await ctx.channel.send("Send a response along with the prompt selection")
            except:
                if arg == "all":
                    if ctx.message.attachments:
                        sess = aiohttp.ClientSession()
                        req = await sess.get(str(ctx.message.attachments[0]))
                        soup = BeautifulSoup(await req.read(), 'html.parser')
                        async with aiofile.AIOFile(
                                os.path.join(r"C:\Users\Anthony. N\PycharmProjects\pythonProject\venv\personalfrf.txt"),
                                'wb') as x_file:
                            await x_file.write(await req.read())
                        await sess.close()

                        dat = open(r"C:\Users\Anthony. N\PycharmProjects\pythonProject\venv\personalfrf.txt", "r")
                        person = dat.read()
                        personal = list(person.split('\n'))
                        print(personal)
                        alerts = []
                        for i in personal[:50]:
                            alertRelease = []
                            alertRelease = await prompts.getResponse(i, (personal.index(i)+1), ctx.message.author.name, str(ctx.message.author.id), "responses.csv")
                            for i in alertRelease:
                                alerts.append(i)
                        for i in alerts:
                            await ctx.channel.send(i)
                        await ctx.channel.send("Recording successful. PLEASE, PLEASE YOU **ONLY NEED TO DO THIS COMMAND ONCE.** If you wanna edit a response, just do ,response [prompt] [edited response].")
                else:
                    await ctx.channel.send(
                        "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
                    await ctx.channel.send("Choose an actual number")
        else:
            await ctx.channel.send(
                "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
            await ctx.channel.send("Select a prompt by typing the respective prompt's number before your response")
    else:
        await ctx.channel.send( "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to use this command in DMs. You don't want to reveal your response.")


@bot.command(
    help='Don\'t know what prompt you responded to? Use this command to look for your responses!'
        + "\n\t ,look [number]: Finds your response for round [number]."
        + "\n\t ,look all: Finds all your responses.",
    brief='Find your responses (must be used in DMs)'
)
async def look(ctx, arg = None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        listy = prompts.openFile("responses.csv")
        if arg != None:
            if arg == "all":
                singleData = prompts.obtainAll(listy, str(ctx.message.author.id))
                await ctx.channel.send("Your responses:")
                for row in singleData:
                    await ctx.channel.send("Response " + str(row[0]) + ": " + row[1])
            else:
                try:
                    num = int(arg)
                    if num <= 50 and num >= 1:
                        await ctx.channel.send(prompts.obtainResponse(listy, str(ctx.message.author.id), arg))
                    else:
                        prompt = "It's called :sparkles: 50 :sparkles: Round February. Not " + str(
                            num) + " Round February."
                except:
                    await ctx.channel.send(
                        "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
                    await ctx.channel.send("Choose an actual number")
        else:
            await ctx.channel.send(
                "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
            await ctx.channel.send("Pick a prompt using the prompt's number")
    else:
        await ctx.channel.send( "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to use this command in DMs. You don't want to reveal your response.")


@bot.command(
    help='Use this command to see if your responses break the prompt\'s technicals before submitting!'
        + "\n\t ,technical [number]: Does your response break the technical for round [number]?",
    brief='Technical checker (must be used in DM\'s)'
)
async def technical(ctx, arg = None, *, args = None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        try:
            if arg != None:
                arg = int(arg)
                checks = prompts.techCheck(arg, args)
                print(checks)
                for i in checks:
                    await ctx.channel.send(i)
                if checks == []:
                    await ctx.channel.send("You have not broken the rules with this response. You are freeeee...")
        except:
            await ctx.channel.send("https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
            await ctx.channel.send("Choose an actual number")
    else:
        await ctx.channel.send( "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to use this command in DMs. You don't want to reveal your response.")


@bot.command(
    help=unfinished,
    brief='Information about the month [UNDER CONSTRUCTION]'
)
async def frf(ctx):
    await ctx.channel.send( "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
    await ctx.channel.send("to be patient. The feature is not finished.")


@bot.command(
    help=unfinished,
    brief='Used to vote for the month (must be used in DM\'s) [UNDER CONSTRUCTION]'
)
async def vote(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.channel.send(
            "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to be patient. The feature is not finished.")
    else:
        await ctx.channel.send("https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to use this command in DMs. You don't want to reveal your response.")


@bot.command(
    help="Wanna see stats? Here's some real-time ones:"
         "\n\t ,graph responses: Responses per Prompt for all 50"
         "\n\t ,graph contestants: Creates a list of who has submitted and how many they responded to.",
    brief='Shows beautiful graphs [UNDER CONSTRUCTION]'
)
async def graph(ctx, arg = None):
    if arg == "responses":
        visualize.responseGraph(responseData)
        await ctx.channel.send(file = discord.File("frfresponse.png"))
    elif arg =="contestants":
        visualize.contestantGraph(responseData)
        await ctx.channel.send(file=discord.File("frfcontestants.png"))
    elif arg == "votes":
        await ctx.channel.send(
            "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to wait. This graph is unavailiable.")
    elif arg == "procrastimeter":
        await ctx.channel.send(
            "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to wait. This graph is unavailiable.")
    elif arg == "contributors":
        await ctx.channel.send(
            "https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("to wait. This graph is unavailiable.")
    else:
        await ctx.channel.send("https://media.discordapp.net/attachments/679485290934435852/935339292396494848/unknown.png")


@bot.command(
    help=unfinished,
    brief='harass - Motivates the host. Effectiveness may vary.'
)
async def harass(ctx, arg=None):
    if arg  == None:
        await ctx.channel.send("**This is Host Malone overriding the command. Do not even try to listen to this calendar. This bot wasn't even built from a full one. Do not trust the entire month of Februrary. This is your last warning.**")
    else:
        await ctx.channel.send("https://media.discordapp.net/attachments/679485290934435852/932138432787021824/Screen_Shot_2022-01-15_at_11.04.59_PM.png")
        await ctx.channel.send("wait")
        mention = f'<@!335849071430336514>'
        if arg == mention:
            for i in range(5):
                await ctx.channel.send(ctx.author.mention)

bot.run('token')


