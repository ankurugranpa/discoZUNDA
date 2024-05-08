import io
from functools import cache
from typing import Callable
from abc import ABC, abstractmethod

import discord
from discord.ext import commands
from discord import app_commands

from util import voicevox


class ButtonUiBase(discord.ui.Button, ABC):
    def __init__(self, name):
        super().__init__(label=name, style=discord.ButtonStyle.primary)
        self.name = name

    @abstractmethod
    def if_name(self, name:str) -> discord.ui.View:
        pass

    async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message(view=self.if_name(self.name))



    


# class ButtonBase(discord.ui.Button):
# 
#     def __init__(self, name):
#         super().__init__(label=name, style=discord.ButtonStyle.primary)
#         self.name = name
#         # self.callback_style = "text"
#         self.callback_style = "ui"
# 
#     def set_callback_type(self, type:str):
#         if type == "text":
#             self.callback_style = "text"
#         elif type == "ui":
#             self.callback_style = "ui"
# 
#     def if_name(self, name:str) -> discord.ui.View:
#         if name == "四国めたん":
#             test_list = [name, name, name, name]
#             return ButtonBaseView(test_list)
#         else:
#             test_list = ["ちがう", "ちがう"]
#             return ButtonBaseView(test_list)
# 
# 
#     async def callback(self, interaction: discord.Interaction):
#         test_list = [1, 2, 3, 4]
# 
#         # button_func(self.name)
#         if self.callback_style == "ui":
#             await interaction.response.send_message(view=self.if_name(self.name))
#         elif self.callback_style == "text":
#             await interaction.response.send_message(f"Cicked:{self.name}")
#         # await interaction.response.send_message(view=ButtonBaseView(test_list))
#         # await interaction.response.send_message(view=self.callback_view())
#         # print(self.name)
#         return self.name



# class ButtonBaseView(discord.ui.View):
# 
#     def __init__(self, name_list:list):
#         super().__init__()
#         self.name_list = name_list
#         self.name_list_len = len(self.name_list)
#         self.page_num_f = 1 # 現在のページ
#         self.page_sum = self._clacpage() # 合計ページ
#         self.menu()
#         self._next_page = "NextPage"
#         self._prev_page = "PrevPage"
# 
#     @cache
#     def _clacpage(self) -> int:
#         if self.name_list_len < 25:
#             return 1
#         elif (self.name_list_len >= 25 and self.name_list_len < 48):
#             return 2
#         else:
#             quotient = (self.name_list_len - 24) // 23
#             remainde = (self.name_list_len - 24) % 23
#             return 1 + quotient + remainde
# 
# 
# 
#     def menu(self):
# 
#         # 総ページ数が1
#         if self.page_sum == 1:
#             for name in self.name_list:
#                 self.add_item(TestButtonUiBase(f"{name}"))
#             
#         # 総ページ数が2
#         elif self.page_sum == 2:
#             if self.page_num_f == 1:
#                 for name in self.name_list[:24]:
#                     self.add_item(TestButtonUiBase(f"{name}"))
#                 self.add_item(TestButtonUiBase(f"{self._next_page}"))
#                 self.page_num_f = 2
#             else:
#                 self.add_item(TestButtonUiBase(f"{self._prev_page}"))
#                 for name in self.name_list[25:]:
#                     self.add_item(TestButtonUiBase(f"{name}"))
# 
#         # 総ページ数が3~
#         else:
#             if self.page_num_f == 1:
#                 for name in self.name_list[:24]:
#                     self.add_item(TestButtonUiBase(f"{name}"))
#                 self.add_item(TestButtonUiBase(f"{self._next_page}"))
#                 self.page_num_f = 2
# 
#             elif self.page_num_f != self.page_sum:
#                 buf_start = ((self.page_num_f - 2) * 23) + 24 
#                 buf_end = buf_start + 24
#                 self.add_item(TestButtonUiBase(f"{self._prev_page}"))
#                 for name in self.name_list[buf_start:buf_end]:
#                     self.add_item(TestButtonUiBase(f"{name}"))
#                 self.add_item(TestButtonUiBase(f"{self._next_page}"))
#                 self.page_num_f += 1
# 
#             elif self.page_num_f == self.page_sum:
#                 buf_start = ((self.page_num_f - 2) * 23) + 24 
#                 self.add_item(TestButtonUiBase(f"{self._prev_page}"))
#                 for name in self.name_list[buf_start:]:
#                     self.add_item(TestButtonUiBase(f"{name}"))

class ButtonBaseUiView(discord.ui.View, ABC):
    def __init__(self, ButtonBase:Callable[[str], discord.ui.Button], name_list:list):
        super().__init__()
        self.name_list = name_list
        self.name_list_len = len(self.name_list)
        self.page_num_f = 1 # 現在のページ
        self.page_sum = self._clacpage() # 合計ページ
        self.ButtonUiBase = ButtonBase
        self._next_page = "NextPage"
        self._prev_page = "PrevPage"
        self.menu()
        

    @cache
    def _clacpage(self) -> int:
        if self.name_list_len < 25:
            return 1
        elif (self.name_list_len >= 25 and self.name_list_len < 48):
            return 2
        else:
            quotient = (self.name_list_len - 24) // 23
            remainde = (self.name_list_len - 24) % 23
            return 1 + quotient + remainde


    def menu(self):

        # 総ページ数が1
        if self.page_sum == 1:
            for name in self.name_list:
                self.add_item(self.ButtonUiBase(name))
            
        # 総ページ数が2
        elif self.page_sum == 2:
            if self.page_num_f == 1:
                for name in self.name_list[:24]:
                    self.add_item(self.ButtonUiBase(name))
                    # self.add_item(ButtonBase(f"{name}"))
                self.add_item(self.ButtonUiBase(self._next_page))
                self.page_num_f = 2
            else:
                self.add_item(ButtonBase("PrevPage"))
                for name in self.name_list[25:]:
                    self.add_item(self.ButtonUiBase(name))
                    # self.add_item(ButtonBase(f"{name}"))

        # 総ページ数が3~
        else:
            if self.page_num_f == 1:
                for name in self.name_list[:24]:
                    self.add_item(self.ButtonUiBase(name))
                    # self.add_item(ButtonBase(f"{name}"))
                self.add_item(self.ButtonUiBase(self._next_page))
                # self.add_item(ButtonBase("NextPage"))
                self.page_num_f = 2

            elif self.page_num_f != self.page_sum:
                buf_start = ((self.page_num_f - 2) * 23) + 24 
                buf_end = buf_start + 24
                self.add_item(self.ButtonUiBase(self._prev_page))
                # self.add_item(ButtonBase("PrevPage"))
                for name in self.name_list[buf_start:buf_end]:
                    self.add_item(self.ButtonUiBase(name))
                    # self.add_item(ButtonBase(f"{name}"))
                self.add_item(self.ButtonUiBase(self._next_page))
                # self.add_item(ButtonBase("NextPage"))
                self.page_num_f += 1

            elif self.page_num_f == self.page_sum:
                buf_start = ((self.page_num_f - 2) * 23) + 24 
                self.add_item(self.ButtonUiBase(self._prev_page))
                # self.add_item(ButtonBase("PrevPage"))
                for name in self.name_list[buf_start:]:
                    self.add_item(self.ButtonUiBase(name))
                    # self.add_item(ButtonBase(f"{name}"))

class ButtonBaseView(ButtonBaseUiView):
    def __init__(self, ButtonBase: Callable[[str], discord.ui.Button], name_list: list):
        super().__init__(ButtonBase, name_list)

class ButtonBase(ButtonUiBase):
    def __init__(self, name):
        super().__init__(name)

    def if_name(self, name: str) -> discord.ui.View:
        if name == "四国めたん":
            test_list = [name, name, name, name]
            return ButtonBaseView(ButtonBase, test_list)
        else:
            test_list = ["yes", "ちがう"]
            return ButtonBaseView(ButtonBase, test_list)


# class ButtonBaseView(discord.ui.View):
# 
#     def __init__(self, name_list:list):
#         super().__init__()
#         self.name_list = name_list
#         self.name_list_len = len(self.name_list)
#         self.page_num_f = 1 # 現在のページ
#         self.page_sum = self._clacpage() # 合計ページ
#         self.menu()
#         # # viewにセレクトを追加
#         # i = 0
#         # for name in name_list:
#         #     if i==25:
#         #         return
#         #     self.add_item(ButtonBase(f"{name}"))
#         #     i = i+ 1
# 
#     @cache
#     def _clacpage(self) -> int:
#         if self.name_list_len < 25:
#             return 1
#         elif (self.name_list_len >= 25 and self.name_list_len < 48):
#             return 2
#         else:
#             quotient = (self.name_list_len - 24) // 23
#             remainde = (self.name_list_len - 24) % 23
#             return 1 + quotient + remainde
# 
# 
# 
#     def menu(self):
# 
#         # 総ページ数が1
#         if self.page_sum == 1:
#             for name in self.name_list:
#                 self.add_item(ButtonBase(f"{name}"))
#             
#         # 総ページ数が2
#         elif self.page_sum == 2:
#             if self.page_num_f == 1:
#                 for name in self.name_list[:24]:
#                     self.add_item(ButtonBase(f"{name}"))
#                 self.add_item(ButtonBase("NextPage"))
#                 self.page_num_f = 2
#             else:
#                 self.add_item(ButtonBase("PrevPage"))
#                 for name in self.name_list[25:]:
#                     self.add_item(ButtonBase(f"{name}"))
# 
#         # 総ページ数が3~
#         else:
#             if self.page_num_f == 1:
#                 for name in self.name_list[:24]:
#                     self.add_item(ButtonBase(f"{name}"))
#                 self.add_item(ButtonBase("NextPage"))
#                 self.page_num_f = 2
# 
#             elif self.page_num_f != self.page_sum:
#                 buf_start = ((self.page_num_f - 2) * 23) + 24 
#                 buf_end = buf_start + 24
#                 self.add_item(ButtonBase("PrevPage"))
#                 for name in self.name_list[buf_start:buf_end]:
#                     self.add_item(ButtonBase(f"{name}"))
#                 self.add_item(ButtonBase("NextPage"))
#                 self.page_num_f += 1
# 
#             elif self.page_num_f == self.page_sum:
#                 buf_start = ((self.page_num_f - 2) * 23) + 24 
#                 self.add_item(ButtonBase("PrevPage"))
#                 for name in self.name_list[buf_start:]:
#                     self.add_item(ButtonBase(f"{name}"))
# 
    # def __top_menu(self) -> list:
    #     """
    #      0 < self.name_list < 25
    #     """
    #     i = 0
    #     for name in self.name_list:
    #         if i == 25:
    #             self.add_item(ButtonBase("NextPage⇒"))
    #         self.add_item(ButtonBase(f"{name}"))
    #     next_list = self.name_list[25:]
    #     return next_list


    # def __middle_menu(self, name_list:list) -> list:
    #     """
    #      26 < self.name_list < 49
    #     """
    #     i = 0
    #     for name in name_list:
    #         if i == 0:
    #             self.add_item(ButtonBase("⇐PrePage"))
    #         if i == 25:
    #             self.add_item(ButtonBase("NextPage⇒"))
    #         self.add_item(ButtonBase(f"{name}"))
    #     next_middle_list = self.name_list[24:]
    #     return next_middle_list

    # def __bottom_menu(self, name_list:list):
    #     i = 0
    #     for name in name_list:
    #         if i == 0:
    #             self.add_item(ButtonBase("⇐PrePage"))
    #         self.add_item(ButtonBase(f"{name}"))



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
        view = ButtonBaseView(ButtonBase, self.voice_vox.speaker_list())
        # print(type(view))
        await interaction.response.send_message(view=view)




async def setup(bot):
    await bot.add_cog(VoiceVox(bot))

async def teardown(bot):
    print('I am being unloaded!')
    await bot.remove_cog(VoiceVox(bot))
