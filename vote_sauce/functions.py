import discord

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

def get_audit_desc(candidates: dict[int, int], guild: discord.Guild):
    text = ""

    for uuid in candidates:
        member = guild.get_member(uuid)
        num_votes = candidates[uuid]
        text += "User **{}** has **{}** vote".format(member.display_name, num_votes)
        
        if (num_votes > 1):
            text += "s"
        text += ".\n"
    
    text += "\nYou can add a vote or change your vote with **/vote**!"
    return text