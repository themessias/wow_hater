import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}'.format(bot))

async def kickMember(member, param):
    channel = bot.get_channel(931670261089071125)
    for activity in member.activities:
            if "world of warcraft" in activity.name.lower():
                try:
                    print("entrou")
                    await channel.send("O membro "+member.name+" foi expulso do"
                    +"servidor. Motivo: **jogando wow**")
                    await member.send("https://discord.gg/6gegE4X6Kg")
                    await member.kick(reason='Jogando WOW')
                except discord.errors.Forbidden:
                    await channel.send("Não possui permissão para expulsar "+member.name)
    else:
        if  param == "manual":
            await channel.send("O membro não está fazendo nada ilegal.")
                
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    milandia = ['miland', 'lamind', 'laminder', 'milan', 'matheus', "limand"]
    
    if [element for element in milandia if (element in message.content)] \
    and "jogando wow" in message.content \
    and bot.user.mentioned_in(message):
        guild = bot.get_guild(657780431256682496)
        miland = guild.get_member(224176860181954562)
        kickMember(miland)
    elif "wow" in message.content or "world of warcraft" in message.content:
        await message.channel.send('Eu odeio wow!')
    
    await bot.process_commands(message)

@bot.event
async def on_member_update(previous, current):
    if current.activity != None:
        await kickMember(current, "auto")

@tasks.loop(minutes=30)
async def checkUsers():
    for guild in bot.guilds:
        for member in guild.members:
            await kickMember(member, "auto")

@bot.command()
async def check(ctx):
    nickname = ctx.message.content.removeprefix("!check ")
    print(nickname)
    for guild in bot.guilds:
        member = guild.get_member_named(nickname)
        print(member)
        if member == None:
            await ctx.channel.send('Membro não encontrado.')
        else:
            await kickMember(member, "manual")

checkUsers.start()

bot.run(os.getenv('TOKEN'))