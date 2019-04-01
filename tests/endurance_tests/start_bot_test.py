#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from concurrent.futures import CancelledError
from threading import Thread
import pytest

from config import *
from core.octobot import OctoBot
from tests.test_utils.config import load_test_config

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


def stop_bot(bot):
    thread = Thread(target=bot.stop)
    thread.start()
    thread.join()


async def test_create_bot(event_loop):
    # launch a bot
    config = load_test_config()
    bot = OctoBot(config)
    await bot.initialize()
    event_loop.call_later(1, stop_bot, bot)
    with pytest.raises(CancelledError):
        await bot.start()


async def test_run_bot(event_loop):
    # launch a bot
    config = load_test_config()
    config[CONFIG_CRYPTO_CURRENCIES] = {
        "Bitcoin":
            {
                "pairs": ["BTC/USDT"]
            }
    }
    bot = OctoBot(config, ignore_config=True)
    bot.time_frames = [TimeFrames.ONE_MINUTE]
    await bot.initialize()
    event_loop.call_later(1.9*60, stop_bot, bot)
    with pytest.raises(CancelledError):
        await bot.start()
