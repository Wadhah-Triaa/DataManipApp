import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkcalendar import DateEntry
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
        main_frame.rowconfigure(0, weight=2)

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

        # RIGHT SIDE: FUNCTIONS LIST 
        functions_frame = ttk.LabelFrame(main_frame, text="Functions", padding="5")
        functions_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        functions_frame.columnconfigure(0, weight=1)
        functions_frame.rowconfigure(0, weight=1)

        func_listbox_frame = ttk.Frame(functions_frame)
        func_listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        func_listbox_frame.columnconfigure(0, weight=1)
        func_listbox_frame.rowconfigure(0, weight=1)

        self.functions_listbox = tk.Listbox(func_listbox_frame, font=("Arial", 10), selectmode=tk.SINGLE,exportselection=False)
        func_scrollbar = ttk.Scrollbar(func_listbox_frame, orient="vertical", command=self.functions_listbox.yview)
        self.functions_listbox.configure(yscrollcommand=func_scrollbar.set)
        self.functions_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        func_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # RIGHT SIDE: COLUMNS LIST 
        cols_frame = ttk.LabelFrame(main_frame, text="Columns", padding="5")
        cols_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        cols_frame.columnconfigure(0, weight=1)
        cols_frame.rowconfigure(0, weight=1)

        cols_listbox_frame = ttk.Frame(cols_frame)
        cols_listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        cols_listbox_frame.columnconfigure(0, weight=1)
        cols_listbox_frame.rowconfigure(0, weight=1)

        self.cols_listbox = tk.Listbox(cols_listbox_frame, font=("Arial", 10), selectmode=tk.SINGLE,exportselection=False)
        cols_scrollbar = ttk.Scrollbar(cols_listbox_frame, orient="vertical", command=self.cols_listbox.yview)
        self.cols_listbox.configure(yscrollcommand=cols_scrollbar.set)
        self.cols_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        cols_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(cols_frame, text="Execute Selected Function",command=self.execute_function).grid(row=2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
      
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
        filetypes=[("CSV files", "*.csv"),("EXCEL files", "*.xlsx")]
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
        
        self.display_data()

    def upload_api_data(self):
        try:
            self.clear_table()
            self.dataTable=fct.DataF(self.name_var.get(),fct.loadAPI)
            self.file_label.config(text=f"API Loaded")
            self.status_var.set(f"API Endpoint: {self.name_var.get()} Loaded Successfully")

            self.display_data()

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
                f.write(self.dataTable) #still much work here

    def clear_table(self):
        self.tree.delete(*self.tree.get_children())
        self.status_var.set("Table cleared")
        self.file_label.config(text="No file selected")
        self.tree["columns"] = ()
        self.clear_cols()

    def add_sample_functions(self):
        self.functions = {
            "Replace a Character":self.dataTable.replaceChars,
            "Rename a column":self.dataTable.renameColumn,
            "Filter by a number":self.dataTable.filterNumerical,
            "Filter by string":self.dataTable.filterString,
            "Filter by Date":self.dataTable.filterByDate,
            "Go back to orignal data":self.dataTable.get_df
        }
        for func in self.functions.keys():
            self.functions_listbox.insert(tk.END, func)

    def add_sample_cols(self):
        self.cols=self.tree["columns"]
        for col in self.cols:
            self.cols_listbox.insert(tk.END, col)
    
    def clear_cols(self):
        self.cols_listbox.delete(0, tk.END)

    def display_data(self):
        self.tree["columns"] = list(self.dataTable.get_columns())
        self.tree["show"] = "headings"  # hide the default column
        if (self.functions_listbox.size()==0):
            self.add_sample_functions()

        self.add_sample_cols()
        # Add column headings
        for col in self.dataTable.get_columns():
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center",width=120, minwidth=80)

        # Insert DataFrame rows into Treeview
        for _, row in self.dataTable.iterrows():
            self.tree.insert("", "end", values=list(row))
        self.status_var.set(self.status_var.get()+ f" With Row Count: {len(self.tree.get_children())} ")

    def execute_function(self):
        try:

            self.function_selection = self.functions_listbox.curselection()[0]
            self.column_selection= self.cols_listbox.curselection()[0]
            self.functions_listbox.selection_set(self.function_selection)
            self.cols_listbox.selection_set(self.column_selection)

        except Exception as e:
            messagebox.showwarning("No Selection", "Please select a function to execute and a column")
            return
        #if not function_selection:
           # messagebox.showwarning("No Selection", "Please select a function to execute")
        #a=self.dataTable.replaceChars(column_selection,"e","a")
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Enter Value")
        self.popup.geometry("350x150")
        self.popup.resizable(False, False) 
        ttk.Button(self.popup, text="Validate", command=self.validate).grid(row=3, column=1, sticky=tk.W, padx=(0, 5))

        match self.function_selection:
            case 0:
                self.old_char=tk.StringVar()
                self.new_char=tk.StringVar()
                #ttk.Label(self.popup, text=column_selection).grid(row=0, column=0, padx=5, pady=5).pack()
                
                ttk.Label(self.popup, text="Enter Old Character: ").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Entry(self.popup, textvariable=self.old_char ,width=30).grid(row=1, column=1, sticky=tk.W,padx=(0, 5) )
                ttk.Label(self.popup, text="Enter New Character: ").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Entry(self.popup, textvariable=self.new_char,width=30).grid(row=2, column=1, sticky=tk.W,padx=(0, 5) )
                #self.functions["Replace a Character"](column_selection,old_char.get(),new_char.get())
                


            case 1:
                #self.functions["Rename a column"](column_selection,"e")
                self.new_col_name=tk.StringVar()

                ttk.Label(self.popup, text=self.column_selection).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Label(self.popup, text="Enter New Column Name: ").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Entry(self.popup, textvariable=self.new_col_name ,width=30).grid(row=1, column=1, sticky=tk.W,padx=(0, 5) )

            case 2:
                #self.functions["Filter by a number"](column_selection,1900,">")
                self.combo = ttk.Combobox(self.popup, values=(">","<","<=",">=","==","!="), state="readonly",width=27)
                self.combo.grid(row=1,column=1,sticky=tk.W,padx=(0, 5))
                self.combo.set("Select function")
                self.value=tk.StringVar()
                ttk.Label(self.popup, text="Enter Value: ").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Entry(self.popup, textvariable=self.value ,width=30).grid(row=0, column=1, sticky=tk.W,padx=(0, 5) )
                
            case 3:
                #self.functions["Filter by string"](column_selection,"e")
                self.value=tk.StringVar()
                ttk.Label(self.popup, text="Enter String: ").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
                ttk.Entry(self.popup, textvariable=self.value ,width=30).grid(row=0, column=1, sticky=tk.W,padx=(0, 5) )


            case 4:
                self.combo = ttk.Combobox(self.popup, values=(">","<","<=",">=","==","!="), state="readonly",width=27)
                self.combo.grid(row=0,column=2,sticky=tk.W,padx=(0, 5))
                self.combo.set("Select function")
                self.date_entry = DateEntry(self.popup, date_pattern='yyyy-mm-dd')
                self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        
            case 5:
                self.functions["Go back to orignal data"]()


        #print("fct",function_selection)
        
   
    def validate (self):
        match self.function_selection:
            case 0:
                self.functions["Replace a Character"](self.column_selection, self.old_char.get(), self.new_char.get())

            case 1:
                self.functions["Rename a column"](self.column_selection,self.new_col_name.get())

            case 2:
                self.functions["Filter by a number"](self.column_selection, int(self.value.get()), self.combo.get())
                
            case 3:
                self.functions["Filter by string"](self.column_selection,self.value.get())

            case 4:
                self.functions["Filter by Date"](self.column_selection,self.date_entry.get(),self.combo.get())           
            case 5:
                self.functions["Go back to orignal data"]()

        self.popup.destroy()  # close the popup when validated
        self.clear_table()
        self.display_data()