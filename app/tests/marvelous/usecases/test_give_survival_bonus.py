import pytest_mock
import pytest
from unittest.mock import MagicMock
import src.marvelous.usecases.give_survival_bonus as target_package
from src.marvelous.usecases.give_survival_bonus import *
from dataclasses import dataclass


@dataclass()
class ApplyCase:
    give_point: int
    before_point: int
    after_point: int


apply_cases = [
    ApplyCase(give_point=1, before_point=0, after_point=1),
    ApplyCase(give_point=-5, before_point=2, after_point=-3),
    ApplyCase(give_point=0, before_point=2, after_point=2),
]


@pytest.mark.parametrize("case", apply_cases)
def test_apply(case: ApplyCase, mocker: pytest_mock.MockerFixture):
    """
    apply() が正しい値を返すか検証する
    """
    user: MagicMock = mocker.Mock(spec_set=["point", "survival_bonus_given"])
    user.point = case.before_point
    user.survival_bonus_given = False

    apply(user, case.give_point)

    assert user.point == case.after_point
    assert user.survival_bonus_given


def test_give_survival_bonus_false(mocker: pytest_mock.MockerFixture):
    discord_id: MagicMock = mocker.Mock()
    give_point: MagicMock = mocker.Mock()
    user: MagicMock = mocker.Mock()
    user.survival_bonus_given = True
    get_func: MagicMock = mocker.patch.object(target_package, "get_user", return_value=user)
    update_func: MagicMock = mocker.patch.object(data_store.users, "update")

    result = give_survival_bonus(discord_id, give_point)

    get_func.assert_called_once_with(discord_id)
    update_func.assert_not_called()
    assert not result


def test_give_survival_bonus_true(mocker: pytest_mock.MockerFixture):
    discord_id: MagicMock = mocker.Mock()
    give_point: MagicMock = mocker.Mock()
    user: MagicMock = mocker.Mock()
    user.survival_bonus_given = False
    get_func: MagicMock = mocker.patch.object(target_package, "get_user", return_value=user)
    apply_func: MagicMock = mocker.patch.object(target_package, "apply", return_value=user)
    update_func: MagicMock = mocker.patch.object(data_store.users, "update")

    result = give_survival_bonus(discord_id, give_point)

    get_func.assert_called_once_with(discord_id)
    apply_func.assert_called_once_with(user, give_point)
    update_func.assert_called_once_with(user)
    assert result
