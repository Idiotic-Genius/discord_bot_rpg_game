import enum

# General constants
COMMAND_PREFIX = "."

# Enemy stat modifiers
ENEMY_MAXHP_MOD = (1, 6)
ENEMY_STR_MOD = (2, 4)
ENEMY_AGI_MOD = (2, 4)
ENEMY_INT_MOD = (2, 4)
ENEMY_DEFENSE_MOD = (2, 3)
ENEMY_XP_MOD = (2, 3)
ENEMY_GOLD_MOD = (1, 2)

# Player constants
PLAYER_LVL_CAP = 10


# Player game modes (indicates what the player is doing)
class GameMode(enum.IntEnum):
    ADVENTURE = 1
    BATTLE = 2

