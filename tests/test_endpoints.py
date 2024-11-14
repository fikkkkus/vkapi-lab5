import pytest
from httpx import AsyncClient

from app.auth import TOKEN
from app.main import app


# Тест для получения всех узлов
@pytest.mark.asyncio
async def test_get_all_nodes():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nodes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Тест для получения узла по ID с его связями
@pytest.mark.asyncio
async def test_get_node_with_relations():
    node_id = "280297099"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/nodes/{node_id}")

    assert response.status_code == 200
    node = response.json()

    # Correcting the access to match the data structure
    assert str(node[0]["node"]["id"]) == node_id


@pytest.mark.asyncio
async def test_add_graph_segment():
    segment_data = {
        "users": [{"id": "1"}, {"id": "2"}],
        "groups": [{"id": "3"}],
        "relations": [
            {"start_id": "1", "end_id": "2", "type": "follow"},
            {"start_id": "2", "end_id": "3", "type": "subscribe"}
        ]
    }

    # Подготовка и выполнение запроса с использованием client.request()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.request(
            method="POST",
            url="/add/nodes/",
            json=segment_data,  # передаем данные как JSON
            headers={
                "Authorization": f"Bearer {TOKEN}",  # если требуется авторизация
                "Content-Type": "application/json"  # указываем, что тело в формате JSON
            }
        )

    # Проверка результата
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Segment added successfully"

# Тест для удаления графа
@pytest.mark.asyncio
async def test_delete_graph_segment():
    node_ids = ["1", "2"]
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.request(
            method="DELETE",
            url="/delete/nodes/",
            json=node_ids,  # передаем данные как JSON
            headers={
                "Authorization": f"Bearer {TOKEN}",  # если требуется авторизация
                "Content-Type": "application/json"  # указываем, что тело в формате JSON
            }
        )

    # Проверка ответа
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert isinstance(response_data, dict)

