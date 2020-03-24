from spools.data import MappableItem

class Event(MappableItem):
    def __init__(track_name, artist_name, project_name, timestamp, img_path=None):
        self.track = Track(self.track_name, self.artist_name, self.project_name, img_path == None)
        self.timestamp = timestamp
        self.img_path = img_path
        self.table = None

    def has_source():
        return self.track.is_saved()

    def download_source():
        self.track.download()

    def resolve():
        if self.is_saved():
            return
        if not self.has_source():
            self.download_source()
        self.save()