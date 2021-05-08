# egldtracker

**Installation** 
Rename the templatecred.py file into cred.py
enter the correct values in the cred.py file.
Execute in fast intervals (5 minutes) the transactionscrawler.py with python3
Execute hourly the all.py with python3


Smart Contract Codes:

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


DB Query to check if new codes appeared

SELECT *  FROM `transactions` WHERE `scaction` NOT LIKE 'cmVEZWxlZ2F0ZVJld2FyZHM=' AND `scaction` NOT LIKE 'cmVsYXllZFR4QDdiMjI2ZTZmNmU2MzY1MjIzYTM%' AND `scaction` NOT LIKE 'dW5EZWxlZ2F0ZU%' AND `scaction` NOT LIKE  'Y2xhaW1SZXdhcmRz' AND `scaction` NOT LIKE 'dW5Cb25kTm9kZXNANmQ2Nj%' AND `scaction` NOT LIKE 'd2l0aGRyYXc=' AND `scaction` NOT LIKE 'ZGVsZWdhdGU=' AND `scaction` NOT LIKE 'dW5Cb25k' AND `scaction` NOT LIKE 'dW5Cb25kVG9rZW5z' AND `scaction` NOT LIKE 'dW5TdGFrZU5vZGVzQD%' AND `scaction` NOT LIKE  'dW5TdGFrZUAwODQzMzdjZjA3Mzc2YWExNTVkNWIxYjYxZTdmMzNmZWFkNDI1NzE5YzFiMzhiZmFkNzlkMjE2ODY5NTY1YjEwMjk5YmYwMmY3M2U2Yzk1MDQ2YmUyNzMyYWQ0NzQwMTA2NTlmMmIyNjEyZTM5NTNmMzExYTMxMzdlN2I4NzMxZDg5Y2UwMDFhMjQ2ZTc4NzkyMTQ1Yzk5NzA5YThlZmQyM2I1MmViMzJlYzM4OGE3YjQ0ZTI4OTE5NjI0NTJkODQ=' AND `scaction` NOT LIKE 'dW5Cb25kTm9kZXNA%'
