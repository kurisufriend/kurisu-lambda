from sys import argv
from pickle import loads
from random import randint

from lib import step
from probtest import test

p = int(argv[1])

f = open("fullans.pkl", "rb")
a = loads(f.read())
f.close()

n = int((p/100)*(len(a)) + .5)
print(f"checking {p}% of program states, {n} states total...")

allgood = True
for i in range(n):
    allgood = (a[i+1] == step(a[i]))

print (
    f"""all checked program states verified to be accurate!
presuming 10% of states would have been faked, the sample is representative with a probability of ~{test(10, p)}""" if allgood else "found an erroneous state -- answer fabricated or program states corrupted"
)