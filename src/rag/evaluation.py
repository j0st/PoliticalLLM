import json
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers import SentenceTransformer

TRAIN_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//train_dataset.json'
VAL_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//val_dataset.json'

with open(TRAIN_DATASET_FPATH, 'r+') as f:
    train_dataset = json.load(f)

with open(VAL_DATASET_FPATH, 'r+') as f:
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

evaluate_st(val_dataset, "exp_finetune", name='ft')

