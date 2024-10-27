import requests
import json
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


# Основные данные пользователя и подписок
class UserData:
    def __init__(self, user_id, first_name, last_name, followers, subscriptions_users, subscriptions_groups):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.followers = followers
        self.subscriptions_users = subscriptions_users
        self.subscriptions_groups = subscriptions_groups


def get_data_from_vk(method, params):
    url = f"https://api.vk.com/method/{method}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Проблемы с HTTP
    except ConnectionError:
        print("Error connecting to the server. Please check your internet connection.")
    except Timeout:
        print("Request timed out. Please try again later.")
    except RequestException as req_err:
        print(f"An error occurred: {req_err}")  # Другие ошибки запроса
    return None  # Возвращаем None в случае ошибки


# Основной метод для получения данных о пользователе
def fetch_user_data(user_id, access_token):
    params = {
        "v": "5.131",
        "access_token": access_token,
        "user_ids": user_id,
        "fields": "followers_count"
    }

    user_info = get_data_from_vk("users.get", params)
    if not user_info or 'response' not in user_info:
        print("Failed to fetch user information.")
        return None

    user_info = user_info["response"][0]

    followers = fetch_followers(user_id, access_token)
    subscriptions_users, subscriptions_groups = fetch_subscriptions(user_id,
                                                                    access_token)

    return UserData(
        user_id=user_info["id"],
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        followers=followers,
        subscriptions_users=subscriptions_users,
        subscriptions_groups=subscriptions_groups
    )


# Функция для получения подписчиков
def fetch_followers(user_id, access_token):
    params = {
        "v": "5.131",
        "access_token": access_token,
        "user_id": user_id
    }
    followers_data = get_data_from_vk("users.getFollowers", params)

    if not followers_data or 'response' not in followers_data:
        print("Failed to fetch followers information.")
        return []

    followers_data = followers_data["response"].get("items", [])

    followers = []
    for follower_id in followers_data:
        follower_info = get_data_from_vk("users.get", {
            "v": "5.131",
            "access_token": access_token,
            "user_ids": follower_id
        })
        if follower_info and 'response' in follower_info:
            follower_info = follower_info["response"][0]
            followers.append({
                "id": follower_info["id"],
                "first_name": follower_info["first_name"],
                "last_name": follower_info["last_name"]
            })
    return followers


# Функция для получения подписок
def fetch_subscriptions(user_id, access_token):
    params = {
        "v": "5.131",
        "access_token": access_token,
        "user_id": user_id
    }
    subscriptions_data = get_data_from_vk("users.getSubscriptions", params)

    if not subscriptions_data or 'response' not in subscriptions_data:
        print("Failed to fetch subscriptions information.")
        return [], []

    subscriptions_users = subscriptions_data["response"].get("users", {}).get("items", [])
    subscriptions_groups = subscriptions_data["response"].get("groups", {}).get("items", [])

    # Получение списка пользователей
    users_info = []
    for user_id in subscriptions_users:
        user_info = get_data_from_vk("users.get", {
            "v": "5.131",
            "access_token": access_token,
            "user_ids": user_id
        })
        if user_info and 'response' in user_info:
            user_info = user_info["response"][0]
            users_info.append({
                "id": user_info["id"],
                "first_name": user_info["first_name"],
                "last_name": user_info["last_name"]
            })

    # Получение списка групп
    groups_info = []
    for group_id in subscriptions_groups:
        group_info = get_data_from_vk("groups.getById", {
            "v": "5.131",
            "access_token": access_token,
            "group_ids": group_id
        })
        if group_info and 'response' in group_info:
            group_info = group_info["response"][0]
            groups_info.append({
                "id": group_info["id"],
                "name": group_info["name"]
            })

    return users_info, groups_info


# Сохранение данных в JSON файл
def save_data_to_file(user_data, file_path):
    data = {
        "id": user_data.id,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "followers": user_data.followers,
        "subscriptions_users": user_data.subscriptions_users,  # Списки пользователей
        "subscriptions_groups": user_data.subscriptions_groups  # Списки групп
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    user_id = input("Введите ID пользователя ВКонтакте: ")
    access_token = input("Введите access token: ")

    user_data = fetch_user_data(user_id, access_token)
    if user_data:
        save_data_to_file(user_data, "result.json")
        print("Данные сохранены в файл result.json в корне проекта")
    else:
        print("Не удалось получить данные о пользователе.")

if __name__ == "__main__":
    main()
