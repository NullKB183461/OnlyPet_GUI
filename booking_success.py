"""
Booking Success Screen - Confirmation and next steps
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any
from datetime import datetime, timedelta
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard
from data_models import BookingStep

class BookingSuccessFrame(ModernFrame):
    """Booking success confirmation"""
    
    def __init__(self, parent, booking_data, on_complete: Callable):
        super().__init__(parent, bg_color="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        
        self.create_scrollable_container()
        self.create_content()
    
    def create_scrollable_container(self):
        """Create scrollable container for all content"""
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8fafc")
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_content(self):
        """Create success confirmation content"""
        parent = self.scrollable_frame
        
        # Success animation area
        self.create_success_header(parent)
        
        # Booking confirmation details
        self.create_confirmation_details(parent)
        
        # Next steps
        self.create_next_steps(parent)
        
        # Action buttons
        self.create_action_buttons(parent)
    
    def create_success_header(self, parent):
        """Create success animation and header"""
        header_frame = ModernFrame(parent, bg_color="#ffffff")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(header_frame, bg="#ffffff")
        content.pack(expand=True, pady=40)
        
        # Success icon (animated effect with color)
        icon_frame = tk.Frame(content, bg="#10b981", width=80, height=80)
        icon_frame.pack(pady=(0, 20))
        icon_frame.pack_propagate(False)
        
        success_icon = ModernLabel(
            icon_frame,
            text="✓",
            style="heading1",
            bg="#10b981",
            fg="white"
        )
        success_icon.pack(expand=True)
        
        # Success message
        title = ModernLabel(
            content,
            text="Booking Confirmed!",
            style="heading1",
            bg="#ffffff",
            fg="#10b981"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ModernLabel(
            content,
            text="Your pet service appointment has been successfully booked.",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
        
        # Booking ID
        if self.booking_data.booking_id:
            booking_id = ModernLabel(
                content,
                text=f"Booking ID: {self.booking_data.booking_id}",
                style="heading4",
                bg="#ffffff",
                fg="#3b82f6"
            )
            booking_id.pack(pady=(15, 0))
    
    def create_confirmation_details(self, parent):
        """Create booking confirmation details"""
        details_frame = ModernFrame(parent, bg_color="#ffffff")
        details_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(details_frame, bg="#ffffff")
        content.pack(expand=True, padx=40, pady=30)
        
        # Title
        title = ModernLabel(
            content,
            text="Appointment Details",
            style="heading3",
            bg="#ffffff"
        )
        title.pack(pady=(0, 20))
        
        # Details grid
        details_container = tk.Frame(content, bg="#ffffff")
        details_container.pack(fill=tk.X)
        
        if self.booking_data.service:
            self.create_detail_row(
                details_container,
                "Service:",
                self.booking_data.service.title
            )
            
            service_category = self.get_service_category(self.booking_data.service.title)
            self.create_detail_row(
                details_container,
                "Category:",
                service_category
            )
            
            self.create_detail_row(
                details_container,
                "Price:",
                f"${self.booking_data.service.price:.2f}"
            )
            
            self.create_detail_row(
                details_container,
                "Duration:",
                self.booking_data.service.duration
            )
            
            # Add service description
            if hasattr(self.booking_data.service, 'description'):
                desc_frame = tk.Frame(details_container, bg="#ffffff")
                desc_frame.pack(fill=tk.X, pady=(15, 8))
                
                desc_label = ModernLabel(
                    desc_frame,
                    text="Service Description:",
                    style="body",
                    bg="#ffffff"
                )
                desc_label.pack(anchor="w")
                
                desc_text = ModernLabel(
                    desc_frame,
                    text=self.booking_data.service.description,
                    style="body",
                    bg="#ffffff",
                    fg="#6b7280",
                    wraplength=400,
                    justify=tk.LEFT
                )
                desc_text.pack(anchor="w", padx=(20, 0))
        
        if self.booking_data.date:
            date_obj = datetime.strptime(self.booking_data.date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            
            self.create_detail_row(
                details_container,
                "Date:",
                formatted_date
            )
        
        if self.booking_data.time:
            self.create_detail_row(
                details_container,
                "Time:",
                self.booking_data.time
            )
            
            # Add estimated completion time
            if self.booking_data.service and hasattr(self.booking_data.service, 'duration'):
                duration_text = self.booking_data.service.duration
                if 'hour' in duration_text.lower():
                    hours = int(duration_text.split()[0]) if duration_text.split()[0].isdigit() else 1
                    start_time = datetime.strptime(self.booking_data.time, "%I:%M %p")
                    end_time = start_time + timedelta(hours=hours)
                    
                    self.create_detail_row(
                        details_container,
                        "Estimated Completion:",
                        end_time.strftime("%I:%M %p")
                    )
        
        if self.booking_data.pet_name:
            self.create_detail_row(
                details_container,
                "Pet Name:",
                self.booking_data.pet_name
            )
        
        if self.booking_data.pet_type:
            self.create_detail_row(
                details_container,
                "Pet Type:",
                self.booking_data.pet_type
            )
            
        if hasattr(self.booking_data, 'pet_age') and self.booking_data.pet_age:
            self.create_detail_row(
                details_container,
                "Pet Age:",
                f"{self.booking_data.pet_age} years"
            )
            
        # Add special notes if available
        if hasattr(self.booking_data, 'notes') and self.booking_data.notes:
            notes_frame = tk.Frame(details_container, bg="#ffffff")
            notes_frame.pack(fill=tk.X, pady=(15, 8))
            
            notes_label = ModernLabel(
                notes_frame,
                text="Special Notes:",
                style="body",
                bg="#ffffff"
            )
            notes_label.pack(anchor="w")
            
            notes_text = ModernLabel(
                notes_frame,
                text=self.booking_data.notes,
                style="body",
                bg="#ffffff",
                fg="#6b7280",
                wraplength=400,
                justify=tk.LEFT
            )
            notes_text.pack(anchor="w", padx=(20, 0))

    def create_detail_row(self, parent, label: str, value: str):
        """Create a detail row with label and value"""
        row_frame = tk.Frame(parent, bg="#ffffff")
        row_frame.pack(fill=tk.X, pady=8)
        
        label_widget = ModernLabel(
            row_frame,
            text=label,
            style="body",
            bg="#ffffff"
        )
        label_widget.pack(side=tk.LEFT)
        
        value_widget = ModernLabel(
            row_frame,
            text=value,
            style="body",
            bg="#ffffff",
            fg="#1f2937"
        )
        value_widget.pack(side=tk.RIGHT)
    
    def create_next_steps(self, parent):
        """Create next steps information"""
        steps_frame = ModernFrame(parent, bg_color="#eff6ff")
        steps_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(steps_frame, bg="#eff6ff")
        content.pack(expand=True, padx=30, pady=30)
        
        # Title
        title = ModernLabel(
            content,
            text="What's Next?",
            style="heading3",
            bg="#eff6ff",
            fg="#1e40af"
        )
        title.pack(pady=(0, 20))
        
        # Steps list
        steps = [
            "You'll receive a confirmation email shortly",
            "We'll send you a reminder 24 hours before your appointment",
            "Please arrive 10 minutes early for check-in",
            "Bring any special items your pet might need"
        ]
        
        for i, step in enumerate(steps, 1):
            step_frame = tk.Frame(content, bg="#eff6ff")
            step_frame.pack(fill=tk.X, pady=5)
            
            step_number = ModernLabel(
                step_frame,
                text=f"{i}.",
                style="body",
                bg="#eff6ff",
                fg="#1e40af"
            )
            step_number.pack(side=tk.LEFT, padx=(0, 10))
            
            step_text = ModernLabel(
                step_frame,
                text=step,
                style="body",
                bg="#eff6ff",
                wraplength=500,
                justify=tk.LEFT
            )
            step_text.pack(side=tk.LEFT)
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        actions_frame = ModernFrame(parent, bg_color="#ffffff")
        actions_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_container = tk.Frame(actions_frame, bg="#ffffff")
        button_container.pack(expand=True, pady=30)
        
        primary_frame = tk.Frame(button_container, bg="#ffffff")
        primary_frame.pack(pady=(0, 15))
        
        # Back to Home button (primary action)
        home_btn = ModernButton(
            primary_frame,
            text="🏠 Back to Home",
            command=lambda: self.on_complete(BookingStep.DISCOVERY),
            style="primary"
        )
        home_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # View My Bookings button
        view_btn = ModernButton(
            primary_frame,
            text="📋 View My Bookings",
            command=lambda: self.on_complete(BookingStep.MANAGEMENT),
            style="secondary"
        )
        view_btn.pack(side=tk.LEFT)
        
        # Secondary actions
        secondary_frame = tk.Frame(button_container, bg="#ffffff")
        secondary_frame.pack(pady=(10, 0))
        
        # Add to calendar button
        calendar_btn = ModernButton(
            secondary_frame,
            text="📅 Add to Calendar",
            command=self.add_to_calendar,
            style="secondary"
        )
        calendar_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Book another service
        book_another_btn = ModernButton(
            secondary_frame,
            text="➕ Book Another Service",
            command=lambda: self.on_complete(BookingStep.DISCOVERY),
            style="secondary"
        )
        book_another_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Share booking
        share_btn = ModernButton(
            secondary_frame,
            text="📤 Share Booking",
            command=self.share_booking,
            style="secondary"
        )
        share_btn.pack(side=tk.LEFT)
    
    def add_to_calendar(self):
        """Add booking to calendar (mock implementation)"""
        messagebox.showinfo(
            "Calendar",
            "Calendar integration would open here.\n\n"
            f"Event: {self.booking_data.service.title if self.booking_data.service else 'Pet Service'}\n"
            f"Date: {self.booking_data.date}\n"
            f"Time: {self.booking_data.time}"
        )
    
    def share_booking(self):
        """Share booking details (mock implementation)"""
        booking_details = f"""
Pet Service Booking Confirmed!

Service: {self.booking_data.service.title if self.booking_data.service else 'N/A'}
Date: {self.booking_data.date}
Time: {self.booking_data.time}
Pet: {self.booking_data.pet_name} ({self.booking_data.pet_type})
Booking ID: {self.booking_data.booking_id}

Book your pet services at PawCare!
        """.strip()
        
        # Copy to clipboard (mock)
        messagebox.showinfo(
            "Share Booking",
            "Booking details copied to clipboard!\n\n" + booking_details
        )
    
    def get_service_category(self, service_title: str) -> str:
        """Get service category based on service title"""
        title_lower = service_title.lower()
        if 'grooming' in title_lower:
            return "Grooming & Beauty"
        elif 'veterinary' in title_lower or 'checkup' in title_lower:
            return "Health & Medical"
        elif 'sitting' in title_lower:
            return "Pet Care"
        elif 'walking' in title_lower:
            return "Exercise & Activity"
        elif 'training' in title_lower:
            return "Training & Behavior"
        else:
            return "Pet Services"
