import pytest
import pytest_mock
from unittest.mock import MagicMock
import src.marvelous.models.user as target_package
from src.marvelous.models.user import *


@pytest.fixture()
def ranked_users() -> Iterable[User]:
    return [
        User(discord_id=2, point=40),
        User(discord_id=3, point=21),
        User(discord_id=0, point=21),
        User(discord_id=4, point=0),
        User(discord_id=1, point=-2)
    ]


def test_get_ranking_succeed(mocker: pytest_mock.MockerFixture, ranked_users: Iterable[User]):
    """
    データストアからランキングが返された場合に、結果として成功を表すオブジェクトが返される
    """
    get_func: MagicMock = mocker.patch.object(data_store.users, "get_marvelous_point_ranking",
                                              return_value=ranked_users)
    result = get_ranking()
    get_func.assert_called_once()
    assert ranked_users == result, "返されるランキングが正しい"


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


def test_register_user_failed_already_exist(mocker: pytest_mock.MockerFixture):
    user: MagicMock = mocker.Mock()
    user.discord_id = mocker.Mock()
    get_func: MagicMock = mocker.patch.object(target_package, "is_user_exist", return_value=True)
    create_func: MagicMock = mocker.patch.object(data_store.users, "create")

    with pytest.raises(AlreadyExistError) as e:
        register_user(user)

    get_func.assert_called_once_with(user.discord_id)
    create_func.assert_not_called()
    assert e.value.user_id == user.discord_id


def test_register_user_succeed(mocker: pytest_mock.MockerFixture):
    user: MagicMock = mocker.Mock()
    user.discord_id = mocker.Mock()
    get_func: MagicMock = mocker.patch.object(target_package, "is_user_exist", return_value=False)
    create_func: MagicMock = mocker.patch.object(data_store.users, "create")

    register_user(user)

    get_func.assert_called_once_with(user.discord_id)
    create_func.assert_called_once_with(user)


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
