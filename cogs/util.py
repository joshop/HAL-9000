from discord.ext import commands
import discord
from discord.ext.commands import TextChannelConverter, RoleConverter
import pickle


def setup(bot):
    bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    """Utility commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args=""):
        """Help command.
        ```//help <command>: Help for a single command
        //help <category>: Help for all the commands in a category.```"""
        names_lower = []
        names = []
        for x in self.bot.cogs.keys():
            names_lower.append(x.lower())
            names.append(x)
        if args.lower() in names_lower:
            args = self.bot.get_cog(names[names_lower.index(args.lower())])
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__" + args.qualified_name + "__",
                                value=args.description + "\n", inline=False)
            for command in args.get_commands():
                embed_var.add_field(name="//" + command.name, value=command.help + "\n", inline=False)
        elif self.bot.get_command(args) in self.bot.commands:
            args = self.bot.get_command(args)
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__//" + args.name + "__", value=args.help + "\n", inline=False)
        else:
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__Help Menu__",
                                value="HAL-9000 is a multipurpose discord bot made by vi#7158 "
                                "and rous#7120.\nThis is the help menu. Do `//help <"
                                "command>` for information on a single command. Do `//help"
                                " <category>` for information on a single category.\nCategories:\n  ",
                                inline=False)
            for cog in self.bot.cogs.values():
                embed_var.add_field(name=cog.qualified_name, value=cog.description, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot and displays the time in milliseconds between your message being sent and the ping message
        being sent. Ignores arguments. """
        m = await ctx.send("Pong?")
        latency = m.created_at - ctx.message.created_at
        await m.edit(content=f"Pong in {int(latency.microseconds/1000)} ms! :ping_pong:")

    @commands.command()
    async def invite(self, ctx):
        """Sends an oath2 link for HAL. Ignores arguments."""
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=717042126776434728&permissions=8&scope=bot")

    @commands.command()
    async def repo(self, ctx):
        """Sends the link to the GitHub repo for HAL. Ignores arguments."""
        await ctx.send("https://github.com/Paradigmmmm/HAL-9000")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def poll(self, ctx, *args):
        """Creates a poll in a the specified channel and optionally pings a role.
        Admin only.
        ```//poll <channel> <role (optional)>```"""
        poll_channel = await TextChannelConverter().convert(ctx, args[0])
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__", value='What is the name of your poll?\nType "cancel" at any time to '
                                                        'cancel poll creation.', inline=False)
        q = await ctx.send(embed=embed)
        response = ""
        while type(response) != discord.Message:
            async for message in ctx.channel.history(limit=5):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    break
        answer = response.content
        if answer.lower() == "cancel":
            await ctx.send("Poll cancelled.")
            return
        title = answer
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__",
                        value='Type a brief description of your poll.\nType "cancel" at any time to cancel poll '
                              'creation.',
                        inline=False)
        q = await ctx.send(embed=embed)
        response_found = False
        while not response_found:
            async for message in ctx.channel.history(limit=5):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    response_found = True
                    break
        answer = response.content
        if answer.lower() == "cancel":
            return
        description = answer
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__",
                        value='How many voting options would you like?.\nType "cancel" at any time to cancel poll '
                              'creation.',
                        inline=False)
        q = await ctx.send(embed=embed)
        response_found = False
        while not response_found:
            async for message in ctx.channel.history(limit=5):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    response_found = True
                    break
        answer = response.content
        num_responses = answer
        if answer.lower() == "cancel":
            await ctx.send("Poll cancelled.")
            return
        options = {}
        for x in range(0, int(num_responses)):
            embed = discord.Embed(color=0xff0008)
            embed.add_field(name="__Poll Creation__",
                            value='Type the text for response #' + str(x+1) + '.\nType "cancel" at any time to cancel '
                                                                              'poll creation.',
                            inline=False)
            q = await ctx.send(embed=embed)
            response_found = False
            while not response_found:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        response_found = True
                        break
            answer = response.content
            if answer.lower() == "cancel":
                await ctx.send("Poll cancelled.")
                return
            text = answer
            embed = discord.Embed(color=0xff0008)
            embed.add_field(name="__Poll Creation__",
                            value='Type the emoji for response #' + str(x+1) + '. MAKE SURE THAT THE EMOJI IS EITHER '
                                                                               'FROM THIS SERVER, OR A GLOBAL '
                                                                               'EMOJI.\nType "cancel" at any time to '
                                                                               'cancel poll creation.',
                            inline=False)
            q = await ctx.send(embed=embed)
            response_found = False
            while not response_found:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        response_found = True
                        break
            answer = response.content
            emoji = answer
            options.update({emoji: text})
        await ctx.send("Sending poll message.")
        response_str = ""
        for x in options.keys():
            response_str = response_str + "\n\n" + x + ": " + options[x]
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="*__POLL: " + title + "__*",
                        value='Description:\n' + description,
                        inline=False)
        embed.add_field(name="*Responses*",
                        value=response_str,
                        inline=False)
        embed.add_field(name="*Created by:*",
                        value=ctx.author.mention,
                        inline=False)
        if args[1] == "everyone":
            thing = "@everyone"
        else:
            thing = args[1]
        poll = await poll_channel.send(thing, embed=embed)
        for x in options.keys():
            await poll.add_reaction(x)

    @commands.command()
    async def color(self, ctx, *args):
        """Commands relating to the color system. ```//color list: Lists color names and hex codes. //color <color
        name>: Sets your color. //color add: Adds a color. Requires manage roles. //color remove: Removes a color.
        Requires manage roles. //color forcedelete: Forcibly deletes a color from the config list. Use only if
        something breaks. Requires manage roles.``` """
        args = ' '.join(args)
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError or KeyError:
            globalconfig = {}
        try:
            config = globalconfig[ctx.guild.id]
        except KeyError:
            config = {}
        if args == "add":
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("Invalid permissions.")
                return
            q = await ctx.send("What would you like the color to be (hex code)?")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            color = answer
            if "#" in color:
                color = color.replace("#", "")
            try:
                color = discord.Colour(int(color, 16))
            except ValueError:
                await ctx.send("Invalid color.")
                return
            q = await ctx.send("What would you like the color name to be?")
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            name = answer
            try:
                colorposition = config["colorposition"]
            except KeyError:
                await ctx.send("You haven't set up a position to move colors to in this server yet. Do //config "
                               "colorposition to set up a position. For now I've created the role at the bottom of "
                               "the list.")
                colorposition = 1
            try:
                colorrole = await ctx.guild.create_role(name=name, colour=color, reason="Automated colour addition.")
                await ctx.guild.edit_role_positions({colorrole: colorposition})
                await ctx.send("Color created.")
            except discord.Forbidden:
                await ctx.send("HAL-9000 does not have the manage roles permission.")
                return
            except discord.InvalidArgument:
                await ctx.send("Invalid args.")
                return
            except discord.HTTPException:
                await ctx.send("An unexpected exception occurred. Try again later.")
                return
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colors.append(colorrole.id)
            config.update({"colors": colors})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
        elif args == "list":
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            print(colors)
            colorroles = []
            for x in colors:
                x = ctx.guild.get_role(x)
                print(x)
                colorroles.append(x)
            text = ""
            for x in colorroles:
                text = text + "\n\n**__Color #" + str(colorroles.index(x)+1) + ":__**\nName: " + x.name + "\nHex " \
                                                                                                          "color: " +\
                       str(x.color)
            await ctx.send(text)
        elif args == "delete":
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("Invalid permissions.")
                return
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            q = await ctx.send("What color would you like to delete?")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            try:
                answer = await RoleConverter().convert(ctx, answer)
                await answer.delete()
            except commands.errors.ConversionError:
                await ctx.send("Exception in deleting role. Deleted already? Proceeding with deletion from config.")
            except discord.Permissions:
                await ctx.send("Invalid permissions to delete role. Proceeding with deletion from config.")
            if answer not in colors:
                await ctx.send("Invalid color in config list.")
                return
            colors.remove(answer.id)
            config.update({"colors": colors})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
        elif args == "forcedelete":
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("Invalid permissions.")
                return
            q = await ctx.send("Do you really want to do this? This will delete a role from the config file forcibly. "
                               "Enter color # to continue.")
            try:
                colors = config["colors"]
            except KeyError:
                colors = []

            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            colors.pop(int(answer))
            await ctx.send("Color removed.")
            config.update({"colors": colors})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
        else:
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colorsthing = []
            colorsl = []
            for colorrrr in colors:
                colorsthing.append((ctx.guild.get_role(colorrrr)).name)
                colorsl.append((ctx.guild.get_role(colorrrr)).name.lower())
            if args.lower() in colorsl:
                try:
                    colorrole = await RoleConverter().convert(ctx, colorsthing[colorsl.index(args.lower())])
                except ValueError:
                    colorrole = await RoleConverter().convert(ctx, args)
            else:
                await ctx.send("That is not a valid color.")
                return
            if colorrole.id not in colors:
                await ctx.send("That is not a valid color.")
                return
            for x in ctx.author.roles:
                if x.id in colors:
                    await ctx.author.remove_roles(x)
            await ctx.author.add_roles(colorrole)
            await ctx.send("Color set to " + colorrole.name + "!")
