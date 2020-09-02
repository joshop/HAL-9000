from datetime import datetime
from discord.ext import MemberConverter
from discord.ext import commands
import discord
import random
import requests
from fuzzywuzzy import process


description = "HAL-9000, the shoddily coded bot made by two teenagers for their shitty server."
bot = commands.Bot(command_prefix = '//', description = description)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def time(ctx):
    """Command for displaying time. Ignores arguments."""
    await ctx.send(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))


@bot.command()
async def coinflip(ctx):
    """Command for flipping a coin. Ignores arguments."""
    await ctx.send(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))


@bot.command()
async def ping(ctx):
    """Pings the bot. Ignores arguments."""
    await ctx.send("Pong! :ping_pong:")


@bot.command()
async def roll(ctx, args):
    """Rolls any amount of dice with any amount of sides. Format: //roll XdX"""
    total = 0
    crits = 0
    critf = 0
    for die in args.split():
        if 'd' not in die:
            total += int(die)
            continue
        num, sides = die.split('d')
        if num == '':
            num = '1'
        rolls = [random.randint(1, int(sides)) for n in range(int(num))]
        if sides == '20':
            crits += rolls.count(20)
            critf += rolls.count(1)
        total += sum(rolls)
    await ctx.send("Result: "+str(total)+"\n***CRITICAL SUCCESS!***"*crits+"\n***CRITICAL FAILURE!***"*critf)


@bot.command()
async def dnd_get(ctx, args):
    """Gets something from the D%D 5e API."""
    endpoint, *args = args.split()
    name = ' '.join(args[:args.index('/')])
    vals = args[args.index('/')+1:]
    of_that_type = requests.get("https://www.dnd5eapi.co/api/"+endpoint).json()
    real_name = process.extractOne(name, of_that_type['results'])[0]
    await ctx.send("Data for `%s`: " % real_name['name'])
    url = real_name['url']
    data = requests.get("https://www.dnd5eapi.co"+url).json()
    props = list(data.keys())
    for val in vals:
        real_val = process.extractOne(val, props)[0]
        if not real_val:
            await ctx.send("`%s`: *not defined*" % val)
        else:
            await ctx.send("`%s => %s`" % (real_val, str(data[real_val])))


@bot.command()
async def ban(ctx, args):
    '''"bans" a user.'''
    converter = MemberConverter()
    user = await converter.convert(ctx, args)
    banroleids = [738456842707140700, 742128809129803806, 742128992286670910, 742129191277035590]
    userbanroles = []
    for x in user.roles:
        if x.id in banroleids:
            userbanroles.append(x)
    x = userbanroles[-1]
    if x != 3:
        await user.add_roles(banroleids.index(x) + 1)
    else:
        await ctx.send("That user is already the highest banned level.")


bot.run(open("token").read())
