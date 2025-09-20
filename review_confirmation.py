"""
Review & Confirmation Screen - Final booking review before confirmation
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any
from datetime import datetime
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard
from data_models import BookingStep

class ReviewConfirmationFrame(ModernFrame):
    """Review and confirmation interface"""
    
    def __init__(self, parent, booking_data, on_complete: Callable, on_back: Callable, on_edit: Callable):
        super().__init__(parent, bg_color="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        self.on_back = on_back
        self.on_edit = on_edit
        
        self.create_content()
    
    def create_content(self):
        """Create review and confirmation content"""
        # Header
        self.create_header()
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Main content in scrollable frame
        main_frame = tk.Frame(scrollable_frame, bg="#f8fafc")
        main_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left column - Booking details
        left_frame = ModernFrame(main_frame, bg_color="#ffffff")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_booking_details(left_frame)
        
        # Right column - Summary and actions
        right_frame = ModernFrame(main_frame, bg_color="#ffffff")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.configure(width=350)
        
        self.create_summary_sidebar(right_frame)
        
        self.create_navigation(scrollable_frame)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_header(self):
        """Create page header"""
        header_frame = ModernFrame(self, bg_color="#ffffff")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(header_frame, bg="#ffffff")
        content.pack(expand=True, pady=20)
        
        title = ModernLabel(
            content,
            text="Review Your Booking",
            style="heading2",
            bg="#ffffff"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ModernLabel(
            content,
            text="Please review all details before confirming your appointment",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
    
    def create_booking_details(self, parent):
        """Create detailed booking review"""
        details_frame = tk.Frame(parent, bg="#ffffff")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Service Details Section
        self.create_review_section(
            details_frame,
            "Service Details",
            self.get_service_details(),
            lambda: self.on_edit(BookingStep.SELECTION)
        )
        
        # Appointment Details Section
        self.create_review_section(
            details_frame,
            "Appointment Details",
            self.get_appointment_details(),
            lambda: self.on_edit(BookingStep.SCHEDULING)
        )
        
        # Pet Information Section
        self.create_review_section(
            details_frame,
            "Pet Information",
            self.get_pet_details(),
            lambda: self.on_edit(BookingStep.PET_INFO)
        )
        
        # Terms and Conditions
        self.create_terms_section(details_frame)
    
    def create_review_section(self, parent, title: str, details: Dict[str, str], edit_callback: Callable):
        """Create a review section with edit capability"""
        section_frame = tk.Frame(parent, bg="#ffffff")
        section_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg="#ffffff")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        section_title = ModernLabel(
            header_frame,
            text=title,
            style="heading3",
            bg="#ffffff"
        )
        section_title.pack(side=tk.LEFT)
        
        edit_btn = ModernButton(
            header_frame,
            text="Edit",
            command=edit_callback,
            style="secondary"
        )
        edit_btn.pack(side=tk.RIGHT)
        
        # Section content
        content_frame = tk.Frame(section_frame, bg="#f8fafc", padx=20, pady=20)
        content_frame.pack(fill=tk.X)
        
        for label, value in details.items():
            detail_frame = tk.Frame(content_frame, bg="#f8fafc")
            detail_frame.pack(fill=tk.X, pady=5)
            
            label_widget = ModernLabel(
                detail_frame,
                text=f"{label}:",
                style="body",
                bg="#f8fafc"
            )
            label_widget.pack(side=tk.LEFT)
            
            value_widget = ModernLabel(
                detail_frame,
                text=value,
                style="body",
                bg="#f8fafc",
                fg="#1f2937"
            )
            value_widget.pack(side=tk.RIGHT)
    
    def create_terms_section(self, parent):
        """Create terms and conditions section"""
        terms_frame = tk.Frame(parent, bg="#ffffff")
        terms_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ModernLabel(
            terms_frame,
            text="Terms & Conditions",
            style="heading3",
            bg="#ffffff"
        )
        title.pack(anchor="w", pady=(0, 15))
        
        terms_content = tk.Frame(terms_frame, bg="#f8fafc", padx=20, pady=20)
        terms_content.pack(fill=tk.X)
        
        terms_text = [
            "• Cancellation must be made at least 24 hours in advance",
            "• Late arrivals may result in shortened service time",
            "• Payment is due at the time of service",
            "• All pets must be up to date on vaccinations",
            "• We reserve the right to refuse service for aggressive pets"
        ]
        
        for term in terms_text:
            term_label = ModernLabel(
                terms_content,
                text=term,
                style="body",
                bg="#f8fafc",
                wraplength=500,
                justify=tk.LEFT
            )
            term_label.pack(anchor="w", pady=2)
        
        # Agreement checkbox
        agreement_frame = tk.Frame(terms_frame, bg="#ffffff")
        agreement_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.agree_var = tk.BooleanVar()
        agree_check = tk.Checkbutton(
            agreement_frame,
            text="I agree to the terms and conditions",
            variable=self.agree_var,
            font=("Segoe UI", 11),
            bg="#ffffff",
            command=self.update_confirm_button
        )
        agree_check.pack(anchor="w")
    
    def create_summary_sidebar(self, parent):
        """Create booking summary sidebar"""
        summary_frame = tk.Frame(parent, bg="#ffffff")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)
        
        # Title
        title = ModernLabel(
            summary_frame,
            text="Booking Summary",
            style="heading3",
            bg="#ffffff"
        )
        title.pack(pady=(0, 20))
        
        # Service summary
        if self.booking_data.service:
            service_card = tk.Frame(summary_frame, bg="#f8fafc", padx=15, pady=15)
            service_card.pack(fill=tk.X, pady=(0, 15))
            
            service_name = ModernLabel(
                service_card,
                text=self.booking_data.service.title,
                style="heading4",
                bg="#f8fafc"
            )
            service_name.pack(anchor="w")
            
            service_price = ModernLabel(
                service_card,
                text=f"${self.booking_data.service.price:.2f}",
                style="heading4",
                bg="#f8fafc",
                fg="#10b981"
            )
            service_price.pack(anchor="w", pady=(5, 0))
            
            service_duration = ModernLabel(
                service_card,
                text=f"Duration: {self.booking_data.service.duration}",
                style="caption",
                bg="#f8fafc"
            )
            service_duration.pack(anchor="w")
        
        # Pricing breakdown
        pricing_frame = tk.Frame(summary_frame, bg="#ffffff")
        pricing_frame.pack(fill=tk.X, pady=(0, 20))
        
        pricing_title = ModernLabel(
            pricing_frame,
            text="Pricing",
            style="heading4",
            bg="#ffffff"
        )
        pricing_title.pack(anchor="w", pady=(0, 10))
        
        # Service fee
        if self.booking_data.service:
            fee_frame = tk.Frame(pricing_frame, bg="#ffffff")
            fee_frame.pack(fill=tk.X, pady=2)
            
            fee_label = ModernLabel(
                fee_frame,
                text="Service Fee:",
                style="body",
                bg="#ffffff"
            )
            fee_label.pack(side=tk.LEFT)
            
            fee_value = ModernLabel(
                fee_frame,
                text=f"${self.booking_data.service.price:.2f}",
                style="body",
                bg="#ffffff"
            )
            fee_value.pack(side=tk.RIGHT)
        
        # Tax
        tax_frame = tk.Frame(pricing_frame, bg="#ffffff")
        tax_frame.pack(fill=tk.X, pady=2)
        
        tax_label = ModernLabel(
            tax_frame,
            text="Tax (8.5%):",
            style="body",
            bg="#ffffff"
        )
        tax_label.pack(side=tk.LEFT)
        
        tax_amount = self.booking_data.service.price * 0.085 if self.booking_data.service else 0
        tax_value = ModernLabel(
            tax_frame,
            text=f"${tax_amount:.2f}",
            style="body",
            bg="#ffffff"
        )
        tax_value.pack(side=tk.RIGHT)
        
        # Separator
        separator = tk.Frame(pricing_frame, bg="#e5e7eb", height=1)
        separator.pack(fill=tk.X, pady=10)
        
        # Total
        total_frame = tk.Frame(pricing_frame, bg="#ffffff")
        total_frame.pack(fill=tk.X, pady=2)
        
        total_label = ModernLabel(
            total_frame,
            text="Total:",
            style="heading4",
            bg="#ffffff"
        )
        total_label.pack(side=tk.LEFT)
        
        total_amount = (self.booking_data.service.price * 1.085) if self.booking_data.service else 0
        total_value = ModernLabel(
            total_frame,
            text=f"${total_amount:.2f}",
            style="heading4",
            bg="#ffffff",
            fg="#10b981"
        )
        total_value.pack(side=tk.RIGHT)
        
        # Confirm button
        self.confirm_btn = ModernButton(
            summary_frame,
            text="Confirm Booking",
            command=self.confirm_booking,
            style="primary"
        )
        self.confirm_btn.pack(fill=tk.X, pady=(30, 0))
        self.confirm_btn.configure(state="disabled")
    
    def create_navigation(self, parent):
        """Create navigation buttons"""
        nav_frame = ModernFrame(parent, bg_color="#ffffff")
        nav_frame.pack(fill=tk.X, pady=(30, 20))
        
        button_frame = tk.Frame(nav_frame, bg="#ffffff")
        button_frame.pack(expand=True, pady=20)
        
        # Back button
        back_btn = ModernButton(
            button_frame,
            text="← Back to Pet Info",
            command=self.on_back,
            style="secondary"
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Additional info text
        info_label = ModernLabel(
            button_frame,
            text="Review all details carefully before confirming",
            style="caption",
            bg="#ffffff",
            fg="#6b7280"
        )
        info_label.pack(side=tk.LEFT, padx=20)
    
    def get_service_details(self) -> Dict[str, str]:
        """Get service details for review"""
        if not self.booking_data.service:
            return {}
        
        details = {
            "Service Name": self.booking_data.service.title,
            "Service Type": self.get_service_category(),
            "Price": f"${self.booking_data.service.price:.2f}",
            "Duration": self.booking_data.service.duration,
            "Description": self.booking_data.service.description,
            "What's Included": self.get_service_inclusions(),
            "Preparation Required": self.get_preparation_notes(),
            "Service Location": "At our facility",
            "Estimated Completion": self.get_estimated_completion()
        }
        
        return details
    
    def get_service_category(self) -> str:
        """Get service category based on service title"""
        service_title = self.booking_data.service.title.lower()
        if "grooming" in service_title:
            return "Professional Grooming"
        elif "sitting" in service_title:
            return "Pet Care Service"
        elif "walking" in service_title:
            return "Exercise & Activity"
        elif "training" in service_title:
            return "Behavioral Training"
        elif "boarding" in service_title:
            return "Overnight Care"
        else:
            return "Pet Service"
    
    def get_service_inclusions(self) -> str:
        """Get what's included in the service"""
        service_title = self.booking_data.service.title.lower()
        if "basic grooming" in service_title:
            return "Bath, brush, nail trim, ear cleaning"
        elif "full grooming" in service_title:
            return "Bath, brush, haircut, nail trim, ear cleaning, teeth brushing"
        elif "sitting" in service_title:
            return "Feeding, playtime, companionship, basic care"
        elif "walking" in service_title:
            return "30-60 min walk, exercise, fresh air"
        elif "training" in service_title:
            return "Basic commands, behavioral guidance, progress report"
        else:
            return "Professional pet care service"
    
    def get_preparation_notes(self) -> str:
        """Get preparation notes for the service"""
        service_title = self.booking_data.service.title.lower()
        if "grooming" in service_title:
            return "Please ensure pet is up-to-date on vaccinations"
        elif "sitting" in service_title:
            return "Provide feeding schedule and emergency contacts"
        elif "walking" in service_title:
            return "Ensure pet is comfortable with leash"
        elif "training" in service_title:
            return "Bring favorite treats and any behavioral concerns"
        else:
            return "Follow pre-service instructions provided"
    
    def get_estimated_completion(self) -> str:
        """Get estimated completion time"""
        if not self.booking_data.time:
            return "TBD"
        
        from datetime import datetime, timedelta
        try:
            # Parse the time and add duration
            time_obj = datetime.strptime(self.booking_data.time, "%I:%M %p")
            
            # Extract duration number (assuming format like "2 hours" or "30 minutes")
            duration_str = self.booking_data.service.duration.lower()
            if "hour" in duration_str:
                hours = int(duration_str.split()[0])
                completion_time = time_obj + timedelta(hours=hours)
            elif "minute" in duration_str:
                minutes = int(duration_str.split()[0])
                completion_time = time_obj + timedelta(minutes=minutes)
            else:
                completion_time = time_obj + timedelta(hours=1)  # Default 1 hour
            
            return completion_time.strftime("%I:%M %p")
        except:
            return "TBD"

    def get_appointment_details(self) -> Dict[str, str]:
        """Get appointment details for review"""
        if not self.booking_data.date or not self.booking_data.time:
            return {}
        
        # Format date for display
        try:
            from datetime import datetime
            date_obj = datetime.strptime(self.booking_data.date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
        except:
            formatted_date = self.booking_data.date
        
        details = {
            "Date": formatted_date,
            "Time": self.booking_data.time,
            "Duration": self.booking_data.service.duration if self.booking_data.service else "TBD",
            "Estimated Completion": self.get_estimated_completion(),
            "Service Location": "At our facility",
            "Arrival Instructions": "Please arrive 10 minutes early"
        }
        
        return details
    
    def get_pet_details(self) -> Dict[str, str]:
        """Get pet details for review"""
        details = {}
        
        if self.booking_data.pet_name:
            details["Pet Name"] = self.booking_data.pet_name
        
        if self.booking_data.pet_type:
            details["Pet Type"] = self.booking_data.pet_type
        
        if self.booking_data.pet_age:
            details["Age"] = f"{self.booking_data.pet_age} years old"
        
        if self.booking_data.pet_weight:
            details["Weight"] = self.booking_data.pet_weight
        
        if self.booking_data.notes:
            details["Additional Information"] = self.booking_data.notes
        else:
            details["Additional Information"] = "None provided"
        
        return details
    
    def update_confirm_button(self):
        """Update confirm button state based on agreement"""
        if hasattr(self, 'confirm_btn'):
            state = "normal" if self.agree_var.get() else "disabled"
            self.confirm_btn.configure(state=state)
    
    def confirm_booking(self):
        """Confirm the booking"""
        if self.agree_var.get():
            # Generate booking ID
            import uuid
            booking_id = str(uuid.uuid4())[:8].upper()
            
            self.booking_data.update({
                "booking_id": booking_id,
                "created_at": datetime.now()
            })
            
            self.on_complete(BookingStep.SUCCESS)
