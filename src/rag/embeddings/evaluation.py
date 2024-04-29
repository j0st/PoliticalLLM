import json

from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers import SentenceTransformer

val_dataset_path = 'data/val_dataset.json'

with open(val_dataset_path, 'r+', encoding="utf-8") as f:
    val_dataset = json.load(f)

def evaluate(dataset, model_id: str, name: str):
    """
    Evaluates sentence transformer models against synthetic dataset generated in synthetic_dataset.py.
    Results are saved in results/sentence-embeddings.
    """
    
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']

    evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs, name=name)
    model = SentenceTransformer(model_id)

    return evaluator(model, output_path='results/sentence-embeddings/')

evaluate(val_dataset, "intfloat/multilingual-e5-base", name='base-model')
evaluate(val_dataset, "jost/multilingual-e5-base-politics-de", name='fine-tuned-model')
