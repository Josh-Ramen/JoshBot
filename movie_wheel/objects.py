import random
from movie_wheel.functions import movie_queue_to_str

class WheelEntry:
    def __init__(self, uuid: int, unseen_movies: list = list(), seen_movies: list = list()):
        self.uuid = uuid
        self.unseen_movies = unseen_movies
        self.seen_movies = seen_movies
    
    # Add a movie to the user's wheel list.
    # Returns True on success, False if the user has seen two movies.
    def add_movie(self, movie_name: str):
        # Reject if two movies were seen.
        if (len(self.seen_movies) == 2):
            print("Already seen two movies! Skipping.")
            return False

        # Don't allow more than two movies
        self.unseen_movies.append(movie_name)
        if (len(self.unseen_movies) + len(self.seen_movies) > 2):
            dropped = self.unseen_movies.pop(0)
            return dropped
        else:
            return True
    
    def delete_movie(self, slot: int):
        return self.unseen_movies.pop(slot)
    
    def watch_movie(self):
        random_index = random.randint(0, len(self.unseen_movies) - 1)
        movie_to_watch = self.unseen_movies.pop(random_index)
        self.seen_movies.append(movie_to_watch)
        return movie_to_watch
    
    def reset(self):
        self.seen_movies.clear()
        self.unseen_movies.clear()
    
    def to_db_entry(self):
        return {
            'uuid': self.uuid,
            'unseen_movies': self.unseen_movies,
            'seen_movies': self.seen_movies
        }
    
    def to_desc(self):
        if (len(self.unseen_movies) == 0 and len(self.seen_movies) == 0):
            return "You haven't submitted any movies."
        
        unseen_movie_str = movie_queue_to_str(self.unseen_movies)
        seen_movie_str = movie_queue_to_str(self.seen_movies)
        desc = "**Unseen movies**: {}\n**Seen movies**: {}".format(unseen_movie_str, seen_movie_str)
        return desc
    
    def compressed_desc(self):
        if (len(self.unseen_movies) == 0 and len(self.seen_movies) == 0):
            return "Empty entry."
        
        unseen_movie_str = movie_queue_to_str(self.unseen_movies)
        seen_movie_str = movie_queue_to_str(self.seen_movies)
        desc = "Unseen: {}; Seen: {}".format(unseen_movie_str, seen_movie_str)
        return desc