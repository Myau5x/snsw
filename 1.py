import requests
import json
from pprint import pprint
import pickle
def download_ledger(start_block,end_block,path):
    for i in range(start_block,end_block+1):
        #if exist file path/i
        name = path+'\\'+str(i)
        nametxt = name+'.txt'
        try:
            ledg = open(name)
            ledg.close()
        except:
            #create file and download ledger number i
            ledg = open(name,'w')
            ledgtxt = open(nametxt,'w')
            adr = 'https://history.ripple.com/v1/ledgers/'+str(i)+'?expand=true'
            adr2 = 'http://test.snapswap.vc/v1/ledgers/'+str(i)
            param = {'expand' : 'true'}

            u=requests.get(adr2,params=param)
            js=u.json()
            tx = js['ledger']['transactions']
            pickle.dump(tx,ledg,2)
            pprint(tx,ledgtxt)
            ledg.close()
            ledgtxt.close()

start_block=14446899
end_block = 14447005
path = r"H:\snsw\ledger"
download_ledger(start_block,end_block,path)
print "Hurray!!!"