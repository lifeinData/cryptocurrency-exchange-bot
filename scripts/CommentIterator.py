import scripts.utilityMethods as utilityMethods
import scripts.MarketDataTable as Market_Table

class CommentIterator:
    # initiates the iterator to go through each comment with the antispam parameters
    # TODO: [MP] give option of max time or max submissions
    def __init__(self, subreddit_string, reddit, max_submissions, anti_spam_functions):
        self.sub_reddit = subreddit_string
        self.reddit = reddit
        self.max_submissions = max_submissions
        self.anti_spam_functions = anti_spam_functions
        self.markets_df = None
        self.json_status = False
        self.complete_table_list = None
        self.utility_methods = utilityMethods.UtilityMethods()
        self.iterate_through_submissions()

    def iterate_through_submissions(self):
        for submission in self.reddit.subreddit(self.sub_reddit).submissions():
            if self.anti_spam_functions.exceed_comments_per_submission(submission) is not True and \
                    self.anti_spam_functions.check_max_comment_depth_level() is False:

                self.iterate_through_comments_of_submission(submission)

    def iterate_through_comments_of_submission(self, submission):
        for comment in submission.comments[:]:
            self.complete_table_list = []
            self.iterate_through_word_of_comment(comment)

    # go through each word of the comment and utilizes binary search to find the word in the list
    # of possible api parameters
    # TODO: [MP] replace "swear_jar_bott" with the actual username argument
    def iterate_through_word_of_comment(self, comment):
        if self.utility_methods.check_repeated_comment(comment.id) is False and comment.author.name != "swear_jar_bott":
            self.find_word_and_comment(comment.body.split(), comment)
        else:
            print('comment id: ' + comment.id + " is repeated")

    def find_word_and_comment(self, comment_words_list, comment):
        for word in comment_words_list:
            currency_name = self.utility_methods.find_word(word)
            proceed_to_comment = self.create_markets_df_using_json(currency_name)

            if proceed_to_comment and len(word) > 2:
                self.index_comment_reply(word)

        self.reply_comment_tables(comment)

    # creates a market data frame out of the found currency json file if it's not a repeated currency
    def create_markets_df_using_json(self, currency_name):
        if currency_name is not None:
            full_match_found = True  # flag if a match is found or not, defaults to not assigned
            repeated_currency = self.utility_methods.check_repeated_currency_status(currency_name)
        else:
            return False

        if full_match_found is True and repeated_currency is False:
            self.markets_df = Market_Table.MarketTable(self.utility_methods.get_exchange_json())
            self.json_status = self.markets_df.get_json_status()  # make sure json file is valid
            return True

    def index_comment_reply(self, comment_word):
        # a list of complete tables if there is more than 1 crypto currency in the comment
        if self.json_status:
            table_comment = self.markets_df.get_table_comment(comment_word)
            if table_comment is not False:
                self.complete_table_list.append(table_comment)
        else:
            print("Json file does not contain enough info")

    def reply_comment_tables(self, comment):
        if self.complete_table_list is not None and self.json_status:
            # replies with the tables if there are any
            complete_table = ""
            for table in self.complete_table_list:
                if complete_table == "":
                    complete_table = table
                else:
                    complete_table = complete_table + '''&nbsp;\n\n&nbsp;\n\n ''' + table

            comment.reply(complete_table)
            print("Replied Successfully to comment " + comment.id)

        else:
            print('No replies for ' + comment.id)
