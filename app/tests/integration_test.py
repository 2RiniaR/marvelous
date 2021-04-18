import sys
import os
import asyncio
import pytest_mock


base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base, "../src"))
from src.marvelous import startup
from src.marvelous.client.discord import message_gateway
import src.marvelous.client.presentation as presentation


async def send(text: str, channel):
    print("\n========================================\n")
    print(text)


async def main(mocker: pytest_mock.MockerFixture):
    user1 = mocker.Mock()
    user1.id = 111111111111111111
    user1.name = "Alice"
    user2 = mocker.Mock()
    user2.id = 222222222222222222
    user2.name = "Bob"
    channel1 = mocker.Mock()
    channel2 = mocker.Mock()

    startup()

    await presentation.check_survival_bonus(user1, channel1)
    await presentation.check_survival_bonus(user2, channel1)

    await presentation.show_status(user1, channel1)
    mocker.patch.object(message_gateway, "send", side_effect=send)
    await presentation.show_ranking(channel1)


def test(mocker: pytest_mock.MockerFixture):
    asyncio.run(main(mocker))

