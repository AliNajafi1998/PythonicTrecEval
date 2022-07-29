# 3 Q0 msmarco_doc_22_449579381 1 12.077800 Anserini
import argparse
import json

parser = argparse.ArgumentParser(
    description="Converts trec format runs to Json.")
parser.add_argument('-i', '--infile', help='Path of run File.')
parser.add_argument('-o', '--outfile', nargs='?',
                    default='run.json', help="Path of run json file.")
args = parser.parse_args()

with open(args.infile, 'r') as inf:
    lines = inf.readlines()
    lines = [line.split() for line in lines]
    q_d_s = [[line[0], line[2], line[4]] for line in lines]
    q_docs = {}
    for q, d, r in q_d_s:
        q = q.strip()
        s = r.strip()
        d = d.strip()
        if q in q_docs:
            q_docs[q].append({d: s})
        else:
            q_docs[q] = [{d: s}]

with open(args.outfile, 'w') as outf:
    json.dump(q_docs, outf)
