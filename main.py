from discord.ext import commands
from datetime import datetime
import discord
import sys
import toml
from cogs.util import Utility


class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.description = "A multipurpose bot made by vi#7158."
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.mod", "cogs.util", "cogs.fun"]
        self.startup()
        self.util = Utility(self)
        # Open config file in append mode.
        open("config.toml", "a")

    async def on_command_error(self, ctx, exception):
        # Exception handling happens here.
        # Returns if command not found.
        if type(exception) is commands.errors.CommandNotFound:
            return
        elif type(exception) is commands.errors.MissingPermissions:
            await ctx.send("You are missing permissions required to run this command.")
            return
        # Prints help message if arguments are missing.
        elif type(exception) is commands.errors.MissingRequiredArgument or IndexError:
            await self.util.help(self.util, ctx, ctx.command.name)
            return
        # Sends exception if unhandled by the previous code.
        await ctx.send(str(exception))
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(ctx.guild.id)]
        except KeyError:
            config = {}
        try:
            logchannel = self.get_channel(config['logchannel'])
        except KeyError:
            return
        await logchannel.send("Error log at " + str(datetime.now()) + ": " + str(exception) + " Type: " + str(
            type(exception)) + ". Invoke message: " + ctx.message.jump_url)

    @staticmethod
    async def on_ready():
        print("HAL-9000")
        print("HAL is ready!")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='//help'))

    @staticmethod
    async def on_connect():
        print("HAL is connected!")

    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except KeyboardInterrupt:
            pass
        except discord.LoginFailure:
            print("Invalid token")
        except discord.HTTPException:
            print("Could not connect.")
        finally:
            self.loop.run_until_complete(self.logout())

    def startup(self):
        print("Loading cogs...")
        for cog in self.loaded_cogs:
            print("Loading " + cog + ".")
            try:
                self.load_extension(cog)
                print("Cog loaded.")
            except Exception as e:
                print("Failed to load cog. Reason: " + str(e))

    async def on_member_ban(self, guild, user):
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(guild.id)]
        except KeyError:
            config = {}
        try:
            systemchannel = self.get_channel(config['systemchannel'])
        except KeyError:
            return
        ban = await guild.fetch_ban(user)
        reason = ban[0]
        if reason is None:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server.")
        else:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server with reason \"" + reason + "\"")
        embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        await systemchannel.send(embed=embed_var)

    async def on_member_join(self, member):
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(member.guild.id)]
        except KeyError:
            config = {}
        try:
            systemchannel = self.get_channel(config['systemchannel'])
        except KeyError:
            return
        embed_var = discord.Embed(color=0xff0008, title="__Ahoy There!__", description=member.mention + " joined the server! Make sure to read #readme!")
        embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        await systemchannel.send(embed=embed_var)

    async def on_member_remove(self, member):
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(member.guild.id)]
        except KeyError:
            config = {}
        try:
            systemchannel = self.get_channel(config['systemchannel'])
        except KeyError:
            return
        embed_var = discord.Embed(color=0xff0008, title="__See You Later!__", description=member.mention + " left the server. See you next time!")
        embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        await systemchannel.send(embed=embed_var)

    async def on_message_delete(self, message):
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(message.guild.id)]
        except KeyError:
            config = {}
        try:
            logchannel = self.get_channel(config['logchannel'])
        except KeyError:
            return
        await logchannel.send("Message sent by "+str(message.author)+" deleted at "+str(datetime.now())+". Contents: "+message.content)
    async def on_message(self, message):
        if "based" in message.content.lower():
            message.reply("""Based on fucking what? BASED ON FYCKING WHAT? You fucking cunt, you notherfucker. All I read is "based based based cringe cringe based", can't you fucking come up with anything else? It feels as if I'm talking to people with fuckijng dementia or something and they keep repeating the same fucking words on loop. BASEd ON FUCKING WHAT??? THE BIBLE? THE OXFORD DICITONARY? MY HAIRY ASSHOLE? OH my God just shut the fuck up it's like you can't form a coherent sentence without using one of these saturated, dumbass words that lost all meaning overtime. "BASEE BASED BASED CRINGE CRINGE WOKE REDPILL CRIMGE WOKE GO FUCK YOURSELF YOU LITTLE BITCH YOU CUNT YOU FUCking asshole you bitch you cunt little shit""")

bot = HAL("//")


@commands.is_owner()
@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down bot.")
    await bot.logout()
    sys.exit()


bot.run()
