from typing import Dict


class User:
    all_users: Dict[str, 'User'] = dict()

    def __init__(self, user_id):
        self.chat_id = None
        self.city = None
        self.city_id = None
        self.hotels_count = None
        self.getting_photos = False
        self.photos_count = None
        self.user_command = None
        self.check_in = None
        self.check_out = None
        self.block_choose_date = False
        self.datetime_input_command = None
        self.hotel_data = []
        self.found_needed_flag = False
        self.price_range = None
        self.distance_range = None

        User.add_user(user_id, self)

    @classmethod
    def get_user(cls, user_id):
        if User.all_users.get(user_id) is None:
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @classmethod
    def del_user(cls, user_id):
        if User.all_users.get(user_id) is not None:
            del User.all_users[user_id]