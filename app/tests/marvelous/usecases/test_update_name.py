import pytest_mock
from unittest.mock import MagicMock
import src.marvelous.usecases.update_name as target_package
from src.marvelous.usecases.update_name import *


def test_update_name_succeed(mocker: pytest_mock.MockerFixture):
    discord_id = 0
    name = "fuga"
    user: MagicMock = mocker.Mock()
    user.display_name = "hoge"
    get_func: MagicMock = mocker.patch.object(target_package, "get_user", return_value=user)
    update_func: MagicMock = mocker.patch.object(data_store.users, "update")

    update_name(discord_id, name)

    assert user.display_name == name
    get_func.assert_called_once_with(discord_id)
    update_func.assert_called_once_with(user)
