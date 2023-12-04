from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """
    Represents a question with multiple choice answers.
    """

    formul: str
    number_of_answers: int
    answers: List[str]
    right_answer: str

    def is_answer_correct(self, answer: str) -> bool:
        """
        Checks if the given answer is correct.
        """
        return answer.lower() == self.right_answer.lower()
