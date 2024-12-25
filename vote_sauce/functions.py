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