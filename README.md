# Cryptocurrency Exchange Bot

## Overview
Reddit bot that gives out the top five exchanges selling a specific cryptocurrency. The crpytocurrency is determined by scanning reddit comments for specific cryptocurrency strings. The program then makes a call to a webservice that returns a json file related to the cryptocurrency. The data in the json file is transformed into a reddit table.

## Files
**/scripts/bitCoinBot.py**
- main() of bot 

*Program Flow:* 
1. Athenticate Credentials for Reddit API calls
2. Search words in comments in specific subreddit
3. If word in comment matches crpytocurrency dictionary, get related json file via HTTPS request
4. Transform json into reddit table format to post

**/scripts/MarketDataTable.py**
- Class responsible for creating reddit table which is then stored in a list if there are more than 1 key word matches

**/scripts/utilityMethods.py**
- Class responsible for providing dictionary search algorithms. Uses binary search to search each comment word in a list of ~2100           entries. 

**/scripts/praw.ini**
- Athentication configurations


**/data files/commentID_list.txt**
- Used as storage for comments replied to already

**/data files/currency list.txt**
- The cleaned up dictionary list used 
