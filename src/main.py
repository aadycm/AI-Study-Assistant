"""
AI Study Assistant - Main Script
--------------------------------
This is the entry point for the AI Study Assistant project.
The goal: Build an AI-driven tool that helps users study efficiently
by summarizing notes, generating quizzes, and organizing study sessions.
"""

import os
# main.py

# --- Imports ---
from pdf_reader import extract_text, split_into_chunks
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- Step 1: Load PDF and split into chunks ---
pdf_text = extract_text("data/notes.pdf")  # make sure your PDF is in the data folder
chunks = split_into_chunks(pdf_text, 500)

print(f"Extracted {len(chunks)} chunks from the PDF")
print(chunks[0])  # show first chunk

# --- Step 2: Embed the chunks ---
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks, convert_to_numpy=True)

# --- Step 3: Build FAISS index ---
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# --- Step 4: Search function ---
def answer_question(question):
    q_emb = model.encode([question], convert_to_numpy=True)
    D, I = index.search(q_emb, k=1)
    best_chunk = chunks[I[0][0]]
    return best_chunk

# You can then later add your interface (CLI or GUI) here

def main():
    print("🧠 Welcome to the AI Study Assistant!")
    print("This tool will help you manage, summarize, and learn your notes with AI.\n")
    
    while True:
        question = input("Ask a question about your notes (or type 'exit' to quit): ")
        if question.lower() in ['exit', 'quit']:
            print("Goodbye! Keep studying :)")
            break
        
        # Get answer from PDF chunks
        answer = answer_question(question)
        print("\nAnswer from notes:")
        print(answer)
        print("-" * 50)

if __name__ == "__main__":
    main()
