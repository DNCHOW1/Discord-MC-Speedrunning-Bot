import discord, random, os
from discord.ext import commands

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = "3=D", intents=intents)

@client.event
async def on_ready():
    print("I'm ready.")

@client.event # varialbe client used above, used to hold instance of the bot
async def on_member_join(member):
    print(f"{member} has joined the server!")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server D:")

# ----------------------- Commands ---------------------------

@client.command()
async def ping(ctx): # name of the function is the name of the command
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases= ["8ball", "test"]) # All the strings in the list can invoke the command
async def _8ball(ctx, *, question):         # * allows to take multiple arguments as one
    responses = ["A", "B", "C", "D",
                 "E", "F", "G", "H"]
    await ctx.send(f"{random.choice(responses)}")

@client.command()
async def displayembed(ctx):
    embed = discord.Embed(
        title = "Title",
        description = "This is a description",
        colour = discord.Colour.blue()
    )

    #embed.set_footer(text="This is a footer.")
    #embed.set_image(url="https://cdn.discordapp.com/avatars/232663256819302400/62a83462251ca018f2d217a5e961d287.webp?size=1024")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/232663256819302400/62a83462251ca018f2d217a5e961d287.webp?size=1024")
    embed.set_author(name="Author Name", icon_url = "https://cdn.discordapp.com/avatars/232663256819302400/62a83462251ca018f2d217a5e961d287.webp?size=1024")
    embed.add_field(name="Field Name", value="Field Value", inline=False) # Not in line, they'll be stacked on top each other'''

    await ctx.send(embed=embed)

# --------------------------- CHECKS ------------------------------------
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int): # No deafult error, can be prone to error!
    await ctx.channel.purge(limit=amount)

def is_it_me(ctx):
    return ctx.author.id == 232663256819302400

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send("THis is main account sausage.")

# -------------------------- Error Handling ------------------
@client.event
async def on_command_error(ctx, error): # More general, happens for all commands
    if isinstance(error, commands.CommandNotFound):
        pass
    '''if isinstance(error, commands.MissingRequiredArgument): # Not specifying amount
        await ctx.send("This will run universally for command errors.")'''

# OR

@clear.error
async def clear_error(ctx, error): # Specifically for the clear command
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in a number.")


client.run("ODA4NDM0OTU3NzY4NDU4MjQw.YCGfuQ.dIdidsCDv4Ks1kR3QdR3_F7tLrA")
