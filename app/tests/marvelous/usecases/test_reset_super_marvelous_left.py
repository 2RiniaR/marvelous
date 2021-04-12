import pytest_mock
from unittest.mock import MagicMock
from marvelous.usecases.reset_super_marvelous_left import *


def test_reset_survival_bonus_succeed(mocker: pytest_mock.MockerFixture):
    """
    データの更新に成功した場合、結果として成功を表すオブジェクトが返される
    """
    count: MagicMock = mocker.Mock()
    update_func: MagicMock = mocker.patch.object(data_store.users, "reset_super_marvelous_left")
    reset_super_marvelous_left(count)
    update_func.assert_called_once_with(count)
