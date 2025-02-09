import pandas as pd
from sklearn.model_selection import train_test_split

# Load preprocessed dataset

# Correct file path
resume_df = pd.read_csv("archive/Resume/Resume.csv")  # Change path if needed

print(resume_df.head())  # Verify it loads correctly
  # Ensure it's structured properly

# Convert structured sections to text format
def format_resume(row):
    return f"""
    Summary: {row['Resume_str']}
    Experience: {row['Resume_str']}
    Education: {row['Resume_str']}
    Skills: {row['Resume_str']}
    Certifications: {row['Resume_str']}
    Projects: {row['Resume_str']}
    """

resume_df["Resume_Text"] = resume_df.apply(format_resume, axis=1)

# Split into training & testing data
train_texts, test_texts = train_test_split(resume_df["Resume_Text"], test_size=0.2, random_state=42)

# Save the training and testing data
train_texts.to_csv("train_resumes.csv", index=False)
test_texts.to_csv("test_resumes.csv", index=False)

print("Training data saved successfully!")

from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load GPT-2
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Save the model after training
model.save_pretrained("resume_generator")
tokenizer.save_pretrained("resume_generator")

print("Model saved successfully! 🚀")
print(resume_df.columns)  # This will print all available column names

