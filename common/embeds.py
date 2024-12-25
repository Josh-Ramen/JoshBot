from discord import Embed, Colour

# Constants

_josh_bot_color = Colour(16441474)

# Descriptions

_help_desc = """I have the honor to be your obedient servant. :star:

__General commands:__
:question: **/help** - It'll display... um, this message. You just used it. Are you okay?
:clipboard: **/changelog** - I can explain what's changed since my last version!
:secret: **/something_cool** - It does something cool.

__More specific commands:__
:film_frames: If you want help with the movie wheel, try **/helpwheel** or **/explainwheel**.
:ballot_box: If you want help with voting, try **/helpvote** or **/explainvote**.
"""

_changelog_desc='''**General changes**
-Since my creator added a new class of functions, I separated out the explanations for each one.

**New functionality!**
-You can vote for who deserves a :coin: **Sauce Coin** at the end of each night!
-For more information, try **/helpvote** or **/explainvote**.
'''

# Embeds

help_embed = Embed(title=":ramen: **I'm JoshBot!** :ramen:", color=_josh_bot_color, description=_help_desc)

changelog_embed = Embed(title=":clipboard: **JoshBot version 1.1!** :clipboard:", color=_josh_bot_color, description=_changelog_desc)
