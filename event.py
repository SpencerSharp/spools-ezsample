import local

class Event(MappableItem):
    def __init__(track_name, artist_name, project_name, timestamp, img_path=None):
        self.track_name = track_name
        self.artist_name = artist_name
        self.project_name = project_name
        self.timestamp = timestamp
        self.img_path = img_path
        self.local = None
        self.source = None

    def already_resolved():
        if self.local == None:
            self.local = local.try_find_event(self)
        return self.local != None

    def has_source():
        if self.source == None:
            self.source = local.try_find_event_source(self)
        return self.source != None

    def download_source():
        ytdl.download_event_source(self)

    def get_path():
        return fs.get_event_path(self)
    
    def save():
        local.save_event(self)

    def resolve():
        if self.already_resolved():
            return
        if not self.has_source():
            self.download_source()
        self.save()