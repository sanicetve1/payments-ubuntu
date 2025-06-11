# train_banking77_classifier.py

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.model_selection import train_test_split

# Step 1: Load JSONL dataset
path_to_jsonl = "C:\\Users\\San\\Desktop\\Projects\\Payments\\HF\\test.jsonl"  # update with your actual path
dataset = load_dataset("json", data_files=path_to_jsonl, split="train")

# Step 2: Create label mappings
labels = sorted(set(example["label"] for example in dataset))
label_to_id = {label: i for i, label in enumerate(labels)}
id_to_label = {i: label for label, i in label_to_id.items()}

dataset = dataset.map(lambda x: {"label": label_to_id[x["label"]]})

# Step 3: Load model and tokenizer
checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(
    checkpoint, num_labels=len(labels), id2label=id_to_label, label2id=label_to_id
)

# Step 4: Tokenize text
def preprocess(example):
    return tokenizer(example["text"], truncation=True, padding="max_length")

tokenized_dataset = dataset.map(preprocess, batched=True)

# Step 5: Define training args
args = TrainingArguments(
    output_dir="./banking77_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    per_device_train_batch_size=16,
    num_train_epochs=3,
    logging_steps=10,
    load_best_model_at_end=True,
    save_total_limit=1,
)

# Step 6: Train model
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

if __name__ == "__main__":
    trainer.train()
    trainer.save_model("./banking77_model")
    tokenizer.save_pretrained("./banking77_model")
    print("\n✅ Model and tokenizer saved to ./banking77_model")
