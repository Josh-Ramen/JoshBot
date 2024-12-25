from discord import Embed
from common.embeds import _josh_bot_color

# Description strings

_wheel_help_desc = '''Here's what I can do as The Movie Wheel :tm: !

__Movie Wheel commands:__
:cinema: **/submit [movie]** - Submit a movie to the wheel.
:mirror: **/check** - Shows you (and only you!) your movie submissions.
:wastebasket: **/delete [number]** - Deletes one of your movie submissions.
:film_frames: **/wheel** - Anonymously prints out all movies left on the wheel.
:clapper: **/spin** - Spins the wheel to randomly select a movie.

__Dangerous commands:__
:rewind: **/unspin** - Resets the "watched" status of all movies on the wheel.
:bomb: **/reset** - Removes all entries on the wheel.
'''

_wheel_explain_desc='''Let me explain! We'll go step-by-step.

**1) Submit**
Basically, everyone can submit up to two movies. I'll keep track of them so you don't have to.
If you submit Movie One and Movie Two, then you try to submit Movie Three, I'll get rid of Movie One. I'm serious about the two movie limit!

**2) Spin**
When you use **/spin**, I'll spin the wheel! The movie selected is random.
...Kind of. I'm biased towards people whose movies haven't been picked yet. If you think that's bad, then yell at my creator.
Once a movie has been spun, it can't be selected again. For this reason, please don't use **/spin** unnecessarily, I'm begging...

**3) Repeat**
Just keep spinning until you run out of movies. I'll tell you when the wheel is empty.

**4) Reset**
If you actually make it to this point and want to do more, then you can **/reset** to do movies again!
Note: my creator is skeptical that you will reach this point.'''

# Embeds

wheel_help_embed = Embed(title=":ramen: **I'm JoshBot!** :ramen:", color=_josh_bot_color, description=_wheel_help_desc)

wheel_explain_embed = Embed(title=":film_frames: **How does this work?** :film_frames:", color=_josh_bot_color, description=_wheel_explain_desc)

def wheel_submit_error_embed(error_msg: str):
    return Embed(title=":x: **Sorry, something went wrong...**", color=_josh_bot_color, description=error_msg)

def wheel_submit_success_embed(msg: str):
    return Embed(title=":white_check_mark: **Alright, done!**", color=_josh_bot_color, description=msg)

def wheel_submit_partial_embed(msg: str):
    return Embed(title=":speech_balloon: **All done! Um, except:**", color=_josh_bot_color, description=msg)

def wheel_delete_error_embed(error_msg: str):
    return Embed(title=":x: **I couldn't delete that...**", color=_josh_bot_color, description=error_msg)

def wheel_delete_success_embed(msg: str):
    return Embed(title=":wastebasket: **Alright, it's gone!**", color=_josh_bot_color, description=msg)

def wheel_check_embed(msg: str):
    return Embed(title=":notebook_with_decorative_cover: **Let's see what you sent me...**", color=_josh_bot_color, description=msg)

def wheel_wheel_embed(msg: str): # Funny method name
    return Embed(title=":film_frames: **Here's what's left on the wheel!**", color=_josh_bot_color, description=msg)

def wheel_spin_error_embed(error_msg: str):
    return Embed(title=":x: **I think the wheel's jammed?**", color=_josh_bot_color, description=error_msg)

def wheel_spin_success_embed(movie: str):
    return Embed(
        title=":ferris_wheel: **You got *{}!*** :ferris_wheel:".format(movie),
        color=_josh_bot_color,
        description="I wonder who submitted that? Actually I know, but I'm not telling."
    )

def wheel_unspin_error_embed(error_msg: str):
    return Embed(title=":x: **I can't.**", color=_josh_bot_color, description=error_msg)

wheel_unspin_success_embed = Embed(title=":rewind: Rewinding the tape...", color=_josh_bot_color, description="All movies are now **unwatched**.")

wheel_reset_success_embed = Embed(title=":bomb: :boom: **The movie wheel BITES THE DUST!** :rewind: :clapper:", color=_josh_bot_color, description="Until next time!")
