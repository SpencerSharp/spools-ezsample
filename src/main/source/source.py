import re
from pathlib import Path
import subprocess as sp
import shlex

exts = ['mp4','mp3','asd','mp4.asd']
conv_exts = ['wav']

artists_dir = Path.cwd()

ffmpeg_cmd = 'ffmpeg -loglevel quiet -i {} -codec copy {} {}'
artist_metadata = '-metadata artist="{}"'
album_metadata = '-metadata album="{}"'
trackno_metadata = '-metadata track="{}/{}"'
mv_cmd = 'mv {} {}'

album_tracks = {}
album_lengths = {}

def get_path(file):
    return shlex.quote(str(file.relative_to(artists_dir)))

def run_cmd(cmd):
    return sp.check_output(shlex.split(cmd))

def add_album(album_dir, artist):
    album_name = album_dir.name
    tracks = {}
    for track_file in album_dir.iterdir():
        if not track_file.is_dir():
            tracks[track_file] = track_file.stat().st_mtime
    album_lengths[album_name] = len(tracks.keys())
    for key, value in sorted(tracks.items(), key=lambda item: item[1]):
        add_track(key, artist, album_name)

def prettify(file_name):
    to_match = re.escape('-')+'[^ {}]*'.format(re.escape('.'))
    capture_group = '({})'.format(to_match)
    pattern = re.compile('.*'+capture_group+re.escape('.')+'(.{3}.*?)')
    matched = re.fullmatch(pattern,file_name)
    
    if matched != None:
        start = matched.span(1)[0]
        end = matched.span(1)[1]
        ext_start = matched.span(2)[0]
        ext_end = matched.span(2)[1]
        if (ext_end == len(file_name)):
            if file_name[ext_start:ext_end] in exts:
                pretty_name = file_name[:start] + file_name[end:]
                return pretty_name
    return file_name

def build_metadata(artist=None, album=None):
    md = []
    if artist != None:
        md.append(artist_metadata.format(artist))
    if album != None:
        md.append(album_metadata.format(album))
        trackno = 1
        if album in album_tracks.keys():
            trackno = album_tracks[album] + 1
        album_tracks[album] = trackno
        md.append(trackno_metadata.format(trackno,album_lengths[album]))
    return ' '.join(md)

def convert(file):
    m4a_file = file.with_name('{}.m4a'.format(file.stem))
    mp4_file = file.with_name('{}.mp4'.format(file.stem))

    if mp4_file.exists():
        return file

    convert_cmd = 'ffmpeg -i {} {}'
    convert_cmd = convert_cmd.format(get_path(file), get_path(m4a_file))
    run_cmd(convert_cmd)
    mv_cmd = 'mv {} {}'
    mv_cmd = mv_cmd.format(get_path(m4a_file), get_path(mp4_file))
    run_cmd(mv_cmd)

    # file.unlink()

    return mp4_file

def add_track(file, artist, album):
    if file.suffix[1:] in conv_exts:
        file = convert(file)
    if file.suffix[1:] not in exts:
        return
    file_path = get_path(file)
    tmp_file = file.with_name('new.'+file.name)
    tmp_file_path = get_path(tmp_file)
    pretty_file = file.with_name(prettify(file.name))

    metadata = build_metadata(artist, album)

    # check existing metadata
    # compare it to metadata
    # if match, return

    cmd = ffmpeg_cmd.format(file_path, metadata, tmp_file_path)

    if file.suffix != '.asd':
        run_cmd(cmd)

        cmd = mv_cmd.format(tmp_file_path, file_path)

        run_cmd(cmd)

    if (pretty_file.name != file.name):
        pretty_file_path = get_path(pretty_file)

        cmd = mv_cmd.format(file_path, pretty_file_path)

        run_cmd(cmd)
    


for artist in artists_dir.iterdir():
    if artist.is_dir():
        artist_name = artist.name
        if artist_name == 'Autechre':
            for file in artist.iterdir():
                if file.is_dir():
                    add_album(file, artist_name)
                else:
                    add_track(file, artist_name, None)