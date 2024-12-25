from collections import defaultdict
from tinydb import TinyDB, Query

from vote_sauce.objects import SauceVote, BankAccount

def find_vote(voter_uuid: int, database: TinyDB):
    search_res = database.search(Query().voter_uuid == voter_uuid)
    if (len(search_res) > 0):
        # Vote found, return existing vote
        match = search_res[0]
        existing_vote = SauceVote(match['voter_uuid'], match['vote_uuid'], match['old_vote_uuid'])
        print("Found existing vote to update: {}".format(existing_vote.compressed_desc()))
        return existing_vote

    # No vote found, return a new one
    new_vote = SauceVote(voter_uuid, -1, -1)
    database.insert(new_vote.to_db_entry())
    return new_vote

def update_vote(vote: SauceVote, new_vote_uuid: int):
    if (vote.vote_uuid != new_vote_uuid):
        # Vote is actually different, so update it
        vote.change_vote(new_vote_uuid)
        return 1
    
    # Vote is the same, don't bother doing anything
    return 0

def send_vote(vote: SauceVote, database: TinyDB):
    database.update(
        { 'vote_uuid': vote.vote_uuid, 'old_vote_uuid': vote.old_vote_uuid },
        Query().voter_uuid == vote.voter_uuid
    )
    print("Successfully updated vote for {}".format(vote.vote_uuid))

def tally_votes(database: TinyDB):
    votes = dict[int, int]()
    highest_tally = 0
    winners = set()

    for vote in database.all():
        # Increment vote count for candidate
        votes[vote['vote_uuid']] = votes.get(vote['vote_uuid'], 0) + 1

        if (votes[vote['vote_uuid']] > highest_tally):
            # New winner candidate
            highest_tally = votes[vote['vote_uuid']]
            winners.clear()
            winners.add(vote['vote_uuid'])
        elif (votes[vote['vote_uuid']] == highest_tally):
            # Candidates are tied
            winners.add(vote['vote_uuid'])
    
    return winners

def purge_votes(database: TinyDB):
    database.truncate()

def audit_votes(database: TinyDB):
    votes = dict[int, int]()

    for vote in database.all():
        # Increment vote count for candidate
        votes[vote['vote_uuid']] = votes.get(vote['vote_uuid'], 0) + 1

    return votes

def get_bank_account(uuid: int, database: TinyDB):
    search_res = database.search(Query().uuid == uuid)
    if (len(search_res) > 0):
        # User found, return existing bank account
        match = search_res[0]
        account = BankAccount(match['uuid'], match['balance'])
        print("Found existing account: {}".format(account.compressed_desc()))
        return account

    # No vote found, return a new one
    new_account = BankAccount(uuid, 0)
    database.insert(new_account.to_db_entry())
    return new_account

def update_bank_account(account: BankAccount, database: TinyDB):
    database.update(
        { 'balance': account.balance },
        Query().uuid == account.uuid
    )
    print("Successfully updated vote for {}".format(account.uuid))

def give_coin(uuid: int, database: TinyDB):
    account = get_bank_account(uuid, database)
    account.add_balance(1)
    update_bank_account(account, database)

def reward_winners(winners: set[int], database: TinyDB):
    for winner in winners:
        give_coin(winner, database)

def get_balance(uuid: int, database: TinyDB):
    account = get_bank_account(uuid, database)
    return account.balance

def get_leaderboard(database: TinyDB):
    leaderboard = defaultdict(int)

    for account in database.all():
        leaderboard[account['uuid']] = account['balance']
    
    # Sort and return
    return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
