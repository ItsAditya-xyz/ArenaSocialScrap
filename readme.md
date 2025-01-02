This code gets the top accounts of arena.social and stores their info in a json file.


user_data has top 10,000 account info as of 2nd January 2025.

- ArenaScrap.py fetches top 10k accounts of arena.social
- fetchBday.py fetches birthday of top 10k accounts
- syncUser.py is required if some accounts in the created .json has createdOn as null 
