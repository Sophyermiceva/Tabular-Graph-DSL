LOAD users;
LOAD friendships;

NODE Person KEY id FROM users;

EDGE FriendOf
    FROM friendships
    SOURCE person_a
    TARGET person_b;
