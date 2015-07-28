import requests
import json
from pprint import pprint
import os.path
import pickle

wallet_snsw = 'rMwjYedjc7qqtKYVLiAccJSmCwih4LnE2q'
currency = ['USD','BTC','EUR']
### test
#wallet_snsw = 'rp2PaYDxVwDvaZVLEQv7bHhoFQEyX1mEx7'
#wallet_snsw = 'r42Yk5EESujvvgWNiyMsZvyUkN7KPx2Swm'
#wallet_snsw = 'rKiCet8SdvWxPXnAgYarFUXMh1zCPz432Y'
wallet_snsw = 'r42astw8JDxKAqrx7Azaunat8JpkagdbVS' #cur CCK
def snappyrevenue_mod(PrevBalance,FinBalance,HighIssuer,LowIssuer):
    PrevBalance=float(PrevBalance)
    FinBalance=float(FinBalance)
    snaprev =0
    #print(PrevBalance,FinBalance,HighIssuer,LowIssuer)
    if HighIssuer == wallet_snsw:
        if PrevBalance>=0 and FinBalance >=0:
            snaprev = FinBalance-PrevBalance
        else:
            raise NameError('Incorrect balance!')
    elif LowIssuer == wallet_snsw:
        if PrevBalance<=0 and FinBalance<=0:
            snaprev = PrevBalance - FinBalance
        else:
            raise NameError('Incorrect balance!')
    return snaprev
def correct_dep_and_wdrwl(destination,account,value):
    correct =0
    if destination == wallet_snsw:
        correct = value
    if account == wallet_snsw:
        correct = -value
    return correct



def minirevenue(transaction,currency):
    minirev=0
    if transaction['meta']['TransactionResult']=='tesSUCCESS':# and transaction['tx']['TransactionType'] == 'Payment':
        affected_nodes = transaction['meta']['AffectedNodes']
        for node in affected_nodes:
            for key in node:
                if node[key]['LedgerEntryType'] != 'RippleState':
                    continue
                else:
                    try:
                        if key == "ModifiedNode" and node[key]['PreviousFields']['Balance']['currency']==currency:
                            minirev += snappyrevenue_mod(node[key]['PreviousFields']['Balance']['value'],node[key]['FinalFields']['Balance']['value'],node[key]['FinalFields']['HighLimit']['issuer'],node[key]['FinalFields']['LowLimit']['issuer'])
                        elif key == "CreatedNode" and node[key]['NewFields']['Balance']['currency']==currency:
                            minirev += snappyrevenue_mod(0,node[key]['NewFields']['Balance']['value'],node[key]['NewFields']['HighLimit']['issuer'],node[key]['NewFields']['LowLimit']['issuer'])
                        elif key == "DeletedNode" and node[key]['PreviousFields']['Balance']['currency']==currency:
                            minirev += snappyrevenue_mod(node[key]['PreviousFields']['Balance']['value'],node[key]['FinalFields']['Balance']['value'],node[key]['FinalFields']['HighLimit']['issuer'],node[key]['FinalFields']['LowLimit']['issuer'])
                    except:
                        raise NameError("Incorrect balances")
        if transaction['tx']['TransactionType'] == 'Payment':
            minirev-=correct_dep_and_wdrwl(transaction['tx']['Destination'],transaction['tx']['Account'],transaction['tx']['Amount']['Value'])


    return minirev

def revenue(start_block,end_block,path,currency):
    rev=0
    for i in range(end_block,start_block-1,-1):
        name = path+'\\'+str(i)
        if os.path.isfile(name):
            ledg = open(name,'rb')
            js = pickle.load(ledg)
            for transaction in js:
                try:
                    rev=rev+minirevenue(transaction,currency)
                except:
                    raise ValueError("Incorrect balances in file",name)
            ledg.close()
        else:
            print 'there are no file'+name
    return rev

start_block=14445690
end_block = 14445690
#14451283
path = r"H:\snsw\ledger"
#try:
#    print revenue(start_block,end_block,path,"CNY")
#except ValueError as err:
 #   print(err.args)

for cur in currency:
    try:
        print 'Balance in ' cur+': '+str(revenue(start_block,end_block,path,cur))
    except ValueError as err:
        print(err.args)
print "Hurray!!!"