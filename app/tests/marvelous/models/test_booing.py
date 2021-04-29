import pytest
import pytest_mock
from src.marvelous.models.booing import *
from dataclasses import dataclass


@pytest.fixture()
def settings():
    return BooingSettings(
        daily_step_limit=10,
        steps_per_bonus=5,
        sender_bonus_point=-1,
        receiver_point=-1
    )


@dataclass()
class SendCase:
    # 入力パラメータ
    before_sender_point: int
    before_receiver_point: int
    after_sender_point: int
    after_receiver_point: int
    penalty: int
    expected_send_result: BooingResult
    expected_cancel_result: BooingResult


send_cases = {
    "no penalty":
        SendCase(
            before_sender_point=10, before_receiver_point=10,
            after_sender_point=10, after_receiver_point=9,
            penalty=0,
            expected_send_result=BooingResult(sender_penalty_diff=0, sender_point_diff=0, receiver_point_diff=-1),
            expected_cancel_result=BooingResult(sender_penalty_diff=0, sender_point_diff=0, receiver_point_diff=1)
        ),
    "with penalty":
        SendCase(
            before_sender_point=10, before_receiver_point=10,
            after_sender_point=9, after_receiver_point=9,
            penalty=1,
            expected_send_result=BooingResult(sender_penalty_diff=1, sender_point_diff=-1, receiver_point_diff=-1),
            expected_cancel_result=BooingResult(sender_penalty_diff=-1, sender_point_diff=1, receiver_point_diff=1)
        ),
}


@pytest.mark.parametrize("case", send_cases.values(), ids=send_cases.keys())
def test_send(case: SendCase, settings: BooingSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.before_sender_point
    sender.booing_penalty.add_step = mocker.Mock(return_value=case.penalty)
    receiver = mocker.Mock()
    receiver.point = case.before_receiver_point
    booing: BooingReaction = BooingReaction(settings)

    booing.send(sender, receiver)

    sender.booing_penalty.add_step.assert_called_once_with(
        step=1,
        today_limit=settings.daily_step_limit,
        step_interval=settings.steps_per_bonus
    )
    assert sender.point == case.after_sender_point
    assert receiver.point == case.after_receiver_point
    assert booing.result == case.expected_send_result


@pytest.mark.parametrize("case", send_cases.values(), ids=send_cases.keys())
def test_cancel(case: SendCase, settings: BooingSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.after_sender_point
    sender.booing_penalty.add_step = mocker.Mock(return_value=-case.penalty)
    receiver = mocker.Mock()
    receiver.point = case.after_receiver_point
    booing: BooingReaction = BooingReaction(settings)

    booing.cancel(sender, receiver)

    sender.booing_penalty.add_step.assert_called_once_with(
        step=-1,
        today_limit=settings.daily_step_limit,
        step_interval=settings.steps_per_bonus
    )
    assert sender.point == case.before_sender_point
    assert receiver.point == case.before_receiver_point
    assert booing.result == case.expected_cancel_result
