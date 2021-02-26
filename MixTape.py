__author__ = 'deepika'


class Users(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "{ ID = " + self.id + " Name = " + self.name + " } "

    def __str__(self):
        return "{ ID = " + self.id + " Name = " + self.name + " } "


class PlayLists(object):
    def __init__(self, id, user_id, song_ids):
        self.id = id
        self.user_id = user_id
        self.song_ids = song_ids


class Songs(object):
    def __init__(self, id, artist, title):
        self.id = id
        self.artist = artist
        self.title = title

    def __repr__(self):
        return "{ SongID = " + self.id + " Artist = " + self.artist + " Title = " + self.title + "}"

    def __str__(self):
        return self.__repr__()


class CustomDeserializer(object):

    def deserialise(self, data):
        users_data = data['users']
        playlists_data = data['playlists']
        songs_data = data['songs']

        users = []
        playlists = []
        songs = []

        for _u in users_data:
            users.append(Users(_u["id"], _u["name"]))

        for _p in playlists_data:
            playlists.append(PlayLists(_p["id"], _p["user_id"], _p["song_ids"]))

        for _s in songs_data:
            songs.append(Songs(_s["id"], _s["title"], _s["artist"]))

        return users, playlists, songs


class Change(object):
    def __init__(self, action, user, playlist, songs = []):
        self.type = action
        self.song_ids = songs
        self.user_id = user
        self.playlist_id = playlist


class BasicChangeHandler(object):

    def __init__(self):
        pass

    def classifyChanges(self, data):
        change_data = data["changes"]

        changes = []
        for _c in change_data:
            changes.append(Change(_c["action"], _c["user_id"], _c["playlist_id"], [] if "song_ids" not in _c else _c["song_ids"]))
        return changes

class MixTape:

    def __init__(self, users, pl, songs):
        self.users = users
        self.playlists = pl
        self.songs = songs


