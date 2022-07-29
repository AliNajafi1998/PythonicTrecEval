import argparse
import json

parser = argparse.ArgumentParser(
    description="Converts trec format QRELS to Json.")
parser.add_argument('-i', '--infile', help='Path of QREL File.')
parser.add_argument('-o', '--outfile', nargs='?',
                    default='qrels.json', help="Path of QREL json file.")
args = parser.parse_args()


with open(args.infile, 'r') as inf:
    lines = inf.readlines()
    lines = [line.split("\t") for line in lines]
    q_d_r = [[line[0], line[2], line[3]] for line in lines]
    q_docs = {}
    for q, d, r in q_d_r:
        q = q.strip()
        r = r.strip()
        d = d.strip()
        if q in q_docs:
            q_docs[q][d] = r
        else:
            q_docs[q] = {d: r}

with open(args.outfile, 'w') as outf:
    json.dump(q_docs, outf)
