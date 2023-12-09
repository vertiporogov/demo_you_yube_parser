from typing import Any
import psycopg2
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

    def create_database(database_name: str, params: dict):
        """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE channels (
                    channel_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    views INTEGER,
                    subscribers INTEGER,
                    videos INTEGER,
                    channel_url TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE videos (
                    video_id SERIAL PRIMARY KEY,
                    channel_id INT REFERENCES channels(channel_id),
                    title VARCHAR NOT NULL,
                    publish_date DATE,
                    video_url TEXT
                )
            """)

        conn.commit()
        conn.close()


def save_date_to_datebase(data: list[dict[str, Any]], datebase_name: str, params: dict) -> None:
    """Сохранение данных о каналах и видео в базу данных"""