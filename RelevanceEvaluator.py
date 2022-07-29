class RelevanceEvaluator:
    def __init__(self, qrels, measures) -> None:
        self.qrels = qrels
        self.measures = measures

    def evaluate(self, run):
        for measure in measure:
            # do the evaluation
            pass

    def _get_precision(self, run, k):
        pass

    def _get_recall(self, run, k):
        pass
 