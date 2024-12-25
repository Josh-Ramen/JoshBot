
class SauceVote:
    def __init__(self, voter_uuid: int, vote_uuid: int, old_vote_uuid: int):
        self.voter_uuid = voter_uuid
        self.vote_uuid = vote_uuid
        self.old_vote_uuid = old_vote_uuid

    def change_vote(self, new_vote_uuid: int):
        self.old_vote_uuid = self.vote_uuid
        self.vote_uuid = new_vote_uuid

    def to_db_entry(self):
        return {
            'voter_uuid': self.voter_uuid,
            'vote_uuid': self.vote_uuid,
            'old_vote_uuid': self.old_vote_uuid
        }

    def compressed_desc(self):
        if (self.old_vote_uuid > 0):
            return "User {} voting {} over {}".format(self.voter_uuid, self.vote_uuid, self.old_vote_uuid)
        return "User {} voting {}".format(self.voter_uuid, self.vote_uuid)