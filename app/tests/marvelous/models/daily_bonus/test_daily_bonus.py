import pytest
import pytest_mock
import src.marvelous.models.daily_bonus.daily_bonus as target_package
from src.marvelous.models.daily_bonus.daily_bonus import *
from dataclasses import dataclass


@dataclass()
class GetMaxAvailableStepArgs:
    current: int
    add: int
    limit: int


get_max_available_step_cases = {
    "case0": (GetMaxAvailableStepArgs(current=3, add=4, limit=12), 4),
    "case1": (GetMaxAvailableStepArgs(current=7, add=5, limit=10), 3),
    "case2": (GetMaxAvailableStepArgs(current=13, add=4, limit=9), 0),
    "case3": (GetMaxAvailableStepArgs(current=7, add=-5, limit=5), -3),
    "case4": (GetMaxAvailableStepArgs(current=9, add=-2, limit=15), -2),
    "case5": (GetMaxAvailableStepArgs(current=3, add=-6, limit=12), -3),
    "case6": (GetMaxAvailableStepArgs(current=8, add=4, limit=8), 0),
    "case7": (GetMaxAvailableStepArgs(current=12, add=-3, limit=12), -3),
    "case8": (GetMaxAvailableStepArgs(current=0, add=0, limit=0), 0)
}


@pytest.mark.parametrize(
    "args, expected",
    get_max_available_step_cases.values(),
    ids=get_max_available_step_cases.keys()
)
def test_get_max_available_step(args: GetMaxAvailableStepArgs, expected: int):
    assert get_max_available_step(args.current, args.add, args.limit) == expected


@dataclass()
class AddStepCase:
    # 入力パラメータ
    before_self: DailyBonus
    step: int
    today_limit: int
    step_interval: int

    # ダミーパラーメータ
    max_available_step: int

    # 出力パラメータ
    expected_self: DailyBonus
    expected_return_value: int


add_step_cases = {
    "case0":
        AddStepCase(before_self=DailyBonus(step=0, today=0), step=1, today_limit=10, step_interval=5,
                    max_available_step=1, expected_self=DailyBonus(step=1, today=1), expected_return_value=0),
    "case1":
        AddStepCase(before_self=DailyBonus(step=4, today=1), step=3, today_limit=10, step_interval=5,
                    max_available_step=3, expected_self=DailyBonus(step=2, today=4), expected_return_value=1),
    "case2":
        AddStepCase(before_self=DailyBonus(step=3, today=10), step=2, today_limit=10, step_interval=5,
                    max_available_step=0, expected_self=DailyBonus(step=3, today=12), expected_return_value=0),
    "case3":
        AddStepCase(before_self=DailyBonus(step=4, today=3), step=-1, today_limit=10, step_interval=5,
                    max_available_step=-1, expected_self=DailyBonus(step=3, today=2), expected_return_value=0),
    "case4":
        AddStepCase(before_self=DailyBonus(step=1, today=7), step=-3, today_limit=10, step_interval=5,
                    max_available_step=-3, expected_self=DailyBonus(step=3, today=4), expected_return_value=-1),
    "case5":
        AddStepCase(before_self=DailyBonus(step=4, today=1), step=-3, today_limit=10, step_interval=5,
                    max_available_step=-3, expected_self=DailyBonus(step=1, today=0), expected_return_value=0),
    "case6":
        AddStepCase(before_self=DailyBonus(step=0, today=0), step=0, today_limit=10, step_interval=5,
                    max_available_step=0, expected_self=DailyBonus(step=0, today=0), expected_return_value=0),
}


@pytest.mark.parametrize("case", add_step_cases.values(), ids=add_step_cases.keys())
def test_add_step(case: AddStepCase, mocker: pytest_mock.MockerFixture):
    mocker.patch.object(target_package, "get_max_available_step", return_value=case.max_available_step)

    return_value = case.before_self.add_step(
        step=case.step, today_limit=case.today_limit, step_interval=case.step_interval)

    assert case.before_self == case.expected_self
    assert return_value == case.expected_return_value
