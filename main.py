import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}'.format(bot))

    #await bot.add_roles(373270735646490628, 666419070106730516)
    for guild in bot.guilds:
        role = guild.get_role(666419070106730516)
        for member in guild.members:
            if member.id == 373270735646490628:
                await member.add_roles(role)
                #await member.add_roles(666419070106730516)
            await checkMember(member, None, "auto")

async def checkMember(member, channel, param):
    if channel == None:
        channelId = bot.guilds[0].text_channels[0].id
        channel = bot.get_channel(channelId)
    if member.activities:
        for activity in member.activities:
            if "world of warcraft" in activity.name.lower():
                await kickMember(member, channel)
    else:
        if param == "manual":
            await channel.send("Member "+member.name+" isn't playing wow.")

async def kickMember(member, channel):
    try:
        await channel.send("Member "+member.name+" was kicked from"
        +" the server.Reason: **Playing WOW**")
        await member.send(os.getenv('INVITE'))
        await member.kick(reason='Playing WOW')
    except discord.errors.Forbidden:
        await channel.send("I can't kick "+member.name)
                
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    milandia = ['miland', 'lamind', 'laminder', 'milan', 'matheus', "limand"]
    
    if [element for element in milandia if (element in message.content)] \
    and "jogando wow" in message.content \
    and bot.user.mentioned_in(message):
        guild = bot.get_guild(message.guild.id)
        miland = guild.get_member(os.getenv('FRIEND'))
        await checkMember(miland, message.channel.id, "manual")
    elif "wow" in message.content or "world of warcraft" in message.content:
        await message.channel.send('I hate wow!')
    
    await bot.process_commands(message)

@bot.event
async def on_member_update(previous, current):
    if current.activity != None:
        await checkMember(current, None, "auto")

@tasks.loop(minutes=30)
async def checkUsers():
    for guild in bot.guilds:
        for member in guild.members:
            await checkMember(member, None, "auto")

@bot.command(
    help="Check if user is playing wow if so he/she is removed from the server",
    brief="Check user's activity"
)
async def check(ctx):
    nickname = ctx.message.content.removeprefix("!check ")
    print(nickname)
    channel = ctx.message.channel
    guild = ctx.guild
    member = guild.get_member_named(nickname)
    print(member)
    if member == None:
        await ctx.channel.send('Membro não encontrado.')
    else:
        await checkMember(member, channel, "manual")

@bot.command()
async def admin(ctx, user: discord.Member):
    guild = ctx.guild
    role = guild.get_role(666419070106730516)
    await user.add_roles(role)

checkUsers.start()

bot.run(os.getenv('TOKEN'))
