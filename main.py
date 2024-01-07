import os
import discord
from discord.ext import commands

from replit import db

from constants import COMMAND_PREFIX, GameMode
from character import Character, str_to_class
from stats import ActorStats
import enemy

import re

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# Utility Functions
def clean_string(input_string):
    # Remove emojis using regex
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE)
    input_string = emoji_pattern.sub('', input_string)

    # Remove spaces and return the result
    return ''.join(input_string.split())


def create_actor_stats(stats_data):
    # stats_keys = [
    #     "str", "agi", "int", "hp", "defense", "max_hp", "level", "exp",
    #     "exp_to_level"
    # ]
    # return ActorStats(**{key: stats_data[key] for key in stats_keys})
    return ActorStats(**stats_data)


def create_enemy(battling_data):
    enemy_class = str_to_class(module='enemy',
                               classname=clean_string(battling_data["name"]))
    return enemy_class(name=battling_data["name"],
                       min_level=battling_data["min_level"],
                       max_level=battling_data["max_level"],
                       stats=create_actor_stats(battling_data["stats"]),
                       inventory=battling_data["inventory"])


def load_character(user_id):
    if "characters" in db.keys() and str(user_id) in db["characters"]:
        character_data = db["characters"][str(user_id)]

        return Character(name=character_data["name"],
                         stats=create_actor_stats(character_data["stats"]),
                         mode=GameMode(character_data["mode"]),
                         battling=create_enemy(character_data["battling"])
                         if character_data["battling"] else None,
                         user_id=user_id)
    else:
        return None


def status_embed(ctx, actor):
    # Create embed with description as current mode
    # TODO: Add proper color scheme
    embed = discord.Embed(title=f"{actor.name} status",
                          description='',
                          color=0xDC143C)
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)

    # Stats field
    parent_class_name = actor.__class__.__bases__[0].__name__
    text = f"""
    **LEVEL:**     {actor.stats.level}
    **HP:**         {actor.stats.hp}/{actor.stats.max_hp}
    **STR:**     {actor.stats.str}
    **AGI:**    {actor.stats.agi}
    **INT:**      {actor.stats.int}
    **DEFENSE:**      {actor.stats.defense}
    """
    if parent_class_name != "Enemy":
        _, exp_needed = actor.ready_to_level_up()
        text += f"**EXP:**         {actor.stats.exp}/{actor.stats.exp+exp_needed}"
    embed.add_field(name="Stats", value=text, inline=True)

    # Inventory field
    # inventory_text = f"Gold: {actor.gold}\n"
    if actor.inventory:
        inventory_text = ""
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
                "str": 5,
                "agi": 5,
                "int": 5,
                "hp": 10,
                "defense": 5,
                "max_hp": 10,
                "level": 1,
                "exp": 0,
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


@bot.command(name="melee", help="Attack the current enemy with melee.")
async def melee(ctx):
    character = load_character(ctx.message.author.id)

    if character.mode != GameMode.BATTLE:
        await ctx.message.reply("Can only call this command in battle!")
        return

    # Simulate battle
    enemy = character.battling

    # Character attacks
    attack_roll, defense_roll, damage, killed, combat_message = character.melee_attack(
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

    # Enemy attacks
    # TODO: Update for variety of attacks
    attack_roll, defense_roll, damage, killed, combat_message = enemy.melee_attack(
        character)
    await ctx.message.reply(combat_message)

    # FIXEME: enemy.fight() does not automatically save character's state
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
    # del db["characters"][str(ctx.message.author.id)]    # Used to dev-test
    character = load_character(ctx.message.author.id)

    character.delete()

    await ctx.message.reply(
        f"Character {character.name} is no more. Create a new one with `!create`."
    )


@bot.command(name="deldev", help="Destroy current character. -Dev only.")
async def delete_dev(ctx):
    del db["characters"][str(ctx.message.author.id)]


bot.run(DISCORD_TOKEN)
