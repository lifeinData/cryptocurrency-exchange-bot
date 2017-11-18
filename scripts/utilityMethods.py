import requests as req


class UtilityMethods:
    def __init__(self, currency_type=None):
        self.currency_type = currency_type
        self.currency_type_dict = dict
        self.currency_key_list = list
        self.currency_value_list = list
        self.currency_key_list_original = list
        self.repeated_currency_list = []
        self.get_all_currencies_dict() # dictionary containing all currency types


    def get_all_currencies_dict(self):
        currency_list = 'C:\Reddit Bot\Bit Coin Bot\data files\currency list.txt'

        # opens the notepad containing all currencies and stores the values
        with open(currency_list):
            data = open(currency_list).readlines()

        data = str(data[0]).split(',')

        # creates a dictionary of the short form and long form
        for s in data[:]:
            if s.find('primary') > 0 or s.find('secondary') > 0:
                data.remove(s)

        # replaces the special characters with blanks
        data = list(i.replace('{', '') for i in data)
        data = list(i.replace('"', '') for i in data)
        data = list(i.split(":")[1] for i in data)

        # makes list into a dictionary using i and i + 2 as key, value respectively
        self.currency_type_dict = dict(data[i:i + 2] for i in range(0, len(data), 2))
        self.append_index_values()  # maps out the indexes of the the key and value lists

    def append_index_values(self):
        self.currency_key_list_original = list(self.currency_type_dict.keys())
        currency_value_list = list(self.currency_type_dict.values())

        def append_index_to_list(currency_list):
            currency_list_appended = []
            for key in currency_list:
                key_index_list = [key, currency_list.index(key)]
                currency_list_appended.append(key_index_list)

            return sorted(currency_list_appended, key=lambda x: x[0].lower())

        self.currency_value_list = append_index_to_list(currency_value_list)
        self.currency_key_list = append_index_to_list(self.currency_key_list_original)

    # gets json file from crpytonator
    def get_exchange_json(self):
        url = 'https://api.cryptonator.com/api/full/' + self.currency_type + "-USD"
        data = req.get(url).json()
        print(url)
        return data

    # checks if the table was already made
    def check_repeated_currency_status(self, currency):
        if self.repeated_currency_list == []:
            self.repeated_currency_list.append(currency)
            return False
        else:
            for currency_name in self.repeated_currency_list:
                if currency_name == self.currency_type:
                    return True

            self.repeated_currency_list.append(currency)
            return False

    # checks if the comment was replied to already
    def check_repeated_comment(self, comment_id):

        comment_list = 'C:\Reddit Bot\Bit Coin Bot\data files\commentID_list.txt'
        comment_txt = open(comment_list, 'r').read()

        if comment_txt.find(comment_id) == -1 and comment_txt == '':
            open(comment_list, 'a').write(comment_id)
        elif comment_txt.find(comment_id) == -1 and comment_txt != '':
            open(comment_list, 'a').write('\n' + comment_id)
        else:
            print('Already replied to comment ' + comment_id)
            return True

        return False

    # tries to find if the target word appears in the list
    #  TODO: complete binary search method
    def find_word(self, target_word):
        #  binary search function for the list and target word
        def binary_search(target_list, target_word):
            if len(target_word) >= 2:
                start = 0
                end = len(target_list) - 1
                while start <= end:
                    middle = (start + end) // 2
                    midpoint = target_list[middle][0].lower()
                    if str(midpoint) > target_word:
                        end = middle - 1
                    elif str(midpoint) < target_word:
                        start = middle + 1
                    else:

                        return [midpoint, target_list[middle][1]]

            return None

        found_currency_type_using_key = binary_search(self.currency_key_list, target_word.lower())
        found_currency_type_using_value = binary_search(self.currency_value_list, target_word.lower())

        if found_currency_type_using_key is not None:
            self.currency_type = found_currency_type_using_key[0].upper()
            return self.currency_type

        elif found_currency_type_using_value is not None:
            self.currency_type = self.currency_key_list_original[found_currency_type_using_value[1]]
            return self.currency_type
        else:
            return None

    def get_currency_name(self):
        return self.currency_type


util = UtilityMethods()
util.get_all_currencies_dict()
