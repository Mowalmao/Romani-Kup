import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import pykakasi
import os

class RomanizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Romani-Kup")
        self.geometry("400x200")

        self.label = tk.Label(self, text="Select a .kup to Romanise :")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self, text="Select the file", command=self.select_file)
        self.select_button.pack(pady=10)

        self.file_path = ""

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Kuriimu's XML", "*.kup"), ("All Files", "*.*")]
        )
        if self.file_path:
            self.label.config(text=f"Selected Files : {os.path.basename(self.file_path)}")
            self.romanize_button = tk.Button(self, text="Romanise and save", command=self.romanize_and_save)
            self.romanize_button.pack(pady=10)

    def romanize_japanese(self, text):
        kakasi = pykakasi.kakasi()
        result = kakasi.convert(text)
        romanized_text = ' '.join([item['hepburn'] for item in result])
        
        # Split slashes with a space and capitalize each word
        romanized_text = romanized_text.replace('/', ' / ')
        romanized_text = ' '.join(word.capitalize() for word in romanized_text.split())
        
        return romanized_text

    def romanize_xml_element(self, element):
        if element.text:
            element.text = self.romanize_japanese(element.text)
        for subelement in element:
            self.romanize_xml_element(subelement)

    def romanize_and_save(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            self.romanize_xml_element(root)

            output_file_path = filedialog.asksaveasfilename(
                defaultextension=".kup",
                filetypes=[("Kuriimu's XML", "*.kup"), ("All files", "*.*")]
            )
            if output_file_path:
                tree.write(output_file_path)
                messagebox.showinfo("Success", f"Romanised KUPs saved in {output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    app = RomanizerApp()
    app.mainloop()
