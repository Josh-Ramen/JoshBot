import datetime
import discord
from discord import app_commands
from discord.ext import tasks
import os.path
import random
from tinydb import TinyDB
from zoneinfo import ZoneInfo

import common.embeds as common_embeds
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

# My consts
my_user_id = 321039002268467200

# Wheel database
# {uuid: int, unseen_movies: list, seen_movies: list}
wheel_database = TinyDB('movie_wheel/movie_wheel_db.json')

# Vote databases
vote_database = TinyDB('vote_sauce/votes_db.json')
bank_database = TinyDB('vote_sauce/bank_db.json')

# Ready listener
@client.event
async def on_ready():
    await tree.sync()

    # Start the loop
    if not tally_job.is_running():
        tally_job.start()
    print("JoshBot is now online!")

# General commands

@tree.command(
    name="help",
    description="Do you need something?"
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=common_embeds.help_embed, ephemeral=True)

@tree.command(
    name="changelog",
    description="Here's what's new!"
)
async def changelog(interaction: discord.Interaction):
    await interaction.response.send_message(embed=common_embeds.changelog_embed)

# Wheel commands

@tree.command(
    name="helpwheel",
    description="I'll list out the wheel commands."
)
async def helpwheel(interaction: discord.Interaction):
    await interaction.response.send_message(embed=wheel_embeds.wheel_help_embed, ephemeral=True)

@tree.command(
    name="explainwheel",
    description="I can explain how the wheel works!"
)
async def explainwheel(interaction: discord.Interaction):
    await interaction.response.send_message(embed=wheel_embeds.wheel_explain_embed, ephemeral=True)

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
        return
    table = wheel_database.table(str(interaction.guild.id))
    entry = wheel_db.find_or_create_user_entry(interaction.user.id, table)

    # Attempt to add a new movie
    add_result = entry.add_movie(movie)
    if (not add_result):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_submit_error_embed("We've already seen both your movies. Wait until next time!"),
            ephemeral=True
        )
        return
    
    # Update wheel database and notify the user
    wheel_db.update_user_entry(entry, table)

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
    # No number input
    if (number is None):
        # VS Code lies, this can be reached if the arg is excluded
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_delete_error_embed("I need the number of the movie you want me to delete. It's either 1 or 2! Use **/check** to see which one comes first and which one comes second."),
            ephemeral=True
        )
        return

    table = wheel_database.table(str(interaction.guild.id))
    entry = wheel_db.find_or_create_user_entry(interaction.user.id, table)

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
    entry = wheel_db.find_or_create_user_entry(interaction.user.id, table)
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
        wheel_db.update_user_entry(entry, table)
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
    table = wheel_database.table(str(interaction.guild.id))
    user_entry = wheel_db.find_or_create_user_entry(interaction.user.id, table)
    await interaction.response.send_message(
        embed=wheel_embeds.wheel_check_embed(user_entry.to_desc()),
        ephemeral=True
    )

@tree.command(
    name="wheel",
    description="I'll show you what's left on the list!"
)
async def wheel(interaction: discord.Interaction):
    table = wheel_database.table(str(interaction.guild.id))
    all_movies_list = wheel_db.accumulate_entries(table)
    await interaction.response.send_message(embed=wheel_embeds.wheel_wheel_embed(all_movies_list))

@tree.command(
    name="spin",
    description="Leave it up to luck!"
)
async def spin(interaction: discord.Interaction):
    table = wheel_database.table(str(interaction.guild.id))
    candidates = wheel_db.get_spin_candidates(table)

    # Check if we just got an empty list
    if (len(candidates) == 0):
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_spin_error_embed("The wheel is currently empty, sorry...")
        )
        return
    
    chosen_entry = wheel_db.select_candidate(candidates)
    movie_to_watch = chosen_entry.watch_movie()
    wheel_db.update_user_entry(chosen_entry, table)

    await interaction.response.send_message(embed=wheel_embeds.wheel_spin_success_embed(movie_to_watch))

# Vote commands

@tree.command(
    name="helpvote",
    description="I'll list out the vote commands."
)
async def helpvote(interaction: discord.Interaction):
    await interaction.response.send_message(embed=vote_embeds.vote_help_embed, ephemeral=True)

@tree.command(
    name="explainvote",
    description="I can explain how voting works!"
)
async def explainvote(interaction: discord.Interaction):
    await interaction.response.send_message(embed=vote_embeds.vote_explain_embed, ephemeral=True)

@tree.command(
    name="vote",
    description="Vote for someone to be tonight's winner!"
)
@app_commands.describe(user="The @ of the user you want to vote for.")
async def vote(interaction: discord.Interaction, user: discord.Member):
    table = vote_database.table(str(interaction.guild.id))

    existing_vote = vote_db.find_vote(interaction.user.id, table)
    update_result = existing_vote.change_vote(user.id)
    if (update_result <= 0):
        # Vote didn't change
        vote_user = interaction.guild.get_member(user.id)
        await interaction.response.send_message(
            embed=vote_embeds.vote_error_embed("You already voted for {} , so there's nothing for me to do...".format(vote_user.mention)),
            ephemeral=True
        )
        return
    
    # Vote was successfully changed
    vote_db.send_vote(existing_vote, table)
    
    vote_desc = vote_functions.get_vote_desc(existing_vote, user, interaction)
    await interaction.response.send_message(
            embed=vote_embeds.vote_success_embed(vote_desc)
        )

@tree.command(
    name="voterandom",
    description="Gamble with your vote!"
)
async def voterandom(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    
    table = vote_database.table(str(interaction.guild.id))

    # Get a random user from the current server
    user = random.choice(interaction.guild.members)

    existing_vote = vote_db.find_vote(interaction.user.id, table)
    update_result = existing_vote.change_vote(user.id)
    if (update_result <= 0):
        # Vote didn't change
        vote_user = interaction.guild.get_member(user.id)
        await interaction.followup.send(
            embed=vote_embeds.vote_error_embed("You randomly selected {} again, so nothing happened.".format(vote_user.mention)),
        )
        return
    
    # Vote was successfully changed
    vote_db.send_vote(existing_vote, table)
    
    vote_desc = vote_functions.get_vote_desc(existing_vote, user, interaction)
    await interaction.followup.send(
            embed=vote_embeds.vote_success_embed(vote_desc)
        )

@tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=ZoneInfo("America/New_York")))
async def tally_job():
    for guild in client.guilds:
        message_dest = guild.system_channel
        vote_table = vote_database.table(str(guild.id))
        bank_table = bank_database.table(str(guild.id))

        winners = vote_db.tally_votes(vote_table)
        if (len(winners) < 1):
            await message_dest.send(embed=vote_embeds.tally_no_votes_embed())
            return

        vote_db.purge_votes(vote_table)
        vote_db.reward_winners(winners, bank_table)
        await message_dest.send(
            embed=vote_embeds.tally_success_embed(vote_functions.get_winner_title(list(winners), guild))
        )

@tree.command(
    name="audit",
    description="Check how many votes everyone has right now."
)
async def audit(interaction: discord.Interaction):
    table = vote_database.table(str(interaction.guild.id))
    
    candidates = vote_db.audit_votes(table)
    if (len(candidates) < 1):
        await interaction.response.send_message(embed=vote_embeds.audit_no_votes_embed(), ephemeral=True)
        return
    
    message = vote_functions.get_audit_desc(candidates, interaction.guild)
    await interaction.response.send_message(embed=vote_embeds.audit_success_embed(message))

@tree.command(
    name="balance",
    description="Check how many Sauce Coins you've earned."
)
async def balance(interaction: discord.Interaction):
    table = bank_database.table(str(interaction.guild.id))
    balance = vote_db.get_balance(interaction.user.id, table)
    await interaction.response.send_message(embed=vote_embeds.balance_success_embed(balance))

@tree.command(
    name="leaderboard",
    description="See who's earned the most coins!"
)
async def leaderboard(interaction: discord.Interaction):
    table = bank_database.table(str(interaction.guild.id))
    leaderboard = vote_db.get_leaderboard(table)
    if (len(leaderboard) == 0):
        await interaction.response.send_message(embed=vote_embeds.leaderboard_empty_embed())
        return
    
    message = vote_functions.get_leaderboard_desc(leaderboard, interaction.guild)
    await interaction.response.send_message(embed=vote_embeds.leaderboard_success_embed(message))

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
        await interaction.response.send_message(
            embed=wheel_embeds.wheel_unspin_error_embed("You need the Administrator permission on this server to do that."),
            ephemeral=True
        )
        return

    table = wheel_database.table(str(interaction.guild.id))
    wheel_db.unwatch_all_entries(table)
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

    table = wheel_database.table(str(interaction.guild.id))
    table.truncate()
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
    
    await interaction.response.send_message("Working on it, boss!", ephemeral=True)
    await tally_job()


# Load secret and run
with open('secret.txt', 'r') as file:
    secret = file.read().rstrip()
    client.run(secret)
