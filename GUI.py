import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import Functions as fct

class CSVViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Viewer with Functions")
        self.root.geometry("1200x700")

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=6)  
        main_frame.columnconfigure(1, weight=2) 
        main_frame.rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, minsize=200)
        
        #LEFT SIDE: DATA VIEWER
        csv_frame = ttk.LabelFrame(main_frame, text="Your Data", padding="5")
        csv_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        csv_frame.columnconfigure(0, weight=1)
        csv_frame.rowconfigure(1, weight=1)

        upload_frame = ttk.Frame(csv_frame)
        upload_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        upload_frame.columnconfigure(1, weight=1)
        
        ttk.Button(upload_frame, text="Upload CSV File", 
                  command=fct.loadCSV("./sales.csv")).grid(row=0, column=0, sticky=tk.W)

        self.file_label = ttk.Label(upload_frame, text="No file selected")
        self.file_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        ttk.Button(upload_frame, text="Clear Table").grid(row=0, column=2, sticky=tk.E)

        table_frame = ttk.Frame(csv_frame)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
             #  Treeview for displaying data
        self.tree = ttk.Treeview(table_frame, show="headings")
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid the treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        #RIGHT SIDE: FUNCTIONS LIST 
        functions_frame = ttk.LabelFrame(main_frame, text="Functions", padding="5")
        functions_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        functions_frame.columnconfigure(0, weight=1)
        functions_frame.rowconfigure(1, weight=1)
   
        listbox_frame = ttk.Frame(functions_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

 
        self.functions_listbox = tk.Listbox(listbox_frame, font=("Arial", 10))
        func_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.functions_listbox.yview)
        self.functions_listbox.configure(yscrollcommand=func_scrollbar.set)
        
        self.functions_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        func_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(functions_frame, text="Execute Selected Function").grid(row=2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar()         # Status bar
        self.status_var.set("Ready - Please upload a CSV file")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

