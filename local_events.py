event_file = 'sample_events.json'
is_loaded = False

def init():
    if not is_loaded:
        saved_events = fs.load_file(event_file)
        is_loaded = True
        set_events(saved_events)

def try_find_event(event):
    if img_path != None:
        matching_imgs = events.loc[event.img_path]
        if matching_imgs != None:
            return matching_imgs[0]
    else:
        matching_tracks = events.loc[event.track_name, event.artist_name, event.project_name]
        for row in matching_tracks:
            if time within X seconds of event.timestamp:
                return row
    return None
    
def try_find_event_source(event):
    if img_path != None:
        # lenient search
    else:
        # exact search

def save_event(event):
    set_events(events.append(event))
    push_to_disk()

def set_events(new_events):
    global events
    events = new_events

def push_to_disk():
    fs.save_file(event_file, events)
