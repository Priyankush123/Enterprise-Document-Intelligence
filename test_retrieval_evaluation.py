from evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
    TestQuery,
)


test_queries = [

    TestQuery(

        query="How many annual leaves are provided?",

        expected="20 days",

    ),

    TestQuery(

        query="What is the work from home policy?",

        expected="two days",

    ),

    TestQuery(

        query="How many medical leaves are provided?",

        expected="15 days",

    ),

    TestQuery(

        query="Can annual leave be carried forward?",

        expected="cannot be carried forward",

    ),

    TestQuery(

        query="How are travel expenses reimbursed?",

        expected="valid receipts",

    ),

]


if __name__ == "__main__":

    evaluator = RetrievalEvaluator()

    evaluator.evaluate(test_queries)