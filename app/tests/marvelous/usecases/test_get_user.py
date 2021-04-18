import pytest
import pytest_mock
from unittest.mock import MagicMock


def test_is_user_exist_true(mocker: pytest_mock.MockerFixture):
    discord_id = 0
    mocker.patch.object(data_store.users, "get_by_id", return_value=mocker.Mock())
    result: bool = is_user_exist(discord_id)
    assert result


def test_is_user_exist_false(mocker: pytest_mock.MockerFixture):
    discord_id = 0
    mocker.patch.object(data_store.users, "get_by_id", return_value=None)
    result: bool = is_user_exist(discord_id)
    assert not result


def test_get_user_failed_not_found(mocker: pytest_mock.MockerFixture):
    """
    データストアからNoneが返された場合に、結果として「ユーザーがいない」ことを示すオブジェクトが返される
    """
    discord_id = 0
    get_func: MagicMock = mocker.patch.object(data_store.users, "get_by_id", return_value=None)

    with pytest.raises(UserNotFoundError) as e:
        get_user(discord_id=discord_id)

    get_func.assert_called_once_with(discord_id)
    assert e.value.user_id == discord_id


def test_get_user_succeed(mocker: pytest_mock.MockerFixture):
    """
    データストアからユーザーが返された場合に、結果として成功を表すオブジェクトが返される
    """
    discord_id = 0
    user: MagicMock = mocker.Mock()
    get_func: MagicMock = mocker.patch.object(data_store.users, "get_by_id", return_value=user)

    result = get_user(discord_id)

    get_func.assert_called_once_with(discord_id)
    assert result == user, "返されるユーザーが正しい"
