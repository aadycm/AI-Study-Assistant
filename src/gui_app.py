import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from main import answer_question

class AIStudyAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Assistant")
        self.root.geometry("600x400")

        # Input label and box
        tk.Label(root, text="Ask a question about your notes:").pack(pady=5)
        self.question_entry = tk.Entry(root, width=70)
        self.question_entry.pack(pady=5)

        # Submit button
        tk.Button(root, text="Get Answer", command=self.get_answer).pack(pady=5)

        # Output box
        self.output_box = scrolledtext.ScrolledText(root, width=70, height=15)
        self.output_box.pack(pady=10)
    
    def get_answer(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Input Needed", "Please type a question!")
            return

        # Get answer from main.py function
        answer = answer_question(question)
        self.output_box.insert(tk.END, f"Q: {question}\nA: {answer}\n{'-'*50}\n")
        self.output_box.see(tk.END)
        self.question_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudyAssistantGUI(root)
    root.mainloop()
