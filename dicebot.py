import random
import re

import noteworthy.botkit as botkit
import noteworthy.botkit.response as response
import noteworthy.botkit.cache as cache

from dice import roll as roll_dice

@botkit.botkit_controller(bot_name='dicebot', bot_prefix='!dice')
class DiceBotController():

    AUTH = botkit.auth.PublicBot
    CLIENT_ARGS = {
        "store_path": "/home/xthemage/Documents/Dicebot/state"
    }

    @botkit.botkit_method
    async def roll(self, dstring, **kwargs):
        result_str, result_value = roll_dice(dstring)
        return response.Notice(f'rolling {result_str}: {result_value}')

with open("creds.json") as f:
    creds = json.load(f)

bot = DiceBotController.create_matrix_bot(creds)
bot.run()
