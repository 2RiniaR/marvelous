import pytest
import pytest_mock
import src.marvelous.models.reaction.booing.booing as target_package
from src.marvelous.models.reaction.booing.booing import *
from dataclasses import dataclass


@dataclass()
class SendCase:
    # 入力パラメータ
    sender_point: int
    receiver_point: int
    settings: BooingSettings

    # ダミーパラーメータ
    penalty: int

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: BooingResult


add_step_cases = {
    "case0":
        SendCase(
            sender_point=0, receiver_point=1,
            settings=BooingSettings(daily_step_limit=10, steps_per_bonus=5, sender_bonus_point=-1, receiver_point=-1),
            penalty=0,
            expected_sender_point=0, expected_receiver_point=0,
            expected_result=BooingResult(sender_penalty_diff=0, sender_point_diff=0, receiver_point_diff=-1)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_send(case: SendCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.booing_penalty.add_step = mocker.Mock(return_value=case.penalty)
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    booing: BooingReaction = BooingReaction(case.settings)

    booing.send(sender, receiver)

    sender.booing_penalty.add_step.assert_called_once_with(
        step=1,
        today_limit=case.settings.daily_step_limit,
        step_interval=case.settings.steps_per_bonus
    )
    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert booing.result == case.expected_result



@dataclass()
class CancelCase:
    # 入力パラメータ
    sender_point: int
    receiver_point: int
    settings: BooingSettings

    # ダミーパラーメータ
    penalty: int

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: BooingResult


add_step_cases = {
    "case0":
        CancelCase(
            sender_point=0, receiver_point=0,
            settings=BooingSettings(daily_step_limit=10, steps_per_bonus=5, sender_bonus_point=-1, receiver_point=-1),
            penalty=0,
            expected_sender_point=0, expected_receiver_point=1,
            expected_result=BooingResult(sender_penalty_diff=0, sender_point_diff=0, receiver_point_diff=1)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_cancel(case: CancelCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.booing_penalty.add_step = mocker.Mock(return_value=case.penalty)
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    booing: BooingReaction = BooingReaction(case.settings)

    booing.cancel(sender, receiver)

    sender.booing_penalty.add_step.assert_called_once_with(
        step=-1,
        today_limit=case.settings.daily_step_limit,
        step_interval=case.settings.steps_per_bonus
    )
    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert booing.result == case.expected_result
