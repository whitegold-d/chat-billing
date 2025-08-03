from dataclasses import dataclass


@dataclass
class MoveTransactionRequest:
    token_giving_user_id: str
    token_taking_user_id: str
    value: int