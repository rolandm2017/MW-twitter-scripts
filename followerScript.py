# A script to follow everyone who follows a given account. This one runs when activated.
import tweepy
from os import path
import time
from datetime import date

with open("secrets.txt", "r") as keys:
    keys = keys.readlines()[0].split(",")
    consumer_key = keys[0]
    consumer_secret = keys[1]
    # Add your access token and secret here...
    access_token = keys[2]
    access_token_secret = keys[3]
    target_account = keys[4][:-1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

database_name = "follower_script_database_{}.txt".format(target_account)

print("Starting script. Will auto-follow accounts who follow @%s" % target_account)
time.sleep(5)


def get_followers_from_db(db_name):
    with open(db_name, "r") as db:
        return db.read().split(",")


def start_following(users):
    """
    :param users: A list of accounts to follow.
    :return: Info about what happened. A list of who was followed + any error messages.
    """
    users_to_remove_from_database = []
    report = []
    report.append("Start of error logging...")
    calls_this_window = 0

    # Reset rate limitation
    time.sleep(60)  # TODO: uncomment the time.sleep for live version
    for user in users:
        try:
            # Follow the user
            api.create_friendship(id=user)  # TODO: uncomment this for live ver

            # Add the user to the report's "users_to_remove_from_database"
            users_to_remove_from_database.append(user)
        except Exception as e:
            report.append("Error detected...\n")
            report.append(str(e))

        calls_this_window += 1
        if calls_this_window > 394:  # Avoid rate limiting
            break

    return users_to_remove_from_database, report


def remove_accounts_from_database(success_stories, db_name):
    """ Removes all the success stories from the day's following activities from the database.

    :param success_stories: Account ids successfully followed by the start_following function.
    :param db_name: The name of the database as a string.
    :return: Remaining accounts in the database.
    """
    remaining_accounts = 0
    skipped_users = 0

    with open(db_name, "r") as db:
        users = db.read().split(",")[:-1]
    with open(db_name, "w") as db:
        for user in users:
            # First time script is run, success_stories is a list of ints.
            # After the first time, success_stories is a list of strings.
            # Hence the need for another if block.
            if int(user) in success_stories:
                skipped_users += 1
            elif user in success_stories:
                skipped_users += 1
            else:
                db.write(str(user))
                db.write(",")
                remaining_accounts += 1

    return remaining_accounts


def convert_report_to_txt(report, targeted_account):
    """ Turns any errors from the script into a .txt file. Used to exit the script.

    :param report: Any errors that need to be logged.
    :param targeted_account: The account the script was run on.
    :return:
    """
    reported_errors = 0

    today = date.today().strftime("%b-%d-%Y")

    report_file = open("report_for_{}_on_{}.txt".format(targeted_account, today), "w")
    for line in report:
        try:
            report_file.write(str(line))
            reported_errors += 1
        except Exception as oops:
            report_file.write("Oops! Couldn't write a line from the report. Info missing because of error: ")
            report_file.write(str(oops))
            report_file.write("\n")

    if reported_errors <= 1:  # There will always be one because I write "Start of error logging..." up above
        report_file.write("No errors detected.")

    report_file.close()


# If the database file exists, open the database and start following people.
if path.exists(database_name):
    print("395 of {}'s followers will be followed today.".format(target_account))
    time.sleep(3)  # Pause so user can read the message
    followers_from_db = get_followers_from_db(database_name)

    successes_and_report = start_following(followers_from_db)
    remainder = remove_accounts_from_database(successes_and_report[0], database_name)
    convert_report_to_txt(successes_and_report[1], target_account)

# if the database file still needs to be built, build the database:
else:
    # Get the total number of the target account's followers and output the expected runtime.
    total_followers = api.get_user(screen_name=target_account).followers_count
    runtime_in_hours = total_followers / 5000 / 60
    runtime_in_minutes = total_followers / 5000
    print("{} has {} followers. Expect the script to run for {} hours or {} minutes.".format(target_account,
                                                                                             total_followers,
                                                                                             runtime_in_hours,
                                                                                             runtime_in_minutes))

    # Build a list of accounts following the target account
    target_followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=target_account).pages():
        target_followers.extend(page)
        time.sleep(60)  # TODO: uncomment this code, remove the break statement

    # Save the list to a .txt file so the user can avoid getting followers every time the script is run
    f = open(database_name, "w+")
    for follower_id in target_followers:
        f.write(str(follower_id))
        f.write(",")
    f.close()

    # Start following people from the list. Auto-exit past 395 follows to avoid rate limiting.
    successes_and_report = start_following(target_followers)
    remainder = remove_accounts_from_database(successes_and_report[0], database_name)
    convert_report_to_txt(successes_and_report[1], target_account)

print("Done for the day. {} accounts remain on the to-follow list. Preparing to exit. 5.....".format(remainder))
# exit()  # todo: remove this exit() when finished debug
time.sleep(2)
print("4....")
time.sleep(1)
print("3...")
time.sleep(1)
print("2..")
time.sleep(1)
print("Thanks for using! Close the program anytime. ")
time.sleep(60)
exit()
