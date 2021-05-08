import requests
import json
import sys
import time
import datetime 

import functions
import authentication
import db

##Variables
timestamp = int(time.time())
timestamp_1h = timestamp - 3600
timestamp_1m = timestamp - 60
timestamp_1h1m = timestamp - 3660
timestamp_10d = timestamp - 864060
today = datetime.datetime.now()

balances = 0
all_transactions = 0
out_tra = 0
in_tra = 0
out_egld = 0
in_egld = 0
fin_out_egld = 0
fin_in_egld = 0
stake_balance = 0
true_staked_val = 0
total_stakes = 0
sc_balance = 0
wallet = ["erd15qltd5ccalm5smmgdc5wnx46ssda3p32xhsz4wpp6usldq7hq7xqq5fmn6","erd16x7le8dpkjsafgwjx0e5kw94evsqw039rwp42m2j9eesd88x8zzs75tzry","erd1rf4hv70arudgzus0ymnnsnc4pml0jkywg2xjvzslg0mz4nn2tg7q7k0t6p","erd1v4ms58e22zjcp08suzqgm9ajmumwxcy4hfkdc23gvynnegjdflmsj6gmaq","erd18umqd6v045nww2g9kgneupj4dwme9lycrpjn293sfkrhpntx9z2ss4kvhg","erd1rm8pg3yrngzyhrjejkz3xq2lfp64mvnt64llj3fyft53d3t4ckjq0q8v4k","erd1043dp0s3yw8vd44s5xvxklnp30ypp7y56mylm9t87vdhhgwcx24s2e2g5y","erd1a56dkgcpwwx6grmcvw9w5vpf9zeq53w3w7n6dmxcpxjry3l7uh2s3h9dtr","erd18s4cfunrctf27ejp3jmvylff7psfdgdssgc7e5aal6yusac62xzqly0yh5","erd1tqun7ku6yrygd0gjezmmz42jffqzlhgtvl2tsch3cel7rfylwzxs2dhrcg","erd1lanz397mngt637705m6sk67jjs9uuqp0rerce73ud48x3xvxtxjqe5umzj","erd1jfempey50xue4wa5hzwmle4p4y6g55dn4327m9pvrynttdscn2eqvaxcgy","erd1z27mr0ertnan43avl4uhrud67awtkqklfsxzpetkp5u26cscsrzqdl56j8","erd1qt827an62lztf74rx7cg2s6utx3dp6l8k9snlttd77zny4dlzr9qccdqgx"]
stakewallet = ["erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllst77y4l","erd1qqqqqqqqqqqqqpgqxwakt2g7u9atsnr03gqcgmhcv38pt7mkd94q6shuwt"]



###Staking Pool Stats
old_stake = functions.staketotal()
cur_stake = functions.stakestatspush(stakewallet)
dif_stake = abs(int(old_stake) - int(cur_stake[1]))

#lala = functions.transactions()

unbonded = functions.unbond(timestamp_1h1m, timestamp_1m)
unbonded10 = functions.unbond10(timestamp_10d, timestamp_1m)
claimed = functions.claimRewards(timestamp_1h1m, timestamp_1m)
redelegated = functions.redelegateRewards(timestamp_1h1m, timestamp_1m)



for i in range(len(wallet)):
    print(wallet[i])
    # Gain access to all exchange wallets balance
    #balances = balances + functions.balance(wallet[i])
    # Sum up all balances on exchanges
 #   balance = round(balances / 1000000000000000000)
    # Gain access to all needed exchange datas
    tv = functions.exchanges(wallet[i], timestamp_1h)
    # Sum up all transactions of exchanges
    all_transactions = all_transactions + tv[0]
    # Sum up all transactions from exchanges
    out_tra = out_tra + tv[1]
    # Sum up all EGLD values sent away from exchanges
    out_egld = out_egld + tv[2]
    # Sum up all transactions to exchanges
    in_tra = in_tra + tv[3]    
    # Sum up all EGLD values from exchanges
    in_egld = in_egld + tv[4]
    balances = balances + tv[5]
    balance = round(balances / 1000000000000000000)

fin_out_egld = round(out_egld / 1000000000000000000)
fin_in_egld = round(in_egld / 1000000000000000000)
#total_egld = round((out_egld + in_egld) / 1000000000000000000)
total_egld = fin_out_egld + fin_in_egld

if fin_out_egld > fin_in_egld:
    trend = "Outflow"
elif fin_out_egld < fin_in_egld:
    trend = "Inflow"
else:
    trend = "Neutral"

if dif_stake > 0:
    stake_trend = f"{dif_stake:,} $EGLD joined the Staking Pool."
elif dif_stake < 0:
    stake_trend = f"{dif_stake:,} $EGLD left the Staking Pool"
else:
    stake_trend = "Nothing changed in Stacking"

file1 = open("/home/ubuntu/egld_tracker/output_test.txt","a")
file1.write(f"""
Date: {today}
Timeframe: 1h
No. $EGLD on Exchanges: {balance:,}
No. Transactions: O:{out_tra:,} I:{in_tra:,} T:{all_transactions:,}
No. $EGLD Transfered: O:{fin_out_egld:,} I:{fin_in_egld:,} T:{total_egld:,}
Trend: {trend}
Staking Pool:
No. $EGLD total staked: {cur_stake[1]:,}
{stake_trend}
Rewards: {claimed} claimed: {redelegated} redelegated
Unbond: {unbonded} initiated: {unbonded10} 10 days locked""")

file1.close()



#for i in range(len(stakewallet)):
#    print(stakewallet[i])
#    sc = int(functions.stakesc(stakewallet[i]))
#    sc_balance = sc_balance + sc
#sc_balances = round(sc_balance / 1000000000000000000)

#print(sc_balances)

#sv = functions.stakevalue()
#true_staked_val = round(sv)


#query = "SELECT staketotal FROM stakes ORDER BY id DESC LIMIT 1"
#cursor.execute(query)
# get all records
#records = cursor.fetchone()
#print("Old staketotal:", records[0])






#cursor = db.db.cursor()
#query = "INSERT INTO stakes (timestamp, sctotal, staketotal) VALUES (%s, %s, %s)"
#values = (timestamp, sc_balances, true_staked_val)
#cursor.execute(query, values)
#db.db.commit()

#functions.stakestatspush(stakewallet)
