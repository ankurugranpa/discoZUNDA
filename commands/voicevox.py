import io

import discord
from discord.ext import commands
from discord import app_commands

from util import voicevox


class SpeakerButton(discord.ui.Button):

    def __init__(self, name):
        super().__init__(label=name, style=discord.ButtonStyle.primary)
        self.name = name

    async def callback(self, interaction: discord.Interaction):
        test_list = [1, 2, 3, 4]
        # await interaction.response.send_message(f"Cicked:{self.name}")
        await interaction.response.send_message(view=SpeakerButtonView(test_list))




class SpeakerButtonView(discord.ui.View):

    def __init__(self, name_list:list):
        super().__init__()
        self.name_list = name_list
        self.name_list_len = len(self.name_list)
        # viewにセレクトを追加
        i = 0
        for name in name_list:
            if i==25:
                return
            self.add_item(SpeakerButton(f"{name}"))
            i = i+ 1

    def menu(self):
        if self.name_list_len < 25:
            for name in self.name_list:
                self.add_item(SpeakerButton(f"{name}"))
        else:
            top_list = self.__top_menu()
            top_list_len = len(top_list)
            if top_list_len%23 == 0:
                self.__bottom_menu(top_list)
            else:
                for i in top_list_len/23:
                    self.__bottom_menu(top_list)





            






    def __top_menu(self) -> list:
        """
         0 < self.name_list < 25
        """
        i = 0
        for name in self.name_list:
            if i == 25:
                self.add_item(SpeakerButton("NextPage⇒"))
            self.add_item(SpeakerButton(f"{name}"))
        next_list = self.name_list[25:]
        return next_list


    def __middle_menu(self, name_list:list) -> list:
        """
         26 < self.name_list < 49
        """
        i = 0
        for name in name_list:
            if i == 0:
                self.add_item(SpeakerButton("⇐PrePage"))
            if i == 25:
                self.add_item(SpeakerButton("NextPage⇒"))
            self.add_item(SpeakerButton(f"{name}"))
        next_middle_list = self.name_list[24:]
        return next_middle_list

    def __bottom_menu(self, name_list:list):
        i = 0
        for name in name_list:
            if i == 0:
                self.add_item(SpeakerButton("⇐PrePage"))
            self.add_item(SpeakerButton(f"{name}"))

            



        




        


        




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





    @app_commands.command(name="ui_test", description="uiのテスト")
    async def ui_test(self, interaction:discord.Interaction):
        # view = discord.ui.View()
        # async def button_callback(interaction):
        #     await interaction.response.send_message("Button was clicked!", ephemeral=True)

        # # Googleのボタンを追加
        # for i in range(10):
        #     button = discord.ui.Button(label="Click Me!", style=discord.ButtonStyle.green)

        #     button.callback = button_callback

        #     # ビュー（ボタンを含むコンテナ）を作成
        #     # view = View()
        #     view.add_item(button)
        #     # view.add_item(discord.ui.Button(label="Click Me!", style=discord.ButtonStyle.green))
        await interaction.response.send_message(view=SpeakerButtonView(self.voice_vox.speaker_list()))




async def setup(bot):
    await bot.add_cog(VoiceVox(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(VoiceVox(bot))
