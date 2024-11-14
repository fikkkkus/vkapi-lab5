from typing import List, Optional

from pydantic import BaseModel

class Node(BaseModel):
    id: str
    label: Optional[str] = None

class Relation(BaseModel):
    start_id: str
    end_id: str
    type: str  # 'follow' или 'subscribe'

class GraphSegment(BaseModel):
    users: List[Node]  # Обязательное поле, больше не имеет значения по умолчанию []
    groups: List[Node]  # Обязательное поле, больше не имеет значения по умолчанию []
    relations: List[Relation]  # Обязательное поле
