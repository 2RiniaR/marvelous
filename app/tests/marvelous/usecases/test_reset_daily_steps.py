import pytest_mock
from unittest.mock import MagicMock
from marvelous.usecases.reset_daily_steps import *


def test_reset_survival_bonus_succeed(mocker: pytest_mock.MockerFixture):
    """
    データの更新に成功した場合、結果として成功を表すオブジェクトが返される
    """
    update_func: MagicMock = mocker.patch.object(data_store.users, "reset_daily_steps")
    reset_daily_steps()
    update_func.assert_called_once()
