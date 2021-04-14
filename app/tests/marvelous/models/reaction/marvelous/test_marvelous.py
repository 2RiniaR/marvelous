import pytest
import pytest_mock
import src.marvelous.models.reaction.marvelous.marvelous as target_package
from src.marvelous.models.reaction.marvelous.marvelous import *
from dataclasses import dataclass


@dataclass()
class SendCase:
    # 入力パラメータ
    sender_point: int
    receiver_point: int
    settings: MarvelousSettings

    # ダミーパラーメータ
    bonus: int

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: MarvelousResult


add_step_cases = {
    "case0":
        SendCase(
            sender_point=0, receiver_point=0,
            settings=MarvelousSettings(daily_step_limit=10, steps_per_bonus=5, sender_bonus_point=1, receiver_point=1),
            bonus=0,
            expected_sender_point=0, expected_receiver_point=1,
            expected_result=MarvelousResult(sender_bonus_diff=0, sender_point_diff=0, receiver_point_diff=1)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_send(case: SendCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.marvelous_bonus.add_step = mocker.Mock(return_value=case.bonus)
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    marvelous: MarvelousReaction = MarvelousReaction(case.settings)

    marvelous.send(sender, receiver)

    sender.marvelous_bonus.add_step.assert_called_once_with(
        step=1,
        today_limit=case.settings.daily_step_limit,
        step_interval=case.settings.steps_per_bonus
    )
    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert marvelous.result == case.expected_result



@dataclass()
class CancelCase:
    # 入力パラメータ
    sender_point: int
    receiver_point: int
    settings: MarvelousSettings

    # ダミーパラーメータ
    bonus: int

    # 出力パラメータ
    expected_sender_point: int
    expected_receiver_point: int
    expected_result: MarvelousResult


add_step_cases = {
    "case0":
        CancelCase(
            sender_point=0, receiver_point=1,
            settings=MarvelousSettings(daily_step_limit=10, steps_per_bonus=5, sender_bonus_point=1, receiver_point=1),
            bonus=0,
            expected_sender_point=0, expected_receiver_point=0,
            expected_result=MarvelousResult(sender_bonus_diff=0, sender_point_diff=0, receiver_point_diff=-1)
        )
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_cancel(case: CancelCase, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.sender_point
    sender.marvelous_bonus.add_step = mocker.Mock(return_value=case.bonus)
    receiver = mocker.Mock()
    receiver.point = case.receiver_point
    marvelous: MarvelousReaction = MarvelousReaction(case.settings)

    marvelous.cancel(sender, receiver)

    sender.marvelous_bonus.add_step.assert_called_once_with(
        step=-1,
        today_limit=case.settings.daily_step_limit,
        step_interval=case.settings.steps_per_bonus
    )
    assert sender.point == case.expected_sender_point
    assert receiver.point == case.expected_receiver_point
    assert marvelous.result == case.expected_result
