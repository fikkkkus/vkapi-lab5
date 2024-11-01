import requests
import logging
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserData:

    def __init__(self, user_id, first_name, last_name, screen_name, followers, subscriptions_users, subscriptions_groups, sex=None, city=None, isEndTreeNode = False):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.screen_name = screen_name
        self.followers = followers
        self.subscriptions_users = subscriptions_users
        self.subscriptions_groups = subscriptions_groups
        self.sex = sex
        self.city = city
        self.isEndTreeNode = isEndTreeNode

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

class UserData:

    def __init__(self, user_id, first_name, last_name, screen_name, followers, subscriptions_users, subscriptions_groups, sex=None, city=None, isEndTreeNode = False):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.screen_name = screen_name
        self.followers = followers
        self.subscriptions_users = subscriptions_users
        self.subscriptions_groups = subscriptions_groups
        self.sex = sex
        self.city = city
        self.isEndTreeNode = isEndTreeNode

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class UserDataCollector:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_data_from_vk(self, method, params):
        url = f"https://api.vk.com/method/{method}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                logger.warning(f"VK API returned an error: {data['error']['error_msg']}")
                return None
            return data
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            logger.error(f"Request failed: {e}")
        return None

    def fetch_followers(self, user_id):
        params = {
            "v": "5.131",
            "access_token": self.access_token,
            "user_id": user_id
        }
        followers_data = self.get_data_from_vk("users.getFollowers", params)
        if not followers_data or 'response' not in followers_data:
            logger.info(f"No followers found or access denied for user_id: {user_id}")
            return []
        return followers_data["response"].get("items", [])

    def fetch_subscriptions(self, user_id):
        params = {
            "v": "5.131",
            "access_token": self.access_token,
            "user_id": user_id
        }
        subscriptions_data = self.get_data_from_vk("users.getSubscriptions", params)

        if not subscriptions_data or 'response' not in subscriptions_data:
            logger.warning("Failed to fetch subscriptions information.")
            return [], []

        subscriptions_groups = subscriptions_data["response"].get("groups", {}).get("items", [])

        users_info = []  # Временный список для хранения информации о пользователях
        groups_info = []  # Временный список для хранения информации о группах
        for group_id in subscriptions_groups:
            group_info = self.get_data_from_vk("groups.getById", {
                "v": "5.131",
                "access_token": self.access_token,
                "group_ids": group_id
            })
            if group_info and 'response' in group_info:
                group_info = group_info["response"][0]
                groups_info.append({
                    "id": group_info["id"],
                    "name": group_info["name"],
                    "screen_name": group_info.get("screen_name", "")
                })

        return users_info, groups_info

    def fetch_user_data(self, user_id):
        params = {
            "v": "5.131",
            "access_token": self.access_token,
            "user_ids": user_id,
            "fields": "followers_count, sex, home_town, screen_name"
        }

        user_info = self.get_data_from_vk("users.get", params)
        if not user_info or 'response' not in user_info:
            logger.warning(f"Failed to fetch user information for user_id: {user_id}")
            return None

        user_info = user_info["response"][0]

        followers = self.fetch_followers(user_id)
        subscriptions_users, subscriptions_groups = self.fetch_subscriptions(user_id)

        return UserData(
            user_id=user_info["id"],
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            followers=followers,
            screen_name=user_info["screen_name"],
            subscriptions_users=subscriptions_users,
            subscriptions_groups=subscriptions_groups,
            sex=user_info.get("sex"),
            city=user_info.get("home_town"),
        )

    def fetch_data_recursive(self, user_id, max_depth=2):
        all_users = []

        def recursive(current_user_id, current_depth):
            # Прерывание рекурсии на заданной глубине
            if current_depth > max_depth:
                return

            user = self.fetch_user_data(current_user_id)

            # Если пользовательские данные получены, добавляем к списку
            if user:
                all_users.append(user)
                # Если достигнут конечный уровень, помечаем листовой узел
                if current_depth == max_depth:
                    user.isEndTreeNode = True
                    return

                # Рекурсивно обходим подписчиков на следующем уровне
                for follower_id in user.followers:
                    recursive(follower_id, current_depth + 1)

        # Запуск рекурсии с начальным уровнем
        recursive(user_id, current_depth=0)

        return all_users