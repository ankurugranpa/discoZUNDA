import asyncio

from discord.ext import commands
import discord

from util import env

class MyBot(commands.Bot):
    async def on_ready(self):
        print('Bot ready.')

    async def setup_hook(self) -> None:
        # すぐに同期したいサーバーのIDを入れる
        guild_ids = [env.MY_GUILD_ID]
        await self.tree.sync(guild=None)  # グローバルコマンドを同期
        

        for guild_id in guild_ids:
            guild = self.get_guild(guild_id)  # Guild オブジェクトを取得
            if guild is not None:
                try:
                    await self.tree.copy_global_to(guild=guild)  # Guild オブジェクトを渡す
                except discord.errors.Forbidden:
                    print(f"サーバーID:{guild_id}に登録できませんでした。")
            else:
                print(f"Guild ID {guild_id} を見つけました")
async def main():
    bot = MyBot(command_prefix="!", intents=discord.Intents.all())

    # Cogを有効化
    # await bot.load_extension("cogs.hello")
    await bot.load_extension(name="commands.hello")
    await bot.load_extension(name="commands.voicevox")
    # Botを起動
    await bot.start(env.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
