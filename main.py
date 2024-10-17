from song import Song
from song_serializer import SongSerializer


def main():
    song = Song("1", "Water of Love", "Dire Straits")

    serializer = SongSerializer()
    print(f'JSON: {serializer.serialize(song, "JSON")}')
    print(f'XML: {serializer.serialize(song, "XML")}')
    # print(f'YAML: {serializer.serialize(song, "YAML")}')


if __name__ == "__main__":
    main()
