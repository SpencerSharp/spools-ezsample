# download_cmd = 'youtube-dl -q -f mp4 --audio-quality 0 --fragment-retries infinite -o {} "ytsearch:{}"'

# def build_yt_search_query(track_name, artist_name, project_name):
#     query = '{}{}'.format(artist_name, track_name)
#     query += " hd audio"
#     query += project_name
#     return query

# class FileItem(object):
#     def __init__(self, args):
#         locals = [find_options(basedir, args)]
#         if len(locals) == 0:
#             self.find_info()
#         else if len(locals == 1):
#             self.info = locals[0].args
#             self.source = locals[0]
#         else:
#             raise
    
#     def find_options(dir, args):
#         for item in dir.iterdir():
#             if args[0] in item.name:
#                 if dir.is_dir():
#                     yield find_options(item, args[1:])
#                 else if len(args) == 1:
#                     yield item

#     def find_info():
#         self.source = None
#         # indefinite generator, prob max capped for timeout
#         for match in discogs.search(self.info):
#             ind = 0
#             for attr in self.info:
#                 if attr in match[ind]:
#                     ind += 1
#                 else:
#                     break
#             if ind == len(self.info):
#                 self.info = match
#                 return
    
#     def download():
#         query = build_yt_search_query(self.info[0], self.info[1], self.info[2])
#         run_cmd(download_cmd.format(self.get_path(),query))
    
#     def is_saved():
#         return self.source == None

import pandas as pd
import os
from pathlib import Path

class ItemTable():
    def __init__(self, name):
        self.file = Path(os.environ['SPOOLS_HOME']) / 'sample' / name
        if not self.file.exists():
            pd.DataFrame().to_json(self.file)

    def add(self, item):
        table = pd.read_json(self.file)
        table = table.append(item.to_dict(),ignore_index=True)
        table.to_json(self.file)

    def exists(self, item):
        table = pd.read_json(self.file)
        if len(table) == 0:
            return False
        return len(table.loc[table['timestamp'] == item.timestamp]) > 0

class Sample(object):
    def __init__(self, track_name, artist_name, project_name, time_in_track, timestamp=None, img_path=None):
        # self.track = FileItem(self.track_name, self.artist_name, self.project_name)
        self.timestamp = timestamp

        self.track_name = track_name
        self.artist_name = artist_name
        self.project_name = project_name
        self.time_in_track = time_in_track

        self.img_path = img_path
        self.path = None
        self.source_path = None

        self.tags = []

        self.table = ItemTable('events')

    # call at nighttime routine
    def resolve(self):
        if self.table.exists(self):
            return
        if not self.track.is_saved():
            self.track.download()
        self.save()

    # call when event processing 
    def save(self):
        if self.table.exists(self):
            return
        self.table.add(self)
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'project_name': self.project_name,
            'time_in_track': self.time_in_track,
            'img_path': self.img_path,
            'path': self.path,
            'source_path': self.source_path,
            'tags': self.tags
        }
