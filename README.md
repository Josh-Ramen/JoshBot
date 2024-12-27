# 🍜 JoshBot 🍜

I would like a good bowl of ramen.

## What is this?

JoshBot is a Discord bot built in Python. It functions exclusively through slash commands.

## What does it do?

v1.0.0 - Currently serves as The Movie Wheel™️. It also has a few joke commands specific to the people in my friends' Discord server.

v1.1.0 - Added SauceVote functionality, and also refactored some small things, mostly to do with help commands.

v1.1.1 - "Table-ized" the code so that each Discord server has its own votes, wheels, etc.

## What is The Movie Wheel ™️ ?

Two of my friends had a recurring movie night, where they would put a big list of movies they both wanted to watch on a wheel and then spin it to randomly determine what they would watch that night. All three Kizumonogatari movies were on that wheel. It was truly the best.

Anyway, they asked me if I could make something like that but for the entire friend group. This is that. Users can interact with it using the following commands...

> /helpwheel - Lists out all relevant commands.
>
> /explainwheel - Explains how the wheel works.
>
> /submit [movie] - Add a movie to the wheel. You get up to two entries.
>
> /delete [number] - Delete a movie you've added to the wheel. This only works on movies that haven't already been seen.
>
> /check - Publicly prints out all movies left on the wheel without revealing who submitted what movie.
>
> /spin - Spins the wheel to get a movie to watch. It is then "removed" from the wheel, and can't be chosen again.
> 
> * A little note: the wheel is biased towards people from whom we haven't seen any movies yet.
>
> /something_cool - Marcus asked for this.

And some admin commands. Probably more too?

## What is Sauce Vote?

At one point like three years ago, someone used the phrase "top funny" to me and it immediately became embedded into my vocabulary. I randomly had the idea to have people "vote on the top funny of the night", and made this to encapsulate that.

Anyone in the server can vote for a user, and at the end of the night (set to 5 AM UTC --> 12 AM EST) the user(s) with the highest number of votes will be awarded a highly valuable* **Sauce Coin.**

> /helpvote - Lists out all relevant commands.
>
> /explainvote - Explains how voting works.
>
> /vote [user] - Vote for a given user.
>
> /audit - Shows current vote tallies.
>
> /leaderboard - Shows everyone's Sauce Coin balance from greatest to least.
>
> /balance - Shows how many Sauce Coins you have. 

*Sauce Coins do not currently do anything.  

## How was it made?
Most of this code was based off the tutorials, example code, and documentation on [discord.py](https://discordpy.readthedocs.io/en/stable/), which is a really great site. I knew basically nothing about making a Discord bot with slash commands, and then was able to code the bulk of the wheel and test it within 6 hours one random night. Making the shitty art in `media/` took longer than that. I highly recommend discord.py for beginners.

## How do I run this?

0. Install Python 3.
1. In the main directory, create a file called `secret.txt`. Grab your bot's token from [Discord's developer portal.](https://discord.com/developers/applications) Paste it into `secret.txt` such that the only content of the file is that token.
2. Optional: change around some values in main.py so that references to my user ID will be yours instead. This way the admin commands will work. You can do the same with the bot's user ID as well to have it match your bot's. Mess around with the code however you want.
3. From the root directory, open up a terminal and run `python3 main.py`.

## How do I submit feature requests?

How are you even looking at this README? Anyway, you can just ask me if you want me to do something. I'll do it if it seems cool. 

## Can I copy the code?

Feel free, as long as you don't use my user ID in some nefarious way. You could probably make all of this yourself without my help, though I'm totally fine with you using this as a reference or even ripping it wholecloth.

## Can I copy the art?

Make your own! It's more fun that way.