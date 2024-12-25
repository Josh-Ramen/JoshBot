import discord
from discord import app_commands
import os.path
from tinydb import TinyDB

import movie_wheel.database as wheel_db
import movie_wheel.embeds as wheel_embeds
import vote_sauce.database as vote_db
import vote_sauce.embeds as vote_embeds
import vote_sauce.functions as vote_functions

# Boiler plate setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Server ID consts
test_server_id = 844722312959754300
real_server_id = 452540746139172866
full_server_list = [discord.Object(id=test_server_id), discord.Object(id=real_server_id)]

# My consts
my_user_id = 321039002268467200

# Wheel database
# {uuid: int, unseen_movies: list, seen_movies: list}
wheel_database = TinyDB('movie_wheel/movie_wheel_db.json')

# Vote databases
vote_database = TinyDB('vote_sauce/votes_db.json')
leaderboard_database = TinyDB('vote_sauce/leaderboard_db.json')

# Ready listener
@client.event
async def on_ready():
    await tree.sync()
    print("JoshBot is now online!")

# General commands

@tree.command(
    name="help",
    description="Do you need something?"
)
async def help(interaction):
    await interaction.response.send_message(embed=wheel_embeds.wheel_help_embed, ephemeral=True)

@tree.command(
    name="explainyourself",
    description="It's not that complicated!"
)
async def explain(interaction):
    await interaction.response.send_message(embed=wheel_embeds.wheel_explain_embed, ephemeral=True)

@tree.command(
    name="changelog",
    description="Here's what's new!"
)
async def explain(interaction):
    await interaction.response.send_message(embed=wheel_embeds.changelog_embed)

# Wheel commands

@tree.command(
    name="submit",
    description="Add something to the wheel!"
)
@app_commands.describe(movie="The name of the movie you'd like everyone to see.")
async def submit(interaction: discord.Interaction, movie: str = None):
    if (movie is None):
        # VS Code lies, this can be reached if the arg is excluded
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_submit_error_embed("You need to submit a movie name... please do that next time."),
            ephemeral=True
        )
    else:
        entry = wheel_db.find_or_create_user_entry(interaction.user.id, wheel_database)

        # Attempt to add a new movie
        add_result = entry.add_movie(movie)
        if (not add_result):
            await interaction.response.send_message(
                embed=wheel_embeds.wheel_submit_error_embed("We've already seen both your movies. Wait until next time!"),
                ephemeral=True
            )
            return
        
        # Update wheel database and notify the user
        wheel_db.update_user_entry(entry, wheel_database)

        if (type(add_result) is str):
            # Partial success, we had to drop a movie
            await interaction.response.send_message(
                embed=wheel_embeds.wheel_submit_partial_embed("I added the movie *{}* to your list, but to do that I had to remove *{}* from your list.".format(movie, add_result)),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=wheel_embeds.wheel_submit_success_embed("I added the movie *{}* to your list.".format(movie)),
                ephemeral=True
            )

@tree.command(
    name="delete",
    description="Did you change your mind?"
)
@app_commands.describe(number="Either 1 or 2; the slot of the movie to delete. (Use /check to see your submissions!)")
async def delete(interaction: discord.Interaction, number: int = None):
    entry = wheel_db.find_or_create_user_entry(interaction.user.id, wheel_database)

    # No number input
    if (number is None):
        # VS Code lies, this can be reached if the arg is excluded
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("I need the number of the movie you want me to delete. It's either 1 or 2! Use **/check** to see which one comes first and which one comes second."),
            ephemeral=True
        )
        return
    
    # Not a number
    num_as_int = None
    try:
        num_as_int = int(number)
    except ValueError:
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("That's not a number. I need either 1 or 2 by themselves!"),
            ephemeral=True
        )
        return
    
    # Number out of range
    if (num_as_int == 0):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("Ah- um. Are you a programmer? I wanted this to be friendly to non-programmers, so I'm not counting from zero... sorry. Anyway, try again with either 1 or 2."),
            ephemeral=True
        )
        return
    if (num_as_int != 1 and num_as_int != 2):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("Okay, that *is* a number... But really, it has to be either 1 or 2! You only get 2 movies, right?"),
            ephemeral=True
        )
        return
    
    # Number not founded in reality
    entry = wheel_db.find_or_create_user_entry(interaction.user.id, wheel_database)
    if (len(entry.unseen_movies) == 0 and len(entry.seen_movies) == 0):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("You haven't even submitted any movies! What do you want me to delete? ...Are you bullying me?"),
            ephemeral=True
        )
        return
    if (len(entry.unseen_movies) == 0):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("All your movies have already been watched. I can't delete a movie you've already seen!"),
            ephemeral=True
        )
        return
    if (num_as_int > len(entry.unseen_movies)):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("You only have one unseen movie! There isn't a second one to delete."),
            ephemeral=True
        )
        return
    
    # We SHOULD be good now but who knows really
    try:
        deleted = entry.delete_movie(num_as_int - 1)
        wheel_db.update_user_entry(entry, wheel_database)
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_success_embed("I deleted *{}* from your list.".format(deleted)),
            ephemeral=True
        )
    except IndexError:
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("To be honest, I don't even know how this happened... I'm kind of embarrassed. Anyway, let my creator know so he can fix it..."),
            ephemeral=True
        )

@tree.command(
    name="check",
    description="Would you like a reminder?"
)
async def check(interaction: discord.Interaction):
    user_entry = wheel_db.find_or_create_user_entry(interaction.user.id, wheel_database)
    await interaction.response.send_message(
        embed=wheel_embeds.wheel_check_embed(user_entry.to_desc()),
        ephemeral=True
    )

@tree.command(
    name="wheel",
    description="I'll show you what's left on the list!"
)
async def wheel(interaction: discord.Interaction):
    all_movies_list = wheel_db.accumulate_entries(wheel_database.all())
    await interaction.response.send_message(embed=wheel_embeds.wheel_wheel_embed(all_movies_list))

@tree.command(
    name="spin",
    description="Leave it up to luck!"
)
async def spin(interaction: discord.Interaction):
    candidates = wheel_db.get_spin_candidates(wheel_database.all())

    # Check if we just got an empty list
    if (len(candidates) == 0):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_spin_error_embed("The wheel is currently empty, sorry...")
        )
        return
    
    chosen_entry = wheel_db.select_candidate(candidates)
    movie_to_watch = chosen_entry.watch_movie()
    wheel_db.update_user_entry(chosen_entry, wheel_database)

    await interaction.response.send_message(embed=wheel_embeds.wheel_spin_success_embed(movie_to_watch))

# Vote commands

@tree.command(
    name="vote",
    description="Vote for someone to be tonight's winner!"
)
@app_commands.describe(user="The @ of the user you want to vote for.")
async def vote(interaction: discord.Interaction, user: discord.Member):
    existing_vote = vote_db.find_vote(interaction.user.id, vote_database)

    update_result = vote_db.update_vote(existing_vote, user.id)
    if (update_result <= 0):
        # Vote didn't change
        vote_user = interaction.guild.get_member(user.id)
        await interaction.response.send_message(
            embed=vote_embeds.vote_error_embed("You already voted for {} , so there's nothing for me to do...".format(vote_user.mention)),
            ephemeral=True
        )
        return
    
    # Vote was successfully changed
    vote_db.send_vote(existing_vote, vote_database)
    # Spite message branch
    if (existing_vote.old_vote_uuid != -1):
        old_vote_user = interaction.guild.get_member(existing_vote.old_vote_uuid)
        await interaction.response.send_message(
            embed=vote_embeds.vote_success_embed(
                "{} voted for {} !\n...And thus removed a vote for {} !".format(interaction.user.mention, user.mention, old_vote_user.mention)
            )
        )
    else:
        await interaction.response.send_message(
            embed=vote_embeds.vote_success_embed(
                "{} voted for {} !".format(interaction.user.mention, user.mention)
            )
        )

async def tally_job():
    guild = client.get_guild(test_server_id)
    message_dest = guild.system_channel
    winners = vote_db.tally_votes(vote_database)
    if (len(winners) < 1):
        await message_dest.send(embed=vote_embeds.tally_no_votes_embed())
        return

    vote_db.purge_votes(vote_database)
    await message_dest.send(
        embed=vote_embeds.tally_success_embed(vote_functions.get_winner_title(list(winners), guild))
    )

@tree.command(
    name="audit",
    description="Check how many votes everyone has right now."
)
async def audit(interaction: discord.Interaction):
    candidates = vote_db.audit_votes(vote_database)
    if (len(candidates) < 1):
        await interaction.response.send_message(embed=vote_embeds.audit_no_votes_embed, ephemeral=True)
        return
    
    message = vote_functions.get_audit_desc(candidates, interaction.guild)
    await interaction.response.send_message(embed=vote_embeds.audit_success_embed(message))

# Joke commands

@tree.command(
    name="something_cool",
    description="By popular demand!"
)
async def something_cool(interaction: discord.Interaction):
    extension = 'gif' if (interaction.user.id == my_user_id) else 'png'
    fp = f'media/something_cool/{interaction.user.id}.{extension}'
    if os.path.isfile(fp):
        await interaction.response.send_message(file=discord.File(fp))
    else:
        await interaction.response.send_message(file=discord.File(fp='media/something_cool/default.png'))

# Admin commands

@tree.command(
    name="unspin",
    description="I was hoping you wouldn't need this..."
)
async def unspin(interaction: discord.Interaction):
    # Check sender permissions
    is_admin = interaction.user.guild_permissions.administrator
    if (not is_admin):
        await interaction.response.send_message(embed=wheel_embeds.wheel_unspin_error_embed("You need the Administrator permission on this server to do that."), ephemeral=True)
        return
    else:
        wheel_db.unwatch_all_entries(wheel_database.all(), wheel_database)
        await interaction.response.send_message(embed=wheel_embeds.wheel_unspin_success_embed)

@tree.command(
    name="reset",
    description="Bring it all back to zero."
)
async def reset(interaction: discord.Interaction):
    # Check sender permissions
    is_josh = interaction.user.id == my_user_id
    if (not is_josh):
        await interaction.response.send_message(file=discord.File(fp='media/no.mp4'))
        return
    else:
        wheel_database.truncate()
        await interaction.response.send_message(embed=wheel_embeds.wheel_reset_success_embed)

@tree.command(
    name="tally",
    description="Bypass the wait time and stop the count now!"
)
async def tally(interaction: discord.Interaction):
    # Check sender permissions
    is_josh = interaction.user.id == my_user_id
    if (not is_josh):
        await interaction.response.send_message(file=discord.File(fp='media/no.mp4'))
        return
    
    await tally_job()


# Load secret and run
with open('secret.txt', 'r') as file:
    secret = file.read().rstrip()
    client.run(secret)