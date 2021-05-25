from dataclasses import dataclass


@dataclass()
class DailyBonus:
    step: int = None
    today: int = None

    def add_step(self, step: int, today_limit: int, step_interval: int) -> int:
        """カウントを進めて、発生したボーナスの回数を返す"""
        available_step = self.get_max_available_step(self.today, step, today_limit)
        self.today = max(0, self.today + step)
        loop = (self.step + available_step) // step_interval
        self.step = (self.step + available_step) % step_interval
        return loop

    @staticmethod
    def get_max_available_step(current: int, add: int, limit: int) -> int:
        if current < 0:
            raise ValueError(f"Current({current}) must be larger then 0.")
        if limit < 0:
            raise ValueError(f"Limit({limit}) must be larger then 0.")

        total = current + add

        if limit <= current and limit <= total:
            return 0
        if current <= limit and total <= limit:
            return max(-current, add)
        if current <= limit <= total:
            return max(0, limit - current)
        if total <= limit <= current:
            return total - limit

        raise ArithmeticError("Unknown state.")
