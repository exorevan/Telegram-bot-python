from dataclasses import dataclass

from loc_types.question import Question


@dataclass
class PersonAndQuestion:
    """
    A class representing a person and their question.
    """

    nickname: str
    question_count: int = 0
    question: Question | None = None
    question_pack_number: int = 0

    def __post_init__(self):
        if not self.nickname:
            raise ValueError("Nickname must be a non-empty string.")
