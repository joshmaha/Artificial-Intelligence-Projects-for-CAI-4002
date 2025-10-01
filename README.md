

# Project 3 — Sentiment Analysis for Movie Reviews

This project implements a TF-IDF + Logistic Regression sentiment classifier for movie reviews. It includes preprocessing, training, saved model/vectorizer artifacts, and scripts to evaluate performance on sample data.

## What’s in this folder

- `hw3.py` — main implementation with `calcSentiment_train(trainFile)` and `calcSentiment_test(review)`.
- `exampleHW3.py` — example usage (same functions as `hw3.py`).
- `convert_imdb_to_json.py` — small evaluator that runs the trained classifier on the provided `reviews.json` dataset and prints accuracy.
- `practice_test_problems.py` — small list of example problems / unit test strings.
- `training_model.pkl`, `vectorizer.pkl` — saved model and vectorizer produced by training (loaded by `calcSentiment_test`).
- `reviews.json` and `test_data.json` — datasets used for testing/evaluation.

## Requirements

- Python 3.8+
- Install required packages (if not already installed):

```powershell
pip install nltk scikit-learn joblib
```

Then download the NLTK resources (once):

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## How to use

- Train a model from a JSONL-style training file (each line is a JSON object with keys `review` and `sentiment`):

```python
from hw3 import calcSentiment_train
calcSentiment_train('trainingFile.jsonlist')
```

- Test the classifier on a single review:

```python
from hw3 import calcSentiment_test
print(calcSentiment_test('This movie was absolutely wonderful!'))
```

- Evaluate the classifier on the bundled `reviews.json` dataset:

```powershell
python convert_imdb_to_json.py
```

## Notes

- The `calcSentiment_test` function expects `training_model.pkl` and `vectorizer.pkl` in the same folder. If you retrain, those files will be overwritten.
- The saved model and vectorizer are included so you can run predictions without retraining.

## Author

Joshua Maharaj


