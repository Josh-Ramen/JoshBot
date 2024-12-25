import discord

from common.constants import bot_user_id
from vote_sauce.objects import SauceVote

def get_vote_desc(vote: SauceVote, new_vote: discord.Member, interaction: discord.Interaction):
    text = "{} voted for {} !"
    guild = interaction.guild
    
    # Spite message branch
    if (vote.old_vote_uuid != -1):
        old_vote_user = guild.get_member(vote.old_vote_uuid)
        text += "\n...And thus removed a vote for {} !"
        # Betrayal
        if (old_vote_user.id == bot_user_id):
            text += "\nA-aha, I guess you changed your mind... That's okay."
        text = text.format(interaction.user.mention, new_vote.mention, old_vote_user.mention)
    else:
        text = text.format(interaction.user.mention, new_vote.mention)
    
    # Flattery message branch
    if (new_vote.id == bot_user_id):
        text += "\n\n...Wait, you voted for me? Awww... thank you."
    
    return text

def get_winner_title(winners: list[int], guild: discord.Guild):
    text = ":moneybag: "

    for i in range(0, len(winners)):
        if (i ==  len(winners) - 1 and i != 0):
            text += "and "
        
        winner = guild.get_member(winners[i])
        text += "**「{}」** ".format(winner.display_name)

        if (len(winners) > 2 and i <  len(winners) - 1):
            text += ", "
    
    text += "won the most votes!"
    return text

def pluralizer(num: int):
    if (num != 1):
        return "s"
    return ""

def get_audit_desc(candidates: dict[int, int], guild: discord.Guild):
    text = ""

    for uuid in candidates:
        member = guild.get_member(uuid)
        num_votes = candidates[uuid]
        text += "User **{}** has **{}** vote{}.\n".format(member.display_name, num_votes, pluralizer(num_votes))
    
    text += "\nYou can add a vote or change your vote with **/vote**!"
    return text

def get_ranking(i: int):
    if i == 0:
        return ":first_place: "
    elif i == 1:
        return ":second_place: "
    elif i == 2:
        return ":third_place: "
    
    return "{}. ".format(i + 1)

def get_leaderboard_desc(leaderboard: list[tuple[int, int]], guild: discord.Guild):
    text = ""
    for i in range(len(leaderboard)):
        tuple = leaderboard[i]
        text += get_ranking(i)
        text += "**{}** with :coin: **{} Sauce Coins**".format(guild.get_member(tuple[0]).display_name, tuple[1])

        if (i != len(leaderboard) - 1):
            text += "\n"
    
    return text