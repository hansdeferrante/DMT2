import pandas as pd
import csv
import sys
import random
import argparse

parser = argparse.ArgumentParser()                                               

parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--seed", "-s", type=int, required=True)
args = parser.parse_args()

# Read in the file and drop the R indices.
df = pd.read_csv(args.file)

# Round up to the first 3 decimals. Might save memory (not sure).
df = df.round(3)
df.sample(frac=1, random_state = args.seed)
df = df.sort_values('srch_id')
df.to_csv(args.file, index = False)

# Read the file in line by line and write out data to ranklib format.
with open(args.file) as inf, open(args.file[:-4]+'.rlf','w') as outf, open(args.file[:-4]+'_properties.txt','w') as poutf:
    
    csvreader = csv.reader(inf);
    header = next(csvreader)
    print(header)
    
    targetIndex = header.index("target")
    srchIndex = header.index("srch_id")
    propIndex = header.index("prop_id")
    
    for line in csvreader:
        target = line.pop(targetIndex)
        prop = line.pop(propIndex)
        target = target if len(target)>0 else 0
        targetqid = ("{} qid:{} ".format(target, line.pop(srchIndex)))
        line[1:] = [(float(x) if x else -99) for x in line[1:]]
        featureset = zip(range(1,len(line)), line[1:])
        features = (" ".join("%s:%s" % tup for tup in featureset))
        outf.write(targetqid + features + "\n")
        poutf.write(prop+"\n")
