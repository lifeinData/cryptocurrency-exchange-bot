import praw
import time
import timeit
# TODO: [LP] figure out how to package
import scripts.AntiSpamFunctions as AntiSpamFunctions
import scripts.CommentIterator as CommentIterator

# TODO: [HP] Enable antispam functions
# TODO: [LP] match double word crpytocurrencies
def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('crypto_exchange_bot', user_agent='web:Crpytocurrency Market Bot V1 (by /u/crypto_exchange)')
    limits = reddit.auth.limits
    print('Authenticated as {}\n'.format(reddit.user.me()))
    print('Here are the limits for today \n' + str(limits))
    return reddit


# main program
def run_currency_exchange_bot(reddit, subreddit):

    # sets parameters for anti-spam functions
    antispam_functions = AntiSpamFunctions.AntiSpamFunctions(reddit, subreddit)
    antispam_functions.set_max_comment_depth_level(max_comment_level=1)
    antispam_functions.set_comments_per_thread(comment_limit=5)

    # sets parameter for how many submissions to go through and initiates the iteration
    max_submissions = 250
    CommentIterator.CommentIterator(subreddit, reddit, max_submissions, antispam_functions)

def main():
    reddit = authenticate()
    while True:
        # 'test_swearjar'
        # 'CryptoMarkets'
        subreddit = 'CryptoMarkets'
        run_currency_exchange_bot(reddit, subreddit)


if __name__ == '__main__':
    main()
