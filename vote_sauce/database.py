from collections import defaultdict
from tinydb import where
from tinydb.table import Table

from vote_sauce.objects import SauceVote, BankAccount

def find_vote(voter_uuid: int, table: Table):
    search_res = table.search(where('voter_uuid') == voter_uuid)
    if (len(search_res) > 0):
        # Vote found, return existing vote
        match = search_res[0]
        existing_vote = SauceVote(match['voter_uuid'], match['vote_uuid'], match['old_vote_uuid'])
        print("Found existing vote to update: {}".format(existing_vote.compressed_desc()))
        return existing_vote

    # No vote found, return a new one
    new_vote = SauceVote(voter_uuid, -1, -1)
    return new_vote

def send_vote(vote: SauceVote, table: Table):
    print("Vote is {}".format(vote.compressed_desc()))
    table.upsert(
        vote.to_db_entry(),
        where('voter_uuid') == vote.voter_uuid
    )
    print("Successfully updated vote for {}".format(vote.vote_uuid))

def tally_votes(table: Table):
    votes = dict[int, int]()
    highest_tally = 0
    winners = set()

    for vote in table.all():
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

def purge_votes(table: Table):
    table.truncate()

def audit_votes(table: Table):
    votes = dict[int, int]()

    for vote in table.all():
        # Increment vote count for candidate
        votes[vote['vote_uuid']] = votes.get(vote['vote_uuid'], 0) + 1

    return votes

def get_bank_account(uuid: int, table: Table):
    search_res = table.search(where('uuid') == uuid)
    if (len(search_res) > 0):
        # User found, return existing bank account
        match = search_res[0]
        account = BankAccount(match['uuid'], match['balance'])
        print("Found existing account: {}".format(account.compressed_desc()))
        return account

    # No account found, return a new one
    new_account = BankAccount(uuid, 0)
    table.insert(new_account.to_db_entry())
    return new_account

def update_bank_account(account: BankAccount, table: Table):
    table.update(
        account.to_db_entry(),
        where('uuid') == account.uuid
    )
    print("Successfully updated bank account for {}".format(account.uuid))

def give_coin(uuid: int, table: Table):
    account = get_bank_account(uuid, table)
    account.add_balance(1)
    update_bank_account(account, table)

def reward_winners(winners: set[int], table: Table):
    for winner in winners:
        give_coin(winner, table)

def get_balance(uuid: int, table: Table):
    account = get_bank_account(uuid, table)
    return account.balance

def get_leaderboard(table: Table):
    leaderboard = defaultdict(int)

    for account in table.all():
        leaderboard[account['uuid']] = account['balance']

    # Sort and return
    return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
