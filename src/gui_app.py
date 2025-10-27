import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from .main import answer_question, chunks, model, index
from .pdf_reader import extract_text, split_into_chunks
import faiss
import numpy as np

class AIStudyAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Assistant")
        self.root.geometry("650x500")

        # Load PDF button
        tk.Button(root, text="Load PDF Notes",command=self.load_pdf).pack(pady=5)

        # Input label and box
        tk.Label(root, text="Ask a question about your notes:").pack(pady=5)
        self.question_entry = tk.Entry(root,width=70)
        self.question_entry.pack(pady=5)

        # Submit button
        tk.Button(root, text="Get Answer",command=self.get_answer).pack(pady=5)

        # Output box
        self.output_box = scrolledtext.ScrolledText(root,width=75,height=20)
        self.output_box.pack(pady=10)

        # Internal variables
        self.chunks = chunks  # from main.
        self.model = model
        self.index = index

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files","*.pdf")])
        if not file_path:
            return
        try:
            pdf_text = extract_text(file_path)
            self.chunks = split_into_chunks(pdf_text,500)
            self.model = model
            embeddings = self.model.encode(self.chunks,convert_to_numpy=True)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)
            messagebox.showinfo("Success",f"Loaded {len(self.chunks)}chunks from PDF.")
        except Exception as e:
            messagebox.showerror("Error",f"Failed to load PDF:{e}")

    def get_answer(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Input Needed","Please type a question!")
            return
        # Searching in the current index
        q_emb = self.model.encode([question],convert_to_numpy=True)
        D, I = self.index.search(q_emb,k=1)
        best_chunk = self.chunks[I[0][0]]
        self.output_box.insert(tk.END,f"Q: {question}\nA: {best_chunk}\n{'-'*50}\n")
        self.output_box.see(tk.END)
        self.question_entry.delete(0,tk.END)

    def summarize_notes(self):
        self.output_box.insert(tk.END,"Summarizing notes...\n")
        summaries = []
        for i, chunk in enumerate(self.chunks):
            # Simple summary: first sentence or first 20 words
            summary = ' '.join(chunk.split()[:20]) + "..."
            summaries.append(summary)
            self.output_box.insert(tk.END,f"Chunk {i+1} summary: {summary}\n")
        self.output_box.insert(tk.END,"Summarization done.\n" + "-"*50 + "\n")
        self.output_box.see(tk.END)

    def generate_flashcards(self):
        self.output_box.insert(tk.END,"Generating flashcards...\n")
        for i, chunk in enumerate(self.chunks):
            # Simple flashcard: first sentence as Q, rest as A
            words = chunk.split()
            question = ' '.join(words[:10]) + "..."
            answer = ' '.join(words[10:30]) + "..."
            self.output_box.insert(tk.END,f"Flashcard {i+1}:\nQ: {question}\nA: {answer}\n{'-'*30}\n")
        self.output_box.insert(tk.END,"Flashcards generated.\n" + "-"*50 + "\n")
        self.output_box.see(tk.END)
	
if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudyAssistantGUI(root)
    root.mainloop()
