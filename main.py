import discord
from random import randint, choice

help_text = [open("help.txt").read()]; help_text.append(discord.Embed(title="Help", url="", description=help_text[0]))
about_text = [open("about.txt").read()]; about_text.append(discord.Embed(title="About", url="https://sidtheloser.netlify.app/", description=about_text[0]))
log_file = open("log.txt", "w").close()

TOKEN = open("SDB.txt", "r").readline()
client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} started session!")
    await client.change_presence(activity=discord.Game("good"), status=discord.Status.online)

@client.event
async def on_message(message):
    string = message.content.lower()
    if not message.author.bot:
        if string.startswith("~"):
            string = string.lstrip("~")
        
            if string.startswith("hello"):
                await message.channel.send(f"Hello {message.author}!")

            elif string.startswith("coin"):
                await message.channel.send(f"{message.author} toseed a coin and got: {choice(['heads', 'tails'])}")

            elif string.startswith("dice"):
                await message.channel.send(f"{message.author} rolled a dice and got: {randint(1, 6)}")

            elif string.startswith("about"):
                await message.channel.send(embed=about_text[1])

            elif string.startswith("say "):
                _ = (message.content.lstrip("~")).lstrip("say ")
                await message.channel.send(_)

            elif string.startswith("status "):
                await client.change_presence(activity=discord.Game(message.content.lstrip("~status ")))

            else:
                await message.channel.send(embed=help_text[1])

            print(f"{message.author}, used command {message.content}")
            log_file = open("log.txt", "a")
            log_file.write(f"{message.author}, used command {message.content}\n")
            log_file.close()

client.run(TOKEN)