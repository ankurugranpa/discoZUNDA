from functools import cache
from typing import Callable
from abc import ABC, abstractmethod


import discord

"""
UI Base Class
"""


class Button(discord.ui.Button, ABC):
    def __init__(self, name):
        super().__init__(label=name, style=discord.ButtonStyle.primary)
        self.name = name

    @abstractmethod
    def if_name(self, name:str) -> discord.ui.View:
        pass

    async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message(view=self.if_name(self.name))

class ButtonView(discord.ui.View, ABC):
    def __init__(self, ButtonBase:Callable[[str], discord.ui.Button], name_list:list):
        super().__init__()
        self.name_list = name_list
        self.name_list_len = len(self.name_list)
        self.page_num_f = 1 # Carrent Page
        self.page_sum = self._clacpage() # Sum Page
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
                self.add_item(self.ButtonUiBase(self._next_page))
                self.page_num_f = 2
            else:
                self.add_item(self.ButtonUiBase(self._prev_page))
                for name in self.name_list[25:]:
                    self.add_item(self.ButtonUiBase(name))

        # 総ページ数が3~
        else:
            if self.page_num_f == 1:
                for name in self.name_list[:24]:
                    self.add_item(self.ButtonUiBase(name))
                self.add_item(self.ButtonUiBase(self._next_page))
                self.page_num_f = 2

            elif self.page_num_f != self.page_sum:
                buf_start = ((self.page_num_f - 2) * 23) + 24 
                buf_end = buf_start + 24
                self.add_item(self.ButtonUiBase(self._prev_page))
                for name in self.name_list[buf_start:buf_end]:
                    self.add_item(self.ButtonUiBase(name))
                self.add_item(self.ButtonUiBase(self._next_page))
                self.page_num_f += 1

            elif self.page_num_f == self.page_sum:
                buf_start = ((self.page_num_f - 2) * 23) + 24 
                self.add_item(self.ButtonUiBase(self._prev_page))
                for name in self.name_list[buf_start:]:
                    self.add_item(self.ButtonUiBase(name))
