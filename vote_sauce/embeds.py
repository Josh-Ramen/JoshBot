from discord import Embed, Colour

# Constants
_josh_bot_color = Colour(16441474)

# Descriptions
_tally_success_desc = """For your democratic success, have a :coin: **Sauce Coin.**
...At least, you would get one if that feature was implemented yet. Sorry! My creator is working on it."""

_tally_no_votes_desc = """Because no votes were submitted, I can't give out any Sauce Coins.
That's alright! You can try again tomorrow."""

_audit_no_votes_desc = """There are no votes to audit.
Try voting with **/vote**."""

# Embeds

def vote_success_embed(msg: str):
    return Embed(title=":ballot_box: **Democracy is working!**", color=_josh_bot_color, description=msg)

def vote_error_embed(error_msg: str):
    return Embed(title=":question: **Your vote didn't change.**", color=_josh_bot_color, description=error_msg)

def tally_success_embed(title: str):
    return Embed(title=title, color=_josh_bot_color, description=_tally_success_desc)

def tally_no_votes_embed():
    return Embed(title=":chart_with_downwards_trend: **No one voted...**", color=_josh_bot_color, description=_tally_no_votes_desc)

def audit_success_embed(msg: str):
    return Embed(title=":popcorn: **Current vote counts:**", color=_josh_bot_color, description=msg)

def audit_no_votes_embed():
    return Embed(title=":chart_with_downwards_trend: **I guess turnout is low?**", color=_josh_bot_color, description=_audit_no_votes_desc)
