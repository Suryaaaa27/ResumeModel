from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd 

# Load dataset
train_dataset = Dataset.from_pandas(pd.read_csv("train_resumes.csv"))
test_dataset = Dataset.from_pandas(pd.read_csv("test_resumes.csv"))

# Load GPT-2 Tokenizer & Model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Define Training Arguments
training_args = TrainingArguments(
    output_dir="./resume_model",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# Save the trained model
model.save_pretrained("./resume_generator")
tokenizer.save_pretrained("./resume_generator")

print("Model training complete! 🚀")
