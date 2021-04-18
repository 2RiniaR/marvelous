import pytest_mock
from unittest.mock import MagicMock


def test_reset_survival_bonus_succeed(mocker: pytest_mock.MockerFixture):
    """
    データの更新に成功した場合、結果として成功を表すオブジェクトが返される
    """
    update_func: MagicMock = mocker.patch.object(data_store.users, "reset_survival_bonus")
    reset_survival_bonus()
    update_func.assert_called_once()
