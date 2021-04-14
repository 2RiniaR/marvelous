import pytest
import pytest_mock
from src.marvelous.models.reaction.super_marvelous.super_marvelous import *
from dataclasses import dataclass


@pytest.fixture()
def settings():
    return SuperMarvelousSettings(
        sender_point=1,
        receiver_point=5
    )


@dataclass()
class SendCase:
    before_sender_point: int
    before_sender_super_marvelous_left: int
    before_receiver_point: int

    after_sender_point: int
    after_sender_super_marvelous_left: int
    after_receiver_point: int

    expected_send_result: SuperMarvelousResult
    expected_cancel_result: SuperMarvelousResult


add_step_cases = {
    "no left count":
        SendCase(
            before_sender_point=0, before_sender_super_marvelous_left=0, before_receiver_point=0,
            after_sender_point=0, after_sender_super_marvelous_left=-1, after_receiver_point=0,
            expected_send_result=SuperMarvelousResult(sender_point_diff=0, receiver_point_diff=0, no_left_count=True),
            expected_cancel_result=SuperMarvelousResult(sender_point_diff=0, receiver_point_diff=0, no_left_count=True)
        ),
    "normal":
        SendCase(
            before_sender_point=0, before_sender_super_marvelous_left=1, before_receiver_point=0,
            after_sender_point=1, after_sender_super_marvelous_left=0, after_receiver_point=5,
            expected_send_result=SuperMarvelousResult(sender_point_diff=1, receiver_point_diff=5, no_left_count=False),
            expected_cancel_result=SuperMarvelousResult(sender_point_diff=-1, receiver_point_diff=-5, no_left_count=False)
        ),
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_send(case: SendCase, settings: SuperMarvelousSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.before_sender_point
    sender.super_marvelous_left = case.before_sender_super_marvelous_left
    receiver = mocker.Mock()
    receiver.point = case.before_receiver_point
    super_marvelous: SuperMarvelousReaction = SuperMarvelousReaction(settings)

    super_marvelous.send(sender, receiver)

    assert sender.point == case.after_sender_point
    assert sender.super_marvelous_left == case.after_sender_super_marvelous_left
    assert receiver.point == case.after_receiver_point
    assert super_marvelous.result == case.expected_send_result


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_cancel(case: SendCase, settings: SuperMarvelousSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.after_sender_point
    sender.super_marvelous_left = case.after_sender_super_marvelous_left
    receiver = mocker.Mock()
    receiver.point = case.after_receiver_point
    super_marvelous: SuperMarvelousReaction = SuperMarvelousReaction(settings)

    super_marvelous.cancel(sender, receiver)

    assert sender.point == case.before_sender_point
    assert sender.super_marvelous_left == case.before_sender_super_marvelous_left
    assert receiver.point == case.before_receiver_point
    assert super_marvelous.result == case.expected_cancel_result
