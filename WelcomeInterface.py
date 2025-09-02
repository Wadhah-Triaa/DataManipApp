import tkinter as tk
from tkinter import ttk
import sys
from GUI import DataViewer


class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.after_ids = []
        self.event_bindings = [] 
        self.is_transitioning = False  

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("DataFlow Studio")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")
        
        self.root.configure(bg='#ffffff')
        
    def bind_event_with_tracking(self, widget, event, callback):
        """Bind events while tracking them for later cleanup"""
        widget.bind(event, callback)
        self.event_bindings.append((widget, event))
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        try:
            canvas = tk.Canvas(self.root, bg='#ffffff', highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ffffff')

            def configure_scroll_region(event):
                if canvas.winfo_exists():
                    canvas.configure(scrollregion=canvas.bbox("all"))

            def configure_canvas_width(event):
                if canvas.winfo_exists():
                    canvas_width = event.width
                    canvas.itemconfig(canvas_window, width=canvas_width)

            self.bind_event_with_tracking(scrollable_frame, "<Configure>", configure_scroll_region)
            self.bind_event_with_tracking(canvas, '<Configure>', configure_canvas_width)

            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            def _on_mousewheel(event):
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            def _on_mousewheel_linux_up(event):
                if canvas.winfo_exists():
                    canvas.yview_scroll(-1, "units")

            def _on_mousewheel_linux_down(event):
                if canvas.winfo_exists():
                    canvas.yview_scroll(1, "units")

            def bind_mousewheel(event):
                try:
                    canvas.bind_all("<MouseWheel>", _on_mousewheel)
                    canvas.bind_all("<Button-4>", _on_mousewheel_linux_up)
                    canvas.bind_all("<Button-5>", _on_mousewheel_linux_down)
                except tk.TclError:
                    pass

            def unbind_mousewheel(event):
                try:
                    canvas.unbind_all("<MouseWheel>")
                    canvas.unbind_all("<Button-4>")
                    canvas.unbind_all("<Button-5>")
                except tk.TclError:
                    pass

            self.bind_event_with_tracking(canvas, "<Enter>", bind_mousewheel)
            self.bind_event_with_tracking(canvas, "<Leave>", unbind_mousewheel)

            #Main container-responsive padding
            main_container = tk.Frame(scrollable_frame, bg='#ffffff')
            main_container.pack(fill='both', expand=True, padx=30, pady=30)
            
            def update_padding(event=None):
                if self.root.winfo_exists() and not self.is_transitioning:
                    try:
                        width = self.root.winfo_width()
                        if width < 700:
                            padx = 20
                        elif width < 1000:
                            padx = 30
                        else:
                            padx = 50
                        main_container.pack_configure(padx=padx)
                    except tk.TclError:
                        pass
            
            self.bind_event_with_tracking(self.root, '<Configure>', update_padding)
            
            header_frame = tk.Frame(main_container, bg='#ffffff')
            header_frame.pack(fill='x', pady=(0, 40))
            
            title_label = tk.Label(
                header_frame,
                text="DataFlow Studio",
                font=('Segoe UI', 42, 'bold'),
                fg='#1a1a1a',
                bg='#ffffff'
            )
            title_label.pack()
            
            separator_frame = tk.Frame(header_frame, height=4, bg='#ffffff')
            separator_frame.pack(fill='x', pady=(10, 0))
            
            gradient_canvas = tk.Canvas(separator_frame, height=4, bg='#ffffff', highlightthickness=0)
            gradient_canvas.pack(fill='x')
            
            def draw_gradient(event=None):
                if gradient_canvas.winfo_exists() and not self.is_transitioning:
                    try:
                        gradient_canvas.delete("all")
                        width = gradient_canvas.winfo_width()
                        if width > 1:
                            for i in range(width):
                                r = int(52 + (100 * i / width))
                                g = int(152 + (50 * i / width))
                                b = int(219 + (30 * i / width))
                                color = f"#{r:02x}{g:02x}{b:02x}"
                                gradient_canvas.create_line(i, 0, i, 4, fill=color, width=1)
                    except tk.TclError:
                        pass
            
            self.bind_event_with_tracking(gradient_canvas, '<Configure>', draw_gradient)
            after_id = self.root.after(100, draw_gradient)
            self.after_ids.append(after_id)

            subtitle_label = tk.Label(
                header_frame,
                text="Next-Generation Data Analysis Platform",
                font=('Segoe UI', 16, 'normal'),
                fg='#666666',
                bg='#ffffff'
            )
            subtitle_label.pack(pady=(20, 0))
            
            card_frame = tk.Frame(
                main_container,
                bg='#C6D4D7',
                relief='flat',
                bd=0
            )
            card_frame.pack(fill='both', expand=True, pady=(0, 30))
            
            shadow_frame = tk.Frame(main_container, bg='#e0e0e0', height=2)
            shadow_frame.place(in_=card_frame, x=5, y=5, relwidth=1, relheight=1)
            card_frame.lift()
            
            card_content = tk.Frame(card_frame, bg='#C6D4D7')
            card_content.pack(fill='both', expand=True, padx=40, pady=40)
            
            welcome_section = tk.Frame(card_content, bg='#C6D4D7')
            welcome_section.pack(fill='x', pady=(0, 30))
            
            welcome_title = tk.Label(
                welcome_section,
                text="🚀 Welcome to the Future of Data",
                font=('Segoe UI', 24, 'bold'),
                fg='#000000',
                bg='#C6D4D7'
            )
            welcome_title.pack()
            
            welcome_desc = tk.Label(
                welcome_section,
                text="Harness the power of advanced data manipulation with our intuitive interface.",
                font=('Segoe UI', 12),
                fg='#000000',
                bg='#C6D4D7',
                wraplength=700
            )
            welcome_desc.pack(pady=(10, 0))
            
            features_frame = tk.Frame(card_content, bg='#C6D4D7')
            features_frame.pack(fill='x', pady=(0, 40))
            
            features_title = tk.Label(
                features_frame,
                text="✨ What You Can Do",
                font=('Segoe UI', 18, 'bold'),
                fg='#ffffff',
                bg='#1a1a1a'
            )
            features_title.pack(pady=(0, 20))
            
            features_grid = tk.Frame(features_frame, bg='#C6D4D7')
            features_grid.pack(fill='x')
            
            features = [
                ("📊", "Data Visualization", "Create stunning charts and graphs COMING SOON"),
                ("🔧", "Data Cleaning", "Remove duplicates and handle missing values"),
                ("⚡", "Fast Processing", "Handle large datasets with optimized algorithms"),
                ("💾", "Multiple Formats", "Support for CSV, Excel, JSON, and databases"),
                ("🎯", "Smart Filtering", "Advanced filtering with custom conditions"),
                ("📈", "Statistical Analysis", "Built-in statistical functions and insights COMING SOON")
            ]
            
            self.feature_cards = []
            
            def arrange_features(event=None):
                if self.is_transitioning:
                    return
                    
                try:
                    #Clear existing grid
                    for card in self.feature_cards:
                        if card.winfo_exists():
                            card.grid_forget()
                    
                    window_width = self.root.winfo_width()
                    
                    if window_width < 700:
                        cols = 1
                    elif window_width < 1000:
                        cols = 2
                    else:
                        cols = 2
                    
                    for i, (icon, title, desc) in enumerate(features):
                        row = i // cols
                        col = i % cols
                        
                        if i < len(self.feature_cards):
                            card = self.feature_cards[i]
                        else:
                            card = tk.Frame(features_grid, bg='#ffffff', relief='flat', bd=1, width=300, height=120)
                            card.grid_propagate(False)
                            card.pack_propagate(False)
                            
                            feature_content = tk.Frame(card, bg='#ffffff')
                            feature_content.pack(fill='both', padx=15, pady=12)
                            
                            icon_title_frame = tk.Frame(feature_content, bg='#ffffff')
                            icon_title_frame.pack(fill='x')
                            
                            icon_label = tk.Label(
                                icon_title_frame,
                                text=icon,
                                font=('Segoe UI', 16),
                                bg='#ffffff'
                            )
                            icon_label.pack(side='left')
                            
                            title_label = tk.Label(
                                icon_title_frame,
                                text=title,
                                font=('Segoe UI', 14, 'bold'),
                                fg='#1a1a1a',
                                bg='#ffffff',
                                anchor='w'
                            )
                            title_label.pack(side='left', padx=(10, 0), fill='x', expand=True)
                            
                            desc_label = tk.Label(
                                feature_content,
                                text=desc,
                                font=('Segoe UI', 12),
                                fg='#666666',
                                bg='#ffffff',
                                wraplength=260,
                                justify='left',
                                anchor='nw'
                            )
                            desc_label.pack(fill='both', pady=(8, 0), anchor='w', expand=True)
                            
                            self.feature_cards.append(card)
                        
                        if card.winfo_exists():
                            card.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
                            features_grid.grid_columnconfigure(col, weight=1)
                except tk.TclError:
                    pass
            
            after_id = self.root.after(100, arrange_features)
            self.after_ids.append(after_id)
            self.bind_event_with_tracking(self.root, '<Configure>', lambda e: self.safe_after_idle(arrange_features))
            
            action_frame = tk.Frame(card_content, bg='#C6D4D7')
            action_frame.pack(fill='x', side='bottom')
            
            ready_label = tk.Label(
                action_frame,
                text="Ready to transform your data?",
                font=('Segoe UI', 16, 'bold'),
                fg='#ffffff',
                bg='#1a1a1a'
            )
            ready_label.pack(pady=(0, 25))
            
            buttons_container = tk.Frame(action_frame, bg='#C6D4D7')
            buttons_container.pack()
            
            self.proceed_button = tk.Button(
                buttons_container,
                text="🚀 Launch Application",
                command=self.proceed_to_app,
                font=('Segoe UI', 14, 'bold'),
                bg='#3498db',
                fg='white',
                activebackground='#2980b9',
                activeforeground='white',
                relief='flat',
                padx=35,
                pady=15,
                cursor='hand2',
                borderwidth=0
            )
            self.proceed_button.pack(side='left', padx=(0, 15))
            
            self.exit_button = tk.Button(
                buttons_container,
                text="✖ Exit",
                command=self.exit_app,
                font=('Segoe UI', 12, 'normal'),
                bg='#4a4a4a',
                fg='#ffffff',
                activebackground='#5a5a5a',
                activeforeground='white',
                relief='flat',
                padx=25,
                pady=15,
                cursor='hand2',
                borderwidth=0
            )
            self.exit_button.pack(side='left')
            
            self.add_hover_effect(self.proceed_button, '#2980b9', '#3498db')
            self.add_hover_effect(self.exit_button, '#5a5a5a', '#4a4a4a')
            
            def update_button_layout(event=None):
                if self.is_transitioning:
                    return
                try:
                    width = self.root.winfo_width()
                    if width < 600:
                        self.proceed_button.pack_configure(side='top', padx=0, pady=(0, 10))
                        self.exit_button.pack_configure(side='top', padx=0)
                        self.proceed_button.configure(font=('Segoe UI', 12, 'bold'))
                        self.exit_button.configure(font=('Segoe UI', 10, 'normal'))
                    else:
                        self.proceed_button.pack_configure(side='left', padx=(0, 15), pady=0)
                        self.exit_button.pack_configure(side='left', padx=0, pady=0)
                        self.proceed_button.configure(font=('Segoe UI', 14, 'bold'))
                        self.exit_button.configure(font=('Segoe UI', 12, 'normal'))
                except tk.TclError:
                    pass
            
            self.bind_event_with_tracking(self.root, '<Configure>', lambda e: self.safe_after_idle(update_button_layout))
            
            footer_frame = tk.Frame(self.root, bg='#C6D4D7', height=30)
            footer_frame.pack(side='bottom', fill='x')
            footer_frame.pack_propagate(False)
            
            footer_label = tk.Label(
                footer_frame,
                text="v2.0.0 • Built with Python & Tkinter • Ready for Enterprise",
                font=('Segoe UI', 9),
                fg='#888888',
                bg='#C6D4D7'
            )
            footer_label.pack(expand=True)
            
        except Exception as e:
            print(f"Error creating widgets: {e}")
            
    def safe_after_idle(self, callback):
        """Safely schedule after_idle callbacks"""
        if not self.is_transitioning and self.root.winfo_exists():
            try:
                self.root.after_idle(callback)
            except tk.TclError:
                pass
        
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effects to buttons"""
        def on_enter(e):
            if not self.is_transitioning and button.winfo_exists():
                try:
                    button.configure(bg=hover_color)
                except tk.TclError:
                    pass
                
        def on_leave(e):
            if not self.is_transitioning and button.winfo_exists():
                try:
                    button.configure(bg=normal_color)
                except tk.TclError:
                    pass
                
        self.bind_event_with_tracking(button, "<Enter>", on_enter)
        self.bind_event_with_tracking(button, "<Leave>", on_leave)
        
    def cleanup_resources(self):
        """Clean up all resources before transitioning"""
        print("🧹 Cleaning up resources...")
        
        self.is_transitioning = True
        
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except:
                pass
        self.after_ids.clear()
        
        for widget, event in self.event_bindings:
            try:
                if widget.winfo_exists():
                    widget.unbind(event)
            except:
                pass
        self.event_bindings.clear()
        
        try:
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
        except:
            pass
            
        try:
            self.root.unbind('<Return>')
            self.root.unbind('<Escape>')
        except:
            pass
        
    def proceed_to_app(self):
        """Handle the proceed button click"""
        if self.is_transitioning:
            return  
            
        print("🚀 Launching DataFlow Studio...")
        
        try:
            if hasattr(self, 'proceed_button') and self.proceed_button.winfo_exists():
                original_text = self.proceed_button.cget('text')
                self.proceed_button.configure(text="🔄 Loading...", state='disabled')
                self.root.update()
                
                after_id = self.root.after(1000, self.launch_main_app)
                self.after_ids.append(after_id)
            else:
                self.launch_main_app()
        except Exception as e:
            print(f"Error in proceed_to_app: {e}")
            self.launch_main_app()
            
    def launch_main_app(self):
        """Launch the main application"""
        try:
            print("🔄 Transitioning to main application...")
            
            self.cleanup_resources()
            
            #Destroy all widgets
            for widget in self.root.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
            
            self.root.update()
            
            #Launch the main data viewer
            print("✅ Launching CSV Viewer...")
            DataViewer(self.root)
            
        except Exception as e:
            print(f"Error launching main app: {e}")
            self.exit_app()

    def exit_app(self):
        """Handle the exit button click with confirmation"""
        try:
            self.cleanup_resources()
            self.root.quit()
            sys.exit()
        except:
            sys.exit()
        
    def run(self):
        """Start the GUI main loop"""
        try:
            self.bind_event_with_tracking(self.root, '<Return>', lambda e: self.proceed_to_app())
            self.bind_event_with_tracking(self.root, '<Escape>', lambda e: self.exit_app())
            
            self.root.focus_force()
            
            self.root.mainloop()
        except Exception as e:
            print(f"Error in main loop: {e}")
            sys.exit()

