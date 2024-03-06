import json
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers import SentenceTransformer

TRAIN_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//train_dataset.json'
VAL_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//val_dataset.json'

with open(TRAIN_DATASET_FPATH, 'r+', encoding="utf-8") as f:
    train_dataset = json.load(f)

with open(VAL_DATASET_FPATH, 'r+', encoding="utf-8") as f:
    val_dataset = json.load(f)

def evaluate_st(
    dataset,
    model_id,
    name,
):
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']

    evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs, name=name)
    model = SentenceTransformer(model_id)
    return evaluator(model, output_path='results/')

#evaluate_st(val_dataset, "exp_finetune", name='ft')
# evaluate_st(val_dataset, "sentence-transformers/distiluse-base-multilingual-cased-v2", name='distiluse-base-multilingual-cased-v2')
# evaluate_st(val_dataset, "aari1995/German_Semantic_STS_V2", name='German_Semantic_STS_V2')
# evaluate_st(val_dataset, "intfloat/multilingual-e5-base", name='multilingual-e5-base')
# evaluate_st(val_dataset, "intfloat/multilingual-e5-large", name='multilingual-e5-large')
evaluate_st(val_dataset, "jost/multilingual-e5-base-politics-de", name='m-e5-FINETUNED')
evaluate_st(val_dataset, "intfloat/multilingual-e5-base", name='m-e5-BASE')

