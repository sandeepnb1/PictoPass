import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext, Menu
from hashlib import sha256, sha1, md5

class ImageHashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Hash Calculator")

        self.selected_image = ""
        self.hash_algorithms = [('SHA-256', sha256), ('SHA-1', sha1), ('MD5', md5)]
        self.current_algorithm = sha256

        self.create_menu()
        self.create_ui()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_ui(self):
        ttk.Label(self.root, text="Image Hash Calculator", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(self.root, text="Upload Image", command=self.upload_image).pack(pady=5)

        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_result, state="disabled")
        self.clear_button.pack(pady=5)

        ttk.Label(self.root, text="Hash Algorithm:").pack()
        algorithm_names = [algo[0] for algo in self.hash_algorithms]
        self.algorithm_combobox = ttk.Combobox(self.root, values=algorithm_names)
        self.algorithm_combobox.pack()
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.update_algorithm)

        ttk.Button(self.root, text="Calculate Hash", command=self.calculate_hash).pack(pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        self.progress_bar = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress_bar.pack(fill="x")

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, width=40)
        self.result_text.pack(pady=5)

    def upload_image(self):
        self.selected_image = filedialog.askopenfilename(title="Select an Image File")
        if self.selected_image:
            self.clear_button.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Selected Image: {self.selected_image}")

    def clear_result(self):
        self.selected_image = ""
        self.clear_button.config(state="disabled")
        self.algorithm_combobox.set("")
        self.result_text.delete(1.0, tk.END)
        self.progress_bar.stop()

    def update_algorithm(self, event):
        selected_algorithm_name = self.algorithm_combobox.get()
        for algo_name, algo_func in self.hash_algorithms:
            if algo_name == selected_algorithm_name:
                self.current_algorithm = algo_func
                break

    def calculate_hash(self):
        if not self.selected_image:
            messagebox.showerror("Error", "No image selected.")
            return

        self.progress_bar.start()

        try:
            with open(self.selected_image, "rb") as f:
                hash_obj = self.current_algorithm()
                chunk_size = 8192

                while chunk := f.read(chunk_size):
                    hash_obj.update(chunk)

                readable_hash = hash_obj.hexdigest()
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Selected Image: {self.selected_image}\n")
                self.result_text.insert(tk.END, f"Hash Algorithm: {self.algorithm_combobox.get()}\n")
                self.result_text.insert(tk.END, f"Hash: {readable_hash}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.progress_bar.stop()

    def show_about(self):
        messagebox.showinfo("About", "Image Hash Calculator\nVersion 1.0\n\nDeveloped by Sandeep N Bhandarkar")

def main():
    root = tk.Tk()
    app = ImageHashApp(root)
    style = ttk.Style()
    style.theme_use("clam")  # Use the "clam" theme for a clean appearance
    root.mainloop()

if __name__ == "__main__":
    main()
