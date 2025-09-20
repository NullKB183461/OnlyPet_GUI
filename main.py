"""
Pet Service Booking System - Python GUI Application
Main application entry point with modern UI styling
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui_components import ModernFrame, ModernButton, ModernLabel, ModernEntry
    from data_models import BookingData, Service, BookingStep
    from service_discovery import ServiceDiscoveryFrame
    from service_selection import ServiceSelectionFrame
    from date_time_scheduling import DateTimeSchedulingFrame
    from pet_information import PetInformationFrame
    from review_confirmation import ReviewConfirmationFrame
    from booking_success import BookingSuccessFrame
    from booking_management import BookingManagementFrame
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all component files are in the same directory")
    sys.exit(1)

class PetBookingApp:
    """Main application class managing the booking flow"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        
        # Application state
        self.current_step = BookingStep.DISCOVERY
        self.booking_data = BookingData()
        self.step_history = []
        
        # UI Components
        self.main_container = None
        self.header_frame = None
        self.breadcrumbs_frame = None
        self.content_frame = None
        self.current_content = None
        
        self.setup_ui()
        self.show_step(BookingStep.DISCOVERY)
    
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("PawCare - Pet Service Booking")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg='#f8fafc')
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def setup_styles(self):
        """Configure modern UI styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure(
            "Modern.TButton",
            background="#3b82f6",
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 12),
            font=("Segoe UI", 10, "bold")
        )
        
        style.map(
            "Modern.TButton",
            background=[("active", "#2563eb"), ("pressed", "#1d4ed8")]
        )
        
        # Configure secondary button style
        style.configure(
            "Secondary.TButton",
            background="#e5e7eb",
            foreground="#374151",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 12),
            font=("Segoe UI", 10)
        )
        
        style.map(
            "Secondary.TButton",
            background=[("active", "#d1d5db"), ("pressed", "#9ca3af")]
        )
    
    def setup_ui(self):
        """Initialize main UI layout"""
        # Main container
        self.main_container = tk.Frame(self.root, bg='#f8fafc')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Breadcrumbs
        self.create_breadcrumbs()
        
        # Content area
        self.content_frame = tk.Frame(self.main_container, bg='#ffffff', relief=tk.FLAT)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
    
    def create_header(self):
        """Create application header"""
        self.header_frame = tk.Frame(self.main_container, bg='#f8fafc', height=80)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        self.header_frame.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(self.header_frame, bg='#f8fafc')
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(
            logo_frame,
            text="🐾 PawCare",
            font=("Segoe UI", 24, "bold"),
            fg="#1f2937",
            bg='#f8fafc'
        )
        title_label.pack(side=tk.LEFT, pady=20)
        
        subtitle_label = tk.Label(
            logo_frame,
            text="Professional Pet Services",
            font=("Segoe UI", 12),
            fg="#6b7280",
            bg='#f8fafc'
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.header_frame, bg='#f8fafc')
        nav_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        manage_btn = ttk.Button(
            nav_frame,
            text="Manage Bookings",
            style="Secondary.TButton",
            command=lambda: self.show_step(BookingStep.MANAGEMENT)
        )
        manage_btn.pack(side=tk.RIGHT, padx=(10, 0), pady=20)
    
    def create_breadcrumbs(self):
        """Create breadcrumb navigation"""
        self.breadcrumbs_frame = tk.Frame(self.main_container, bg='#f8fafc', height=50)
        self.breadcrumbs_frame.pack(fill=tk.X, pady=(0, 10))
        self.breadcrumbs_frame.pack_propagate(False)
        
        self.update_breadcrumbs()
    
    def update_breadcrumbs(self):
        """Update breadcrumb display based on current step"""
        # Clear existing breadcrumbs
        for widget in self.breadcrumbs_frame.winfo_children():
            widget.destroy()
        
        steps = [
            (BookingStep.DISCOVERY, "Services"),
            (BookingStep.SELECTION, "Select"),
            (BookingStep.SCHEDULING, "Schedule"),
            (BookingStep.PET_INFO, "Pet Info"),
            (BookingStep.REVIEW, "Review"),
            (BookingStep.SUCCESS, "Complete")
        ]
        
        breadcrumb_container = tk.Frame(self.breadcrumbs_frame, bg='#f8fafc')
        breadcrumb_container.pack(expand=True)
        
        for i, (step, label) in enumerate(steps):
            # Step circle
            if step == self.current_step:
                bg_color = "#3b82f6"
                fg_color = "white"
            elif self.is_step_completed(step):
                bg_color = "#10b981"
                fg_color = "white"
            else:
                bg_color = "#e5e7eb"
                fg_color = "#6b7280"
            
            circle = tk.Label(
                breadcrumb_container,
                text=str(i + 1),
                width=3,
                height=1,
                bg=bg_color,
                fg=fg_color,
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT
            )
            circle.pack(side=tk.LEFT, padx=(0, 5))
            
            # Step label
            step_label = tk.Label(
                breadcrumb_container,
                text=label,
                font=("Segoe UI", 10),
                fg="#374151" if step == self.current_step else "#6b7280",
                bg='#f8fafc'
            )
            step_label.pack(side=tk.LEFT, padx=(0, 20))
            
            # Arrow separator (except for last item)
            if i < len(steps) - 1:
                arrow = tk.Label(
                    breadcrumb_container,
                    text="→",
                    font=("Segoe UI", 12),
                    fg="#9ca3af",
                    bg='#f8fafc'
                )
                arrow.pack(side=tk.LEFT, padx=(0, 20))
    
    def is_step_completed(self, step: BookingStep) -> bool:
        """Check if a step has been completed"""
        step_order = [
            BookingStep.DISCOVERY,
            BookingStep.SELECTION,
            BookingStep.SCHEDULING,
            BookingStep.PET_INFO,
            BookingStep.REVIEW,
            BookingStep.SUCCESS
        ]
        
        try:
            current_index = step_order.index(self.current_step)
            step_index = step_order.index(step)
            return step_index < current_index
        except ValueError:
            return False
    
    def show_step(self, step: BookingStep):
        """Navigate to a specific step"""
        # Save current step to history
        if self.current_step != step:
            self.step_history.append(self.current_step)
        
        self.current_step = step
        self.update_breadcrumbs()
        
        # Clear current content
        if self.current_content:
            self.current_content.destroy()
        
        try:
            if step == BookingStep.DISCOVERY:
                self.current_content = ServiceDiscoveryFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete
                )
            elif step == BookingStep.SELECTION:
                self.current_content = ServiceSelectionFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete,
                    self.go_back
                )
            elif step == BookingStep.SCHEDULING:
                self.current_content = DateTimeSchedulingFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete,
                    self.go_back
                )
            elif step == BookingStep.PET_INFO:
                self.current_content = PetInformationFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete,
                    self.go_back
                )
            elif step == BookingStep.REVIEW:
                self.current_content = ReviewConfirmationFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete,
                    self.go_back,
                    self.edit_step
                )
            elif step == BookingStep.SUCCESS:
                self.current_content = BookingSuccessFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete
                )
            elif step == BookingStep.MANAGEMENT:
                self.current_content = BookingManagementFrame(
                    self.content_frame, 
                    self.booking_data, 
                    self.on_step_complete
                )
            
            if self.current_content:
                self.current_content.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load step {step.value}: {str(e)}")
            print(f"[v0] Error loading step {step.value}: {e}")
    
    def on_step_complete(self, next_step: BookingStep, data: Dict[str, Any] = None):
        """Handle step completion and data updates"""
        if data:
            self.booking_data.update(data)
        
        self.show_step(next_step)
    
    def go_back(self):
        """Navigate to previous step"""
        if self.step_history:
            previous_step = self.step_history.pop()
            self.current_step = previous_step
            self.show_step(previous_step)
    
    def edit_step(self, step: BookingStep):
        """Navigate to a specific step for editing"""
        self.show_step(step)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Application entry point"""
    try:
        app = PetBookingApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        print(f"[v0] Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
