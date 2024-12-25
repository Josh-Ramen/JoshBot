from tinydb import TinyDB, Query

from vote_sauce.objects import SauceVote

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