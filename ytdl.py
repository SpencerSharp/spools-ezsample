from pydub import AudioSegment
import subprocess
import shlex

# subprocess.call([ 'dl "ytsearch:{}"'.format(query) ], shell=False)

download_cmd = 'youtube-dl -q -f mp4 --audio-quality 0 --fragment-retries infinite -o {} "ytsearch:{}"'

def build_yt_search_query(track_name, artist_name, project_name):
    query = '{}{}'.format(artist_name, track_name)
    query += " hd audio"
    query += project_name
    return query

def download_event_source(event):
    query = build_yt_search_query(event.track_name, event.artist_name, event.project_name)
    run_cmd(download_cmd.format(event.get_path(),query))

    # sound = AudioSegment.from_file(Path.cwd() / 'out.mp4')
    # sample = sound[ms-10000:ms]
    # sample.export('sample{}.mp4'.format(count), format="mp4")
    # (Path.cwd() / 'out.mp4').unlink()