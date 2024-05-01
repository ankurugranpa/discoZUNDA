import discord
from discord.ext import commands
from discord import app_commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog Ready")
    
    @app_commands.command(name="hello")
    async def hello(self,interaction:discord.Interaction):
        await interaction.response.send_message("hello!")
