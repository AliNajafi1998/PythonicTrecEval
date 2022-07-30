from typing import List


class RelevanceEvaluator:
    def __init__(self, qrels, measures) -> None:
        self.qrels = qrels
        self.measures = measures

    def evaluate(self, run):
        for measure in measure:
            # do the evaluation
            pass

    def _get_precision(self, run, k=1000):
        q_prec = {}
        for q in run:
            rankded_list: List = run[q][:k]
            prec = 0
            for r in rankded_list:
                retrievd_doc = list(r.keys())[0]
                for real_doc in self.qrels[q]:
                    if retrievd_doc in real_doc:
                        prec += 1
                        break
            q_prec[q] = prec/len(rankded_list)
        return q_prec

    def _get_recall(self, run, k=1000):
        q_recall = {}
        for q in run:
            qrels = self.qrels[q][:k]
            rankded_list: List = run[q][:k]
            rec = 0
            for r in rankded_list:
                retrievd_doc = list(r.keys())[0]
                for real_doc in qrels:
                    if retrievd_doc in real_doc:
                        rec += 1
                        break

            q_recall[q] = rec/len(qrels)
        return q_recall

    def _get_map(self):
        pass
