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


def transactionCrawler():
    tra_start = "0"
    tra_size = "2000"
    
    for i in range(5):
        transactions(tra_start,tra_size)
        tra_start = int(tra_start) + int(tra_size)
        tra_start = str(tra_start)

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
        except Exception as e: pass

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
    r = requests.get('https://internal-api.elrond.com/transactions?from=' + range_start + '&size=' + range_end + '&fields=txHash,receiver,receiverShard,sender,senderShard,status,timestamp,value', headers=authentication.headers)
#    r = requests.get('https://internal-api.elrond.com/transactions/b6d6260553e16d5cb25fddcce3f186cf4170d9a2eb20180c87bdbf4b634ecde4', headers=authentication.headers, timeout=100)
    json_object = json.loads(r.content)
    unbond_query = "INSERT INTO unBond(txHash, miniBlockHash, nonce, round, value, receiver, sender, receiverShard, senderShard, gasPrice, gasLimit, gasUsed, fee, data, signature, timestamp, status, scResults0relayedValue, scResults0prevTxHash, scResults0gasLimit, scResults0originalTxHash, scResults0receiver, scResults0data, scResults0sender, scResults0nonce, scResults0value, scResults0hash, scResults0callType, scResults0gasPrice, scResults1relayedValue, scResults1prevTxHash, scResults1gasLimit, scResults1originalTxHash, scResults1receiver, scResults1data, scResults1sender, scResults1nonce, scResults1value, scResults1hash, scResults1callType, scResults1gasPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    claim_query = "INSERT INTO claimRewards(txHash, miniBlockHash, nonce, round, value, receiver, sender, receiverShard, senderShard, gasPrice, gasLimit, gasUsed, fee, data, signature, timestamp, status, scResults0relayedValue, scResults0prevTxHash, scResults0gasLimit, scResults0originalTxHash, scResults0receiver, scResults0data, scResults0sender, scResults0nonce, scResults0value, scResults0hash, scResults0callType, scResults0gasPrice, scResults1relayedValue, scResults1prevTxHash, scResults1gasLimit, scResults1originalTxHash, scResults1receiver, scResults1data, scResults1sender, scResults1nonce, scResults1value, scResults1hash, scResults1callType, scResults1gasPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    redelegate_query = "INSERT INTO redelegateRewards(txHash, miniBlockHash, nonce, round, value, receiver, sender, receiverShard, senderShard, gasPrice, gasLimit, gasUsed, fee, data, signature, timestamp, status, scResults0relayedValue, scResults0prevTxHash, scResults0gasLimit, scResults0originalTxHash, scResults0receiver, scResults0data, scResults0sender, scResults0nonce, scResults0value, scResults0hash, scResults0callType, scResults0gasPrice, scResults1relayedValue, scResults1prevTxHash, scResults1gasLimit, scResults1originalTxHash, scResults1receiver, scResults1data, scResults1sender, scResults1nonce, scResults1value, scResults1hash, scResults1callType, scResults1gasPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for json in json_object:
        try:
            if json['data'] == "dW5Cb25k":
                m1 = json['txHash']
                m2 = json['miniBlockHash']
                m3 = json['nonce']
                m4 = json['round']
                m5 = json['value']
                m6 = json['receiver']
                m7 = json['sender']
                m8 = json['receiverShard']
                m9 = json['senderShard']
                m10 = json['gasPrice']
                m11 = json['gasLimit']
                m12 = json['gasUsed']
                m13 = json['fee']
                m14 = json['data']
                m15 = json['signature']
                m16 = json['timestamp']
                m17 = json['status']
                m18 = json['scResults'][0]['relayedValue']
                m19 = json['scResults'][0]['prevTxHash']
                m20 = json['scResults'][0]['gasLimit']
                m21 = json['scResults'][0]['originalTxHash']
                m22 = json['scResults'][0]['receiver']
                m23 = json['scResults'][0]['data']
                m24 = json['scResults'][0]['sender']
                m25 = json['scResults'][0]['nonce']
                m26 = json['scResults'][0]['value']
                m27 = json['scResults'][0]['hash']
                m28 = json['scResults'][0]['callType']
                m29 = json['scResults'][0]['gasPrice']
                m30 = json['scResults'][1]['relayedValue']
                m31 = json['scResults'][1]['prevTxHash']
                m32 = json['scResults'][1]['gasLimit']
                m33 = json['scResults'][1]['originalTxHash']
                m34 = json['scResults'][1]['receiver']
                m35 = json['scResults'][1]['data']
                m36 = json['scResults'][1]['sender']
                m37 = json['scResults'][1]['nonce']
                m38 = json['scResults'][1]['value']
                m39 = json['scResults'][1]['hash']
                m40 = json['scResults'][1]['callType']
                m41 = json['scResults'][1]['gasPrice']

                values = (m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27, m28, m29, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40, m41)
                cursor.execute(unbond_query, values)
                db.db.commit()

            elif json['data'] == "Y2xhaW1SZXdhcmRz":
                m1 = json['txHash']
                m2 = json['miniBlockHash']
                m3 = json['nonce']
                m4 = json['round']
                m5 = json['value']
                m6 = json['receiver']
                m7 = json['sender']
                m8 = json['receiverShard']
                m9 = json['senderShard']
                m10 = json['gasPrice']
                m11 = json['gasLimit']
                m12 = json['gasUsed']
                m13 = json['fee']
                m14 = json['data']
                m15 = json['signature']
                m16 = json['timestamp']
                m17 = json['status']
                m18 = json['scResults'][0]['relayedValue']
                m19 = json['scResults'][0]['prevTxHash']
                m20 = json['scResults'][0]['gasLimit']
                m21 = json['scResults'][0]['originalTxHash']
                m22 = json['scResults'][0]['receiver']
                try:
                    m23 = json['scResults'][0]['data']
                except:
                    m23 = 0
                m24 = json['scResults'][0]['sender']
                m25 = json['scResults'][0]['nonce']
                m26 = json['scResults'][0]['value']
                m27 = json['scResults'][0]['hash']
                m28 = json['scResults'][0]['callType']
                m29 = json['scResults'][0]['gasPrice']
                m30 = json['scResults'][1]['relayedValue']
                m31 = json['scResults'][1]['prevTxHash']
                m32 = json['scResults'][1]['gasLimit']
                m33 = json['scResults'][1]['originalTxHash']
                m34 = json['scResults'][1]['receiver']
                try:
                    m35 = json['scResults'][1]['data']
                except:
                    m35 = 0
                m36 = json['scResults'][1]['sender']
                c37 = json['scResults'][1]['nonce']
                m38 = json['scResults'][1]['value']
                m39 = json['scResults'][1]['hash']
                m40 = json['scResults'][1]['callType']
                m41 = json['scResults'][1]['gasPrice']

                values1 = (m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27, m28, m29, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40, m41)
                cursor.execute(claim_query, values1)

                db.db.commit()
            elif json['data'] == "cmVEZWxlZ2F0ZVJld2FyZHM=":
                m1 = json['txHash']
                m2 = json['miniBlockHash']
                m3 = json['nonce']
                m4 = json['round']
                m5 = json['value']
                m6 = json['receiver']
                m7 = json['sender']
                m8 = json['receiverShard']
                m9 = json['senderShard']
                m10 = json['gasPrice']
                m11 = json['gasLimit']
                m12 = json['gasUsed']
                m13 = json['fee']
                m14 = json['data']
                m15 = json['signature']
                m16 = json['timestamp']
                m17 = json['status']
                m18 = json['scResults'][0]['relayedValue']
                m19 = json['scResults'][0]['prevTxHash']
                m20 = json['scResults'][0]['gasLimit']
                m21 = json['scResults'][0]['originalTxHash']
                m22 = json['scResults'][0]['receiver']
                try:
                    m23 = json['scResults'][0]['data']
                except:
                    m23 = 0
                print(m23)
                m24 = json['scResults'][0]['sender']
                m25 = json['scResults'][0]['nonce']
                m26 = json['scResults'][0]['value']
                m27 = json['scResults'][0]['hash']
                m28 = json['scResults'][0]['callType']
                m29 = json['scResults'][0]['gasPrice']
                m30 = json['scResults'][1]['relayedValue']
                m31 = json['scResults'][1]['prevTxHash']
                m32 = json['scResults'][1]['gasLimit']
                m33 = json['scResults'][1]['originalTxHash']
                m34 = json['scResults'][1]['receiver']
                try:
                    m35 = json['scResults'][1]['data']
                except:
                    m35 = 0
                print(m35)
                m36 = json['scResults'][1]['sender']
                c37 = json['scResults'][1]['nonce']
                m38 = json['scResults'][1]['value']
                m39 = json['scResults'][1]['hash']
                m40 = json['scResults'][1]['callType']
                m41 = json['scResults'][1]['gasPrice']

                values1 = (m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27, m28, m29, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40, m41)
                cursor.execute(redelegate_query, values1)

                db.db.commit()
#        except Exception as e: print(e)
        except Exception as e: pass


def unbond(timestamp_1h1m, timestamp_1m):
    
    query = f"SELECT SUM(val) / 1000000000000000000 FROM (SELECT scResults0value AS val FROM `unBond` WHERE `scResults0data` LIKE 'ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} UNION ALL SELECT scResults1value AS val FROM `unBond` WHERE `scResults1data` LIKE 'ZGVsZWdhdGlvbiBzdGFrZSB1bmJvbmQ=' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m}) total"
    cursor.execute(query)

    records = cursor.fetchone()
    print(records[0])
    try:
        return round((records[0]),2)
    except Exception as e: pass


def redelegateRewards(timestamp_1h1m, timestamp_1m):

    query = f"SELECT SUM(val) / 1000000000000000000 FROM (SELECT scResults0value AS val FROM `redelegateRewards` WHERE `scResults0data` LIKE '0' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} UNION ALL SELECT scResults1value AS val FROM `redelegateRewards` WHERE `scResults1data` LIKE '0' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m}) total"
    cursor.execute(query)
    print(query)

    records = cursor.fetchone()
    
    try:
        return round((records[0]),2)
    except Exception as e: pass


def claimRewards(timestamp_1h1m, timestamp_1m):

#    query = f"SELECT value1 FROM `transactions` WHERE `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} AND `scaction` LIKE 'Y2xhaW1SZXdhcmRz' AND `status` LIKE 'success' "
    query = f"SELECT SUM(val) / 1000000000000000000 FROM (SELECT scResults0value AS val FROM `claimRewards` WHERE `scResults0data` NOT LIKE 'QDZmNmI=' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m} UNION ALL SELECT scResults1value AS val FROM `claimRewards` WHERE `scResults1data` NOT LIKE 'QDZmNmI=' AND `timestamp` BETWEEN {timestamp_1h1m} AND {timestamp_1m}) total"
    cursor.execute(query)
    print(query)

    records = cursor.fetchone()

    try:
        return round((records[0]),2)
    except Exception as e: pass
