
class SauceVote:
    def __init__(self, voter_uuid: int, vote_uuid: int, old_vote_uuid: int):
        self.voter_uuid = voter_uuid
        self.vote_uuid = vote_uuid
        self.old_vote_uuid = old_vote_uuid

    #: Updates vote to a new user ID.
    #: Returns 1 on success, 0 if there's no change.
    def change_vote(self, new_vote_uuid: int):
        if (self.vote_uuid != new_vote_uuid):
        # Vote is actually different, so update it
            self.old_vote_uuid = self.vote_uuid
            self.vote_uuid = new_vote_uuid
            return 1

        # Vote is the same, don't bother doing anything
        return 0

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

class BankAccount:
    def __init__(self, uuid: int, balance: int):
        self.uuid = uuid
        self.balance = balance

    def add_balance(self, to_add: int):
        self.balance += to_add

    def to_db_entry(self):
        return {
            'uuid': self.uuid,
            'balance': self.balance
        }

    def compressed_desc(self):
        return "User {} has a balance of {}".format(self.uuid, self.balance)
