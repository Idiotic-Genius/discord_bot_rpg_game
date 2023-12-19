import os
import discord
from discord.ext import commands

from replit import db

from constants import COMMAND_PREFIX, GameMode
from character import Character

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# Helper functions
def load_character(user_id):
    return Character(**db["characters"][str(user_id)])


MODE_COLOR = {
    GameMode.BATTLE: 0xDC143C,
    GameMode.ADVENTURE: 0x005EB8,
}


def status_embed(ctx, actor):
    # Create embed with description as current mode
    embed = discord.Embed(title=f"{actor.name} status",
                          description='',
                          color=0xDC143C)
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)

    # Stats field
    parent_class_name = actor.__class__.__bases__[0].__name__
    if parent_class_name == "Enemy":
        embed.add_field(name="Stats",
                        value=f"""
        **HP:**         {actor.hp}/{actor.max_hp}
        **ATTACK:**     {actor.attack}
        **DEFENSE:**    {actor.defense}
        **MANA:**       {actor.mana}
        **LEVEL:**      {actor.level}
        """,
                        inline=True)
    else:
        _, xp_needed = actor.ready_to_level_up()

        embed.add_field(name="Stats",
                        value=f"""
        **HP:**         {actor.hp}/{actor.max_hp}
        **ATTACK:**     {actor.attack}
        **DEFENSE:**    {actor.defense}
        **MANA:**       {actor.mana}
        **LEVEL:**      {actor.level}
        **XP:**         {actor.xp}/{actor.xp+xp_needed}
        """,
                        inline=True)

        # Inventory field
        inventory_text = f"Gold: {actor.gold}\n"
        if actor.inventory:
            inventory_text += "\n".join(actor.inventory)

        embed.add_field(name="Inventory", value=inventory_text, inline=True)

    return embed


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


# Commands
@bot.command(name="create", help="Create a character.")
async def create(ctx, name=None):
    user_id = ctx.message.author.id

    # if no name is specified, use the creator's nickname
    if not name:
        name = ctx.message.author.name

    # create characters dictionary if it does not exist
    if "characters" not in db.keys():
        db["characters"] = {}

    # only create a new character if the user does not already have one
    if user_id not in db["characters"] or not db["characters"][user_id]:
        character = Character(
            **{
                "name": name,
                "hp": 16,
                "max_hp": 16,
                "attack": 2,
                "defense": 1,
                "mana": 0,
                "level": 1,
                "xp": 0,
                "gold": 0,
                "inventory": [],
                "mode": GameMode.ADVENTURE,
                "battling": None,
                "user_id": user_id
            })
        character.save_to_db()
        await ctx.message.reply(
            f"New level 1 character created: {name}. Enter `{COMMAND_PREFIX}status` to see your stats."
        )
    else:
        await ctx.message.reply("You have already created your character.")


@bot.command(name="status", help="Get information about your character.")
async def status(ctx):
    try:
        character = load_character(ctx.message.author.id)
        embed = status_embed(ctx, character)
        await ctx.message.reply(embed=embed)
    except KeyError:
        await ctx.message.reply("You have not created your character yet.")


@bot.command(name="hunt", help="Look for an enemy to fight.")
async def hunt(ctx):
    character = load_character(ctx.message.author.id)

    if character.mode != GameMode.ADVENTURE:
        await ctx.message.reply("Can only call this command outside of battle!"
                                )
        return

    enemy = character.hunt()
    embed = status_embed(ctx, enemy)
    await ctx.message.reply(embed=embed)

    # Send reply
    await ctx.message.reply(
        f"You encounter a {enemy.name}. Do you `{COMMAND_PREFIX}fight` or `{COMMAND_PREFIX}flee`?"
    )


@bot.command(name="fight", help="Fight the current enemy.")
async def fight(ctx):
    character = load_character(ctx.message.author.id)

    if character.mode != GameMode.BATTLE:
        await ctx.message.reply("Can only call this command in battle!")
        return

    # Simulate battle
    enemy = character.battling

    # Character attacks
    attack_roll, defense_roll, damage, killed, combat_message = character.fight(
        enemy)
    await ctx.message.reply(combat_message)

    # End battle in victory if enemy killed
    if killed:
        xp, gold, ready_to_level_up = character.defeat(enemy)

        await ctx.message.reply(
            f"{character.name} vanquished the {enemy.name}, earning {xp} XP and {gold} GOLD. HP: {character.hp}/{character.max_hp}."
        )

        if ready_to_level_up:
            await ctx.message.reply(
                f"{character.name} has earned enough XP to advance to level {character.level+1}. Enter `{COMMAND_PREFIX}levelup` with the stat (HP, ATTACK, DEFENSE) you would like to increase. e.g. `{COMMAND_PREFIX}levelup hp` or `{COMMAND_PREFIX}levelup attack`."
            )

        return

    # Enemy attacks
    attack_roll, defense_roll, damage, killed, combat_message = enemy.fight(
        character)
    await ctx.message.reply(combat_message)

    # enemy.fight() does not automatically save character's state
    character.save_to_db()

    # End battle in death if character killed
    if killed:
        character.die()

        await ctx.message.reply(
            f"{character.name} was defeated by a {enemy.name} and is no more. Rest in peace, brave adventurer."
        )
        return

    # No deaths, battle continues
    await ctx.message.reply(
        f"The battle rages on! Do you `{COMMAND_PREFIX}fight` or `{COMMAND_PREFIX}flee`?"
    )


@bot.command(name="flee", help="Flee the current enemy.")
async def flee(ctx):
    character = load_character(ctx.message.author.id)

    if character.mode != GameMode.BATTLE:
        await ctx.message.reply("Can only call this command in battle!")
        return

    enemy = character.battling
    damage, killed = character.flee(enemy)

    if killed:
        character.die()
        await ctx.message.reply(
            f"{character.name} was killed fleeing the {enemy.name}, and is no more. Rest in peace, brave adventurer."
        )
    elif damage:
        await ctx.message.reply(
            f"{character.name} flees the {enemy.name}, taking {damage} damage. HP: {character.hp}/{character.max_hp}"
        )
    else:
        await ctx.message.reply(
            f"{character.name} flees the {enemy.name} with their life but not their dignity intact. HP: {character.hp}/{character.max_hp}"
        )


@bot.command(
    name="levelup",
    help=
    "Advance to the next level. Specify a stat to increase (HP, ATTACK, DEFENSE)."
)
async def levelup(ctx, increase):
    character = load_character(ctx.message.author.id)

    if character.mode != GameMode.ADVENTURE:
        await ctx.message.reply("Can only call this command outside of battle!"
                                )
        return

    ready, xp_needed = character.ready_to_level_up()
    if not ready:
        await ctx.message.reply(
            f"You need another {xp_needed} to advance to level {character.level+1}"
        )
        return

    if not increase:
        await ctx.message.reply(
            "Please specify a stat to increase (HP, ATTACK, DEFENSE)")
        return

    increase = increase.lower()
    if increase == "hp" or increase == "hitpoints" or increase == "max_hp" or increase == "maxhp":
        increase = "max_hp"
    elif increase == "attack" or increase == "att":
        increase = "attack"
    elif increase == "defense" or increase == "def" or increase == "defence":
        increase = "defense"

    success, new_level = character.level_up(increase)
    if success:
        await ctx.message.reply(
            f"{character.name} advanced to level {new_level}, gaining 1 {increase.upper().replace('_', ' ')}."
        )
    else:
        await ctx.message.reply(f"{character.name} failed to level up.")


@bot.command(name="delete", help="Destroy current character.")
async def delete(ctx):
    character = load_character(ctx.message.author.id)

    character.delete()

    await ctx.message.reply(
        f"Character {character.name} is no more. Create a new one with `!create`."
    )


bot.run(DISCORD_TOKEN)
