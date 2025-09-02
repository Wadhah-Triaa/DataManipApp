import tkinter as tk
from WelcomeInterface import WelcomePage
def main():
    root = tk.Tk()
    app = WelcomePage(root)
    root.mainloop()


if __name__ == "__main__":
    main()