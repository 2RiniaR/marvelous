import pytest_mock
import pytest
from unittest.mock import MagicMock
import marvelous.models.services.register_user as target_package


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
