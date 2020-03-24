from spools import spotify
from spools.ezsample import Event

Track t, double time = spotify.get_running()
Event e = Event(t.track_name, t.project_name, t.artist_name, time)
e.save()