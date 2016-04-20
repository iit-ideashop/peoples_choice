import os, time, base64
import config as cf
import actions as ac

def getCardBlocking():
    while(True):
        print("Waiting for card...")
        #
        # Invoke utility and read its standard output of card data
        #
        fd = os.popen(cf.cmdpcprox+' -getactiveid="%s" -waitforgetactiveid=3600')
        s = fd.read()
        if(fd.close()):
            return None
        if(len(s) == 0):
            continue
        bts=base64.b16decode(s.replace(" ",""))
        cardnum = bytearray(bts[0:3])
        facility = bytearray(bts[2:4])
        cardnum[2] = cardnum[2] & 0x0F
        facility[0] = facility[0] & 0xF0
        cardnum_int = int.from_bytes(cardnum, byteorder='little', signed=False)
        facility_int = int.from_bytes(facility, byteorder='little', signed=False)
        return (cardnum_int,facility_int)
    
def getCardNonBlocking():
        print("Waiting for card...")
        #
        # Invoke utility and read its standard output of card data
        #
        fd = os.popen(cf.cmdpcprox+' -getactiveid="%s" -waitforgetactiveid=10')
        s = fd.read()
        if(fd.close()):
            return None
        if(len(s) == 0):
            return None
        bts=base64.b16decode(s.replace(" ",""))
        cardnum = bytearray(bts[0:3])
        facility = bytearray(bts[2:4])
        cardnum[2] = cardnum[2] & 0x0F
        facility[0] = facility[0] & 0xF0
        cardnum_int = int.from_bytes(cardnum, byteorder='little', signed=False)
        facility_int = int.from_bytes(facility, byteorder='little', signed=False)
        return (cardnum_int,facility_int)
    
if (__name__ == '__main__'):
    while(True):
        cs = getCardBlocking()
        if not(cs):
            print("Error running pcProx driver program, exiting!")
            os._exit(0)
        else:
            print(cs)
            if cs[1] in cf.valid_facilities:
                ac.onValidCard(cs)
            else:
                ac.onInvalidCard(cs)
        time.sleep(2.0)
                

