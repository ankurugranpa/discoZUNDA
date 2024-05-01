import discord
from discord.ext import commands
from discord import app_commands

# commands.Cogを継承する
class VoiceVox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # イベントリスナー(ボットが起動したときやメッセージを受信したとき等)
    @commands.Cog.listener()
    async def on_ready(self):
        print("[VoiceVox] on Ready")


	

    # コマンドデコレーター(descriptionで説明が書ける)
    # @app_commands.command(name="speak", description="メッセージを読み上げます。")
    # @app_commands.describe(talk_content="話す内容", speaker="話者")
    # async def speak(self, integrations discord:Interaction):
    #     talk_content = "test"
    #     await interaction.response.send_message(talk_content)

    @app_commands.command(name="aiueo")
    async def aiueo(self,interaction:discord.Interaction):
        await interaction.response.send_message("tintin")

    @app_commands.command(name="joinvc", description="ボイスチャンネルに接続")
    async def joinvc(self, interaction:discord.Interaction, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        await interaction.response.send_message("join")
        await channel.connect()

    @app_commands.command(name="testplay", description="音声の再生") 
    async def testplay(self, integration:discord.Interaction):
        source = discord.FFmpegPCMAudio("/home/ahahahaha/discoZUNDA/commands/test.wav")
        integration.guild.voice_client.play(source)
        
        # voice.play()




    # @app_commands.command(name="greet", description="指定したユーザーに挨拶をします。")
    # @app_commands.describe(user="挨拶を送るユーザー")
    # async def greet(self, interaction: discord.Interaction, user: discord.User):
    #     greeting = f"Hello, {user.display_name}!"
    #     await interaction.response.send_message(greeting)


async def setup(bot):
    await bot.add_cog(VoiceVox(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(VoiceVox(bot))
