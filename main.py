import discord
from random import randint, choice
from json import load, dump

propability = 10
help_text = f'''
--Classic--

"~hello" for a hello message.
"~coin" to toss a coin.
"~dice" to roll a dice.
"~about" to know more about the developer of this dumb bot.
"~help" to show this message again.

"~say <text to say>" to make the bot say.
"~status <status text>" to change the status..

--Game Related--

"~mine" to mine for coins, getting from 0 to {propability} amount of coin.
"~bal" to show your wallet balance.

"~rob <mention>" to rob people mentioned..
"~gift <mention> <amount>" to gift other people with your money.
'''

about_text = """
This is SDB, full name, Sid's Dumb Bot.
As expected, this bot is made by an idiot named Sid.
Thats it...yeah...thats all about this bot.

https://github.com/sid-the-loser/sdb
"""

help_text = discord.Embed(title="Help", url="", description=help_text)
about_text = discord.Embed(title="About", url="https://sidtheloser.netlify.app/", description=about_text)
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
                    await message.channel.send(f"As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a {propability} chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = {"money": 0}
                _ = randint(0, propability)
                game_data[str(message.author.id)]["money"] += _
                await message.channel.send(f"Congratulations, you just got {_} coins!")

            elif string.startswith("bal"):
                if not str(message.author.id) in game_data:
                    await message.channel.send(f"As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a {propability} chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = {"money": 0}
                
                await message.channel.send(f"{message.author.name}'s wallet has: {game_data[str(message.author.id)]['money']} coins.")

            elif string.startswith("rob "):
                if not str(message.author.id) in game_data:
                    await message.channel.send(f"As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a {propability} chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = {"money": 0}
                __ = message.content.lstrip("~rob")
                _ = ""

                for i in range(len(__)):
                    if __[i] == " ":
                        pass
                    else:
                        _ += __[i]


                if _.startswith("<@") and _.endswith(">"):
                    _ = _[2:len(_)-1]
                    _ = _.lstrip("!")

                    if _ in game_data:
                        if game_data[_]["money"] > 0:
                            money_lost = randint(1, game_data[_]["money"])
                            game_data[_]["money"] -= money_lost
                            game_data[str(message.author.id)]["money"] += money_lost
                            await message.channel.send(f"{message.content.lstrip('~rob ')} was robbed by {message.author.name}! Robbed {money_lost} coins!")
                        else:
                            await message.channel.send(f"{message.content.lstrip('~rob ')} is too poor for that!")

                    else:
                        await message.channel.send(f"{message.content.lstrip('~rob ')} doesnot have a SDB account!")

                else:
                    await message.channel.send(f"{message.content.lstrip('~rob ')} is not refering to any one person!")

            elif string.startswith("gift "):
                if not str(message.author.id) in game_data:
                    await message.channel.send("As you are playing this game for the first time, let me explain what you are gonna get. This is a game about mining coins and you have 1 in a million chance of getting a coin. The more the coins you have, the more you can show off.")
                    game_data[str(message.author.id)] = {"money": 0}
                    
                _ = message.content.split(" ")

                while True:
                    try:
                        for i in range(len(_)):
                            if _[i] == "":
                                del _[i]

                        break
                    except IndexError:
                        pass

                if _[1].startswith("<@") and _[1].endswith(">"):
                    _[1] = _[1][2:len(_[1])-1]
                    _[1] = _[1].lstrip("!")
                    _[2] = int(_[2])

                    if _[1] in game_data:
                        if game_data[str(message.author.id)]["money"] >= _[2]:
                            game_data[str(message.author.id)]["money"] -= _[2]
                            game_data[_[1]]["money"] += _[2]
                            await message.channel.send(f"{message.author.name} send {_[2]} coins to {message.content.split(' ')[1]}")
                        else:
                            await message.channel.send("Not enough balance!")
                    else:
                        await message.channel.send(f"{message.content.split(' ')[1]} doesnot have a SDB account!")
                
                else:
                    await message.channel.send(f"{message.content.split(' ')[1]} is not refering to any one person!")

            else:
                await message.channel.send(embed=help_text)

            print(f"{message.author}, used command {message.content}")
            log_file = open("log.txt", "a", encoding="utf-8")
            log_file.write(f"{message.author}, used command {message.content}\n")
            log_file.close()
            dump(game_data, open("game.json", "w"))

client.run(TOKEN)
