import datetime
import discord
from discord.ext import commands
from discord import app_commands
from sys import version_info as sysv

from cogs.lancocog import LancoCog


class Tools(LancoCog):
    tools_group = app_commands.Group(name="tools", description="Tool commands")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tools cog loaded")
        await super().on_ready()

    @tools_group.command(name="ping", description="Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        lat = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Pong!", description=f"🏓 {lat} ms", color=0x00FF00)
        await interaction.response.send_message(embed=embed)

    @tools_group.command(name="status", description="Show bot status")
    async def status(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{self.bot.user.name} Status",
            description=f"Various diagnostic information",
            color=0x00FF00,
        )
        embed.add_field(name="Python", value=f"{sysv.major}.{sysv.minor}.{sysv.micro}")
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Users", value=f"{len(self.bot.users)}")
        embed.add_field(name="Commands", value=f"{len(self.bot.commands)}")
        embed.add_field(
            name="Slash Commands", value=f"{len(self.bot.tree.get_commands())}"
        )
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        uptime = datetime.datetime.now() - self.bot.start_time
        embed.add_field(
            name="Uptime",
            value=f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds // 60) % 60}m {uptime.seconds % 60}s",
        )

        cog_names = [cog.__class__.__name__ for cog in self.bot.cogs.values()]
        embed.add_field(name=f"Cogs ({len(cog_names)})", value=", ".join(cog_names))

        embed.set_footer(
            text=f"Version: {self.bot.version} | Commit: {self.bot.commit[:7]}"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Tools(bot))
