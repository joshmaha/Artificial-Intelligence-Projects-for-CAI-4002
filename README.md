
# Project 4 — ModernBERT Classifier (statement analysis)

This project contains Jupyter notebooks that implement and evaluate a ModernBERT-based classifier for analyzing statements. The notebooks include data preparation, model fine-tuning, evaluation, and examples of inference on new statements.

The classifier was used to analyze different statement types (e.g., sentiment, claim detection, or other statement labels — see the notebook cells for exact label sets used in the experiments).

## Files in this folder

- `HW4 template.ipynb` — starter notebook with instructions and placeholders for exercises.
- `HW4_done.ipynb` — final notebook that demonstrates data processing, model fine-tuning, evaluation metrics, and sample predictions.


## Key concepts covered

- Loading and preprocessing labeled statement datasets.
- Tokenizing text for transformer models using Hugging Face tokenizers.
- Fine-tuning a pre-trained BERT-like model (ModernBERT) on a classification head using PyTorch/transformers.
- Evaluating model performance: accuracy, precision, recall, F1, confusion matrices.
- Running inference on new statements and visualizing predictions.

## Requirements

- Python 3.8+
- Recommended packages (install in a virtual environment):

```powershell
pip install transformers torch torchvision torchaudio datasets scikit-learn matplotlib jupyterlab
```

Notes:
- Use a machine with a CUDA-capable GPU for reasonable fine-tuning speed. CPU-only runs are possible but slow.
- If your environment uses a specific `ModernBERT` distribution or a private model name, update the model name used in the notebook cells (e.g., `model_name = "modernbert-base"`).

## How to run the notebooks

1. Open the folder and start Jupyter Lab / Notebook:

```powershell
jupyter lab
```

2. Open `HW4_done.ipynb` and run cells in order. Key sections in the notebook:

- Data loading & preprocessing — update file paths if your data lives elsewhere.
- Tokenizer & dataset preparation — choose the `model_name` variable.
- Model build & training loop — tune `learning_rate`, `batch_size`, `num_epochs`.
- Evaluation — runs validation and prints metrics; save `best_model.pt` for inference.
- Inference examples — run sample statements to see classifier outputs.

## Quick reproducible example (in notebook Python cells)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import torch

model_name = "bert-base-uncased"  # replace with your ModernBERT model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Example training args
training_args = TrainingArguments(
	output_dir="./models",
	per_device_train_batch_size=8,
	per_device_eval_batch_size=8,
	num_train_epochs=3,
	evaluation_strategy="epoch",
	save_strategy="epoch",
)

# Use Trainer API in the notebook to fine-tune and evaluate (see notebook cells for full pipeline)
```

## Tips & troubleshooting

- If you run out of GPU memory, reduce `per_device_train_batch_size` or use gradient accumulation.
- For small datasets, freeze the base model and train only the classification head first to avoid overfitting.
- Use the `datasets` library and Hugging Face tokenizers for consistent and efficient preprocessing.

## Outputs and artifacts

- Trained model weights (e.g., `best_model.pt`) — saved by the notebook during training.
- Evaluation logs and saved plots — included in the notebook outputs.

## Next steps (optional)

- Export the trained model to ONNX for faster inference.
- Create a small Flask/FastAPI wrapper that loads the saved weights and exposes a /predict endpoint for real-time classification.

## Author

Joshua Maharaj
