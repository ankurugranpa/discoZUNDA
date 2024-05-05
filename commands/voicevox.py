import io
import re

import discord
from discord.ext import commands
from discord import app_commands

from util import voicevox



class BasicView(discord.ui.View):
    @discord.ui.button(label="Click!")
    async def click(self, interaction: discord.Interaction, button: discord.Button) -> None:
        await interaction.response.send_message("Clicked")


class VoiceVox(commands.Cog):
    def __init__(self, bot, timeout=180):
        self.bot = bot
        self.role_name = "autotts"
        self.voice_vox = voicevox.VoiceVox()
        # super().__init__(timeout=timeout)
    
    # Bot on Ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("[VoiceVox] on Ready")

    # receive message
    @commands.Cog.listener()
    async def on_message(self, message):
            if message.author.bot == True:
                return
            if discord.utils.get(message.author.roles, name=self.role_name).name == self.role_name:
                # voice_vox = voicevox.VoiceVox()
                bite_source = self.voice_vox.req_voice(message.content)
                # bite_source = voice_vox.req_voice(message.content)
                wav_io = io.BytesIO(bite_source)
                source = discord.FFmpegPCMAudio(source=wav_io, pipe=True)
                message.guild.voice_client.play(source)




    @app_commands.command(name="testplay", description="音声の再生") 
    async def testplay(self, interaction:discord.Interaction):
        source = discord.FFmpegPCMAudio("/home/ahahahaha/discoZUNDA/commands/test.wav")
        await interaction.response.send_message("これはテストです")
        interaction.guild.voice_client.play(source)


    @app_commands.command(name="tts", description="messageの読み上げ") 
    @app_commands.describe(text="読み上げテキスト")
    async def tts(self, interaction:discord.Interaction, text:str):
        # voice_vox = voicevox.VoiceVox()
        bite_source = self.voice_vox.req_voice(text)
        # bite_source = voice_vox.req_voice(text)
        wav_io = io.BytesIO(bite_source)
        source = discord.FFmpegPCMAudio(source=wav_io, pipe=True)
        interaction.guild.voice_client.play(source)
        await interaction.response.send_message(f"読み上げ[{text}]")

    @app_commands.command(name="autotts", description="メッセージの自動読み上げ")
    async def autotts(self, interaction:discord.Interaction):
        if discord.utils.get(interaction.guild.roles, name=self.role_name) is None:
            await interaction.guild.create_role(name=self.role_name)
            response = f"ロール:{self.role_name}を作成しました\n"
        else:
            response = ""
        print(discord.utils.get(interaction.user.roles))
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=self.role_name))
        await interaction.response.send_message(response + f"{interaction.user.name}に{self.role_name}を付与しました")

    @app_commands.command(name="endautotts", description="メッセージの自動読み上げ")
    async def endautotts(self, interaction:discord.Interaction):
        await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, name=self.role_name))
        await interaction.response.send_message(f"{interaction.user.name}から{self.role_name}を削除しました")


    @app_commands.command(name="setspeaker", description="話者の選択")
    async def setspeaker(self, interaction:discord.Interaction, speaker_num:int):
        # view = SampleView(timeout=None)
        # await interaction.response.send_message(view)
        self.voice_vox.set_speaker(speaker_num)
        await interaction.response.send_message(f"{speaker_num}に設定しました")
        # await interaction.response.send_message(view=BasicView())


async def setup(bot):
    await bot.add_cog(VoiceVox(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(VoiceVox(bot))
