import discord, random, datetime, os
from datetime import datetime as dt
from discord.ext import commands

client = commands.Bot(command_prefix = "[--")
os.chdir(os.getcwd()+"\Minecraft Speedrunning")

# TODO: Handle timedelta >= 1 day(Your time is laughable and will not be submitted to the leaderboard)

class LBDict(dict):
    t3 = []

    def dict_from_file(self, filename):
        with open(filename, "r") as f:
            for data in f.readlines():
                name, time, proof, date = data.replace("\n", "").split(" - ")
                self[name] = [formatTime(time), proof, date]
        self.updateTop()

    def dict_to_file(self, filename):
        with open(filename, "w") as f:
            for k,v in self.items():
                formatted = " - ".join(str(i) for i in v)
                f.write(f"{k} - {formatted}\n")

    def sort(self):
        ordered_lb = sorted(self.items(), key=lambda x: x[1][0])
        self.clear()
        self.update(dict(ordered_lb))
        self.updateTop()

    def updateTop(self):
        # Assumes that everything has been sorted beforehand
        # If Less than 3 entries, will any entries will be top 3
        keys = list(self.keys())
        if len(keys) >= 3:
            self.t3 = keys[:3]
        else: # Not enough entries
            self.t3 = keys

    def lbChange(self, new):
        # Name subject to change; Assumes time is already formatted
        # Checks to see if the new time
        vals = list(self.values())
        if len(vals) in [1, 2, 3]:
            return True
        return any(new < data[0] for data in vals[:3])

    def pop(self, *args):
        _ = super().pop(*args)
        if _:
            self.updateTop()
            self.dict_to_file("speedrun_data.txt")
        return _

    def getT3(self):
        return self.t3

@client.command(aliases=["lb"])
async def leaderboard(ctx):
    # Check for duplicates
    # Check sorted
    # Check if present
    # Assumes time values are timedelta

    lb = list(lb_data.items())

    embed = discord.Embed(
        title = "Minecraft FSG Any \% Leaderboard:",
        description = "Filtered Seed Glitchless Ordered by Personal Bests\nhttps://repl.it/@AndyNovo/filteredseed",
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url="https://www.logaster.com/blog/wp-content/uploads/2020/06/image14-3.png")
    embed.add_field(value="Name", name="\u200b", inline=True)
    embed.add_field(value="Time", name="\u200b", inline=True)
    embed.add_field(value="Date", name="\u200b", inline=True)

    j = 1
    for i in lb: #i[0] = name, i[1][0] = time, i[1][1] = proof, i[1][2] = date
        embed.add_field(value=f"{j}. {i[0]}", name="\u200b", inline=True)
        embed.add_field(value=f"[{i[1][0]}]({i[1][1]})", name="\u200b", inline=True) # Can format so time has clickable link
        embed.add_field(value=i[1][2], name="\u200b", inline=True)
        j+=1

    await ctx.send(embed=embed)

@client.command()
async def submit(ctx, *, sub):
    # Time,Proof link
    # IF wrong submission, ask for correct submission
    # Check if submission has all necesaary. If it doesn't, throw error
    if sub.count(" / ") != 1 or sub[:10].count(":") != 2:
        raise Exception() # Error!

    user = str(ctx.author) # Must concatenate because raw data is very different. Str gets only name
    time, proof = sub.split(" / ")
    time = formatTime(time)

    pb_data = lb_data.get(user) # Must str because raw data is very different
    if pb_data: # If data present for author
        if time < pb_data[0]:
            await ctx.send(f"PB Improvement! {pb_data[0]} -> {time}")
            lb_data[user] = [time, proof, datetime.date.today()] # Updating PB
        else:
            await ctx.send(f"Your PB({pb_data[0]}) is still better...")
    else:
        lb_data[user] = [time, proof, datetime.date.today()]
        await ctx.send(f"Your time has been recorded. {user} - {time} {proof} {datetime.date.today()}")

    if lb_data.lbChange(time):
        present = user in lb_data.getT3()
        if present and time < pb_data[0]:
            await ctx.send(f"Your time({time}) has been updated in the top 3.")
        elif not present: # If user not in top 3 then this is their best
            await ctx.send(f"Your time({time}) has broken top 3 in the leaderboard!!!")
    lb_data.sort()
    lb_data.dict_to_file("speedrun_data.txt")

@client.command()
async def removeme(ctx):
    name = str(ctx.author)
    _ = lb_data.pop(name, None)
    if _: # Name in lb list
        await ctx.send("Your time has been removed.")
    else: # Name not in lb list
        await ctx.send("???\nYou don't have a time on the leaderboard.")

@client.command()
async def info(ctx):
    embed = discord.Embed(
        title = "Minecraft FSG Any \% Info",
        description = """Filtered Seed Glitchless Information
                         Use link https://repl.it/@AndyNovo/filteredseed for good seeds
                         Submit only a link of photo of in game time or livesplit as proof

                         The current "good seed" traits:
                            * A village or shipwreck in the pos/pos quadrant of the overworld between 0 and 80 in both X and Z
                            * A ruined_portal near (0 to 144 but not in the village)
                            * Your spawn between -48 and 144 in both coordinates
                            * In the nether there is a structure close to 0,0 in three quadrants (+/+, -/+, +/-) these are all designed to be within 128 of 0,0 in each coordinate although in the negative dimensions they can't be produced with values between -64 and 0.

                         There will always be 1 or more bastions (pos/pos guaranteed) and exactly 1 fortress generated within 128 blocks of 0,0.""",
        colour = discord.Colour.blue()
    )
    await ctx.send(embed=embed)

@submit.error
async def submit_error(ctx, error): # Specifically for the clear command
    print(error)
    await ctx.send("Submit in the proper format plz: [--submit h:mm:ss / link")

def formatTime(t):
    h, m, s = t.split(":")
    return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

lb_data = LBDict()
lb_data.dict_from_file("speedrun_data.txt")

client.run("____")
