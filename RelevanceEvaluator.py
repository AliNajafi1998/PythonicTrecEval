from typing import List


class RelevanceEvaluator:
    def __init__(self, qrels, measures) -> None:
        self.qrels = qrels
        self.measures = measures

    def evaluate(self, run, precision_k=1000, recall_k=1000):
        precision = None
        recall = None
        map = None

        if "percision" in self.measures:
            precision = self._get_precision(run, precision_k)
        if "recall" in self.measures:
            recall = self._get_recall(run, recall_k)
        if "map" in self.measures:
            if precision is None:
                precision = self._get_precision(run, precision_k)
            map = self._get_map(precision)

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

    def _get_map(self, q_precision):
        return sum(q_precision.values()) / len(q_precision)

    def _get_reciprocal_rank(self, run):
        q_rr = {}
        for q in run:
            rankded_list: List = run[q]
            first_rel = list(self.qrels[0].keys())[0]
            flag = False
            for index, r in enumerate(rankded_list):
                index += 1
                if first_rel == list(r.keys())[0]:
                    q_rr[q] = 1/index
                    flag = True
            if flag == False:
                q_rr[q] = 0
        return q_rr
