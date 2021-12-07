import discord
from random import randint, choice
from json import load, dump

help_text = discord.Embed(title="Help", url="", description=open("help.txt").read())
about_text = discord.Embed(title="About", url="https://sidtheloser.netlify.app/", description=open("about.txt").read())
log_file = open("log.txt", "w").close()
status = open("status.txt", encoding="utf-8").readline()
game_data = load(open("game.json"))

TOKEN = open("SDB.txt", "r").readline()
client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} started session!")
    await client.change_presence(activity=discord.Game(status), status=discord.Status.online)

@client.event
async def on_message(message):
    global game_data
    string = message.content.lower()
    if not message.author.bot:
        if string.startswith("~"):
            string = string.lstrip("~")
        
            if string.startswith("hello"):
                await message.channel.send(f"Hello {message.author.name}!")

            elif string.startswith("coin"):
                await message.channel.send(f"{message.author.name} toseed a coin and got: {choice(['heads', 'tails'])}")

            elif string.startswith("dice"):
                await message.channel.send(f"{message.author.name} rolled a dice and got: {randint(1, 6)}")

            elif string.startswith("about"):
                await message.channel.send(embed=about_text)

            elif string.startswith("say "):
                await message.channel.send(message.content.lstrip("~say "))

            elif string.startswith("status "):
                await client.change_presence(activity=discord.Game(message.content.lstrip("~status ")))
                _ = open("status.txt", "w", encoding="utf-8"); _.write(message.content.lstrip("~status ")); _.close; del _
                await message.channel.send(f"{message.author.name} changed the status of the bot to: {message.content.lstrip('~status ')}")
            
            elif string.startswith("mine"):
                if not str(message.author.id) in game_data:
                    await message.channel.send("As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a million chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = 0
                if randint(1, 1000000) == 1:
                    game_data[str(message.author.id)] += 1
                    await message.channel.send("Congratulations, you just got a coin!")
                else:
                    await message.channel.send("So sed, you got nothin.")

            elif string.startswith("bal"):
                if not str(message.author.id) in game_data:
                    await message.channel.send("As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a million chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = 0
                
                await message.channel.send(f"{message.author.name}'s wallet has: {game_data[str(message.author.id)]} coins.")

            else:
                await message.channel.send(embed=help_text)

            print(f"{message.author}, used command {message.content}")
            log_file = open("log.txt", "a", encoding="utf-8")
            log_file.write(f"{message.author}, used command {message.content}\n")
            log_file.close()
            dump(game_data, open("game.json", "w"))

client.run(TOKEN)
