import dataclasses


SENT_MARVELOUS_COUNT_BONUS_INTERVAL = 5
SENT_MARVELOUS_COUNT_BONUS_DAY_LIMIT = 10
SENT_BOO_COUNT_BONUS_INTERVAL = 5
SENT_BOO_COUNT_BONUS_DAY_LIMIT = 10

SENT_MARVELOUS_BONUS_POINT = 1
RECEIVE_MARVELOUS_POINT = 1
SENT_SUPER_MARVELOUS_POINT = 1
RECEIVE_SUPER_MARVELOUS_POINT = 10
SENT_BOO_BONUS_POINT = -1
RECEIVE_BOO_POINT = -1


@dataclasses.dataclass
class User:
    discord_id: str
    twitter_id: str = ""
    github_id: str = ""
    marvelous: int = 0
    sent_marvelous_count: int = 0
    today_sent_marvelous_bonus_count: int = 0
    sent_boo_count: int = 0
    today_sent_boo_bonus_count: int = 0
    sleeping: bool = False
    super_marvelous_left_count: int = 0

    def reset_bonus(self):
        self.today_sent_boo_bonus_count = 0
        self.today_sent_marvelous_bonus_count = 0

    def send_marvelous(self):
        self.sent_marvelous_count += 1
        if self.today_sent_marvelous_bonus_count >= SENT_MARVELOUS_COUNT_BONUS_DAY_LIMIT:
            return

        self.today_sent_marvelous_bonus_count += 1
        if self.sent_marvelous_count >= SENT_MARVELOUS_COUNT_BONUS_INTERVAL:
            self._give_sent_marvelous_bonus()

    def _give_sent_marvelous_bonus(self):
        self.set_marvelous(self.marvelous + SENT_MARVELOUS_BONUS_POINT)
        self.sent_marvelous_count = 0

    def receive_marvelous(self):
        self.set_marvelous(self.marvelous + RECEIVE_MARVELOUS_POINT)

    def send_super_marvelous(self) -> (bool, str):
        if self.super_marvelous_left_count <= 0:
            return False, "「めっちゃえらい」の残り数が0です"
        self.set_marvelous(self.marvelous + SENT_SUPER_MARVELOUS_POINT)
        return True, ""

    def receive_super_marvelous(self):
        self.set_marvelous(self.marvelous + RECEIVE_SUPER_MARVELOUS_POINT)

    def send_boo(self):
        self.sent_boo_count += 1
        if self.today_sent_boo_bonus_count >= SENT_BOO_COUNT_BONUS_DAY_LIMIT:
            return

        self.today_sent_boo_bonus_count += 1
        if self.sent_boo_count >= SENT_BOO_COUNT_BONUS_INTERVAL:
            self._give_sent_boo_bonus()

    def receive_boo(self):
        self.set_marvelous(self.marvelous + RECEIVE_BOO_POINT)

    def _give_sent_boo_bonus(self):
        self.set_marvelous(self.marvelous + SENT_BOO_BONUS_POINT)
        self.sent_boo_count = 0

    def set_marvelous(self, value: int):
        self.marvelous = max(0, value)

