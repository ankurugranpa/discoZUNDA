import discord
from discord.ext import commands
from discord import app_commands

from util import env

# commands.Cogを継承する
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # イベントリスナー(ボットが起動したときやメッセージを受信したとき等)
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Hello] on Ready")
	

    # コマンドデコレーター(descriptionで説明が書ける)
    @app_commands.command(name="kakikukeko")
    async def kakikukeko(self,interaction:discord.Interaction):
        await interaction.response.send_message("tintin")

    @app_commands.command(name="greet", description="指定したユーザーに挨拶をします。")
    @app_commands.describe(user="挨拶を送るユーザー")
    async def greet(self, interaction: discord.Interaction, user: discord.User):
        greeting = f"Hello, {user.display_name}!"
        await interaction.response.send_message(greeting)


async def setup(bot):
    await bot.add_cog(MyCog(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(MyCog(bot))
