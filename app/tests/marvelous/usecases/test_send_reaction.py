import pytest_mock
import pytest
from unittest.mock import MagicMock, call
import src.marvelous.usecases.send_reaction as target_package
from src.marvelous.usecases.send_reaction import *


def test_check_self_user_failed(mocker: pytest_mock.MockerFixture):
    sender_id: MagicMock = mocker.Mock()
    with pytest.raises(SelfUserActionError) as e:
        check_self_user(sender_id, sender_id)
    assert e.value.user_id == sender_id


def test_check_self_user_succeed(mocker: pytest_mock.MockerFixture):
    sender_id: MagicMock = mocker.Mock()
    receiver_id: MagicMock = mocker.Mock()
    check_self_user(sender_id, receiver_id)


def test_update_reaction_forward(mocker: pytest_mock.MockerFixture):
    sender_id: MagicMock = mocker.Mock()
    receiver_id: MagicMock = mocker.Mock()
    reaction: MagicMock = mocker.Mock()
    reaction.send = mocker.Mock()
    sender: MagicMock = mocker.Mock()
    receiver: MagicMock = mocker.Mock()
    check_self_func: MagicMock = mocker.patch.object(target_package, "check_self_user")

    def dummy_get_user(user_id):
        if user_id == sender_id:
            return sender
        elif user_id == receiver_id:
            return receiver
        else:
            pytest.fail()

    get_func: MagicMock = mocker.patch.object(target_package, "get_user", side_effect=dummy_get_user)
    update_func: MagicMock = mocker.patch.object(data_store.users, "update")

    update_reaction(sender_id, receiver_id, reaction, True)

    check_self_func.assert_called_once_with(sender_id, receiver_id)
    get_func.assert_has_calls(calls=[call(sender_id), call(receiver_id)])
    reaction.send.assert_called_once_with(sender, receiver)
    update_func.assert_has_calls(calls=[call(sender), call(receiver)])


def test_update_reaction_backward(mocker: pytest_mock.MockerFixture):
    sender_id: MagicMock = mocker.Mock()
    receiver_id: MagicMock = mocker.Mock()
    reaction: MagicMock = mocker.Mock()
    reaction.cancel = mocker.Mock()
    sender: MagicMock = mocker.Mock()
    receiver: MagicMock = mocker.Mock()
    check_self_func: MagicMock = mocker.patch.object(target_package, "check_self_user")

    def dummy_get_user(user_id):
        if user_id == sender_id:
            return sender
        elif user_id == receiver_id:
            return receiver
        else:
            pytest.fail()

    get_func: MagicMock = mocker.patch.object(target_package, "get_user", side_effect=dummy_get_user)
    update_func: MagicMock = mocker.patch.object(data_store.users, "update")

    update_reaction(sender_id, receiver_id, reaction, False)

    check_self_func.assert_called_once_with(sender_id, receiver_id)
    get_func.assert_has_calls(calls=[call(sender_id), call(receiver_id)])
    reaction.cancel.assert_called_once_with(sender, receiver)
    update_func.assert_has_calls(calls=[call(sender), call(receiver)])
