import pytest
import pytest_mock
import src.marvelous.models.reaction.super_marvelous.super_marvelous as target_package
from src.marvelous.models.reaction.super_marvelous.super_marvelous import *
from dataclasses import dataclass


@dataclass()
class SendCase:
    # 入力パラメータ
    sender_point: int
    sender_super_marvelous_left: int
    receiver_point: int
    settings: SuperMarvelousSettings

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: SuperMarvelousResult


add_step_cases = {
    "no left count":
        SendCase(
            sender_point=0, sender_super_marvelous_left=0, receiver_point=0,
            settings=SuperMarvelousSettings(sender_point=1, receiver_point=5),
            expected_sender_point=0, expected_receiver_point=0,
            expected_result=SuperMarvelousResult(sender_point_diff=0, receiver_point_diff=0, no_left_count=True)
        ),
    "normal":
        SendCase(
            sender_point=0, sender_super_marvelous_left=1, receiver_point=0,
            settings=SuperMarvelousSettings(sender_point=1, receiver_point=5),
            expected_sender_point=1, expected_receiver_point=5,
            expected_result=SuperMarvelousResult(sender_point_diff=1, receiver_point_diff=5, no_left_count=False)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_send(case: SendCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.super_marvelous_left = case.sender_super_marvelous_left
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    super_marvelous: SuperMarvelousReaction = SuperMarvelousReaction(case.settings)

    super_marvelous.send(sender, receiver)

    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert super_marvelous.result == case.expected_result


@dataclass()
class CancelCase:
    # 入力パラメータ
    sender_point: int
    sender_super_marvelous_left: int
    receiver_point: int
    settings: SuperMarvelousSettings

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: SuperMarvelousResult


add_step_cases = {
    "no left count":
        SendCase(
            sender_point=0, sender_super_marvelous_left=-1, receiver_point=0,
            settings=SuperMarvelousSettings(sender_point=1, receiver_point=5),
            expected_sender_point=0, expected_receiver_point=0,
            expected_result=SuperMarvelousResult(sender_point_diff=0, receiver_point_diff=0, no_left_count=True)
        ),
    "normal":
        SendCase(
            sender_point=1, sender_super_marvelous_left=0, receiver_point=5,
            settings=SuperMarvelousSettings(sender_point=1, receiver_point=5),
            expected_sender_point=0, expected_receiver_point=0,
            expected_result=SuperMarvelousResult(sender_point_diff=-1, receiver_point_diff=-5, no_left_count=False)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_cancel(case: CancelCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.super_marvelous_left = case.sender_super_marvelous_left
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    super_marvelous: SuperMarvelousReaction = SuperMarvelousReaction(case.settings)

    super_marvelous.cancel(sender, receiver)

    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert super_marvelous.result == case.expected_result
