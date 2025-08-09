import GUI

def main():
    root = GUI.tk.Tk()
    app = GUI.CSVViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()