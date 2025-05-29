import random
from tinydb import where
from tinydb.table import Table
from movie_wheel.objects import WheelEntry

def find_or_create_user_entry(uuid: int, table: Table):
    user_search = table.search(where('uuid') == uuid)
    if (len(user_search) > 0):
        match = user_search[0]
        entry = WheelEntry(match['uuid'], match['unseen_movies'], match['seen_movies'])
        print("Found user with UUID {}, returning existing entry: {}".format(uuid, entry.compressed_desc()))
        return entry
    else:
        print("No entry found! Creating new entry for UUID {}...".format(uuid))
        new_entry = WheelEntry(uuid)
        table.insert(new_entry.to_db_entry())
        return new_entry

def update_user_entry(entry: WheelEntry, table: Table):
    print("Updating UUID {}'s entry...".format(entry.uuid))
    table.upsert(
        entry.to_db_entry(),
        where('uuid') == entry.uuid,
    )
    print("Success! New entry output: {}".format(entry.compressed_desc()))

def get_spin_candidates(table: Table):
    entries = table.all()
    candidates = []

    # Favor non-selected people first
    for entry in entries:
        if (len(entry['seen_movies']) == 0 and len(entry['unseen_movies']) > 0):
            candidates.append(entry)
    if (len(candidates) != 0):
        return candidates
    
    # Favor once-selected people next
    for entry in entries:
        if (len(entry['unseen_movies']) == 1):
            candidates.append(entry)

    if (len(candidates) != 0):
        return candidates
    
    # It's so over
    return list()

def select_candidate(candidates: list):
    random_index = random.randint(0, len(candidates) - 1)
    chosen = candidates[random_index]
    chosen_entry = WheelEntry(chosen['uuid'], chosen['unseen_movies'], chosen['seen_movies'])
    return chosen_entry

def unwatch_all_entries(table: Table):
    entries = table.all()
    for entry in entries:
        wheel_entry = WheelEntry(entry['uuid'], entry['unseen_movies'], entry['seen_movies'])
        # Ignore entries with no watched movies
        if (len(wheel_entry.seen_movies) == 0):
            continue
        
        # Pop from seen movies into unseen movies
        while (len(wheel_entry.seen_movies) > 0):
            wheel_entry.unseen_movies.append(wheel_entry.seen_movies.pop())
        
        # Update entry
        update_user_entry(wheel_entry, table)


def accumulate_entries(table: Table):
    entries = table.all()

    output = ""
    have_seen_movies = False
    for item in entries:
        unseen_queue = item['unseen_movies']
        for movie in unseen_queue:
            output += "{}\n".format(movie)
        if (not have_seen_movies and len(item['seen_movies']) > 0):
            have_seen_movies = True
    
    # Special text for empty output
    if (output == ""):
        if (not have_seen_movies):
            output = "Um... no one submitted anything yet."
        else:
            output = "We've seen every movie on the wheel! Congratulations! :tada:"
    return output