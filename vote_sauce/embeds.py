from discord import Embed, Colour

from common.embeds import _josh_bot_color
from common.functions import pluralizer

# Descriptions

_vote_help_desc = """Here's what I can do for voting!

__Vote commands:__
:ballot_box: **/vote [user]** - Vote for a user in this server, or change your vote.
:mag: **/audit** - Check how many votes are in right now.
:bank: **/balance** - Check how many :coin: **Sauce Coins** you've earned.
:bar_chart: **/leaderboard** - See who's earned the most :coin: **Sauce Coins** so far.

__Dangerous commands:__
:octagonal_sign: **/tally** - Stop the count immediately and reward whoever has the most votes.
"""

_vote_explain_desc = """It's a lot more simple than the wheel, I promise!

**1) Vote**
Use **/vote [user]** to submit a vote for someone. I think your vote should be for whoever did the top funny. 
If you want to change your vote at any time, just do it again with a different user! That'll change your vote.

**2) Wait**
The tally comes in at around 12 PM EST. At that point, whoever has the most votes will earn :coin: **1 Sauce Coin.**

...That's it! You can't do anything with sauce coins or anything. We're not making a cryptocurrency, that'd be stupid, right?

You can check who has the most :coin: **Sauce Coins** with **/leaderboard** and check your own balance with **/balance.** 
"""

_tally_success_desc = """For your democratic success, have a :coin: **Sauce Coin.**
You can check your balance with **/balance**, or see the current rankings with **/leaderboard**."""

_tally_no_votes_desc = """Because no votes were submitted, I can't give out any Sauce Coins.
That's alright! You can try again tomorrow."""

_audit_no_votes_desc = """There are no votes to audit.
Try voting with **/vote**."""

_leaderboard_empty_desc = """None of you have earned any :coin: **Sauce Coins**, so there's no leaderboard to display."""

# Embeds

vote_help_embed = Embed(title=":ramen: **I'm JoshBot!** :ramen:", color=_josh_bot_color, description=_vote_help_desc)

vote_explain_embed = Embed(title=":ballot_box: **How does this work?** :ballot_box:", color=_josh_bot_color, description=_vote_explain_desc)

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

def balance_success_embed(balance: int):
    return Embed(
        title=":bank: **Just checking your account...**",
        color=_josh_bot_color,
        description="You have :coin: **{}** Sauce Coin{}.".format(balance, pluralizer(balance))
    )

def leaderboard_success_embed(msg: str):
    return Embed(title=":chart: Here's how it stands!", color=_josh_bot_color, description=msg)

def leaderboard_empty_embed():
    return Embed(title=":money_with_wings: **It appears you're all broke.**", color=_josh_bot_color, description=_leaderboard_empty_desc)
