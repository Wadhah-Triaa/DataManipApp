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
        main_frame.columnconfigure(0, weight=3)  
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
        
        #Get data using CSV/EXCEL
        ttk.Button(upload_frame, text="Upload File", command=self.upload_file).grid(row=0, column=0, sticky=tk.W)
        
        #Get data using API
        api_frame = ttk.Frame(upload_frame)
        api_frame.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.name_var = tk.StringVar()
        ttk.Label(api_frame, text="Or Use API Endpoint").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(api_frame, textvariable=self.name_var ,width=30).grid(row=0, column=1, sticky=tk.W,padx=(0, 5) )
        ttk.Button(api_frame,command=self.upload_api_data, text="Get Data ").grid(row=0, column=2, sticky=tk.W)
        #Table Clearance
        self.file_label = ttk.Label(upload_frame, text="No file selected")
        self.file_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        ttk.Button(upload_frame,command=self.clear_table, text="Clear Table").grid(row=0, column=4, sticky=tk.E)

        table_frame = ttk.Frame(csv_frame)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
             #  Treeview for displaying data
        self.tree = ttk.Treeview(table_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

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
        self.status_var.set("Ready - Please upload a file or provide an API")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0,  sticky=(tk.W, tk.E), pady=(10, 0),padx=(0,25))
        status_bar.columnconfigure(0, weight=0)
        #Save Button
        self.save_btn=ttk.Button(main_frame,text="Save File As",command=self.save_file).grid(row=2, column=1,  sticky=(tk.W, tk.E), pady=(5, 0),padx=10)

    def upload_file(self):
        self.clear_table()
        file_path = filedialog.askopenfilename(
        title="Select File ",
        filetypes=[("All files", "*.*"),("CSV files", "*.csv"),("EXCEL files", "*.xlsx")]
    )
        if file_path:
            try:
                if file_path.lower().endswith(".csv"):
                    self.dataTable=fct.DataF(file_path,fct.loadCSV)
                elif file_path.lower().endswith(".xlsx"):
                    self.dataTable=fct.DataF(file_path,fct.loadExcel)

                filename = file_path.split('/')[-1]  
                self.file_label.config(text=f"File: {filename}")
                self.status_var.set(f"File: {filename} Loaded Successfully")

                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading CSV file:\n{str(e)}")
                self.status_var.set("Error loading file")
        self.tree["columns"] = list(self.dataTable.get_columns())
        self.tree["show"] = "headings"  # hide the default column

        # Add column headings
        for col in self.dataTable.get_columns():
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center",width=120, minwidth=80)

        # Insert DataFrame rows into Treeview
        for _, row in self.dataTable.iterrows():
            self.tree.insert("", "end", values=list(row))

    def upload_api_data(self):
        try:
            self.clear_table()
            self.dataTable=fct.DataF(self.name_var.get(),fct.loadAPI)
            self.tree["columns"] = list(self.dataTable.get_columns())
            self.tree["show"] = "headings"  # hide the default column

            # Add column headings
            for col in self.dataTable.get_columns():
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center",width=120, minwidth=80,)

            # Insert DataFrame rows into Treeview
            for _, row in self.dataTable.iterrows():
                self.tree.insert("", "end", values=list(row))
            self.status_var.set(f"API Endpoint: {self.name_var.get()} Loaded Successfully")
        except Exception as e:
                messagebox.showerror("Error", f"Error Loading API")
                self.status_var.set("Error loading API,That's not an API endpoint")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # default extension if user doesn't type one
        filetypes=[
            ("Text Files", "*.txt"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("All Files", "*.*")
        ],
        title="Save your file"
    )

        if file_path:
            print("Saving to:", file_path)
            with open(file_path, "w") as f:
                f.write(self.dataTable)

    def clear_table(self):
        self.tree.delete(*self.tree.get_children())
        self.status_var.set("Table cleared")
        self.file_label.config(text="No file selected")
        self.tree["columns"] = ()



    