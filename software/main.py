from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
from joblib import load
from Bio import SeqIO
import tkinter as tk
import pandas as pd
import numpy as np
import re

data = np.load("./uniprotSeq.npz")  

class MLFastaClassifier:
    
    def __init__(self, master):
        self.master = master
        master.title("ML Adhesive Classifier")
        
        self.path_label = tk.Label(master, text="Select your fasta file:")
        self.path_label.place(x=5, y=5)
        
        self.path_entry = tk.Entry(master, width=40)
        self.path_entry.place(x=5, y=35)
        
        image = Image.open("./logo.png")
        image = image.resize((70, 70))
        self.image_tk = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(master,image=self.image_tk)
        self.image_label.place(x=450, y=15)
        
        self.choose_button = tk.Button(master, height=1, width=8, text="Browse", command=self.buttonAskFile)
        self.choose_button.place(x=300, y=30)
        
        self.classify_button = tk.Button(master, height=1, width=8, text="Process", command=self.classify)
        self.classify_button.place(x=5, y=60)
        
        self.save_button = tk.Button(master, height=1, width=8, text="Save", command=self.saveFile)
        self.save_button.place(x=75, y=60)
        
        self.result_text = scrolledtext.ScrolledText(master, height=15, width=80, wrap=tk.WORD)
        self.result_text.place(x=5, y=95)

    def buttonAskFile(self):
        file_path = filedialog.askopenfilename(filetypes = ((('FASTA files', '*.fasta'), ('All files', '*.*'))))
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, file_path)

    def extractEntryId(self, entry_name):
        match = re.match(r".*\|([A-Z0-9]+)\|.*", entry_name)
        if match:
            return match.group(1)
        else:
            return "N/A"
    
    def readFasta(self, file_path):
        Entry = [str(record.id) for record in SeqIO.parse(file_path, 'fasta')]
        entry_names = [self.extractEntryId(entry) for entry in Entry]
        return entry_names

    def embedEntry(self, entry):
        return data[entry]

    def classify(self):
        fasta_path = self.path_entry.get()
        entries = self.readFasta(fasta_path)
        
        self.result_text.delete("1.0", tk.END)
        
        for entry in entries:
            
            embedded_entry = self.embedEntry(entry)
            svm_model = load('./svm.joblib')
            scaler = load('./scaler.joblib')
            
            X_reshaped = embedded_entry.reshape(1, -1)
            X_scaled = scaler.transform(X_reshaped)
            
            svm_pred = svm_model.predict_proba(X_scaled)
            
            if svm_pred[0][1]>=0 and svm_pred[0][1]<0.3:
                pred="Impossible"
            elif svm_pred[0][1]>=0.3 and svm_pred[0][1]<0.5:
                pred="Not quite"
            elif svm_pred[0][1]>=0.5 and svm_pred[0][1]<0.7:
                pred="Can be"
            elif svm_pred[0][1]>=0.7 and svm_pred[0][1]<=1:
                pred="Highly possible"
                
            self.result_text.insert(tk.END, "Prediction for {:10}: {:6.2%} {:15}\n".format(entry,svm_pred[0][1],pred))

    def saveFile(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            data_to_save = self.result_text.get("1.0", tk.END)
            df = pd.DataFrame(data_to_save.split("\n"), columns=["Classification Result"])
            
            try:
                df.to_excel(file_path, index=False)
                print(f"Saved classification results to {file_path}")
                messagebox.showinfo("Notification", "File saved!")

            except Exception as e:
                print("An error occurred while saving:", e)    

root = tk.Tk()

root.iconbitmap('icon.ico')
root.geometry("600x340")


app = MLFastaClassifier(root)

root.mainloop()