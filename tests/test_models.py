import pytest
from app.models import Node, Relation, GraphSegment
from pydantic import ValidationError


# Тест для модели Node
def test_node_validation():
    # Правильные данные
    node_data = {"id": "1", "label": "User"}
    node = Node(**node_data)
    assert node.id == "1"
    assert node.label == "User"

    # Данные с отсутствующим id (должен быть исключение)
    with pytest.raises(ValidationError):
        Node(id=None)

    # Данные с неправильным типом id (должен быть исключение)
    with pytest.raises(ValidationError):
        Node(id=123)  # id должен быть строкой


# Тест для модели Relation
def test_relation_validation():
    # Правильные данные
    relation_data = {"start_id": "1", "end_id": "2", "type": "follow"}
    relation = Relation(**relation_data)
    assert relation.start_id == "1"
    assert relation.end_id == "2"
    assert relation.type == "follow"

    # Данные с отсутствующим типом
    with pytest.raises(ValidationError):
        Relation(start_id="1", end_id="2", type=None)

    # Данные с неправильным типом
    with pytest.raises(ValidationError):
        Relation(start_id="1", end_id="2", type=123)  # type должен быть строкой


def test_graph_segment_validation():
    # Правильные данные
    segment_data = {
        "users": [{"id": "1"}],
        "groups": [{"id": "2"}],
        "relations": [{"start_id": "1", "end_id": "2", "type": "follow"}]
    }
    segment = GraphSegment(**segment_data)
    assert len(segment.users) == 1
    assert len(segment.groups) == 1
    assert len(segment.relations) == 1

    # Данные с отсутствующими обязательными полями (не переданы "users" или "groups")
    with pytest.raises(ValidationError):
        GraphSegment(relations=[
            {"start_id": "1", "end_id": "2", "type": "follow"}])  # Ошибка из-за отсутствия "users" и "groups"

