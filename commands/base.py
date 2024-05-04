import discord
from discord.ext import commands
from discord import app_commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_name = "autotts"
    
    # Bot on Ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Base] on Ready")

    @app_commands.command(name="joinvc", description="ボイスチャンネルに接続")
    async def joinvc(self, interaction:discord.Interaction, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        await channel.connect()
        await interaction.response.send_message("join")

    @app_commands.command(name="leavevc", description="ボイスチャンネルから離れる")
    async def leavevc(self, interaction:discord.Interaction):
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message(f"leave")


async def setup(bot):
    await bot.add_cog(Base(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(Base(bot))
