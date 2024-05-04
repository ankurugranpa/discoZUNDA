import io

import discord
from discord.ext import commands
from discord import app_commands

from util import voicevox



class VoiceVox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_name = "autotts"
    
    # Bot on Ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("[VoiceVox] on Ready")

    # receive message
    @commands.Cog.listener()
    async def on_message(self,interaction:discord.Interaction, message):
    #   if discord.utils.get(interaction.guild.roles, name=role_name) is True:
    #         voice_vox = voicevox.VoiceVox()
    #         bite_source = voice_vox.req_voice(message)
    #         wav_io = io.BytesIO(bite_source)
    #         source = discord.FFmpegPCMAudio(source=wav_io, pipe=True)
    #         interaction.guild.voice_client.play(source)
            print(message)
            # await interaction.response.send_message(f"読み上げ:[{message}]")



    @app_commands.command(name="testplay", description="音声の再生") 
    async def testplay(self, interaction:discord.Interaction):
        source = discord.FFmpegPCMAudio("/home/ahahahaha/discoZUNDA/commands/test.wav")
        await interaction.response.send_message("これはテストです")
        interaction.guild.voice_client.play(source)


    @app_commands.command(name="tts", description="messageの読み上げ") 
    @app_commands.describe(text="読み上げテキスト")
    async def tts(self, interaction:discord.Interaction, text:str):
        voice_vox = voicevox.VoiceVox()
        bite_source = voice_vox.req_voice(text)
        wav_io = io.BytesIO(bite_source)
        source = discord.FFmpegPCMAudio(source=wav_io, pipe=True)
        interaction.guild.voice_client.play(source)
        await interaction.response.send_message(f"読み上げ[{text}]")

    @app_commands.command(name="autotts", description="メッセージの自動読み上げ")
    async def autotts(self, interaction:discord.Interaction):
        if discord.utils.get(interaction.guild.roles, name=self.role_name) is None:
            await interaction.guild.create_role(name=self.role_name)
            response = f"ロール:{self.role_name}を作成しました\n"
        print(discord.utils.get(interaction.user.roles))
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=self.role_name))
        await interaction.response.send_message(response + f"{interaction.user.name}に{self.role_name}を付与しました")

    @app_commands.command(name="endautotts", description="メッセージの自動読み上げ")
    async def endautotts(self, interaction:discord.Interaction):
        await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, name=self.role_name))
        await interaction.response.send_message(f"{interaction.user.name}から{self.role_name}を削除しました")


        


async def setup(bot):
    await bot.add_cog(VoiceVox(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(VoiceVox(bot))
