import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime, timedelta
import csv
import threading
import time
import random

class UltimateHabitTrackerProMax:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker Pro Max")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Extended themes with new color variants
        self.themes = {
            'dark': {
                'bg_primary': '#1a1a1a', 'bg_secondary': '#2d2d2d', 'bg_card': '#333333',
                'accent': '#6366f1', 'accent_hover': '#4f46e5', 'success': '#10b981',
                'warning': '#f59e0b', 'danger': '#ef4444', 'text_primary': '#ffffff',
                'text_secondary': '#a1a1aa', 'border': '#404040'
            },
            'light': {
                'bg_primary': '#ffffff', 'bg_secondary': '#f8fafc', 'bg_card': '#ffffff',
                'accent': '#3b82f6', 'accent_hover': '#2563eb', 'success': '#059669',
                'warning': '#d97706', 'danger': '#dc2626', 'text_primary': '#1f2937',
                'text_secondary': '#6b7280', 'border': '#e5e7eb'
            },
            'forest': {
                'bg_primary': '#0f1419', 'bg_secondary': '#1e2d2f', 'bg_card': '#2d4a4f',
                'accent': '#4ade80', 'accent_hover': '#22c55e', 'success': '#059669',
                'warning': '#eab308', 'danger': '#ef4444', 'text_primary': '#ecfdf5',
                'text_secondary': '#86efac', 'border': '#374151'
            },
            'ocean': {
                'bg_primary': '#0c1826', 'bg_secondary': '#1e3a5f', 'bg_card': '#2d5a87',
                'accent': '#38bdf8', 'accent_hover': '#0ea5e9', 'success': '#06b6d4',
                'warning': '#f59e0b', 'danger': '#ef4444', 'text_primary': '#f0f9ff',
                'text_secondary': '#7dd3fc', 'border': '#475569'
            },
            'sunset': {
                'bg_primary': '#2d1b1b', 'bg_secondary': '#4a2c2a', 'bg_card': '#6b3e3e',
                'accent': '#f97316', 'accent_hover': '#ea580c', 'success': '#84cc16',
                'warning': '#eab308', 'danger': '#dc2626', 'text_primary': '#fef2f2',
                'text_secondary': '#fed7aa', 'border': '#7c2d12'
            },
            'cosmic': {
                'bg_primary': '#0f0f23', 'bg_secondary': '#1a1a2e', 'bg_card': '#16213e',
                'accent': '#9333ea', 'accent_hover': '#7c3aed', 'success': '#22d3ee',
                'warning': '#fbbf24', 'danger': '#f87171', 'text_primary': '#e0e7ff',
                'text_secondary': '#c4b5fd', 'border': '#374151'
            }
        }
        
        self.current_theme = 'dark'
        self.colors = self.themes[self.current_theme]
        
        # Enhanced categories and features
        self.categories = ["Health", "Learning", "Productivity", "Mindfulness", "Social", "Creative", "Finance", "Personal", "Other"]
        self.difficulty_levels = {"Easy": 1, "Medium": 3, "Hard": 5, "Expert": 8}
        self.habit_types = ["Daily", "Weekly", "Quantity", "Time-based"]
        self.moods = ["😢 Terrible", "😕 Bad", "😐 Okay", "😊 Good", "😄 Great"]
        
        # Comprehensive achievement system
        self.all_achievements = {
            "first_step": {"name": "First Step", "desc": "Complete your first habit", "icon": "👶", "progress_func": self.get_total_completions, "target": 1},
            "week_warrior": {"name": "Week Warrior", "desc": "Maintain a 7-day streak", "icon": "🔥", "progress_func": self.get_max_current_streak, "target": 7},
            "month_master": {"name": "Month Master", "desc": "Maintain a 30-day streak", "icon": "👑", "progress_func": self.get_max_current_streak, "target": 30},
            "century_club": {"name": "Century Club", "desc": "Maintain a 100-day streak", "icon": "💎", "progress_func": self.get_max_current_streak, "target": 100},
            "habit_starter": {"name": "Habit Starter", "desc": "Track 3 different habits", "icon": "🌱", "progress_func": lambda: len(self.habits), "target": 3},
            "habit_collector": {"name": "Habit Collector", "desc": "Track 10 different habits", "icon": "📚", "progress_func": lambda: len(self.habits), "target": 10},
            "habit_master": {"name": "Habit Master", "desc": "Track 25 different habits", "icon": "🎓", "progress_func": lambda: len(self.habits), "target": 25},
            "points_100": {"name": "Century Points", "desc": "Earn 100 points", "icon": "🥉", "progress_func": lambda: self.settings.get('total_points', 0), "target": 100},
            "points_500": {"name": "Point Champion", "desc": "Earn 500 points", "icon": "🥈", "progress_func": lambda: self.settings.get('total_points', 0), "target": 500},
            "points_1000": {"name": "Point Legend", "desc": "Earn 1000 points", "icon": "🥇", "progress_func": lambda: self.settings.get('total_points', 0), "target": 1000},
            "points_5000": {"name": "Point Master", "desc": "Earn 5000 points", "icon": "🏆", "progress_func": lambda: self.settings.get('total_points', 0), "target": 5000},
            "perfect_week": {"name": "Perfect Week", "desc": "Complete all habits for 7 days", "icon": "⭐", "progress_func": self.get_perfect_days_streak, "target": 7},
            "perfect_month": {"name": "Perfect Month", "desc": "Complete all habits for 30 days", "icon": "🌟", "progress_func": self.get_perfect_days_streak, "target": 30},
            "health_focused": {"name": "Health Champion", "desc": "Complete 50 health habits", "icon": "💪", "progress_func": lambda: self.get_category_completions("Health"), "target": 50},
            "learning_lover": {"name": "Learning Lover", "desc": "Complete 50 learning habits", "icon": "📖", "progress_func": lambda: self.get_category_completions("Learning"), "target": 50},
            "productivity_pro": {"name": "Productivity Pro", "desc": "Complete 50 productivity habits", "icon": "⚡", "progress_func": lambda: self.get_category_completions("Productivity"), "target": 50},
            "early_bird": {"name": "Early Bird", "desc": "Complete habits before 8 AM (10 times)", "icon": "🌅", "progress_func": self.get_early_completions, "target": 10},
            "night_owl": {"name": "Night Owl", "desc": "Complete habits after 10 PM (10 times)", "icon": "🦉", "progress_func": self.get_late_completions, "target": 10},
            "combo_master": {"name": "Combo Master", "desc": "Complete 5 habits in one day", "icon": "🎯", "progress_func": self.get_max_daily_completions, "target": 5},
            "social_butterfly": {"name": "Social Butterfly", "desc": "Share 5 achievements", "icon": "🦋", "progress_func": lambda: self.settings.get('shares_count', 0), "target": 5},
        }
        
        self.data_file = "habits_pro_max.json"
        self.settings_file = "settings_max.json"
        self.habits = self.load_data()
        self.settings = self.load_settings()
        self.selected_habit = tk.StringVar()
        self.current_view = "dashboard"
        self.pet_level = self.settings.get('pet_level', 1)
        self.pet_happiness = self.settings.get('pet_happiness', 50)
        
        # Keyboard bindings
        self.root.bind('<Key>', self.handle_keypress)
        self.root.focus_set()
        
        self.setup_ui()
        self.refresh_all_views()
        self.start_reminder_system()
        self.update_pet_status()
    
    def handle_keypress(self, event):
        if event.keysym == 'space':
            self.quick_toggle_habit()
        elif event.state == 4:  # Ctrl key
            if event.keysym == 'n':
                self.focus_add_habit()
            elif event.keysym == 's':
                self.export_data()
            elif event.keysym == 'a':
                self.show_view("achievements")
            elif event.keysym == 't':
                self.cycle_theme()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for habit_name, habit_data in data.items():
                        if isinstance(habit_data, list):
                            data[habit_name] = {
                                'completions': habit_data,
                                'category': 'Other',
                                'difficulty': 'Medium',
                                'daily_goal': 1,
                                'notes': {},
                                'reminders': [],
                                'created_date': datetime.now().isoformat(),
                                'habit_type': 'Daily',
                                'dependencies': [],
                                'completion_times': {},
                                'mood_ratings': {},
                                'photos': {}
                            }
                        else:
                            habit_data.setdefault('habit_type', 'Daily')
                            habit_data.setdefault('dependencies', [])
                            habit_data.setdefault('completion_times', {})
                            habit_data.setdefault('mood_ratings', {})
                            habit_data.setdefault('photos', {})
                    return data
            except:
                return {}
        return {}
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    settings.setdefault('achieved', [])
                    settings.setdefault('pet_level', 1)
                    settings.setdefault('pet_happiness', 50)
                    settings.setdefault('current_challenge', None)
                    settings.setdefault('challenge_progress', 0)
                    settings.setdefault('shares_count', 0)
                    settings.setdefault('mood_history', {})
                    settings.setdefault('buddy_code', self.generate_buddy_code())
                    settings.setdefault('early_completions', 0)
                    settings.setdefault('late_completions', 0)
                    return settings
            except:
                return {}
        return {
            'theme': 'dark',
            'sound_enabled': True,
            'achievements': [],
            'achieved': [],
            'total_points': 0,
            'pet_level': 1,
            'pet_happiness': 50,
            'current_challenge': None,
            'challenge_progress': 0,
            'shares_count': 0,
            'mood_history': {},
            'buddy_code': self.generate_buddy_code(),
            'early_completions': 0,
            'late_completions': 0
        }
    
    def generate_buddy_code(self):
        import hashlib
        unique_string = f"{time.time()}_{random.randint(1000, 9999)}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:8].upper()
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.habits, f, indent=2)
    
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def setup_ui(self):
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill='both', expand=True)
        
        self.create_navigation()
        
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.create_dashboard_view()
        self.create_analytics_view()
        self.create_achievements_view()
        self.create_social_view()
        self.create_settings_view()
        
        self.show_view("dashboard")
    
    def create_navigation(self):
        nav_frame = tk.Frame(self.main_container, bg=self.colors['bg_secondary'], height=70)
        nav_frame.pack(fill='x', padx=20, pady=(20, 0))
        nav_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(nav_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side='left', fill='y')
        
        tk.Label(title_frame, text="🎯 Habit Tracker Pro Max", 
                font=('Segoe UI', 18, 'bold'), 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(pady=15)
        
        # Virtual pet
        pet_frame = tk.Frame(nav_frame, bg=self.colors['bg_secondary'])
        pet_frame.pack(side='left', padx=20, fill='y')
        
        pet_emoji = self.get_pet_emoji()
        self.pet_label = tk.Label(pet_frame, text=f"{pet_emoji} Lv.{self.pet_level}", 
                                 font=('Segoe UI', 14, 'bold'), 
                                 bg=self.colors['bg_secondary'], fg=self.colors['accent'])
        self.pet_label.pack(pady=10)
        
        happiness_bar = tk.Frame(pet_frame, bg=self.colors['border'], width=100, height=6)
        happiness_bar.pack()
        happiness_fill = tk.Frame(happiness_bar, bg=self.colors['success'], height=6)
        happiness_fill.place(x=0, y=0, width=self.pet_happiness, height=6)
        
        # Navigation buttons
        nav_buttons = tk.Frame(nav_frame, bg=self.colors['bg_secondary'])
        nav_buttons.pack(side='right', fill='y')
        
        self.nav_dashboard = self.create_nav_button(nav_buttons, "📊 Dashboard", "dashboard")
        self.nav_analytics = self.create_nav_button(nav_buttons, "📈 Analytics", "analytics")
        self.nav_achievements = self.create_nav_button(nav_buttons, "🏆 Achievements", "achievements")
        self.nav_social = self.create_nav_button(nav_buttons, "👥 Social", "social")
        self.nav_settings = self.create_nav_button(nav_buttons, "⚙️ Settings", "settings")
        
        # Stats display
        stats_frame = tk.Frame(nav_buttons, bg=self.colors['bg_secondary'])
        stats_frame.pack(side='right', padx=10, pady=10)
        
        self.points_label = tk.Label(stats_frame, text=f"🏆 {self.settings.get('total_points', 0)} pts", 
                                    font=('Segoe UI', 11, 'bold'), 
                                    bg=self.colors['bg_secondary'], fg=self.colors['warning'])
        self.points_label.pack()
        
        max_streak = self.get_max_current_streak()
        self.streak_label = tk.Label(stats_frame, text=f"🔥 {max_streak} days", 
                                    font=('Segoe UI', 11, 'bold'), 
                                    bg=self.colors['bg_secondary'], fg=self.colors['danger'])
        self.streak_label.pack()
    
    def get_pet_emoji(self):
        base_pets = ["🐱", "🐶", "🐰", "🐸", "🐯", "🦁", "🐵", "🐼"]
        if self.pet_happiness > 80:
            return "😊" + base_pets[min(self.pet_level // 5, 7)]
        elif self.pet_happiness > 50:
            return "😐" + base_pets[min(self.pet_level // 5, 7)]
        else:
            return "😔" + base_pets[min(self.pet_level // 5, 7)]
    
    def create_nav_button(self, parent, text, view_name):
        btn = tk.Button(parent, text=text, 
                       command=lambda: self.show_view(view_name),
                       bg=self.colors['accent'] if self.current_view == view_name else self.colors['bg_card'],
                       fg=self.colors['text_primary'], font=('Segoe UI', 9, 'bold'),
                       border=0, cursor='hand2', relief='flat')
        btn.pack(side='right', padx=3, pady=10, ipadx=8)
        return btn
    
    def create_dashboard_view(self):
        self.dashboard_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        
        # Top row
        top_row = tk.Frame(self.dashboard_frame, bg=self.colors['bg_primary'])
        top_row.pack(fill='x', pady=(0, 10))
        
        # Challenge card
        challenge_card = tk.Frame(top_row, bg=self.colors['bg_card'], width=350)
        challenge_card.pack(side='left', fill='y', padx=(0, 10))
        challenge_card.pack_propagate(False)
        
        tk.Label(challenge_card, text="🎯 Daily Challenge", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        self.challenge_label = tk.Label(challenge_card, text="Complete 3 habits today!", 
                                       font=('Segoe UI', 10), 
                                       bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        self.challenge_label.pack(pady=(0, 10))
        
        # Mood tracker
        mood_card = tk.Frame(top_row, bg=self.colors['bg_card'])
        mood_card.pack(side='left', fill='both', expand=True)
        
        tk.Label(mood_card, text="😊 Today's Mood", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        mood_frame = tk.Frame(mood_card, bg=self.colors['bg_card'])
        mood_frame.pack(pady=(0, 10))
        
        for i, mood in enumerate(["😢", "😕", "😐", "😊", "😄"]):
            btn = tk.Button(mood_frame, text=mood, font=('Segoe UI', 14),
                           command=lambda m=i+1: self.set_mood(m),
                           bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                           border=0, cursor='hand2', width=2)
            btn.pack(side='left', padx=2)
        
        # Main content
        main_content = tk.Frame(self.dashboard_frame, bg=self.colors['bg_primary'])
        main_content.pack(fill='both', expand=True)
        
        # Left panel
        left_panel = tk.Frame(main_content, bg=self.colors['bg_secondary'], width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Add habit card
        add_card = tk.Frame(left_panel, bg=self.colors['bg_card'])
        add_card.pack(fill='x', padx=15, pady=15)
        
        tk.Label(add_card, text="Add New Habit", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(15, 10))
        
        self.habit_entry = tk.Entry(add_card, font=('Segoe UI', 11), 
                                   bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                                   insertbackground=self.colors['text_primary'], border=0, width=35)
        self.habit_entry.pack(pady=5, ipady=8)
        self.habit_entry.bind('<Return>', lambda e: self.add_habit())
        
        # Category and Type
        cat_type_frame = tk.Frame(add_card, bg=self.colors['bg_card'])
        cat_type_frame.pack(fill='x', padx=15, pady=2)
        
        cat_frame = tk.Frame(cat_type_frame, bg=self.colors['bg_card'])
        cat_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        tk.Label(cat_frame, text="Category:", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w')
        self.category_var = tk.StringVar(value="Other")
        category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var, 
                                     values=self.categories, state='readonly', width=12)
        category_combo.pack(fill='x')
        
        type_frame = tk.Frame(cat_type_frame, bg=self.colors['bg_card'])
        type_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        tk.Label(type_frame, text="Type:", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w')
        self.type_var = tk.StringVar(value="Daily")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                 values=self.habit_types, state='readonly', width=12)
        type_combo.pack(fill='x')
        
        # Difficulty and Goal
        diff_goal_frame = tk.Frame(add_card, bg=self.colors['bg_card'])
        diff_goal_frame.pack(fill='x', padx=15, pady=2)
        
        diff_frame = tk.Frame(diff_goal_frame, bg=self.colors['bg_card'])
        diff_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        tk.Label(diff_frame, text="Difficulty:", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w')
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_combo = ttk.Combobox(diff_frame, textvariable=self.difficulty_var, 
                                       values=list(self.difficulty_levels.keys()), state='readonly', width=12)
        difficulty_combo.pack(fill='x')
        
        goal_frame = tk.Frame(diff_goal_frame, bg=self.colors['bg_card'])
        goal_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        tk.Label(goal_frame, text="Daily Goal:", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w')
        self.goal_var = tk.StringVar(value="1")
        goal_entry = tk.Entry(goal_frame, textvariable=self.goal_var, font=('Segoe UI', 9), 
                             bg=self.colors['bg_primary'], fg=self.colors['text_primary'], width=12)
        goal_entry.pack(fill='x')
        
        add_btn = self.create_modern_button(add_card, "Add Habit", 
                                          self.add_habit, self.colors['accent'], width=30)
        add_btn.pack(pady=(10, 15))
        
        # Smart suggestions
        suggestions_card = tk.Frame(left_panel, bg=self.colors['bg_card'])
        suggestions_card.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(suggestions_card, text="🧠 Smart Suggestions", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        self.suggestions_label = tk.Label(suggestions_card, text="Add more habits to see suggestions!", 
                                         font=('Segoe UI', 9), 
                                         bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                                         wraplength=300)
        self.suggestions_label.pack(pady=(0, 10), padx=10)
        
        # Quick actions
        actions_card = tk.Frame(left_panel, bg=self.colors['bg_card'])
        actions_card.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(actions_card, text="Quick Actions", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        actions_grid = tk.Frame(actions_card, bg=self.colors['bg_card'])
        actions_grid.pack(pady=(0, 10))
        
        row1 = tk.Frame(actions_grid, bg=self.colors['bg_card'])
        row1.pack(fill='x', pady=2)
        self.create_modern_button(row1, "✓ Complete", self.log_habit_today, self.colors['success'], width=15).pack(side='left', padx=2)
        self.create_modern_button(row1, "✗ Remove", self.remove_habit_today, self.colors['danger'], width=15).pack(side='left', padx=2)
        
        row2 = tk.Frame(actions_grid, bg=self.colors['bg_card'])
        row2.pack(fill='x', pady=2)
        self.create_modern_button(row2, "📝 Note", self.add_habit_note, self.colors['accent'], width=15).pack(side='left', padx=2)
        self.create_modern_button(row2, "📸 Photo", self.add_habit_photo, self.colors['accent'], width=15).pack(side='left', padx=2)
        
        row3 = tk.Frame(actions_grid, bg=self.colors['bg_card'])
        row3.pack(fill='x', pady=2)
        self.create_modern_button(row3, "📅 Calendar", self.show_calendar, self.colors['accent'], width=15).pack(side='left', padx=2)
        self.create_modern_button(row3, "⏰ Reminder", self.set_reminder, self.colors['warning'], width=15).pack(side='left', padx=2)
        
        row4 = tk.Frame(actions_grid, bg=self.colors['bg_card'])
        row4.pack(fill='x', pady=2)
        self.create_modern_button(row4, "🔗 Dependency", self.set_dependency, self.colors['warning'], width=15).pack(side='left', padx=2)
        self.create_modern_button(row4, "🗑 Delete", self.delete_habit, self.colors['danger'], width=15).pack(side='left', padx=2)
        
        # Shortcuts info
        shortcuts_card = tk.Frame(left_panel, bg=self.colors['bg_card'])
        shortcuts_card.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(shortcuts_card, text="⌨️ Keyboard Shortcuts", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(8, 3))
        
        shortcuts_text = """Space: Toggle habit • Ctrl+N: New habit
Ctrl+S: Export • Ctrl+A: Achievements • Ctrl+T: Theme"""
        
        tk.Label(shortcuts_card, text=shortcuts_text, font=('Segoe UI', 8), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                justify='left').pack(pady=(0, 8), padx=8)
        
        # Right panel
        right_panel = tk.Frame(main_content, bg=self.colors['bg_secondary'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Filter controls
        filter_frame = tk.Frame(right_panel, bg=self.colors['bg_secondary'])
        filter_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        tk.Label(filter_frame, text="Filter:", font=('Segoe UI', 10), 
                bg=self.colors['bg_secondary'], fg=self.colors['text_secondary']).pack(side='left')
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All"] + self.categories, state='readonly', width=12)
        filter_combo.pack(side='left', padx=10)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_habit_list())
        
        self.view_mode = tk.StringVar(value="Cards")
        view_toggle = ttk.Combobox(filter_frame, textvariable=self.view_mode, 
                                  values=["Cards", "List", "Grid"], state='readonly', width=8)
        view_toggle.pack(side='left', padx=10)
        view_toggle.bind('<<ComboboxSelected>>', lambda e: self.refresh_habit_list())
        
        # Today's overview
        today_card = tk.Frame(right_panel, bg=self.colors['bg_card'])
        today_card.pack(fill='x', padx=15, pady=(5, 10))
        
        tk.Label(today_card, text="Today's Progress", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        self.create_mini_contribution_graph(today_card)
        
        self.today_progress_label = tk.Label(today_card, text="", font=('Segoe UI', 10), 
                                           bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        self.today_progress_label.pack(pady=(5, 10))
        
        # Habits list
        habits_card = tk.Frame(right_panel, bg=self.colors['bg_card'])
        habits_card.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        habits_header = tk.Frame(habits_card, bg=self.colors['bg_card'])
        habits_header.pack(fill='x', padx=15, pady=(15, 5))
        
        tk.Label(habits_header, text="Your Habits", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(side='left')
        
        self.habit_stats_label = tk.Label(habits_header, text="", font=('Segoe UI', 10), 
                                         bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        self.habit_stats_label.pack(side='right')
        
        # Scrollable habits list
        self.create_scrollable_habits_list(habits_card)
        
        # Selected habit stats
        self.stats_card = tk.Frame(right_panel, bg=self.colors['bg_card'], height=200)
        self.stats_card.pack(fill='x', padx=15, pady=(0, 15))
        self.stats_card.pack_propagate(False)
        
        tk.Label(self.stats_card, text="📊 Habit Analysis", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        self.stats_label = tk.Label(self.stats_card, text="Select a habit to view detailed analysis", 
                                   font=('Segoe UI', 10), justify='left',
                                   bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        self.stats_label.pack(padx=15, pady=(0, 10), anchor='w')
    
    def create_analytics_view(self):
        self.analytics_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        
        # Top metrics row
        metrics_row = tk.Frame(self.analytics_frame, bg=self.colors['bg_primary'])
        metrics_row.pack(fill='x', pady=(0, 20))
        
        # Overall stats card
        overall_card = tk.Frame(metrics_row, bg=self.colors['bg_card'], width=300)
        overall_card.pack(side='left', fill='y', padx=(0, 10))
        overall_card.pack_propagate(False)
        
        tk.Label(overall_card, text="📊 Overall Statistics", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.overall_stats_label = tk.Label(overall_card, text="", font=('Segoe UI', 10), 
                                          bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                                          justify='left')
        self.overall_stats_label.pack(padx=15, pady=(0, 15), anchor='w')
        
        # Predictions card
        predictions_card = tk.Frame(metrics_row, bg=self.colors['bg_card'], width=300)
        predictions_card.pack(side='left', fill='y', padx=10)
        predictions_card.pack_propagate(False)
        
        tk.Label(predictions_card, text="🔮 AI Predictions", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.predictions_label = tk.Label(predictions_card, text="", font=('Segoe UI', 9), 
                                         bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                                         justify='left', wraplength=250)
        self.predictions_label.pack(padx=15, pady=(0, 15), anchor='w')
        
        # Weather correlation card
        weather_card = tk.Frame(metrics_row, bg=self.colors['bg_card'])
        weather_card.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(weather_card, text="🌤️ Weather Impact", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.weather_stats_label = tk.Label(weather_card, text="", font=('Segoe UI', 10), 
                                           bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                                           justify='left')
        self.weather_stats_label.pack(padx=15, pady=(0, 15), anchor='w')
        
        # Contribution graph
        contrib_card = tk.Frame(self.analytics_frame, bg=self.colors['bg_card'])
        contrib_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(contrib_card, text="📈 Contribution Graph (Last 12 weeks)", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.create_contribution_graph(contrib_card)
        
        # Details row
        details_row = tk.Frame(self.analytics_frame, bg=self.colors['bg_primary'])
        details_row.pack(fill='both', expand=True)
        
        # Category breakdown
        left_analytics = tk.Frame(details_row, bg=self.colors['bg_card'], width=400)
        left_analytics.pack(side='left', fill='y', padx=(0, 10))
        left_analytics.pack_propagate(False)
        
        tk.Label(left_analytics, text="📁 Category Performance", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.category_stats_label = tk.Label(left_analytics, text="", font=('Segoe UI', 10), 
                                           bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                                           justify='left')
        self.category_stats_label.pack(padx=15, pady=(0, 15), anchor='w')
        
        # Insights
        right_analytics = tk.Frame(details_row, bg=self.colors['bg_card'])
        right_analytics.pack(side='right', fill='both', expand=True)
        
        tk.Label(right_analytics, text="🧠 Smart Insights & Correlations", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.insights_label = tk.Label(right_analytics, text="", font=('Segoe UI', 10), 
                                      bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                                      justify='left', wraplength=500)
        self.insights_label.pack(padx=15, pady=(0, 15), anchor='w')
    
    def create_achievements_view(self):
        self.achievements_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        
        # Header
        header_frame = tk.Frame(self.achievements_frame, bg=self.colors['bg_card'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="🏆 Achievement Center", 
                font=('Segoe UI', 18, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        # Achievement statistics
        achieved_count = len(self.settings.get('achieved', []))
        total_count = len(self.all_achievements)
        completion_percentage = (achieved_count / total_count) * 100 if total_count > 0 else 0
        
        stats_text = f"Progress: {achieved_count}/{total_count} achievements ({completion_percentage:.1f}%)"
        tk.Label(header_frame, text=stats_text, 
                font=('Segoe UI', 12), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=(0, 15))
        
        # Progress bar
        progress_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        progress_frame.pack(pady=(0, 15))
        
        progress_bg = tk.Frame(progress_frame, bg=self.colors['border'], width=400, height=10)
        progress_bg.pack()
        
        if completion_percentage > 0:
            progress_fill_width = int(400 * (completion_percentage / 100))
            progress_fill = tk.Frame(progress_bg, bg=self.colors['success'], height=10)
            progress_fill.place(x=0, y=0, width=progress_fill_width, height=10)
        
        # Filter buttons
        categories_frame = tk.Frame(self.achievements_frame, bg=self.colors['bg_primary'])
        categories_frame.pack(fill='x', pady=(0, 20))
        
        filter_frame = tk.Frame(categories_frame, bg=self.colors['bg_primary'])
        filter_frame.pack()
        
        self.achievement_filter = tk.StringVar(value="All")
        filter_options = ["All", "Achieved", "In Progress", "Locked"]
        
        self.filter_buttons = {}
        for option in filter_options:
            btn = tk.Button(filter_frame, text=option,
                           command=lambda o=option: self.filter_achievements(o),
                           bg=self.colors['accent'] if option == "All" else self.colors['bg_card'],
                           fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold'),
                           border=0, cursor='hand2', relief='flat')
            btn.pack(side='left', padx=5, ipadx=10, ipady=5)
            self.filter_buttons[option] = btn
        
        # Scrollable achievements list
        achievements_container = tk.Frame(self.achievements_frame, bg=self.colors['bg_primary'])
        achievements_container.pack(fill='both', expand=True)
        
        self.achievements_canvas = tk.Canvas(achievements_container, bg=self.colors['bg_primary'], 
                                           highlightthickness=0, border=0)
        achievements_scrollbar = ttk.Scrollbar(achievements_container, orient="vertical", 
                                             command=self.achievements_canvas.yview)
        self.achievements_scrollable_frame = tk.Frame(self.achievements_canvas, bg=self.colors['bg_primary'])
        
        self.achievements_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.achievements_canvas.configure(scrollregion=self.achievements_canvas.bbox("all"))
        )
        
        self.achievements_canvas.create_window((0, 0), window=self.achievements_scrollable_frame, anchor="nw")
        self.achievements_canvas.configure(yscrollcommand=achievements_scrollbar.set)
        
        self.achievements_canvas.pack(side="left", fill="both", expand=True)
        achievements_scrollbar.pack(side="right", fill="y")
        
        self.refresh_achievements_display()
    
    def create_social_view(self):
        self.social_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        
        # Header
        header_frame = tk.Frame(self.social_frame, bg=self.colors['bg_card'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="👥 Social Hub", 
                font=('Segoe UI', 18, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        # Buddy code
        buddy_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        buddy_frame.pack(pady=(0, 15))
        
        tk.Label(buddy_frame, text=f"Your Buddy Code: {self.settings.get('buddy_code', 'ERROR')}", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['accent']).pack()
        
        tk.Label(buddy_frame, text="Share this code with friends to compare progress!", 
                font=('Segoe UI', 10), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()
        
        # Social features
        social_row = tk.Frame(self.social_frame, bg=self.colors['bg_primary'])
        social_row.pack(fill='x', pady=(0, 20))
        
        # Share achievements
        share_card = tk.Frame(social_row, bg=self.colors['bg_card'], width=300)
        share_card.pack(side='left', fill='y', padx=(0, 10))
        share_card.pack_propagate(False)
        
        tk.Label(share_card, text="📱 Share Progress", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        share_buttons = tk.Frame(share_card, bg=self.colors['bg_card'])
        share_buttons.pack(pady=(0, 15))
        
        self.create_modern_button(share_buttons, "📸 Share Streak", 
                                self.share_streak, self.colors['accent'], width=20).pack(pady=3)
        
        self.create_modern_button(share_buttons, "🏆 Share Achievement", 
                                self.share_achievement, self.colors['success'], width=20).pack(pady=3)
        
        self.create_modern_button(share_buttons, "📊 Share Stats", 
                                self.share_stats, self.colors['warning'], width=20).pack(pady=3)
        
        # Buddy comparison
        buddy_card = tk.Frame(social_row, bg=self.colors['bg_card'])
        buddy_card.pack(side='left', fill='both', expand=True)
        
        tk.Label(buddy_card, text="🤝 Buddy Comparison", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        buddy_input_frame = tk.Frame(buddy_card, bg=self.colors['bg_card'])
        buddy_input_frame.pack(pady=(0, 10))
        
        self.buddy_code_entry = tk.Entry(buddy_input_frame, font=('Segoe UI', 11), 
                                        bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                                        width=20, insertbackground=self.colors['text_primary'])
        self.buddy_code_entry.pack(side='left', padx=(0, 10), ipady=5)
        
        self.create_modern_button(buddy_input_frame, "Compare", 
                                self.compare_with_buddy, self.colors['accent']).pack(side='left')
        
        self.buddy_comparison_label = tk.Label(buddy_card, text="Enter a buddy code to compare progress!", 
                                             font=('Segoe UI', 10), 
                                             bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                                             wraplength=400)
        self.buddy_comparison_label.pack(padx=15, pady=(0, 15))
        
        # Leaderboard
        leaderboard_card = tk.Frame(self.social_frame, bg=self.colors['bg_card'])
        leaderboard_card.pack(fill='both', expand=True)
        
        tk.Label(leaderboard_card, text="🏅 Global Leaderboard (Simulated)", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.create_leaderboard(leaderboard_card)
    
    def create_settings_view(self):
        self.settings_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        
        # Theme selection
        theme_card = tk.Frame(self.settings_frame, bg=self.colors['bg_card'])
        theme_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(theme_card, text="🎨 Theme Selection", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        theme_grid = tk.Frame(theme_card, bg=self.colors['bg_card'])
        theme_grid.pack(pady=(0, 15))
        
        # First row of themes
        theme_row1 = tk.Frame(theme_grid, bg=self.colors['bg_card'])
        theme_row1.pack(pady=5)
        
        for theme_name in ['dark', 'light', 'forest']:
            btn = self.create_modern_button(theme_row1, f"{theme_name.title()}", 
                                          lambda t=theme_name: self.change_theme(t), 
                                          self.colors['accent'] if theme_name == self.current_theme else self.colors['bg_secondary'])
            btn.pack(side='left', padx=5)
        
        # Second row of themes
        theme_row2 = tk.Frame(theme_grid, bg=self.colors['bg_card'])
        theme_row2.pack(pady=5)
        
        for theme_name in ['ocean', 'sunset', 'cosmic']:
            btn = self.create_modern_button(theme_row2, f"{theme_name.title()}", 
                                          lambda t=theme_name: self.change_theme(t), 
                                          self.colors['accent'] if theme_name == self.current_theme else self.colors['bg_secondary'])
            btn.pack(side='left', padx=5)
        
        # Sound settings
        sound_card = tk.Frame(self.settings_frame, bg=self.colors['bg_card'])
        sound_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(sound_card, text="🔊 Sound & Notifications", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        sound_options = tk.Frame(sound_card, bg=self.colors['bg_card'])
        sound_options.pack(pady=(0, 15))
        
        self.sound_var = tk.BooleanVar(value=self.settings.get('sound_enabled', True))
        sound_check = tk.Checkbutton(sound_options, text="Enable completion sounds", 
                                    variable=self.sound_var, font=('Segoe UI', 10),
                                    bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                                    selectcolor=self.colors['bg_secondary'],
                                    command=self.save_sound_setting)
        sound_check.pack(anchor='w', padx=15)
        
        # Data management
        data_card = tk.Frame(self.settings_frame, bg=self.colors['bg_card'])
        data_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(data_card, text="💾 Data Management", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        data_buttons = tk.Frame(data_card, bg=self.colors['bg_card'])
        data_buttons.pack(pady=(0, 15))
        
        self.create_modern_button(data_buttons, "📤 Export Data", 
                                self.export_data, self.colors['accent']).pack(side='left', padx=5)
        
        self.create_modern_button(data_buttons, "📥 Import Data", 
                                self.import_data, self.colors['accent']).pack(side='left', padx=5)
        
        self.create_modern_button(data_buttons, "🔄 Backup to Cloud", 
                                self.backup_to_cloud, self.colors['success']).pack(side='left', padx=5)
        
        self.create_modern_button(data_buttons, "🗑 Reset All Data", 
                                self.reset_all_data, self.colors['danger']).pack(side='left', padx=5)
        
        # Enhanced habit templates
        templates_card = tk.Frame(self.settings_frame, bg=self.colors['bg_card'])
        templates_card.pack(fill='both', expand=True)
        
        tk.Label(templates_card, text="📋 Enhanced Habit Templates", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=15)
        
        self.create_enhanced_habit_templates(templates_card)
    
    def create_enhanced_habit_templates(self, parent):
        templates = [
            ("💪 Morning Workout", "Health", "Medium", 1, "Daily", "Get your blood pumping!"),
            ("📚 Read 30 Minutes", "Learning", "Easy", 1, "Daily", "Feed your mind daily"),
            ("🧘 Meditation", "Mindfulness", "Easy", 1, "Daily", "Find inner peace"),
            ("💧 Drink 8 Glasses Water", "Health", "Easy", 8, "Quantity", "Stay hydrated"),
            ("🌅 Wake Up at 6 AM", "Productivity", "Hard", 1, "Daily", "Early bird gets the worm"),
            ("📝 Gratitude Journal", "Mindfulness", "Easy", 1, "Daily", "Count your blessings"),
        ]
        
        template_container = tk.Frame(parent, bg=self.colors['bg_card'])
        template_container.pack(padx=15, pady=(0, 15), fill='both', expand=True)
        
        for i, (name, category, difficulty, goal, habit_type, description) in enumerate(templates):
            if i % 3 == 0:
                row_frame = tk.Frame(template_container, bg=self.colors['bg_card'])
                row_frame.pack(fill='x', pady=5)
            
            template_card = tk.Frame(row_frame, bg=self.colors['bg_secondary'], width=180)
            template_card.pack(side='left', padx=5, fill='y')
            template_card.pack_propagate(False)
            
            tk.Label(template_card, text=name, font=('Segoe UI', 10, 'bold'), 
                    bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(pady=(8, 2))
            
            tk.Label(template_card, text=description, font=('Segoe UI', 8), 
                    bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                    wraplength=160).pack(pady=2)
            
            add_btn = tk.Button(template_card, text="+ Add", 
                               command=lambda n=name, c=category, d=difficulty, g=goal, t=habit_type: 
                               self.add_enhanced_template_habit(n, c, d, g, t),
                               bg=self.colors['accent'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 8, 'bold'), border=0, cursor='hand2')
            add_btn.pack(pady=(2, 8))
    
    def create_scrollable_habits_list(self, parent):
        list_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.habits_canvas = tk.Canvas(list_frame, bg=self.colors['bg_primary'], 
                                      highlightthickness=0, border=0)
        self.habits_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                             command=self.habits_canvas.yview)
        self.habits_scrollable_frame = tk.Frame(self.habits_canvas, bg=self.colors['bg_primary'])
        
        self.habits_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.habits_canvas.configure(scrollregion=self.habits_canvas.bbox("all"))
        )
        
        self.habits_canvas.create_window((0, 0), window=self.habits_scrollable_frame, anchor="nw")
        self.habits_canvas.configure(yscrollcommand=self.habits_scrollbar.set)
        
        self.habits_canvas.pack(side="left", fill="both", expand=True)
        self.habits_scrollbar.pack(side="right", fill="y")
    
    def create_mini_contribution_graph(self, parent):
        graph_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        graph_frame.pack(pady=5)
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=48)
        
        days_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        days_frame.pack()
        
        current_date = start_date
        for week in range(7):
            week_frame = tk.Frame(days_frame, bg=self.colors['bg_card'])
            week_frame.pack(side='left', padx=1)
            
            for day in range(7):
                if current_date <= end_date:
                    completions = self.get_daily_completions(current_date.strftime("%Y-%m-%d"))
                    
                    if completions == 0:
                        color = self.colors['border']
                    elif completions <= 2:
                        color = '#0e4429'
                    elif completions <= 4:
                        color = '#006d32'
                    else:
                        color = '#00a83f'
                    
                    day_square = tk.Frame(week_frame, bg=color, width=12, height=12)
                    day_square.pack(pady=1)
                day_square.pack_propagate(False)
            
            current_date += timedelta(days=1)
        
        # Legend
        legend_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        legend_frame.pack(pady=(10, 0))
        
        tk.Label(legend_frame, text="Less", font=('Segoe UI', 8), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side='left', padx=(0, 5))
        
        colors = [self.colors['border'], '#0e4429', '#006d32', '#26a641', '#39d353']
        for color in colors:
            square = tk.Frame(legend_frame, bg=color, width=11, height=11)
            square.pack(side='left', padx=1)
            square.pack_propagate(False)
        
        tk.Label(legend_frame, text="More", font=('Segoe UI', 8), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side='left', padx=(5, 0))
    
    def create_contribution_graph(self, parent):
        """Create a larger contribution graph for the analytics view"""
        graph_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        graph_frame.pack(pady=15, padx=20)
        
        # Calculate date range (last 12 weeks = 84 days)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=83)  # 84 days total (12 weeks)
        
        # Create month labels
        months_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        months_frame.pack(anchor='w', padx=(30, 0))  # Offset for day labels
        
        current_month = None
        month_positions = []
        
        # Calculate month positions
        current_date = start_date
        day_count = 0
        
        while current_date <= end_date:
            if current_date.day == 1 or current_month != current_date.strftime("%b"):
                current_month = current_date.strftime("%b")
                month_positions.append((current_month, day_count))
            current_date += timedelta(days=1)
            day_count += 1
        
        # Add month labels
        for month, position in month_positions:
            week_pos = position // 7
            month_label = tk.Label(months_frame, text=month, 
                                font=('Segoe UI', 9), 
                                bg=self.colors['bg_card'], 
                                fg=self.colors['text_secondary'])
            month_label.pack(side='left')
            
            # Add spacing based on week position
            if week_pos > 0:
                spacer = tk.Frame(months_frame, bg=self.colors['bg_card'], width=week_pos * 15)
                spacer.pack(side='left')
        
        # Create the main graph area
        main_graph_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        main_graph_frame.pack()
        
        # Day labels (left side)
        days_labels_frame = tk.Frame(main_graph_frame, bg=self.colors['bg_card'])
        days_labels_frame.pack(side='left', fill='y')
        
        day_names = ['Mon', 'Wed', 'Fri']  # Show every other day to avoid crowding
        for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            if day in day_names:
                tk.Label(days_labels_frame, text=day, 
                        font=('Segoe UI', 8), 
                        bg=self.colors['bg_card'], 
                        fg=self.colors['text_secondary']).pack(pady=(1, 1))
            else:
                # Add empty space for non-labeled days
                tk.Frame(days_labels_frame, bg=self.colors['bg_card'], height=14).pack(pady=(1, 1))
        
        # Contribution squares
        squares_frame = tk.Frame(main_graph_frame, bg=self.colors['bg_card'])
        squares_frame.pack(side='left', padx=(10, 0))
        
        # Calculate weeks
        current_date = start_date
        week_number = 0
        
        while current_date <= end_date:
            # Start a new week column
            week_frame = tk.Frame(squares_frame, bg=self.colors['bg_card'])
            week_frame.pack(side='left', padx=1)
            
            # Add 7 days to the week column
            for day_in_week in range(7):
                if current_date <= end_date:
                    date_str = current_date.strftime("%Y-%m-%d")
                    completions = self.get_daily_completions(date_str)
                    
                    # Color based on completion count
                    if completions == 0:
                        color = self.colors['border']
                    elif completions <= 1:
                        color = '#0e4429'
                    elif completions <= 3:
                        color = '#006d32'
                    elif completions <= 5:
                        color = '#26a641'
                    else:
                        color = '#39d353'
                    
                    # Create square with tooltip info
                    square = tk.Frame(week_frame, bg=color, width=12, height=12, 
                                    cursor='hand2')
                    square.pack(pady=1)
                    square.pack_propagate(False)
                    
                    # Add tooltip functionality (simplified)
                    def create_tooltip(date_str, completions, square_widget):
                        def on_enter(event):
                            tooltip_text = f"{date_str}: {completions} habits"
                            # You could implement a proper tooltip here
                            square_widget.configure(relief='raised', bd=1)
                        
                        def on_leave(event):
                            square_widget.configure(relief='flat', bd=0)
                        
                        square_widget.bind('<Enter>', on_enter)
                        square_widget.bind('<Leave>', on_leave)
                    
                    create_tooltip(date_str, completions, square)
                    current_date += timedelta(days=1)
                else:
                    # Empty square for padding
                    empty_square = tk.Frame(week_frame, bg=self.colors['bg_primary'], 
                                        width=12, height=12)
                    empty_square.pack(pady=1)
                    empty_square.pack_propagate(False)
            
            week_number += 1
        
        # Legend
        legend_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        legend_frame.pack(pady=(15, 0))
        
        tk.Label(legend_frame, text="Less", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side='left', padx=(0, 5))
        
        # Legend colors
        legend_colors = [self.colors['border'], '#0e4429', '#006d32', '#26a641', '#39d353']
        for color in legend_colors:
            legend_square = tk.Frame(legend_frame, bg=color, width=12, height=12)
            legend_square.pack(side='left', padx=1)
            legend_square.pack_propagate(False)
        
        tk.Label(legend_frame, text="More", font=('Segoe UI', 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side='left', padx=(5, 0))
        
        # Stats below the graph
        stats_frame = tk.Frame(graph_frame, bg=self.colors['bg_card'])
        stats_frame.pack(pady=(10, 0))
        
        # Calculate some stats
        total_days = (end_date - start_date).days + 1
        active_days = sum(1 for i in range(total_days) 
                        if self.get_daily_completions((start_date + timedelta(days=i)).strftime("%Y-%m-%d")) > 0)
        
        stats_text = f"📊 {active_days}/{total_days} active days ({(active_days/total_days)*100:.1f}%) in the last 12 weeks"
        tk.Label(stats_frame, text=stats_text, font=('Segoe UI', 10), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()
    
    def create_leaderboard(self, parent):
        leaderboard_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        leaderboard_frame.pack(padx=20, pady=(0, 20))
        
        fake_users = [
            ("HabitMaster2024", self.settings.get('total_points', 0) + random.randint(100, 500)),
            ("ProductivityPro", self.settings.get('total_points', 0) + random.randint(50, 300)),
            ("You", self.settings.get('total_points', 0)),
            ("ZenWarrior", self.settings.get('total_points', 0) - random.randint(10, 100)),
            ("HealthyLiving", self.settings.get('total_points', 0) - random.randint(20, 150)),
        ]
        
        fake_users.sort(key=lambda x: x[1], reverse=True)
        
        for i, (username, points) in enumerate(fake_users[:5]):
            rank_frame = tk.Frame(leaderboard_frame, bg=self.colors['bg_card'])
            rank_frame.pack(fill='x', pady=2)
            
            rank_color = self.colors['warning'] if username == "You" else self.colors['text_secondary']
            tk.Label(rank_frame, text=f"#{i+1}", font=('Segoe UI', 10, 'bold'), 
                    bg=self.colors['bg_card'], fg=rank_color, width=3).pack(side='left')
            
            username_color = self.colors['accent'] if username == "You" else self.colors['text_primary']
            tk.Label(rank_frame, text=username, font=('Segoe UI', 10, 'bold' if username == "You" else 'normal'), 
                    bg=self.colors['bg_card'], fg=username_color).pack(side='left', padx=10)
            
            tk.Label(rank_frame, text=f"{points} pts", font=('Segoe UI', 10), 
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side='right')
    
    def create_modern_button(self, parent, text, command, bg_color, width=12, height=1):
        btn = tk.Button(parent, text=text, command=command, 
                       bg=bg_color, fg=self.colors['text_primary'],
                       font=('Segoe UI', 9, 'bold'), border=0, cursor='hand2',
                       width=width, height=height, relief='flat')
        
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    def lighten_color(self, color):
        color_map = {
            self.colors['accent']: self.colors['accent_hover'],
            self.colors['success']: '#059669',
            self.colors['warning']: '#d97706',
            self.colors['danger']: '#dc2626',
            self.colors['bg_card']: self.colors['border'],
            self.colors['bg_secondary']: self.colors['border']
        }
        return color_map.get(color, color)
    
    def create_habit_card(self, parent, habit_name, is_selected=False):
        habit_data = self.habits[habit_name]
        bg_color = self.colors['accent'] if is_selected else self.colors['bg_card']
        
        card_frame = tk.Frame(parent, bg=bg_color, cursor='hand2')
        card_frame.pack(fill='x', padx=5, pady=3)
        
        info_frame = tk.Frame(card_frame, bg=bg_color)
        info_frame.pack(fill='x', padx=15, pady=12)
        
        # Header with name and category
        header_frame = tk.Frame(info_frame, bg=bg_color)
        header_frame.pack(fill='x')
        
        name_label = tk.Label(header_frame, text=habit_name, 
                             font=('Segoe UI', 12, 'bold'), 
                             bg=bg_color, fg=self.colors['text_primary'])
        name_label.pack(side='left')
        
        # Category badge
        category = habit_data.get('category', 'Other')
        category_label = tk.Label(header_frame, text=f"📁 {category}", 
                                 font=('Segoe UI', 8), 
                                 bg=self.colors['warning'], fg=self.colors['text_primary'])
        category_label.pack(side='right', padx=(5, 0))
        
        # Progress bar for daily goal
        progress_frame = tk.Frame(info_frame, bg=bg_color)
        progress_frame.pack(fill='x', pady=(5, 0))
        
        today = datetime.now().strftime("%Y-%m-%d")
        completions_today = habit_data['completions'].count(today)
        daily_goal = habit_data.get('daily_goal', 1)
        progress = min(completions_today / daily_goal, 1.0)
        
        # Progress bar
        progress_bg = tk.Frame(progress_frame, bg=self.colors['border'], height=6)
        progress_bg.pack(fill='x')
        
        if progress > 0:
            progress_fill = tk.Frame(progress_bg, bg=self.colors['success'], height=6)
            progress_fill.place(x=0, y=0, relwidth=progress, height=6)
        
        # Stats
        streak = self.get_streak(habit_name)
        completion_rate = self.get_completion_rate(habit_name, 7)
        difficulty = habit_data.get('difficulty', 'Medium')
        
        goal_text = f"{completions_today}/{daily_goal}"
        if completions_today >= daily_goal:
            status_text = "✓ Complete"
        else:
            status_text = "○ Pending"
        
        stats_text = f"🔥 {streak} days • {completion_rate:.0f}% (7d) • {difficulty} • {goal_text} • {status_text}"
        stats_label = tk.Label(info_frame, text=stats_text, 
                              font=('Segoe UI', 9), 
                              bg=bg_color, fg=self.colors['text_secondary'])
        stats_label.pack(anchor='w', pady=(2, 0))
        
        # Click handler
        def on_click(event):
            self.select_habit(habit_name)
        
        # Bind click events
        for widget in [card_frame, info_frame, header_frame, name_label, progress_frame, stats_label]:
            widget.bind("<Button-1>", on_click)
            if not is_selected:
                widget.bind("<Enter>", lambda e: card_frame.configure(bg=self.colors['border']))
                widget.bind("<Leave>", lambda e: card_frame.configure(bg=self.colors['bg_card']))
        
        return card_frame
    
    def refresh_habit_list(self):
        for widget in self.habits_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.habits:
            no_habits_label = tk.Label(self.habits_scrollable_frame, 
                                      text="No habits yet.\nAdd your first habit to get started!", 
                                      font=('Segoe UI', 11), 
                                      bg=self.colors['bg_primary'], 
                                      fg=self.colors['text_secondary'],
                                      justify='center')
            no_habits_label.pack(expand=True, pady=50)
            return
        
        # Filter habits by category
        filter_category = self.filter_var.get()
        filtered_habits = []
        
        for habit_name, habit_data in self.habits.items():
            if filter_category == "All" or habit_data.get('category', 'Other') == filter_category:
                filtered_habits.append(habit_name)
        
        # Sort by completion status and name
        def sort_key(habit_name):
            today = datetime.now().strftime("%Y-%m-%d")
            is_complete = today in self.habits[habit_name]['completions']
            return (not is_complete, habit_name.lower())
        
        filtered_habits.sort(key=sort_key)
        
        for habit in filtered_habits:
            is_selected = habit == self.selected_habit.get()
            self.create_habit_card(self.habits_scrollable_frame, habit, is_selected)
        
        # Update habit stats
        total_habits = len(filtered_habits)
        today = datetime.now().strftime("%Y-%m-%d")
        completed_today = sum(1 for h in filtered_habits if today in self.habits[h]['completions'])
        
        if hasattr(self, 'habit_stats_label'):
            self.habit_stats_label.configure(text=f"{completed_today}/{total_habits} completed today")
    
    def get_daily_completions(self, date_str):
        total = 0
        for habit_data in self.habits.values():
            total += habit_data['completions'].count(date_str)
        return total
    
    def refresh_achievements_display(self):
        for widget in self.achievements_scrollable_frame.winfo_children():
            widget.destroy()
        
        filter_type = self.achievement_filter.get()
        achieved = self.settings.get('achieved', [])
        
        for ach_id, ach_data in self.all_achievements.items():
            current_progress = ach_data['progress_func']()
            target = ach_data['target']
            is_achieved = ach_id in achieved
            
            # Apply filter
            if filter_type == "Achieved" and not is_achieved:
                continue
            elif filter_type == "Locked" and (is_achieved or current_progress > 0):
                continue
            elif filter_type == "In Progress" and (is_achieved or current_progress == 0):
                continue
            
            self.create_achievement_card(self.achievements_scrollable_frame, ach_id, ach_data, 
                                       current_progress, is_achieved)
    
    def create_achievement_card(self, parent, ach_id, ach_data, current_progress, is_achieved):
        if is_achieved:
            card_bg = self.colors['success']
        elif current_progress > 0:
            card_bg = self.colors['warning']
        else:
            card_bg = self.colors['bg_card']
        
        card_frame = tk.Frame(parent, bg=card_bg, relief='raised', bd=1)
        card_frame.pack(fill='x', padx=20, pady=5)
        
        content_frame = tk.Frame(card_frame, bg=card_bg)
        content_frame.pack(fill='x', padx=15, pady=10)
        
        # Left side - icon and info
        left_frame = tk.Frame(content_frame, bg=card_bg)
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Icon and title
        header_frame = tk.Frame(left_frame, bg=card_bg)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text=ach_data['icon'], font=('Segoe UI', 20), 
                bg=card_bg, fg=self.colors['text_primary']).pack(side='left', padx=(0, 10))
        
        title_frame = tk.Frame(header_frame, bg=card_bg)
        title_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(title_frame, text=ach_data['name'], font=('Segoe UI', 12, 'bold'), 
                bg=card_bg, fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(title_frame, text=ach_data['desc'], font=('Segoe UI', 10), 
                bg=card_bg, fg=self.colors['text_secondary']).pack(anchor='w')
        
        # Right side - progress
        right_frame = tk.Frame(content_frame, bg=card_bg)
        right_frame.pack(side='right')
        
        if is_achieved:
            status_text = "✅ ACHIEVED!"
            tk.Label(right_frame, text=status_text, font=('Segoe UI', 10, 'bold'), 
                    bg=card_bg, fg=self.colors['text_primary']).pack()
        else:
            # Progress bar
            progress_frame = tk.Frame(right_frame, bg=card_bg)
            progress_frame.pack()
            
            progress_bg = tk.Frame(progress_frame, bg=self.colors['border'], width=150, height=8)
            progress_bg.pack()
            
            if current_progress > 0:
                progress_percentage = min(current_progress / ach_data['target'], 1.0)
                progress_width = int(150 * progress_percentage)
                progress_fill = tk.Frame(progress_bg, bg=self.colors['accent'], height=8)
                progress_fill.place(x=0, y=0, width=progress_width, height=8)
            
            # Progress text
            progress_text = f"{current_progress}/{ach_data['target']}"
            tk.Label(right_frame, text=progress_text, font=('Segoe UI', 9), 
                    bg=card_bg, fg=self.colors['text_secondary']).pack()
    
    def filter_achievements(self, filter_type):
        self.achievement_filter.set(filter_type)
        
        # Update filter button colors
        for option, btn in self.filter_buttons.items():
            if option == filter_type:
                btn.configure(bg=self.colors['accent'])
            else:
                btn.configure(bg=self.colors['bg_card'])
        
        self.refresh_achievements_display()
    
    # Achievement progress tracking functions
    def get_total_completions(self):
        total = 0
        for habit_data in self.habits.values():
            total += len(habit_data['completions'])
        return total
    
    def get_max_current_streak(self):
        if not self.habits:
            return 0
        return max([self.get_streak(habit) for habit in self.habits.keys()] + [0])
    
    def get_perfect_days_streak(self):
        if not self.habits:
            return 0
        
        streak = 0
        current_date = datetime.now().date()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            all_completed = True
            
            for habit_data in self.habits.values():
                daily_goal = habit_data.get('daily_goal', 1)
                completions = habit_data['completions'].count(date_str)
                if completions < daily_goal:
                    all_completed = False
                    break
            
            if all_completed and len(self.habits) > 0:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
            if streak > 365:
                break
        
        return streak
    
    def get_category_completions(self, category):
        total = 0
        for habit_name, habit_data in self.habits.items():
            if habit_data.get('category') == category:
                total += len(habit_data['completions'])
        return total
    
    def get_early_completions(self):
        return self.settings.get('early_completions', 0)
    
    def get_late_completions(self):
        return self.settings.get('late_completions', 0)
    
    def get_max_daily_completions(self):
        max_daily = 0
        date_counts = {}
        
        for habit_data in self.habits.values():
            for completion in habit_data['completions']:
                date_counts[completion] = date_counts.get(completion, 0) + 1
                max_daily = max(max_daily, date_counts[completion])
        
        return max_daily
    
    # Add all the methods from your paste.txt here:
    def show_calendar(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title(f"Calendar: {habit_name}")
        calendar_window.geometry("600x500")
        calendar_window.configure(bg=self.colors['bg_primary'])
        
        # Header
        header_frame = tk.Frame(calendar_window, bg=self.colors['bg_secondary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"📅 {habit_name}", 
                font=('Segoe UI', 16, 'bold'), 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(pady=15)
        
        # Calendar content
        content_frame = tk.Frame(calendar_window, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.create_calendar_grid(content_frame, habit_name)

    def create_calendar_grid(self, parent, habit_name, days=28):
        habit_data = self.habits[habit_name]
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        grid_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        grid_frame.pack(expand=True)
        
        current_date = start_date
        row = 0
        col = 0
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            
            completions = habit_data['completions'].count(date_str)
            daily_goal = habit_data.get('daily_goal', 1)
            
            if current_date == end_date:
                bg_color = self.colors['accent']  # Today
            elif completions >= daily_goal:
                bg_color = self.colors['success']  # Goal met
            elif completions > 0:
                bg_color = self.colors['warning']  # Partial
            else:
                bg_color = self.colors['bg_card']  # Not done
            
            day_frame = tk.Frame(grid_frame, bg=bg_color, width=80, height=80)
            day_frame.grid(row=row, column=col, padx=2, pady=2)
            day_frame.pack_propagate(False)
            
            tk.Label(day_frame, text=str(current_date.day), 
                    font=('Segoe UI', 12, 'bold'), 
                    bg=bg_color, fg=self.colors['text_primary']).pack(pady=(10, 0))
            
            if completions > 0:
                if completions >= daily_goal:
                    indicator = "✓"
                else:
                    indicator = f"{completions}/{daily_goal}"
                
                tk.Label(day_frame, text=indicator, 
                        font=('Segoe UI', 9, 'bold'), 
                        bg=bg_color, fg=self.colors['text_primary']).pack()
            
            col += 1
            if col >= 7:
                col = 0
                row += 1
            
            current_date += timedelta(days=1)

    def get_streak(self, habit_name):
        if habit_name not in self.habits:
            return 0
        
        dates = sorted(self.habits[habit_name]['completions'])
        if not dates:
            return 0
        
        date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        most_recent = max(date_objects).date()
        
        if most_recent != today and most_recent != yesterday:
            return 0
        
        streak = 0
        current_date = most_recent
        
        while current_date.strftime("%Y-%m-%d") in dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak

    def get_best_streak(self, habit_name):
        if habit_name not in self.habits or not self.habits[habit_name]['completions']:
            return 0
        
        dates = sorted([datetime.strptime(date, "%Y-%m-%d").date() 
                       for date in self.habits[habit_name]['completions']])
        
        if not dates:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            if dates[i] == dates[i-1] + timedelta(days=1):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak

    def get_completion_rate(self, habit_name, days=30):
        if habit_name not in self.habits:
            return 0
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        completed_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.strftime("%Y-%m-%d") in self.habits[habit_name]['completions']:
                completed_days += 1
            current_date += timedelta(days=1)
        
        return (completed_days / days) * 100

    def refresh_today_progress(self):
        total_habits = len(self.habits)
        if total_habits == 0:
            self.today_progress_label.configure(text="No habits to track today")
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        completed_goals = 0
        total_goals = 0
        
        for habit_name, habit_data in self.habits.items():
            daily_goal = habit_data.get('daily_goal', 1)
            completions_today = habit_data['completions'].count(today)
            
            total_goals += daily_goal
            completed_goals += min(completions_today, daily_goal)
        
        progress_percent = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        
        progress_text = f"📊 Progress: {completed_goals}/{total_goals} goals completed ({progress_percent:.0f}%)"
        self.today_progress_label.configure(text=progress_text)

    def update_smart_suggestions(self):
        if not self.habits:
            self.suggestions_label.configure(text="Add your first habit to get started!")
            return
        
        suggestions = []
        user_categories = set(habit_data.get('category', 'Other') for habit_data in self.habits.values())
        
        # Suggest missing categories
        missing_categories = set(self.categories[:5]) - user_categories
        if missing_categories:
            category = list(missing_categories)[0]
            if category == "Health":
                suggestions.append("💪 Add a Health habit like 'Exercise' or 'Drink Water'")
            elif category == "Learning":
                suggestions.append("📚 Consider a Learning habit like 'Read' or 'Learn Language'")
            elif category == "Mindfulness":
                suggestions.append("🧘 Try a Mindfulness habit like 'Meditate' or 'Journal'")
        
        if not suggestions:
            suggestions.append("🚀 You're doing great! Keep up the momentum!")
        
        suggestion_text = "\n\n".join(suggestions[:2])
        self.suggestions_label.configure(text=suggestion_text)

    def refresh_analytics(self):
        total_habits = len(self.habits)
        total_completions = sum(len(data['completions']) for data in self.habits.values())
        
        if total_habits == 0:
            self.overall_stats_label.configure(text="No data available")
            return
        
        avg_completion = sum(self.get_completion_rate(habit, 30) for habit in self.habits) / total_habits
        best_habit = max(self.habits.keys(), key=lambda h: self.get_completion_rate(h, 30))
        best_rate = self.get_completion_rate(best_habit, 30)
        
        overall_text = f"""📊 Total Habits: {total_habits}
✅ Total Completions: {total_completions}
📈 Average 30-day Rate: {avg_completion:.1f}%
🏆 Most Consistent: {best_habit} ({best_rate:.1f}%)
🏅 Total Points: {self.settings.get('total_points', 0)}"""
        
        self.overall_stats_label.configure(text=overall_text)
        
        # Predictions
        predictions_text = f"""Based on your patterns:
• You're most likely to succeed with {best_habit}
• Try scheduling habits in the morning
• Focus on 3-5 core habits for best results"""
        
        self.predictions_label.configure(text=predictions_text)
        
        # Weather impact (simulated)
        weather_text = f"""Simulated weather correlations:
☀️ Sunny days: +15% completion rate
🌧️ Rainy days: -8% completion rate
❄️ Cold days: Morning habits suffer most"""
        
        self.weather_stats_label.configure(text=weather_text)

    def quick_toggle_habit(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        habit_data = self.habits[habit_name]
        
        if today in habit_data['completions']:
            self.remove_habit_today()
        else:
            self.log_habit_today()

    def focus_add_habit(self):
        self.show_view("dashboard")
        self.habit_entry.focus_set()

    def cycle_theme(self):
        theme_names = list(self.themes.keys())
        current_index = theme_names.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_names)
        self.change_theme(theme_names[next_index])

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.colors = self.themes[theme_name]
        self.settings['theme'] = theme_name
        self.save_settings()
        
        # Recreate UI with new theme
        self.main_container.destroy()
        self.setup_ui()
        self.refresh_all_views()
        self.update_status(f"🎨 Changed theme to {theme_name.title()}")

    def save_sound_setting(self):
        self.settings['sound_enabled'] = self.sound_var.get()
        self.save_settings()

    def export_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        
        if filename:
            if filename.endswith('.csv'):
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Habit', 'Date', 'Category', 'Difficulty', 'Notes'])
                    
                    for habit_name, habit_data in self.habits.items():
                        category = habit_data.get('category', 'Other')
                        difficulty = habit_data.get('difficulty', 'Medium')
                        
                        for completion in habit_data['completions']:
                            note = habit_data['notes'].get(completion, '')
                            writer.writerow([habit_name, completion, category, difficulty, note])
                
                self.update_status(f"📊 Data exported to {filename}")
            else:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.habits, f, indent=2)
                self.update_status(f"📊 Data exported to {filename}")

    def import_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
                
                if messagebox.askyesno("Import Data", "This will replace all current data. Continue?"):
                    self.habits = import_data
                    self.save_data()
                    self.refresh_all_views()
                    self.update_status("📥 Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {str(e)}")

    def backup_to_cloud(self):
        messagebox.showinfo("Cloud Backup", "Cloud backup feature coming soon!")
        self.update_status("☁️ Cloud backup simulated")

    def reset_all_data(self):
        if messagebox.askyesno("Reset All Data", 
                              "This will permanently delete ALL habits and data. Are you sure?"):
            if messagebox.askyesno("Final Confirmation", 
                                  "This action cannot be undone. Really delete everything?"):
                self.habits = {}
                self.settings = {'theme': self.current_theme, 'sound_enabled': True, 'achievements': [], 'total_points': 0}
                self.selected_habit.set("")
                
                self.save_data()
                self.save_settings()
                self.refresh_all_views()
                self.update_status("🗑 All data has been reset")

    def share_streak(self):
        max_streak = self.get_max_current_streak()
        share_text = f"🔥 I'm on a {max_streak}-day habit streak! Building better habits! #HabitTracker"
        messagebox.showinfo("Share", f"Share this text:\n\n{share_text}")
        self.settings['shares_count'] = self.settings.get('shares_count', 0) + 1
        self.save_settings()

    def share_achievement(self):
        achievements = self.settings.get('achieved', [])
        if not achievements:
            messagebox.showinfo("No Achievements", "Complete some achievements first!")
            return
        
        latest_achievement = achievements[-1] if achievements else "First habit completed"
        share_text = f"🏆 Achievement Unlocked: {latest_achievement}! #Achievement"
        messagebox.showinfo("Share", f"Share this text:\n\n{share_text}")

    def share_stats(self):
        total_habits = len(self.habits)
        total_points = self.settings.get('total_points', 0)
        max_streak = self.get_max_current_streak()
        
        share_text = f"📊 My habit stats: {total_habits} habits, {total_points} points, {max_streak}-day streak! #HabitTracker"
        messagebox.showinfo("Share", f"Share this text:\n\n{share_text}")

    def compare_with_buddy(self):
        buddy_code = self.buddy_code_entry.get().strip().upper()
        
        if not buddy_code:
            messagebox.showwarning("Warning", "Please enter a buddy code!")
            return
        
        # Simulate buddy data
        your_points = self.settings.get('total_points', 0)
        your_streak = self.get_max_current_streak()
        
        buddy_points = random.randint(max(0, your_points - 200), your_points + 200)
        buddy_streak = random.randint(max(0, your_streak - 5), your_streak + 5)
        
        comparison_text = f"""🤝 Buddy Comparison with {buddy_code}:

📊 Points: You: {your_points} | Buddy: {buddy_points}
🔥 Streak: You: {your_streak} | Buddy: {buddy_streak}

Keep pushing each other! 💪"""
        
        self.buddy_comparison_label.configure(text=comparison_text)

    def play_sound(self, sound_type):
        if not self.settings.get('sound_enabled', True):
            return
        
        try:
            import winsound
            if sound_type == "complete":
                winsound.Beep(800, 200)
            elif sound_type == "achievement":
                winsound.Beep(1000, 500)
            elif sound_type == "add":
                winsound.Beep(600, 150)
        except ImportError:
            print(f"\a")  # Terminal bell

    def start_reminder_system(self):
        def check_reminders():
            while True:
                try:
                    current_time = datetime.now().strftime('%H:%M')
                    
                    for habit_name, habit_data in self.habits.items():
                        for reminder_time in habit_data.get('reminders', []):
                            if reminder_time == current_time:
                                self.root.after(0, lambda h=habit_name: self.show_reminder(h))
                    
                    time.sleep(60)
                except:
                    break
        
        reminder_thread = threading.Thread(target=check_reminders, daemon=True)
        reminder_thread.start()

    def show_reminder(self, habit_name):
        if messagebox.askyesno("Habit Reminder", 
                              f"⏰ Time for '{habit_name}'!\n\nMark as completed?"):
            self.selected_habit.set(habit_name)
            self.log_habit_today()

    def update_pet_status(self):
        today = datetime.now().date()
        recent_completions = 0
        
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            recent_completions += self.get_daily_completions(date)
        
        if recent_completions >= 21:
            self.pet_happiness = min(100, self.pet_happiness + 5)
        elif recent_completions >= 14:
            self.pet_happiness = min(100, self.pet_happiness + 2)
        elif recent_completions >= 7:
            self.pet_happiness = max(0, self.pet_happiness - 1)
        else:
            self.pet_happiness = max(0, self.pet_happiness - 3)
        
        total_points = self.settings.get('total_points', 0)
        new_level = (total_points // 50) + 1
        
        if new_level > self.pet_level:
            self.pet_level = new_level
            messagebox.showinfo("Pet Level Up!", f"🎉 Your pet reached level {self.pet_level}!")
            self.play_sound("achievement")
        
        self.settings['pet_level'] = self.pet_level
        self.settings['pet_happiness'] = self.pet_happiness
        self.save_settings()

    def check_achievements(self, habit_name):
        achieved = self.settings.get('achieved', [])
        new_achievements = []
        
        for ach_id, ach_data in self.all_achievements.items():
            if ach_id not in achieved:
                current_progress = ach_data['progress_func']()
                if current_progress >= ach_data['target']:
                    new_achievements.append(ach_id)
        
        if new_achievements:
            achieved.extend(new_achievements)
            self.settings['achieved'] = achieved
            self.save_settings()
            
            achievement_names = [self.all_achievements[ach]['name'] for ach in new_achievements]
            achievement_text = "\n".join([f"🏆 {name}" for name in achievement_names])
            messagebox.showinfo("Achievement Unlocked!", f"Congratulations!\n\n{achievement_text}")
            self.play_sound("achievement")

    def refresh_all_views(self):
        if hasattr(self, 'main_container'):
            self.refresh_habit_list()
            self.refresh_today_progress()
            self.update_pet_status()
            
            if hasattr(self, 'points_label'):
                self.points_label.configure(text=f"🏆 {self.settings.get('total_points', 0)} pts")
            if hasattr(self, 'streak_label'):
                max_streak = self.get_max_current_streak()
                self.streak_label.configure(text=f"🔥 {max_streak} days")
            if hasattr(self, 'pet_label'):
                pet_emoji = self.get_pet_emoji()
                self.pet_label.configure(text=f"{pet_emoji} Lv.{self.pet_level}")

    def update_status(self, message):
        # Simple status update - can be enhanced with actual status bar
        print(f"Status: {message}")
    
    # Core functionality methods
    def add_habit(self):
        habit_name = self.habit_entry.get().strip()
        if not habit_name:
            return
        
        if habit_name in self.habits:
            messagebox.showwarning("Warning", f"Habit '{habit_name}' already exists!")
            return
        
        try:
            daily_goal = int(self.goal_var.get())
        except:
            daily_goal = 1
        
        self.habits[habit_name] = {
            'completions': [],
            'category': self.category_var.get(),
            'difficulty': self.difficulty_var.get(),
            'daily_goal': daily_goal,
            'habit_type': self.type_var.get(),
            'notes': {},
            'reminders': [],
            'dependencies': [],
            'completion_times': {},
            'mood_ratings': {},
            'photos': {},
            'created_date': datetime.now().isoformat()
        }
        
        self.save_data()
        self.habit_entry.delete(0, tk.END)
        self.goal_var.set("1")
        self.refresh_all_views()
        self.play_sound("add")
        self.update_status(f"✅ Added habit: {habit_name}")
        self.check_achievements(habit_name)

    def add_enhanced_template_habit(self, name, category, difficulty, goal, habit_type):
        if name in self.habits:
            messagebox.showwarning("Warning", f"Habit '{name}' already exists!")
            return
        
        self.habits[name] = {
            'completions': [],
            'category': category,
            'difficulty': difficulty,
            'daily_goal': goal,
            'habit_type': habit_type,
            'notes': {},
            'reminders': [],
            'dependencies': [],
            'completion_times': {},
            'mood_ratings': {},
            'photos': {},
            'created_date': datetime.now().isoformat()
        }
        
        self.save_data()
        self.refresh_all_views()
        self.play_sound("add")
        self.update_status(f"✅ Added enhanced habit: {name}")

    def log_habit_today(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        habit_data = self.habits[habit_name]
        
        # Check dependencies
        dependencies = habit_data.get('dependencies', [])
        today = datetime.now().strftime("%Y-%m-%d")
        
        for dependency in dependencies:
            if dependency in self.habits:
                if today not in self.habits[dependency]['completions']:
                    messagebox.showwarning("Dependency Not Met", 
                                         f"Complete '{dependency}' first before '{habit_name}'!")
                    return
        
        # Check if daily goal is reached
        completions_today = habit_data['completions'].count(today)
        daily_goal = habit_data.get('daily_goal', 1)
        
        if completions_today < daily_goal:
            habit_data['completions'].append(today)
            
            # Track completion time
            current_time = datetime.now().strftime("%H:%M")
            if today not in habit_data['completion_times']:
                habit_data['completion_times'][today] = []
            habit_data['completion_times'][today].append(current_time)
            
            self.save_data()
            
            # Award points
            points = self.difficulty_levels[habit_data.get('difficulty', 'Medium')]
            self.settings['total_points'] = self.settings.get('total_points', 0) + points
            
            # Track early/late completions
            hour = int(current_time.split(':')[0])
            if hour < 8:
                self.settings['early_completions'] = self.settings.get('early_completions', 0) + 1
            elif hour >= 22:
                self.settings['late_completions'] = self.settings.get('late_completions', 0) + 1
            
            self.save_settings()
            self.check_achievements(habit_name)
            self.pet_happiness = min(100, self.pet_happiness + 2)
            
            self.refresh_all_views()
            self.play_sound("complete")
            
            new_completions = completions_today + 1
            if new_completions >= daily_goal:
                self.update_status(f"🎉 Daily goal completed for '{habit_name}'! (+{points} pts)")
            else:
                remaining = daily_goal - new_completions
                self.update_status(f"✅ Progress on '{habit_name}' ({new_completions}/{daily_goal}, {remaining} more needed)")
        else:
            self.update_status(f"Daily goal for '{habit_name}' already completed!")

    def remove_habit_today(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        habit_data = self.habits[habit_name]
        
        if today in habit_data['completions']:
            habit_data['completions'].remove(today)
            
            points = self.difficulty_levels[habit_data.get('difficulty', 'Medium')]
            self.settings['total_points'] = max(0, self.settings.get('total_points', 0) - points)
            
            self.save_data()
            self.save_settings()
            self.refresh_all_views()
            self.update_status(f"Removed '{habit_name}' completion for today (-{points} pts)")
        else:
            self.update_status(f"'{habit_name}' was not completed today")

    def delete_habit(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete '{habit_name}' and all its data?"):
            del self.habits[habit_name]
            self.save_data()
            self.selected_habit.set("")
            self.refresh_all_views()
            self.update_status(f"🗑 Deleted habit: {habit_name}")

    def show_view(self, view_name):
        # Hide all views
        for frame in [self.dashboard_frame, self.analytics_frame, self.achievements_frame, 
                     self.social_frame, self.settings_frame]:
            frame.pack_forget()
        
        # Update navigation buttons
        for btn in [self.nav_dashboard, self.nav_analytics, self.nav_achievements, 
                   self.nav_social, self.nav_settings]:
            btn.configure(bg=self.colors['bg_card'])
        
        # Show selected view
        self.current_view = view_name
        if view_name == "dashboard":
            self.dashboard_frame.pack(fill='both', expand=True)
            self.nav_dashboard.configure(bg=self.colors['accent'])
            self.update_smart_suggestions()
        elif view_name == "analytics":
            self.analytics_frame.pack(fill='both', expand=True)
            self.nav_analytics.configure(bg=self.colors['accent'])
            self.refresh_analytics()
        elif view_name == "achievements":
            self.achievements_frame.pack(fill='both', expand=True)
            self.nav_achievements.configure(bg=self.colors['accent'])
            self.refresh_achievements_display()
        elif view_name == "social":
            self.social_frame.pack(fill='both', expand=True)
            self.nav_social.configure(bg=self.colors['accent'])
        elif view_name == "settings":
            self.settings_frame.pack(fill='both', expand=True)
            self.nav_settings.configure(bg=self.colors['accent'])

    def select_habit(self, habit_name):
        self.selected_habit.set(habit_name)
        self.refresh_habit_list()
        self.show_habit_stats(habit_name)
        self.update_status(f"Selected: {habit_name}")

    def show_habit_stats(self, habit_name):
        if habit_name not in self.habits:
            return
        
        habit_data = self.habits[habit_name]
        streak = self.get_streak(habit_name)
        completion_7 = self.get_completion_rate(habit_name, 7)
        completion_30 = self.get_completion_rate(habit_name, 30)
        total_logs = len(habit_data['completions'])
        best_streak = self.get_best_streak(habit_name)
        
        stats_text = f"""🔥 Current Streak: {streak} days
🏆 Best Streak: {best_streak} days
📊 This Week: {completion_7:.0f}% complete
📈 This Month: {completion_30:.0f}% complete
📝 Total Completions: {total_logs}
📁 Category: {habit_data.get('category', 'Other')}
⚡ Difficulty: {habit_data.get('difficulty', 'Medium')}
🎯 Daily Goal: {habit_data.get('daily_goal', 1)}"""
        
        self.stats_label.configure(text=stats_text)

    # Additional methods for enhanced functionality
    def set_mood(self, mood_value):
        today = datetime.now().strftime("%Y-%m-%d")
        self.settings['mood_history'][today] = mood_value
        self.save_settings()
        self.update_status(f"😊 Mood set: {self.moods[mood_value-1]}")

    def add_habit_note(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        note = simpledialog.askstring("Add Note", f"Add a note for '{habit_name}' today:")
        if note:
            today = datetime.now().strftime("%Y-%m-%d")
            self.habits[habit_name]['notes'][today] = note
            self.save_data()
            self.update_status(f"📝 Added note for '{habit_name}'")

    def add_habit_photo(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        filename = filedialog.askopenfilename(
            title="Select habit photo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if filename:
            today = datetime.now().strftime("%Y-%m-%d")
            self.habits[habit_name]['photos'][today] = filename
            self.save_data()
            self.update_status(f"📸 Photo added for '{habit_name}'")

    def set_reminder(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        time_str = simpledialog.askstring("Set Reminder", 
                                         f"Set reminder time for '{habit_name}' (HH:MM format):")
        if time_str:
            try:
                time.strptime(time_str, '%H:%M')
                self.habits[habit_name]['reminders'].append(time_str)
                self.save_data()
                self.update_status(f"⏰ Reminder set for '{habit_name}' at {time_str}")
            except:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM (e.g., 14:30)")

    def set_dependency(self):
        habit_name = self.selected_habit.get()
        if not habit_name:
            self.update_status("Please select a habit first")
            return
        
        other_habits = [h for h in self.habits.keys() if h != habit_name]
        if not other_habits:
            messagebox.showinfo("Info", "No other habits available for dependencies")
            return
        
        dependency = simpledialog.askstring("Set Dependency", 
                                           f"Which habit must be completed before '{habit_name}'?\n" +
                                           f"Available: {', '.join(other_habits)}")
        
        if dependency and dependency in other_habits:
            if 'dependencies' not in self.habits[habit_name]:
                self.habits[habit_name]['dependencies'] = []
            
            if dependency not in self.habits[habit_name]['dependencies']:
                self.habits[habit_name]['dependencies'].append(dependency)
                self.save_data()
                self.update_status(f"🔗 Dependency set: {dependency} → {habit_name}")
            else:
                self.update_status("Dependency already exists")


# Main function to run the app
def main():
    root = tk.Tk()
    app = UltimateHabitTrackerProMax(root)
    root.mainloop()

if __name__ == "__main__":
    main()