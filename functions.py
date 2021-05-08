import requests
import tweepy
import authentication
import json
import db
import time
import cred

##DB Connection
cursor = db.db.cursor()

#Authenticate to Telegram
def telegram_bot_sendtext(bot_message):

    bot_token = cred.telegram_api_key
    bot_chatID = cred.trelegram_chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cred.twitter_consumer_key,
    cred.twitter_consumer_secret)
auth.set_access_token(cred.twitter_access_token,
    cred.twitter_acces_key)

api = tweepy.API(auth)

def exchanges(wallet, timestamp_1h):
    #TRANSACTIONS
    r = requests.get('https://internal-api.elrond.com/transactions?size=2000&sender=' + wallet + '&receiver=' + wallet + '&condition=should&fields=txHash,receiver,receiverShard,sender,senderShard,status,timestamp,value', headers=authentication.headers)
    rwv = requests.get('https://internal-api.elrond.com/accounts/' + wallet, headers=authentication.headers)
    json_object = json.loads(r.content)
    json_object_wv = json.loads(rwv.content)

    balance = (int((json_object_wv["balance"])))

    #Variables
    transaction_count = 0
    outflow_tra_count = 0
    outflow_egld_count = 0
    inflow_tra_count = 0
    inflow_egld_count = 0
    for i in range(2000):
        try:
            timestamps = (json_object[i]["timestamp"])
            senders = (json_object[i]["sender"])
            values = (int((json_object[i]["value"])))

            if timestamps >= timestamp_1h:
                #bb = (json_object[i]["txHash"])
                transaction_count = transaction_count +1
                if senders == wallet:
                    outflow_tra_count = outflow_tra_count + 1
                    outflow_egld_count = (outflow_egld_count + values)
                else:
                    inflow_tra_count = inflow_tra_count + 1
                    inflow_egld_count =  (inflow_egld_count + values)
        except:
            message = "no data"
    return transaction_count, outflow_tra_count, outflow_egld_count, inflow_tra_count, inflow_egld_count, balance
    

def balance(wallet):
    r = requests.get('https://internal-api.elrond.com/accounts/' + wallet, headers=authentication.headers)

    json_object = json.loads(r.content)

    balance = (int((json_object["balance"])))
    return balance

def stakesc(wallet):
    rwv = requests.get('https://internal-api.elrond.com/accounts/' + wallet, headers=authentication.headers)
    json_object_wv = json.loads(rwv.content)
    balance = (int((json_object_wv["balance"])))
    return balance


def stakevalue():
    rs = requests.get('https://internal-api.elrond.com/economics', headers=authentication.headers)
    json_object_rs = json.loads(rs.content)
    staked_value = (int((json_object_rs["staked"])))
    return staked_value

def staketotal():
    record = 0
    query = "SELECT staketotal FROM stakes ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    # get all records
    record = cursor.fetchone()
    
    return record[0]

def stakestatspush(stakewallet):
    timestamp = int(time.time())
    sc_balances = 0
    sc_balance = 0
    true_staked_val = 0
    for i in range(len(stakewallet)):
        print(stakewallet[i])
        sc = int(stakesc(stakewallet[i]))
        sc_balance = sc_balance + sc
    sc_balances = round(sc_balance / 1000000000000000000)

    sv = stakevalue()
    true_staked_val = round(sv)

    query = "INSERT INTO stakes (timestamp, sctotal, staketotal) VALUES (%s, %s, %s)"
    values = (timestamp, sc_balances, true_staked_val)
    cursor.execute(query, values)
    db.db.commit()

    return sc_balances, true_staked_val

def transactions(range_start,range_end):
    import json
    #execute query 5 time
    r = requests.get('https://internal-api.elrond.com/transactions?from=' + range_start + '&size=' + range_end + '&fields=txHash,receiver,receiverShard,sender,senderShard,status,timestamp,value', headers=authentication.headers, timeout=100)
#        print(r.content)
#        print(r.headers)
    json_object = json.loads(r.content)
#        print(json_object)
        #print(r.content)

#        r = requests.get('https://internal-api.elrond.com/transactions?from' + range_start + '=&size=' + range_end + 'fields=txHash,receiver,receiverShard,sender,senderShard,status,timestamp,value', headers=authentication.headers)
    query = "INSERT INTO transactions (txHash, timestamp, scaction, status, value1, value2) VALUES (%s, %s, %s, %s, %s, %s)"
    for json in json_object:
        tx = json['txHash']
#        print(tx)
        ts = json['timestamp']
        val = json['value']
        st = json['status']
        value2 = 0
        try:
            dat = json['data']
            if json['scResults']:
                a = (len(json['scResults']))
                ## Check if it has status @ok@ then take second val as val1
                if a ==  2 and json['scResults'][0]['data'] == "QDZmNmI=" and json['scResults'][0]['data'] != "ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=":
                    ##Check if its unbond and write in val1
                    value1 = json['scResults'][1]['value']

                ## Check if it has status @ok@ then take first val as val1
                elif a == 2 and json['scResults'][1]['data'] == "QDZmNmI=" and json['scResults'][0]['data'] != "ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=":
                    ##Check if its unbond and write in val1
                    value1 = json['scResults'][0]['value']
                        ## Check if data delegation stake unbound
                elif a == 2 and json['scResults'][0]['data'] == "ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=":
                    value1 = json['scResults'][0]['value']
                elif a == 2 and json['scResults'][1]['data'] == "ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=":
                    value1 = json['scResults'][1]['value']

                if value1 != 0 and value1 != "0":
                    values = (tx, ts, dat, st, value1, value2)

                # print(values)
                if st == "success":
                    cursor.execute(query, values)
                    db.db.commit()
                        #print(cursor.rowcount, "record inserted")
#            except Exception as e: print(e)
        except Exception as e: pass

def delegate(timestamp_1h1m, timestamp_1m):

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'ZGVsZWdhdGU=' AND `status` LIKE 'success' "
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

        counterC = round(counter / 1000000000000000000)

    print(counterC)

def withdraw(timestamp_1h1m, timestamp_1m):

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'd2l0aGRyYXc=' AND `status` LIKE 'success' "
    cursor.execute(query)

    print(query)
    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

        counterC = round(counter / 1000000000000000000)

    print(counterC)


def undelegate(timestamp_1h1m, timestamp_1m):

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'dW5EZWxlZ2F0ZU%' AND `status` LIKE 'success' "
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

        counterC = round(counter / 1000000000000000000)

    print(counterC)

def stake(timestamp_1h1m, timestamp_1m):

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'c3Rha2U=' AND `status` LIKE 'success' "
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

        counterC = round(counter / 1000000000000000000)

    print(counterC)

def unstake(timestamp_1h1m, timestamp_1m):

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'dW5TdGFrZU%' AND `status` LIKE 'success' "
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

        counterC = round(counter / 1000000000000000000)

    print(counterC)

def fixscvalues(timestamp_1h1m, timestamp_1m, code):
    ############
    ## CODES:
    ## claimRewards : Y2xhaW1SZXdhcmRz
    ## redelegateRewards: cmVEZWxlZ2F0ZVJld2FyZHM=
    ## unbond: dW5Cb25k

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE '{code}' AND `status` LIKE 'success' "
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))

    counterC = round((counter / 1000000000000000000),2)

    #print(counterC)
    return counterC

def unbond10(timestamp_10d, timestamp_1m):
    ############
    ## CODES:
    ## unbond: dW5Cb25k
    ## last 1 days

    counter = 0
    counterC = 0

    query = f"SELECT value1,value2 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_10d} AND {timestamp_1m} AND `scaction` LIKE 'dW5Cb25k' AND `status` LIKE 'success' "
    cursor.execute(query)
    print(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
       # counter = counter + (int(record[0]))
#        if len(record[0]) == 20:
        counter = counter + (int(record[0]))
 #       elif len(record[1]) == 20:
  #          counter = counter + (int(record[1]))
    counterC = round((counter / 1000000000000000000),2)

    return counterC

def unbond(timestamp_1h1m, timestamp_1m):
    ############
    ## CODES:
    ## unbond: dW5Cb25k
    ## last 1 days

    counter = 0
    counterC = 0

    query = f"SELECT value1,value2 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'dW5Cb25k' AND `status` LIKE 'success' "
    cursor.execute(query)
    print(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
       # counter = counter + (int(record[0]))
#        if len(record[0]) == 20:
        counter = counter + (int(record[0]))
 #       elif len(record[1]) == 20:
 #           counter = counter + (int(record[1]))

    counterC = round((counter / 1000000000000000000),2)

    return counterC


def redelegateRewards(timestamp_1h1m, timestamp_1m):
    ############
    ## CODES:
    ## redelegate:  cmVEZWxlZ2F0ZVJld2FyZHM=
    ## last 1 days

    counter = 0
    counterC = 0

    query = f"SELECT value1,value2 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'cmVEZWxlZ2F0ZVJld2FyZHM=' AND `status` LIKE 'success' "
    cursor.execute(query)
    print(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
       # counter = counter + (int(record[0]))
#        if len(record[0]) == 17:
        counter = counter + (int(record[0]))
#        elif len(record[1]) == 17:
#            counter = counter + (int(record[1]))

        counterC = round((counter / 1000000000000000000),2)

    return counterC


def claimRewards(timestamp_1h1m, timestamp_1m):
    ############
    ## CODES:
    ## redelegate:  cmVEZWxlZ2F0ZVJld2FyZHM=
    ## last 1 days

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'Y2xhaW1SZXdhcmRz' AND `status` LIKE 'success' "
    cursor.execute(query)
    print(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
       # counter = counter + (int(record[0]))
#        if len(record[0]) == 16:
        counter = counter + (int(record[0]))
#       elif len(record[1]) == 16:
#           counter = counter + (int(record[1]))

        counterC = round((counter / 1000000000000000000),2)

    return counterC


def undelegate(timestamp_1h1m, timestamp_1m):
    ############
    ## CODES:
    ## dW5EZWxlZ2F0ZUA%
    ## dW5EZWxlZ2F0ZUB%

    counter = 0
    counterC = 0

    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'dW5EZWxlZ2F0ZUA%' OR 'dW5EZWxlZ2F0ZUB%' AND `status` LIKE 'success' "
    cursor.execute(query)
    print(query)
    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        counter = counter + (int(record[0]))
        print((record[0]))
        print("-",counter,"-")

    counterC = round(counter / 1000000000000000000)

    #print(counterC)
    return counterC


