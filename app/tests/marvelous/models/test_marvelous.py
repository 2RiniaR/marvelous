import pytest
import pytest_mock
from src.marvelous.models.marvelous import *
from dataclasses import dataclass


@pytest.fixture()
def settings():
    return MarvelousSettings(
        daily_step_limit=10,
        steps_per_bonus=5,
        sender_bonus_point=1,
        receiver_point=1
    )


@dataclass()
class SendCase:
    # 入力パラメータ
    before_sender_point: int
    before_receiver_point: int
    after_sender_point: int
    after_receiver_point: int
    bonus: int
    expected_send_result: MarvelousResult
    expected_cancel_result: MarvelousResult


send_cases = {
    "no bonus":
        SendCase(
            before_sender_point=10, before_receiver_point=10,
            after_sender_point=10, after_receiver_point=11,
            bonus=0,
            expected_send_result=MarvelousResult(sender_bonus_diff=0, sender_point_diff=0, receiver_point_diff=1),
            expected_cancel_result=MarvelousResult(sender_bonus_diff=0, sender_point_diff=0, receiver_point_diff=-1)
        ),
    "with bonus":
        SendCase(
            before_sender_point=10, before_receiver_point=10,
            after_sender_point=11, after_receiver_point=11,
            bonus=1,
            expected_send_result=MarvelousResult(sender_bonus_diff=1, sender_point_diff=1, receiver_point_diff=1),
            expected_cancel_result=MarvelousResult(sender_bonus_diff=-1, sender_point_diff=-1, receiver_point_diff=-1)
        ),
}


@pytest.mark.parametrize("case", send_cases.values(), ids=send_cases.keys())
def test_send(case: SendCase, settings: MarvelousSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.before_sender_point
    sender.marvelous_bonus.add_step = mocker.Mock(return_value=case.bonus)
    receiver = mocker.Mock()
    receiver.point = case.before_receiver_point
    marvelous: MarvelousReaction = MarvelousReaction(settings)

    marvelous.send(sender, receiver)

    sender.marvelous_bonus.add_step.assert_called_once_with(
        step=1,
        today_limit=settings.daily_step_limit,
        step_interval=settings.steps_per_bonus
    )
    assert sender.point == case.after_sender_point
    assert receiver.point == case.after_receiver_point
    assert marvelous.result == case.expected_send_result


@pytest.mark.parametrize("case", send_cases.values(), ids=send_cases.keys())
def test_cancel(case: SendCase, settings: MarvelousSettings, mocker: pytest_mock.MockerFixture):
    sender = mocker.Mock()
    sender.point = case.after_sender_point
    sender.marvelous_bonus.add_step = mocker.Mock(return_value=-case.bonus)
    receiver = mocker.Mock()
    receiver.point = case.after_receiver_point
    marvelous: MarvelousReaction = MarvelousReaction(settings)

    marvelous.cancel(sender, receiver)

    sender.marvelous_bonus.add_step.assert_called_once_with(
        step=-1,
        today_limit=settings.daily_step_limit,
        step_interval=settings.steps_per_bonus
    )
    assert sender.point == case.before_sender_point
    assert receiver.point == case.before_receiver_point
    assert marvelous.result == case.expected_cancel_result
