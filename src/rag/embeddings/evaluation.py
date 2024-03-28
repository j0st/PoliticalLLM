import json

from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers import SentenceTransformer

TRAIN_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//train_dataset.json'
VAL_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//val_dataset.json'

with open(TRAIN_DATASET_FPATH, 'r+', encoding="utf-8") as f:
    train_dataset = json.load(f)

with open(VAL_DATASET_FPATH, 'r+', encoding="utf-8") as f:
    val_dataset = json.load(f)

def evaluate(dataset, model_id, name):
    """
    Evaluates sentence transformer models against synthetic dataset generated in synthetic_dataset.py.
    """
    
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']

    evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs, name=name)
    model = SentenceTransformer(model_id)
    return evaluator(model, output_path='results/')

evaluate(val_dataset, "intfloat/multilingual-e5-base", name='m-e5-BASE')
