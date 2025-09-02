# 🧰 Data ETL GUI App (Tkinter)

This is a GUI-based ETL (Extract, Transform, Load) application built with **Python** and **Tkinter**. It allows users to upload dataset files or input API URLs, view the data in a table, manipulate it using built-in tools, and export the cleaned data as CSV or Excel files.

---

## 📌 Features

- **📂 Upload Dataset File**  
  Supports CSV and Excel formats.
  
- **🌐 Load Data from API**  
  Input a custom API URL that returns JSON data.

- **🧮 Data Preview**  
  View raw and transformed data in a scrollable Treeview table.

- **🧰 Data Manipulation Functions**  
  The app currently supports the following data transformation features:

  - Replace a character in the dataset  
  - Rename a column  
  - Filter rows by numerical values  
  - Filter rows by string values  
  - Filter rows by date range  
  - Translate entire columns using Google Translate  
  - Drop unwanted columns  
  - Sort data by specified order  
  - Show top or bottom rows of the dataset  
  - Remove duplicates (keep last occurrence)  
  - Remove all duplicated rows  
  - Split a column into multiple columns  
  - Reset to original (unmodified) dataset  

  *More functions and improvements are coming soon!*

- **💾 Save Transformed Dataset**  
  Export cleaned data to:  
  - CSV  
  - Excel (`.xlsx`)

---

## 🖼️ GUI Overview

- **Top Left Panel:** Upload dataset or input API  
- **Center Panel:** Table view (Treeview)  
- **Right Panel:** Data transformation tools  
- **Bottom Right Buttons:** Save/export options  

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+  
- Install required libraries:

```bash
pip install -r requirements.txt
```
## 🐞 Feedback & Contributions

If you find any bugs, issues, or have suggestions for new features, please feel free to **open an issue** or **submit a pull request**. Your feedback is highly appreciated and helps make this project better!

