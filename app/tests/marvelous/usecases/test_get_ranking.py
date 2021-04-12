import pytest
import pytest_mock
from unittest.mock import MagicMock
from src.marvelous.usecases.get_ranking import *


@pytest.fixture()
def ranked_users() -> Iterable[User]:
    return [
        User(discord_id=2, point=40),
        User(discord_id=3, point=21),
        User(discord_id=0, point=21),
        User(discord_id=4, point=0),
        User(discord_id=1, point=-2)
    ]


def test_get_ranking_succeed(mocker: pytest_mock.MockerFixture, ranked_users: Iterable[User]):
    """
    データストアからランキングが返された場合に、結果として成功を表すオブジェクトが返される
    """
    get_func: MagicMock = mocker.patch.object(data_store.users, "get_marvelous_point_ranking",
                                              return_value=ranked_users)
    result = get_ranking()
    get_func.assert_called_once()
    assert ranked_users == result, "返されるランキングが正しい"
