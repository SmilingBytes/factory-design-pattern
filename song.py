from song_serializer import BaseSerializer


class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist

    def serialize(self, serializer: BaseSerializer):
        serializer.start_object("song", self.song_id)
        serializer.add_property("title", self.title)
        serializer.add_property("artist", self.artist)
