# egldtracker

### Requirements
- python3.x
-- tweepy
--mysql-connector-python
- system
-- mysql/mariadb


## Installation

Rename the template_cred.py file into cred.py enter the correct values in the cred.py file.

### Execution
The script transactionscrawler.py grabs the last 2000 transactions from explorer.elrond.com. You have to execute the script more often when elronds ecosystem grows.
Use this cronjob to execute the crawler in 5 minute intervals.
```sh
*/5 * * * * path_to_python3 path_to_script/transactions_crawler.py > /dev/null 2>&1
```

The main script runs on a hourly base. Execute the all.py script in a cronjob like this.
```sh
1 * * * * path_to_python3 path_to_script/all.py > /dev/null 2>&1
```

### Smart Contract Codes
Through reverse engineering I found out which codes stand for what. But the list can and will grow. There is currently too little data available. <br>
reDelegateRewards = 'cmVEZWxlZ2F0ZVJld2FyZHM=' 
relayedTo = starts with 'cmVsYXllZFR4QDdiMjI2ZTZmNmU2MzY1MjIzYTM' 
unDelegate = starts with 'dW5EZWxlZ2F0ZU'
claimRewards = 'Y2xhaW1SZXdhcmRz' 
unBondNodes = starts with 'dW5Cb25kTm9kZXNA' 
withdraw = 'd2l0aGRyYXc=' 
delegate = 'ZGVsZWdhdGU=' 
unBond = 'dW5Cb25k' 
unBondTokens = 'dW5Cb25kVG9rZW5z' 
unStakeNodes = starts with 'dW5TdGFrZU5vZGVzQD'Q 
unStake = unconfirmed dW5TdGFrZUAwODQzMzdjZjA3Mzc2YWExNTVkNWIxYjYxZTdmMzNmZWFkNDI1NzE5YzFiMzhiZmFkNzlkMjE2ODY5NTY1YjEwMjk5YmYwMmY3M2U2Yzk1MDQ2YmUyNzMyYWQ0NzQwMTA2NTlmMmIyNjEyZTM5NTNmMzExYTMxMzdlN2I4NzMxZDg5Y2UwMDFhMjQ2ZTc4NzkyMTQ1Yzk5NzA5YThlZmQyM2I1MmViMzJlYzM4OGE3YjQ0ZTI4OTE5NjI0NTJkODQ= or starts with dW5T

**DB Query to check if new codes appeared**

SELECT * FROM transactions WHERE scaction NOT LIKE 'cmVEZWxlZ2F0ZVJld2FyZHM=' AND scaction NOT LIKE 'cmVsYXllZFR4QDdiMjI2ZTZmNmU2MzY1MjIzYTM%' AND scaction NOT LIKE 'dW5EZWxlZ2F0ZU%' AND scaction NOT LIKE 'Y2xhaW1SZXdhcmRz' AND scaction NOT LIKE 'dW5Cb25kTm9kZXNANmQ2Nj%' AND scaction NOT LIKE 'd2l0aGRyYXc=' AND scaction NOT LIKE 'ZGVsZWdhdGU=' AND scaction NOT LIKE 'dW5Cb25k' AND scaction NOT LIKE 'dW5Cb25kVG9rZW5z' AND scaction NOT LIKE 'dW5TdGFrZU5vZGVzQD%' AND scaction NOT LIKE 'dW5TdGFrZUAwODQzMzdjZjA3Mzc2YWExNTVkNWIxYjYxZTdmMzNmZWFkNDI1NzE5YzFiMzhiZmFkNzlkMjE2ODY5NTY1YjEwMjk5YmYwMmY3M2U2Yzk1MDQ2YmUyNzMyYWQ0NzQwMTA2NTlmMmIyNjEyZTM5NTNmMzExYTMxMzdlN2I4NzMxZDg5Y2UwMDFhMjQ2ZTc4NzkyMTQ1Yzk5NzA5YThlZmQyM2I1MmViMzJlYzM4OGE3YjQ0ZTI4OTE5NjI0NTJkODQ=' AND scaction NOT LIKE 'dW5Cb25kTm9kZXNA%'


