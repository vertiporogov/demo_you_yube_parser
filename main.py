from utils import get_you_tube_data, create_database, save_date_to_datebase
from config import config


def main():
    api_key = 'AIzaSyARTbNiiO1YNuLkmV_exygBJoEzBJ79T3A'
    channel_ids = [
        # 'UC-OVMPlMA3-YCIeg4z5z23A',  # вДудь
        'UCwHL6WHUarjGfUM_586me8w'  # Редакция
    ]
    params = config()

    data = get_you_tube_data(api_key, channel_ids)
    create_database('YouTube', params)
    # save_date_to_database(data, 'YouTube', params)


if __name__ == '__main__':
    main()
