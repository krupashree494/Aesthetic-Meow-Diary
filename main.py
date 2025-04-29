from tkinter import *
from tkinter import messagebox, font, ttk
from datetime import datetime
import sqlite3
import os
from PIL import Image, ImageTk, ImageSequence  # You'll need to install pillow: pip install pillow
import random
import time

# Application settings
APP_TITLE = "My Secret Diary"

# Define multiple themes
THEMES = {
    "Pink Bliss": {
        "primary": "#FF97C1",        # Brighter pink
        "secondary": "#FFC9DE",      # Softer light pink
        "accent": "#FFECF5",         # Very light pink with more purple tint
        "text_dark": "#8B4F6D",      # Deeper purple for better contrast
        "text_light": "#FFFFFF",     # White
        "button": "#FF77B8",         # Brighter pink for buttons
        "highlight": "#FFCEF2",      # Highlight color for hover effects
        "border": "#FFADD6"          # Border color
    },
    "Ocean Breeze": {
        "primary": "#89CFF0",
        "secondary": "#B0E0E6",
        "accent": "#E0FFFF",
        "text_dark": "#1E3A5F",
        "text_light": "#FFFFFF",
        "button": "#77C3EC",
        "highlight": "#A6D8E7",
        "border": "#89CFF0"
    },
    "Sunset Glow": {
        "primary": "#FF6F61",
        "secondary": "#FFA07A",
        "accent": "#FFDAB9",
        "text_dark": "#8B4513",
        "text_light": "#FFFFFF",
        "button": "#FF8C69",
        "highlight": "#FFB6C1",
        "border": "#FF6F61"
    },
    "Forest Retreat": {
        "primary": "#228B22",
        "secondary": "#32CD32",
        "accent": "#90EE90",
        "text_dark": "#006400",
        "text_light": "#FFFFFF",
        "button": "#20B2AA",
        "highlight": "#98FB98",
        "border": "#228B22"
    },
    "Golden Hour": {
        "primary": "#FFD700",
        "secondary": "#FFEC8B",
        "accent": "#FFFACD",
        "text_dark": "#8B7500",
        "text_light": "#FFFFFF",
        "button": "#FFC125",
        "highlight": "#FFEFD5",
        "border": "#FFD700"
    },
    "Midnight Sky": {
        "primary": "#191970",
        "secondary": "#4169E1",
        "accent": "#87CEEB",
        "text_dark": "#000080",
        "text_light": "#FFFFFF",
        "button": "#1E90FF",
        "highlight": "#ADD8E6",
        "border": "#191970"
    },
    "Berry Smoothie": {
        "primary": "#8A2BE2",
        "secondary": "#9370DB",
        "accent": "#D8BFD8",
        "text_dark": "#4B0082",
        "text_light": "#FFFFFF",
        "button": "#7B68EE",
        "highlight": "#E6E6FA",
        "border": "#8A2BE2"
    },
    "Coral Reef": {
        "primary": "#FF7F50",
        "secondary": "#FFA07A",
        "accent": "#FFE4B5",
        "text_dark": "#8B4513",
        "text_light": "#FFFFFF",
        "button": "#FF8C69",
        "highlight": "#FFB6C1",
        "border": "#FF7F50"
    },
    "Lavender Dream": {
        "primary": "#E6E6FA",
        "secondary": "#D8BFD8",
        "accent": "#FFF0F5",
        "text_dark": "#800080",
        "text_light": "#FFFFFF",
        "button": "#DDA0DD",
        "highlight": "#E6E6FA",
        "border": "#E6E6FA"
    },
    "Mint Fresh": {
        "primary": "#98FB98",
        "secondary": "#AFEEEE",
        "accent": "#F0FFF0",
        "text_dark": "#2E8B57",
        "text_light": "#FFFFFF",
        "button": "#7FFFD4",
        "highlight": "#AFEEEE",
        "border": "#98FB98"
    }
}

# Default theme
THEME_COLOR = THEMES["Pink Bliss"]

# Dummy credentials (in a real app, use proper authentication)
USERNAME = "u"
PASSWORD = "p"

# Database setup
def setup_database():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = sqlite3.connect("data/diary.db")
    cursor = conn.cursor()
    
    # Create diary entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            mood TEXT,
            font_family TEXT,
            font_size INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Class to handle GIF animation
class AnimatedGif:
    def __init__(self, master, gif_path, width=100, height=100):
        self.master = master
        self.is_running = False
        self.frames = []
        self.delay = 100  # Default delay between frames
        
        # Load the GIF frames
        try:
            gif = Image.open(gif_path)
            self.frames = []
            self.delays = []
            
            # Extract all frames and their individual delays
            for frame in ImageSequence.Iterator(gif):
                frame = frame.copy()
                # Resize the frame
                frame = frame.resize((width, height), Image.LANCZOS)
                # Convert to Tkinter PhotoImage
                photoframe = ImageTk.PhotoImage(frame)
                self.frames.append(photoframe)
                
                # Try to get frame-specific delay
                try:
                    self.delays.append(frame.info['duration'])
                except:
                    self.delays.append(100)  # Default 100ms delay
            
            # If we only have one frame, it's not animated
            self.is_animated = len(self.frames) > 1
            
            # Create a label to display the frames
            self.label = Label(master, image=self.frames[0], bg=master['bg'])
            
            # Start animation
            if self.is_animated:
                self.current_frame = 0
                self.start_animation()
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            # Create a placeholder label
            dummy_img = Image.new('RGB', (width, height), color='pink')
            photo_img = ImageTk.PhotoImage(dummy_img)
            self.frames = [photo_img]
            self.label = Label(master, image=photo_img, bg=master['bg'])
    
    def pack(self, **kwargs):
        self.label.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.label.grid(**kwargs)
    
    def place(self, **kwargs):
        self.label.place(**kwargs)
    
    def start_animation(self):
        if not self.is_animated:
            return
        
        self.is_running = True
        self.update_animation()
    
    def update_animation(self):
        if not self.is_running:
            return
        
        # Update to the next frame
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.configure(image=self.frames[self.current_frame])
        
        # Use frame-specific delay if available
        frame_delay = self.delays[self.current_frame] if self.current_frame < len(self.delays) else 100
        
        # Schedule the next update
        self.label.after(frame_delay, self.update_animation)
    
    def stop_animation(self):
        self.is_running = False
    
    def set_frame(self, frame_index):
        if 0 <= frame_index < len(self.frames):
            self.label.configure(image=self.frames[frame_index])
    
    def update_background(self, bg_color):
        self.label.configure(bg=bg_color)

# Custom styles and widgets
class RoundedButton(Button):
    def __init__(self, master=None, **kwargs):
        kwargs.update({
            'relief': 'flat',
            'bd': 0,
            'bg': THEME_COLOR["button"],
            'fg': THEME_COLOR["text_light"],
            'activebackground': THEME_COLOR["primary"],
            'activeforeground': THEME_COLOR["text_light"],
            'padx': 0,
            'pady': 0
        })
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self['background'] = THEME_COLOR["primary"]
        
    def on_leave(self, e):
        self['background'] = THEME_COLOR["button"]

class DiaryEntryCard(Frame):
    def __init__(self, master, title, date, entry_id, callback, **kwargs):
        kwargs.update({'bg': THEME_COLOR["accent"], 'padx': 10, 'pady': 10, 'bd': 1, 'relief': 'ridge'})
        super().__init__(master, **kwargs)
        
        self.entry_id = entry_id
        self.callback = callback
        
        # Title with date
        title_frame = Frame(self, bg=THEME_COLOR["accent"])
        title_frame.pack(fill=X, expand=True)
        
        title_label = Label(title_frame, text=title, font=("Comic Sans MS", 11, "bold"), 
                           bg=THEME_COLOR["accent"], fg=THEME_COLOR["text_dark"], anchor="w")
        title_label.pack(side=LEFT, fill=X, expand=True)
        
        date_label = Label(title_frame, text=date, font=("Comic Sans MS", 9), 
                          bg=THEME_COLOR["accent"], fg=THEME_COLOR["text_dark"])
        date_label.pack(side=RIGHT)
        
        # Buttons
        button_frame = Frame(self, bg=THEME_COLOR["accent"])
        button_frame.pack(fill=X, pady=(5, 0))
        
        view_btn = Button(button_frame, text="View", font=("Comic Sans MS", 8),
                         bg=THEME_COLOR["button"], fg=THEME_COLOR["text_light"],
                         command=lambda: self.callback("view", self.entry_id), relief=FLAT)
        view_btn.pack(side=LEFT, padx=2)
        
        delete_btn = Button(button_frame, text="Delete", font=("Comic Sans MS", 8),
                           bg=THEME_COLOR["button"], fg=THEME_COLOR["text_light"],
                           command=lambda: self.callback("delete", self.entry_id), relief=FLAT)
        delete_btn.pack(side=LEFT, padx=2)

# Application Functionality
class DiaryApp:
    def __init__(self):
        self.current_font = ("Comic Sans MS", 12)
        setup_database()
        
        # Initialize the Tkinter application first
        self.login_window = Tk()
        self.login_window.title(f"Login to {APP_TITLE}")
        self.login_window.geometry("350x500")
        self.login_window.configure(bg=THEME_COLOR["accent"])
        self.login_window.resizable(False, False)
        
        # Setup login widgets and start the application
        self.setup_login_widgets()
        self.login_window.mainloop()
    
    def load_animated_cat(self, parent_frame, cat_index=None):
        # Define paths to your cat GIF images
        cat_paths = [
            "cat1.gif",  # Orange tabby with blue collar - happy
            "cat2.gif",  # White cat with red collar - neutral
            "cat3.gif",  # Orange tabby with food bowl - sad/hungry
        ]
        
        # If a specific index is provided, use it; otherwise choose randomly
        if cat_index is None:
            cat_path = random.choice(cat_paths)
        else:
            cat_index = min(max(0, cat_index), len(cat_paths) - 1)  # Ensure valid index
            cat_path = cat_paths[cat_index]
        
        # Create and return an animated GIF
        return AnimatedGif(parent_frame, cat_path, width=100, height=100)
    
    def setup_login_widgets(self):
        # Create a frame for login
        login_frame = Frame(self.login_window, bg=THEME_COLOR["secondary"], padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=450)  # Increased height
        
        # Title and decorative elements
        Label(login_frame, text="✨ " + APP_TITLE + " ✨", 
              font=("Comic Sans MS", 16, "bold"), bg=THEME_COLOR["secondary"], 
              fg=THEME_COLOR["text_dark"]).pack(pady=(10, 10))
        
        # Add an animated cat to the login screen
        cat_frame = Frame(login_frame, bg=THEME_COLOR["secondary"])
        cat_frame.pack(pady=10)
        
        self.login_cat = self.load_animated_cat(cat_frame)
        self.login_cat.pack()
        
        # Username field
        Label(login_frame, text="Username:", font=("Comic Sans MS", 12), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(pady=(15, 2), anchor=W)
        self.user_entry = Entry(login_frame, font=("Comic Sans MS", 10), bd=0, bg="white", width=30)
        self.user_entry.pack(ipady=5)
        
        # Password field
        Label(login_frame, text="Password:", font=("Comic Sans MS", 12), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(pady=(10, 2), anchor=W)
        self.pass_entry = Entry(login_frame, show="*", font=("Comic Sans MS", 10), bd=0, bg="white", width=30)
        self.pass_entry.pack(ipady=5)
        
        # Login button
        login_btn = RoundedButton(login_frame, text="Login", font=("Comic Sans MS", 12, "bold"), 
                                 command=self.check_login)
        login_btn.pack(pady=15)
        
        # Add a cute footer
        Label(login_frame, text="Your thoughts, safely kept 💖", 
             font=("Comic Sans MS", 8), bg=THEME_COLOR["secondary"], 
             fg=THEME_COLOR["text_dark"]).pack(side=BOTTOM, pady=5)
    
    def check_login(self):
        entered_user = self.user_entry.get()
        entered_pass = self.pass_entry.get()
        
        if entered_user == USERNAME and entered_pass == PASSWORD:
            self.login_window.destroy()
            self.open_diary()
        else:
            messagebox.showerror("Login Failed", "Incorrect Username or Password")
    
    def open_diary(self):
        self.diary = Tk()
        self.diary.title(APP_TITLE)
        self.diary.geometry("650x600")
        self.diary.configure(bg=THEME_COLOR["accent"])
        self.diary.resizable(True, True)
        
        # Create header
        header_frame = Frame(self.diary, bg=THEME_COLOR["primary"], height=80)
        header_frame.pack(fill=X)
        
        # Layout header with title and cat
        # Put cat on the right side
        cat_frame = Frame(header_frame, bg=THEME_COLOR["primary"])
        cat_frame.pack(side=RIGHT, padx=20)
        
        self.header_cat = self.load_animated_cat(cat_frame)
        self.header_cat.pack()
        
        # Title with decorations
        title_label = Label(header_frame, text=f"✨ {APP_TITLE} ✨", 
                           font=("Comic Sans MS", 20, "bold"), 
                           bg=THEME_COLOR["primary"], fg=THEME_COLOR["text_light"])
        title_label.pack(pady=15, side=LEFT, padx=20)
        
        # Date display
        current_date = datetime.now().strftime("%A, %d %B %Y")
        date_frame = Frame(self.diary, bg=THEME_COLOR["secondary"], height=40)
        date_frame.pack(fill=X)
        
        date_label = Label(date_frame, text=current_date, 
                          font=("Comic Sans MS", 12), 
                          bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"])
        date_label.pack(pady=8)
        
        # Button to add new entry
        button_frame = Frame(self.diary, bg=THEME_COLOR["accent"], height=60)
        button_frame.pack(fill=X, pady=10)
        
        new_entry_btn = RoundedButton(button_frame, text="✏️ Write New Entry", 
                                     font=("Comic Sans MS", 12, "bold"),
                                     command=self.open_new_entry)
        new_entry_btn.pack(pady=10)
        
        # Theme selection button
        theme_btn = RoundedButton(button_frame, text="🎨 Change Theme", 
                                 font=("Comic Sans MS", 12, "bold"), command=self.change_theme)
        theme_btn.pack(pady=10, side=RIGHT, padx=10)

        # Create diary entries display area
        self.entries_canvas = Canvas(self.diary, bg=THEME_COLOR["accent"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.diary, orient=VERTICAL, command=self.entries_canvas.yview)
        self.entries_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.entries_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # Frame inside canvas for entries
        self.entries_frame = Frame(self.entries_canvas, bg=THEME_COLOR["accent"])
        self.entries_canvas.create_window((0, 0), window=self.entries_frame, anchor=NW)

        # Configure the frame to expand with the canvas
        self.entries_frame.bind(
            "<Configure>", 
            lambda e: self.entries_canvas.configure(scrollregion=self.entries_canvas.bbox("all"))
        )
        # Load and display entries
        self.display_entries()
        
        self.diary.mainloop()

    def change_theme(self):
        # Create a new window for theme selection
        theme_window = Toplevel(self.diary)
        theme_window.title("Change Theme")
        theme_window.geometry("300x400")
        theme_window.configure(bg=THEME_COLOR["accent"])

        # Add a label
        Label(theme_window, text="Choose a Theme", font=("Comic Sans MS", 14, "bold"), 
              bg=THEME_COLOR["accent"], fg=THEME_COLOR["text_dark"]).pack(pady=10)

        # Create buttons for each theme
        for theme_name, theme_colors in THEMES.items():
            theme_btn = Button(theme_window, text=theme_name, font=("Comic Sans MS", 12),
                              bg=theme_colors["button"], fg=theme_colors["text_light"],
                              command=lambda t=theme_colors: self.apply_theme(t))
            theme_btn.pack(fill=X, padx=20, pady=5)

    def apply_theme(self, theme_colors):
        global THEME_COLOR
        THEME_COLOR = theme_colors

        # Update the colors of the main diary window
        self.diary.configure(bg=THEME_COLOR["accent"])
        self.entries_canvas.configure(bg=THEME_COLOR["accent"])
        self.entries_frame.configure(bg=THEME_COLOR["accent"])

        # Update the header
        header_frame = self.diary.winfo_children()[0]
        header_frame.configure(bg=THEME_COLOR["primary"])
        for child in header_frame.winfo_children():
            if isinstance(child, Label):
                child.configure(bg=THEME_COLOR["primary"], fg=THEME_COLOR["text_light"])
            elif isinstance(child, Frame):
                child.configure(bg=THEME_COLOR["primary"])

        # Update the cat image background in the header
        if hasattr(self, 'header_cat'):
            self.header_cat.update_background(THEME_COLOR["primary"])

        # Update the date frame
        date_frame = self.diary.winfo_children()[1]
        date_frame.configure(bg=THEME_COLOR["secondary"])
        for child in date_frame.winfo_children():
            if isinstance(child, Label):
                child.configure(bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"])

        # Update the button frame
        button_frame = self.diary.winfo_children()[2]
        button_frame.configure(bg=THEME_COLOR["accent"])
        for child in button_frame.winfo_children():
            if isinstance(child, RoundedButton):
                child.configure(bg=THEME_COLOR["button"], fg=THEME_COLOR["text_light"],
                               activebackground=THEME_COLOR["primary"], activeforeground=THEME_COLOR["text_light"])

        # Update the entries
        self.display_entries()

        # Update the login window cat background if the login window is still open
        if hasattr(self, 'login_cat'):
            self.login_cat.update_background(THEME_COLOR["secondary"])

        # Update the new entry window cat background if it's open
        if hasattr(self, 'entry_cat'):
            self.entry_cat.update_background(THEME_COLOR["secondary"])

        # Update the view entry window cat background if it's open
        if hasattr(self, 'view_cat'):
            self.view_cat.update_background(THEME_COLOR["accent"])

    def handle_entry_action(self, action, entry_id):
        if action == "view":
            self.view_entry(entry_id)
        elif action == "delete":
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
                conn = sqlite3.connect("data/diary.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM diary_entries WHERE id = ?", (entry_id,))
                conn.commit()
                conn.close()
                self.display_entries()  # Refresh the display

    def view_entry(self, entry_id):
        conn = sqlite3.connect("data/diary.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, date, mood, font_family, font_size FROM diary_entries WHERE id = ?", (entry_id,))
        entry = cursor.fetchone()
        conn.close()

        if not entry:
            messagebox.showerror("Error", "Entry not found!")
            return

        title, content, date, mood, font_family, font_size = entry
        font_family = font_family or "Comic Sans MS"
        font_size = font_size or 12

        # Create a new window to view the entry
        view_window = Toplevel(self.diary)
        view_window.title(f"Diary: {title}")
        view_window.geometry("550x500")  # Increased height for cat
        view_window.configure(bg=THEME_COLOR["accent"])

        # Add cat based on mood
        cat_frame = Frame(view_window, bg=THEME_COLOR["accent"])
        cat_frame.pack(fill=X, pady=5)

        cat_index = 0  # Default to happy cat
        if mood:
            if "Sad" in mood or "Angry" in mood:
                cat_index = 2  # Sad/hungry cat
            elif "Neutral" in mood or "Thoughtful" in mood:
                cat_index = 1  # Neutral cat

        self.view_cat = self.load_animated_cat(cat_frame, cat_index)
        self.view_cat.pack()

        # Header with title and date
        header = Frame(view_window, bg=THEME_COLOR["primary"], padx=10, pady=10)
        header.pack(fill=X)

        Label(header, text=title, font=("Comic Sans MS", 16, "bold"), 
              bg=THEME_COLOR["primary"], fg=THEME_COLOR["text_light"]).pack(anchor=W)

        mood_text = f"Mood: {mood}" if mood else ""
        date_mood = Frame(header, bg=THEME_COLOR["primary"])
        date_mood.pack(fill=X)

        Label(date_mood, text=date, font=("Comic Sans MS", 10), 
              bg=THEME_COLOR["primary"], fg=THEME_COLOR["text_light"]).pack(side=LEFT)

        if mood:
            Label(date_mood, text=mood_text, font=("Comic Sans MS", 10), 
                  bg=THEME_COLOR["primary"], fg=THEME_COLOR["text_light"]).pack(side=RIGHT)

        # Content area
        content_frame = Frame(view_window, bg=THEME_COLOR["accent"], padx=15, pady=15)
        content_frame.pack(fill=BOTH, expand=True)

        # Use a Text widget with disabled state to show formatted content
        content_display = Text(content_frame, wrap=WORD, font=(font_family, font_size),
                              bg=THEME_COLOR["accent"], fg=THEME_COLOR["text_dark"],
                              bd=0, padx=5, pady=5)
        content_display.insert(END, content)
        content_display.config(state=DISABLED)  # Make it read-only
        content_display.pack(fill=BOTH, expand=True)

        # Close button
        close_btn = RoundedButton(view_window, text="Close", font=("Comic Sans MS", 10),
                                 command=view_window.destroy)
        close_btn.pack(pady=10)

        # Handler for window close
        def on_window_close():
            self.view_cat.stop_animation()
            view_window.destroy()

        view_window.protocol("WM_DELETE_WINDOW", on_window_close)

    def display_entries(self):
        # Clear existing entries
        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        # Get entries from database
        conn = sqlite3.connect("data/diary.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, date FROM diary_entries ORDER BY id DESC")
        entries = cursor.fetchall()
        conn.close()

        if not entries:
            empty_frame = Frame(self.entries_frame, bg=THEME_COLOR["accent"])
            empty_frame.pack(pady=30)

            # Add an animated cat for empty diary
            self.empty_cat = self.load_animated_cat(empty_frame, 1)  # Neutral cat
            self.empty_cat.pack()

            empty_label = Label(empty_frame, text="Your diary is empty. Write your first entry!",
                               font=("Comic Sans MS", 12), bg=THEME_COLOR["accent"], 
                               fg=THEME_COLOR["text_dark"])
            empty_label.pack(pady=10)
            return

        # Display each entry as a card
        for entry_id, title, date in entries:
            entry_card = DiaryEntryCard(self.entries_frame, title, date, entry_id, 
                                       callback=self.handle_entry_action, width=600)
            entry_card.pack(fill=X, pady=5, padx=5)

    def open_new_entry(self):
        entry_window = Toplevel(self.diary)
        entry_window.title("New Diary Entry")
        entry_window.geometry("600x550")  # Increased height for cat
        entry_window.configure(bg=THEME_COLOR["secondary"])

        # Add default cat at the top
        cat_frame = Frame(entry_window, bg=THEME_COLOR["secondary"])
        cat_frame.pack(fill=X, pady=5)

        self.entry_cat = self.load_animated_cat(cat_frame, 0)  # Start with happy cat
        self.entry_cat.pack()

        # Button frame (now moved to top for better visibility)
        button_frame = Frame(entry_window, bg=THEME_COLOR["secondary"], padx=15, pady=10)
        button_frame.pack(fill=X)

        def save_entry():
            title = title_entry.get().strip()
            content = text_area.get("1.0", END).strip()
            selected_mood = mood_var.get()
            selected_font = font_family.get()
            selected_size = font_size.get()

            if not title or not content:
                messagebox.showwarning("Warning", "Title and content cannot be empty!")
                return

            date = datetime.now().strftime("%d %B %Y, %H:%M")

            conn = sqlite3.connect("data/diary.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO diary_entries (title, content, date, mood, font_family, font_size) VALUES (?, ?, ?, ?, ?, ?)",
                (title, content, date, selected_mood, selected_font, selected_size)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Saved", "Diary entry saved! 💖")
            self.entry_cat.stop_animation()
            entry_window.destroy()
            self.display_entries()  # Refresh the entries

        save_btn = RoundedButton(button_frame, text="💾 Save Entry", font=("Comic Sans MS", 10, "bold"),
                                command=save_entry)
        save_btn.pack(side=LEFT, padx=0, pady=0)

        # Title section
        title_frame = Frame(entry_window, bg=THEME_COLOR["secondary"], padx=15, pady=10)
        title_frame.pack(fill=X)

        Label(title_frame, text="Title:", font=("Comic Sans MS", 12, "bold"), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(anchor=W)

        title_entry = Entry(title_frame, font=("Comic Sans MS", 12), bd=0, width=50)
        title_entry.pack(fill=X, ipady=5, pady=5)

        # Mood selection with cat image update
        mood_frame = Frame(entry_window, bg=THEME_COLOR["secondary"], padx=15, pady=5)
        mood_frame.pack(fill=X)

        Label(mood_frame, text="How are you feeling today?", font=("Comic Sans MS", 10), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(side=LEFT)

        moods = ["😊 Happy", "😐 Neutral", "😢 Sad", "😡 Angry", "🤔 Thoughtful", "🥰 Loved"]
        mood_var = StringVar()
        mood_dropdown = ttk.Combobox(mood_frame, textvariable=mood_var, values=moods, 
                                    width=15, font=("Comic Sans MS", 10))
        mood_dropdown.pack(side=LEFT, padx=10)

        # Update cat based on mood
        self.current_cat_frame = cat_frame

        def update_cat_mood(*args):
            mood = mood_var.get()

            # Remove old cat animation
            self.entry_cat.stop_animation()
            self.entry_cat.label.pack_forget()

            # Choose cat image based on mood
            if "Happy" in mood or "Loved" in mood:
                self.entry_cat = self.load_animated_cat(cat_frame, 0)  # Happy cat
            elif "Sad" in mood or "Angry" in mood:
                self.entry_cat = self.load_animated_cat(cat_frame, 2)  # Sad cat
            else:
                self.entry_cat = self.load_animated_cat(cat_frame, 1)  # Neutral cat

            self.entry_cat.pack()

        mood_var.trace("w", update_cat_mood)

        # Font selection
        font_frame = Frame(entry_window, bg=THEME_COLOR["secondary"], padx=15, pady=5)
        font_frame.pack(fill=X)

        Label(font_frame, text="Font:", font=("Comic Sans MS", 10), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(side=LEFT)

        fonts = ["Comic Sans MS", "Arial", "Verdana", "Georgia", "Courier New"]
        font_family = StringVar(value="Comic Sans MS")
        font_dropdown = ttk.Combobox(font_frame, textvariable=font_family, values=fonts, 
                                    width=15, font=("Comic Sans MS", 10))
        font_dropdown.pack(side=LEFT, padx=10)

        Label(font_frame, text="Size:", font=("Comic Sans MS", 10), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(side=LEFT)

        font_sizes = [10, 12, 14, 16, 18]
        font_size = IntVar(value=12)
        size_dropdown = ttk.Combobox(font_frame, textvariable=font_size, 
                                     values=font_sizes, width=5, font=("Comic Sans MS", 10))
        size_dropdown.pack(side=LEFT, padx=10)

        # Apply font button
        def update_font():
            text_area.configure(font=(font_family.get(), font_size.get()))

        font_btn = Button(font_frame, text="Apply Font", font=("Comic Sans MS", 8),
                         bg=THEME_COLOR["button"], fg=THEME_COLOR["text_light"],
                         command=update_font, relief=FLAT)
        font_btn.pack(side=LEFT, padx=10)

        # Content area
        content_frame = Frame(entry_window, bg=THEME_COLOR["secondary"], padx=15, pady=10)
        content_frame.pack(fill=BOTH, expand=True)

        Label(content_frame, text="Write your thoughts:", font=("Comic Sans MS", 12, "bold"), 
             bg=THEME_COLOR["secondary"], fg=THEME_COLOR["text_dark"]).pack(anchor=W)

        text_area = Text(content_frame, wrap=WORD, font=(font_family.get(), font_size.get()),
                        bg="white", fg=THEME_COLOR["text_dark"], padx=10, pady=10)
        text_area.pack(fill=BOTH, expand=True, pady=10)

        # Handler for window close
        def on_window_close():
            self.entry_cat.stop_animation()
            entry_window.destroy()

        entry_window.protocol("WM_DELETE_WINDOW", on_window_close)

# Run the application
if __name__ == "__main__":
    app = DiaryApp()