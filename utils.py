from typing import Any

import youtube
from googleapiclient.discovery import build

def get_you_tube_data(api_key: str, channel_ids: [str]) -> list[dict[str, Any]]:
    """Получение данных о каналах и видео с них с помощью API-YouTube"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    data = []
    videos_data = []
    next_page_token = None

    for i in channel_ids:
        channel_data = youtube.channels().list(part='snippet, statistics', id=i).execute()

        while True:
            response = youtube.search().list(part='id,snippet', channelId=i, type='video',
                                                 order='date', maxResults=50, pageToken=next_page_token).execute()

            videos_data.extend(response['items'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        data.append({
            'channel': channel_data['items'][0],
            'videos': videos_data
        })

    return data

def create_datebase(datebase_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения информации о канале и видео"""


def save_date_to_datebase(data: list[dict[str, Any]], datebase_name: str, params: dict) -> None:
    """Сохранение данных о каналах и видео в базу данных"""