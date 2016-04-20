import os
base = os.path.dirname(os.path.realpath(__file__))
cmdpcprox = '"C:\Program Files (x86)\RF IDeas\CmdpcProx\CmdpcProx"'
pass_sound = base+'\\Pass.wav'
fail_sound = base+'\\Fail.wav'
valid_facilities = [16,192]
#Newline delimited team list
infile="teams_spring_2016.txt"

#This stays private!
#Set of hashes that can vote unlimited number of times
double_allow=('')
#Unique security key to prevent unintended cardnumber disclosure
hash_salt=""
