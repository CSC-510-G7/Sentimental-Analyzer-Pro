import random
import pprint
# put keys given form the TA in this list
keys = [
    "key a", "key b", "key c", "key d",
    "key e", "key f", "key g", "key h",
    "key i", "key j", "key k"
    ]
# put the URL or the Name of the source you want each 
# tester to evaluate in this list
sources = list(range(1, 21))

number_of_lab_rats = len(keys)

# ajust this variable to detemin how many variables you want
# each tester to evaluate
sources_per_rat = 5
key_sources_pairs = {} 
for x in range(0,number_of_lab_rats):    
    key_sources_pairs[keys[x]] = random.sample(sources, sources_per_rat)

pprint.pprint(key_sources_pairs)
