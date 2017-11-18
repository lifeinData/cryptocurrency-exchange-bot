import collections, praw


# TODO: Function get gets the top level comment
# TODO: Function that limits the amount of the comments you can post on a specific thread

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('crypto_exchange_bot',
                         user_agent='web:Cryptocurrency Market Bot V1 (by /u/crypto_exchange)')
    limits = reddit.auth.limits
    print('Authenticated as {}\n'.format(reddit.user.me()))
    print('Here are the limits for today \n' + str(limits))
    return reddit


class AntiSpamFunctions:
    def __init__(self, reddit, subreddit_string):
        self.reddit = reddit
        self.all_submissions = reddit.subreddit(subreddit_string).submissions()
        self.comment_limit = None
        self.submissions = None
        self.max_comment_level = None

    # TODO: [MP] allow input of %s
    #  checks if you've submitted more than the limit you set yourself
    def exceed_comments_per_submission(self, submission):
        return True if self.get_submissions_by_self(submission) > self.comment_limit else False

    # TODO: [LP] Awkward use of submission parameter here, might need to seperate out into another function later on
    # counts the # of submissions submitted by yourself for that specific thread
    def get_submissions_by_self(self, submission):
        self.submissions = submission
        self_comment_counter = 0
        for comment in submission.comments[:]:
            if comment.author.name == str(self.reddit.user._me):
                self_comment_counter += 1

        return self_comment_counter

    def set_comments_per_thread(self, comment_limit):
        self.comment_limit = comment_limit

    # TODO: [LP] Slow right now, could find alternative way of doing this
    #  Reply UP TO '@integer parameter : max_comment_level' depth of comment level
    def check_max_comment_depth_level(self):
        for comments in self.submissions.comments[:]:
            # submission.comments.replace_more(limit=0)
            comment_queue = comments.replies[:]
            print('initial ID = ' + comments.id)
            index = 0
            while True:
                try:
                    comment = comment_queue[index]
                    comment_queue.extend(comment.replies)
                    index += 1
                    print(comment.body)
                except IndexError:
                    break

            net_reply_comments = len(comment_queue) - self.max_comment_level

            return True if net_reply_comments > 0 else False

    def set_max_comment_depth_level(self, max_comment_level):
        self.max_comment_level = max_comment_level

    # TODO: [LP] relies on a notepad right now, make it not rely on a note pad
    @staticmethod
    def append_comment_to_ignorelist(level_of_comments, comment_level):
        comment_list = 'C:\Reddit Bot\Bit Coin Bot\data files\commentID_list.txt'
        comment_level = 1 if comment_level < 0 else comment_level
        for comment_id in level_of_comments[comment_level:]:
            open(comment_list, 'a').write('\n' + str(comment_id))