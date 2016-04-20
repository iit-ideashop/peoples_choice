import audioplayer
import time
import config as cf
import hashlib


''' Keycode for enter = 13, keycode for control = 17 '''
def onValidCard(cardspec):
    audioplayer.playWav(cf.pass_sound)
    rawstr = str(cardspec[0])+str(cardspec[1])+cf.hash_salt
    hashed = hashlib.sha256(rawstr.encode('utf-8')).hexdigest()
    print(hashed)

def onInvalidCard(cardspec):
    print("Invalid Facility Code %d! Check that you are scanning an IIT ID card." % cardspec[1])
    audioplayer.playWav(cf.fail_sound)
