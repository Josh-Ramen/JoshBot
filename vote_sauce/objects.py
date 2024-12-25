
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

class BankEntry:
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
