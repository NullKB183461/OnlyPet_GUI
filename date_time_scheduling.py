"""
Date & Time Scheduling Screen - Calendar and time slot selection
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, List
from datetime import datetime, timedelta
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard
from data_models import BookingStep

class DateTimeSchedulingFrame(ModernFrame):
    """Date and time scheduling interface"""
    
    def __init__(self, parent, booking_data, on_complete: Callable, on_back: Callable):
        super().__init__(parent, bg_color="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        self.on_back = on_back
        
        self.selected_date = booking_data.date
        self.selected_time = booking_data.time
        
        # Store references to buttons for updating
        self.date_buttons = {}
        self.time_buttons = {}
        
        # Generate available dates and times
        self.available_dates = self.generate_available_dates()
        self.time_slots = [
            "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"
        ]
        
        self.create_content()
    
    def generate_available_dates(self) -> List[str]:
        """Generate next 14 days as available dates"""
        dates = []
        today = datetime.now()
        
        for i in range(1, 15):  # Skip today, start from tomorrow
            date = today + timedelta(days=i)
            # Skip Sundays (weekday 6)
            if date.weekday() != 6:
                dates.append(date.strftime("%Y-%m-%d"))
        
        return dates
    
    def create_content(self):
        """Create scheduling interface"""
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()
        
        main_canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_main = tk.Frame(main_canvas, bg="#f8fafc")
        
        scrollable_main.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_main, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Pack main canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header
        self.create_header(scrollable_main)
        
        # Service summary
        self.create_service_summary(scrollable_main)
        
        scheduling_container = tk.Frame(scrollable_main, bg="#f8fafc")
        scheduling_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Date selection (left side) - Calendar style
        date_frame = ModernFrame(scheduling_container, bg_color="#ffffff")
        date_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.create_calendar_date_selection(date_frame)
        
        # Time selection (right side)
        time_frame = ModernFrame(scheduling_container, bg_color="#ffffff")
        time_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        self.create_time_selection(time_frame)
        
        # Navigation
        self.create_navigation(scrollable_main)

    def create_header(self, parent):
        """Create page header"""
        header_frame = ModernFrame(parent, bg_color="#ffffff")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(header_frame, bg="#ffffff")
        content.pack(expand=True, pady=20)
        
        title = ModernLabel(
            content,
            text="Schedule Your Appointment",
            style="heading2",
            bg="#ffffff"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ModernLabel(
            content,
            text="Select your preferred date and time for the service",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
    
    def create_service_summary(self, parent):
        """Create service summary card"""
        if not self.booking_data.service:
            return
        
        summary_frame = ModernCard(parent)
        summary_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Service info
        info_frame = tk.Frame(summary_frame, bg="#ffffff")
        info_frame.pack(fill=tk.X)
        
        # Title and price
        title_frame = tk.Frame(info_frame, bg="#ffffff")
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        title = ModernLabel(
            title_frame,
            text=self.booking_data.service.title,
            style="heading4",
            bg="#ffffff"
        )
        title.pack(side=tk.LEFT)
        
        price = ModernLabel(
            title_frame,
            text=f"${self.booking_data.service.price:.0f}",
            style="heading4",
            bg="#ffffff",
            fg="#10b981"
        )
        price.pack(side=tk.RIGHT)
        
        # Duration
        duration = ModernLabel(
            info_frame,
            text=f"Duration: {self.booking_data.service.duration}",
            style="caption",
            bg="#ffffff"
        )
        duration.pack(anchor="w")
    
    def create_calendar_date_selection(self, parent):
        """Create calendar-style date selection interface"""
        # Header
        header = ModernLabel(
            parent,
            text="Select Date",
            style="heading3",
            bg="#ffffff"
        )
        header.pack(pady=(25, 20))
        
        calendar_container = tk.Frame(parent, bg="#ffffff")
        calendar_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # Days of week header
        days_header = tk.Frame(calendar_container, bg="#ffffff")
        days_header.pack(fill=tk.X, pady=(0, 10))
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            day_label = ModernLabel(
                days_header,
                text=day,
                style="caption",
                bg="#ffffff",
                fg="#6b7280"
            )
            day_label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
            days_header.columnconfigure(i, weight=1)
        
        calendar_grid = tk.Frame(calendar_container, bg="#ffffff")
        calendar_grid.pack(fill=tk.X)
        
        # Create calendar layout
        current_row = 0
        current_col = 0
        
        for date_str in self.available_dates:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_num = date_obj.strftime("%d")
            weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
            
            # Start new row if we've filled 7 columns
            if current_col >= 7:
                current_row += 1
                current_col = 0
            
            # Skip to correct weekday column for first row
            if current_row == 0 and current_col == 0:
                current_col = weekday
            
            is_selected = self.selected_date == date_str
            
            date_btn = tk.Button(
                calendar_grid,
                text=day_num,
                font=("Segoe UI", 12, "bold" if is_selected else "normal"),
                width=4,
                height=2,
                bg="#3b82f6" if is_selected else "#f8fafc",
                fg="white" if is_selected else "#374151",
                activebackground="#2563eb",
                relief=tk.FLAT,
                bd=2 if is_selected else 1,
                cursor="hand2",
                command=lambda d=date_str: self.select_date(d)
            )
            date_btn.grid(row=current_row, column=current_col, padx=2, pady=2, sticky="nsew")
            
            # Store button reference
            self.date_buttons[date_str] = date_btn
            
            current_col += 1
        
        # Configure grid weights
        for i in range(7):
            calendar_grid.columnconfigure(i, weight=1)

    def create_time_selection(self, parent):
        """Create time selection interface"""
        # Header
        header = ModernLabel(
            parent,
            text="Select Time",
            style="heading3",
            bg="#ffffff"
        )
        header.pack(pady=(25, 20))
        
        if not self.selected_date:
            placeholder_frame = tk.Frame(parent, bg="#ffffff")
            placeholder_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=50)
            
            placeholder_icon = ModernLabel(
                placeholder_frame,
                text="📅",
                style="heading2",
                bg="#ffffff"
            )
            placeholder_icon.pack(pady=(0, 15))
            
            placeholder = ModernLabel(
                placeholder_frame,
                text="Please select a date first",
                style="body",
                bg="#ffffff",
                fg="#6b7280"
            )
            placeholder.pack()
            return
        
        time_container = tk.Frame(parent, bg="#ffffff")
        time_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # Morning slots
        morning_frame = tk.Frame(time_container, bg="#ffffff")
        morning_frame.pack(fill=tk.X, pady=(0, 15))
        
        morning_label = ModernLabel(
            morning_frame,
            text="Morning",
            style="heading4",
            bg="#ffffff",
            fg="#6b7280"
        )
        morning_label.pack(anchor="w", pady=(0, 8))
        
        morning_slots = ["9:00 AM", "10:00 AM", "11:00 AM"]
        for time_slot in morning_slots:
            self.create_time_button(morning_frame, time_slot)
        
        # Afternoon slots
        afternoon_frame = tk.Frame(time_container, bg="#ffffff")
        afternoon_frame.pack(fill=tk.X, pady=(0, 15))
        
        afternoon_label = ModernLabel(
            afternoon_frame,
            text="Afternoon",
            style="heading4",
            bg="#ffffff",
            fg="#6b7280"
        )
        afternoon_label.pack(anchor="w", pady=(0, 8))
        
        afternoon_slots = ["12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        for time_slot in afternoon_slots:
            self.create_time_button(afternoon_frame, time_slot)
    
    def create_time_button(self, parent, time_slot):
        """Create individual time slot button"""
        is_selected = self.selected_time == time_slot
        is_available = self.is_time_available(time_slot)
        
        time_btn = tk.Button(
            parent,
            text=time_slot,
            font=("Segoe UI", 11, "bold" if is_selected else "normal"),
            width=15,
            height=2,
            bg="#3b82f6" if is_selected else "#f8fafc" if is_available else "#fca5a5",
            fg="white" if is_selected else "#374151" if is_available else "#7f1d1d",
            activebackground="#2563eb" if is_available else "#fca5a5",
            relief=tk.FLAT,
            bd=2 if is_selected else 1,
            cursor="hand2" if is_available else "not-allowed",
            state="normal" if is_available else "disabled",
            command=lambda t=time_slot: self.select_time(t) if is_available else None
        )
        time_btn.pack(fill=tk.X, pady=3)
        
        self.time_buttons[time_slot] = time_btn
        
        if not is_available and time_slot != self.selected_time:
            unavailable_label = ModernLabel(
                parent,
                text="(Unavailable)",
                style="small",
                bg="#ffffff",
                fg="#ef4444"
            )
            unavailable_label.pack(pady=(0, 5))

    def create_navigation(self, parent):
        """Create navigation buttons"""
        nav_frame = ModernFrame(parent, bg_color="#ffffff")
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_frame = tk.Frame(nav_frame, bg="#ffffff")
        button_frame.pack(expand=True, pady=20)
        
        # Back button
        back_btn = ModernButton(
            button_frame,
            text="← Back to Service Selection",
            command=self.on_back,
            style="secondary"
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.continue_btn = ModernButton(
            button_frame,
            text="Continue to Pet Information →",
            command=self.continue_to_pet_info,
            style="primary"
        )
        self.continue_btn.pack(side=tk.LEFT)
        
        # Update button state based on selections
        self.update_continue_button()
    
    def update_continue_button(self):
        """Update continue button state"""
        if hasattr(self, 'continue_btn'):
            is_ready = bool(self.selected_date and self.selected_time)
            self.continue_btn.configure(
                state="normal" if is_ready else "disabled",
                text="Continue to Pet Information →" if is_ready else "Select Date & Time to Continue"
            )

    def is_time_available(self, time_slot: str) -> bool:
        """Check if time slot is available (mock logic)"""
        # Mock availability - some slots unavailable for demo
        unavailable_slots = ["12:00 PM", "3:00 PM"]
        return time_slot not in unavailable_slots
    
    def select_date(self, date_str: str):
        """Handle date selection"""
        # Reset previous selection
        if self.selected_date and self.selected_date in self.date_buttons:
            old_btn = self.date_buttons[self.selected_date]
            old_btn.configure(
                bg="#f8fafc",
                fg="#374151",
                font=("Segoe UI", 12, "normal"),
                bd=1
            )
        
        # Update new selection
        self.selected_date = date_str
        self.selected_time = None  # Reset time selection
        self.booking_data.update({"date": date_str, "time": None})
        
        # Update new button state
        if date_str in self.date_buttons:
            new_btn = self.date_buttons[date_str]
            new_btn.configure(
                bg="#3b82f6",
                fg="white",
                font=("Segoe UI", 12, "bold"),
                bd=2
            )
        
        # Refresh time selection area only
        self.refresh_time_selection()
    
    def select_time(self, time_slot: str):
        """Handle time selection"""
        # Reset previous selection
        if self.selected_time and self.selected_time in self.time_buttons:
            old_btn = self.time_buttons[self.selected_time]
            is_available = self.is_time_available(self.selected_time)
            old_btn.configure(
                bg="#f8fafc" if is_available else "#fca5a5",
                fg="#374151" if is_available else "#7f1d1d",
                font=("Segoe UI", 11, "normal"),
                bd=1
            )
        
        # Update new selection
        self.selected_time = time_slot
        self.booking_data.update({"time": time_slot})
        
        # Update new button state
        if time_slot in self.time_buttons:
            new_btn = self.time_buttons[time_slot]
            new_btn.configure(
                bg="#3b82f6",
                fg="white",
                font=("Segoe UI", 11, "bold"),
                bd=2
            )
        
        self.update_continue_button()
    
    def refresh_time_selection(self):
        """Refresh only the time selection area"""
        # Find and update time selection frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                scrollable_main = widget.nametowidget(widget.winfo_children()[0])
                for child in scrollable_main.winfo_children():
                    if isinstance(child, tk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ModernFrame):
                                # This is likely our time frame - recreate time selection
                                if len(grandchild.winfo_children()) > 0:
                                    first_child = grandchild.winfo_children()[0]
                                    if hasattr(first_child, 'cget') and 'Select Time' in str(first_child.cget('text') if hasattr(first_child, 'cget') else ''):
                                        # Clear and recreate time selection
                                        for time_widget in grandchild.winfo_children():
                                            time_widget.destroy()
                                        self.time_buttons.clear()
                                        self.create_time_selection(grandchild)
                                        break
    
    def continue_to_pet_info(self):
        """Continue to pet information step"""
        if self.selected_date and self.selected_time:
            self.on_complete(BookingStep.PET_INFO)
