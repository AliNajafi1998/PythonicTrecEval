import math
from typing import List


class RelevanceEvaluator:
    def __init__(self, qrels, measures) -> None:
        self.qrels = qrels
        self.measures = measures

    def evaluate(self, run, precision_k=1000, recall_k=1000, ndcg_k=1000):
        precision = None
        recall = None
        map = None
        rr = None
        mrr = None
        ndcg = None

        if "precision" in self.measures:
            precision = self._get_precision(run, precision_k)
        if "recall" in self.measures:
            recall = self._get_recall(run, recall_k)
        if "map" in self.measures:
            if precision is None:
                precision = self._get_precision(run, precision_k)
            map = self._get_map(precision)
        if 'rr' in self.measures:
            rr = self._get_reciprocal_rank(run)
        if 'mrr' in self.measures:
            if rr is None:
                rr = self._get_reciprocal_rank(run)
            mrr = self._get_mrr(rr)
        if 'ndcg' in self.measures:
            ndcg = self._get_ndcg(run, ndcg_k)
        return {
            f"recall_{recall_k}": recall,
            f"precision_{precision_k}": precision,
            "mean average percision": map,
            "reciprocal rank": rr,
            "MRR": mrr,
            f"ndcg_{ndcg_k}": ndcg

        }

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
            first_rel = list(self.qrels[q][0].keys())[0]
            flag = False
            for index, r in enumerate(rankded_list):
                index += 1
                if first_rel == list(r.keys())[0]:
                    q_rr[q] = 1/index
                    flag = True
                    break
            if flag == False:
                q_rr[q] = 0
        return q_rr

    def _get_ndcg(self, run, k=1000):
        q_ndcg = {}
        for q in run:
            qrels = self.qrels[q][:k]
            rankded_list: List = run[q][:k]
            dcg = 0
            for index, r in enumerate(rankded_list):
                index += 1
                dcg += (math.pow(2, float(list(r.values())
                        [0]) - 1)) / math.log2(index + 1)

            idcg = 0
            ideal_list = [float(list(r.values())[0]) for r in qrels]
            ideal_list.sort(reverse=True)
            for i, r in enumerate(ideal_list):
                i += 1
                idcg += (math.pow(2, r - 1)) / math.log2(i + 1)
            ndcg = dcg/idcg
            q_ndcg[q] = ndcg
        return q_ndcg

    def _get_mrr(self, q_r):
        return sum(q_r.values()) / len(q_r)


if __name__ == "__main__":
    # tests for each of the methods
    qrel = {
        'q1': [
            {'d1': 1},
            {'d2': 2},
            {'d3': 1},
        ],
        'q2': [
            {'d1': 1},
            {'d3': 1},
        ],
    }

    run = {
        'q1': [
            {'d2': 1.0},
            {'d1': 1.0},
            {'d3': 1.0},
        ],
        'q2': [
            {'d1': 1},
        ]
    }

    evaluator = RelevanceEvaluator(
        qrel, ['precision', 'recall', 'map', 'rr', 'ndcg','mrr'])
    print(evaluator.evaluate(run, 2))
