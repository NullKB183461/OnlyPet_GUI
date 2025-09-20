"""
Pet Information Screen - Pet details and special requirements form
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernEntry, ModernCard
from data_models import BookingStep, PET_TYPES, WEIGHT_CATEGORIES

class PetInformationFrame(ModernFrame):
    """Pet information form"""
    
    def __init__(self, parent, booking_data, on_complete: Callable, on_back: Callable):
        super().__init__(parent, bg_color="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        self.on_back = on_back
        
        # Form variables
        self.pet_name_var = tk.StringVar(value=booking_data.pet_name or "")
        self.pet_type_var = tk.StringVar(value=booking_data.pet_type or "")
        self.pet_age_var = tk.StringVar(value=str(booking_data.pet_age) if booking_data.pet_age else "")
        self.pet_weight_var = tk.StringVar(value=booking_data.pet_weight or "")
        self.notes_var = tk.StringVar(value=booking_data.notes or "")
        
        # Validation state
        self.validation_errors = {}
        
        self.create_content()
    
    def create_content(self):
        """Create pet information form"""
        # Header
        self.create_header()
        
        # Create scrollable canvas
        canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content in scrollable frame
        main_frame = tk.Frame(scrollable_frame, bg="#f8fafc")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form container
        form_container = tk.Frame(main_frame, bg="#f8fafc")
        form_container.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Pet details form
        left_frame = ModernFrame(form_container, bg_color="#ffffff")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_pet_form(left_frame)
        
        # Right column - Booking summary
        right_frame = ModernFrame(form_container, bg_color="#ffffff")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.configure(width=300)
        
        self.create_booking_summary(right_frame)
        
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
            text="Pet Information",
            style="heading2",
            bg="#ffffff"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ModernLabel(
            content,
            text="Tell us about your pet so we can provide the best care",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
    
    def create_pet_form(self, parent):
        """Create pet information form"""
        form_frame = tk.Frame(parent, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Pet Name
        self.create_form_field(
            form_frame,
            "Pet Name *",
            self.pet_name_var,
            "Enter your pet's name",
            required=True
        )
        
        # Pet Type
        type_frame = tk.Frame(form_frame, bg="#ffffff")
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        type_label = ModernLabel(
            type_frame,
            text="Pet Type *",
            style="heading4",
            bg="#ffffff"
        )
        type_label.pack(anchor="w", pady=(0, 5))
        
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.pet_type_var,
            values=PET_TYPES,
            state="readonly",
            font=("Segoe UI", 11),
            height=10
        )
        type_combo.pack(fill=tk.X, pady=(0, 5))
        type_combo.bind("<<ComboboxSelected>>", self.validate_form)
        
        if "pet_type" in self.validation_errors:
            error_label = ModernLabel(
                type_frame,
                text=self.validation_errors["pet_type"],
                style="small",
                bg="#ffffff",
                fg="#ef4444"
            )
            error_label.pack(anchor="w")
        
        # Pet Age
        self.create_form_field(
            form_frame,
            "Pet Age (years)",
            self.pet_age_var,
            "Enter age in years",
            validate_func=self.validate_age
        )
        
        # Pet Weight
        weight_frame = tk.Frame(form_frame, bg="#ffffff")
        weight_frame.pack(fill=tk.X, pady=(0, 20))
        
        weight_label = ModernLabel(
            weight_frame,
            text="Pet Weight",
            style="heading4",
            bg="#ffffff"
        )
        weight_label.pack(anchor="w", pady=(0, 5))
        
        weight_combo = ttk.Combobox(
            weight_frame,
            textvariable=self.pet_weight_var,
            values=WEIGHT_CATEGORIES,
            state="readonly",
            font=("Segoe UI", 11)
        )
        weight_combo.pack(fill=tk.X)
        
        # Additional Information
        additional_info_frame = tk.Frame(form_frame, bg="#ffffff")
        additional_info_frame.pack(fill=tk.X, pady=(30, 20))
        
        # Section title
        section_title = ModernLabel(
            additional_info_frame,
            text="Additional Information",
            style="heading3",
            bg="#ffffff"
        )
        section_title.pack(anchor="w", pady=(0, 10))
        
        # Description
        description = ModernLabel(
            additional_info_frame,
            text="Please provide any important details about your pet that will help us provide better care:",
            style="body",
            bg="#ffffff"
        )
        description.pack(anchor="w", pady=(0, 15))
        
        # Text area with better styling
        self.notes_text = tk.Text(
            additional_info_frame,
            height=6,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bd=2,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb",
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.notes_text.pack(fill=tk.X, pady=(0, 10))
        
        # Insert existing notes
        if self.booking_data.notes:
            self.notes_text.insert("1.0", self.booking_data.notes)
        
        # Bind text change event
        self.notes_text.bind("<KeyRelease>", self._on_notes_change)
        
        # Enhanced help text with examples
        help_text = ModernLabel(
            additional_info_frame,
            text="Examples: Allergies to specific foods or medications, behavioral notes (aggressive, anxious, friendly), medical conditions, special care instructions, preferred handling methods, etc.",
            style="small",
            bg="#ffffff",
            fg="#6b7280"
        )
        help_text.pack(anchor="w", pady=(0, 0))
        help_text.configure(wraplength=500)
    
    def _on_notes_change(self, event):
        """Handle notes text change"""
        content = self.notes_text.get("1.0", tk.END).strip()
        self.notes_var.set(content)
    
    def create_form_field(self, parent, label_text, variable, placeholder, required=False, validate_func=None):
        """Create a form field with label and validation"""
        field_frame = tk.Frame(parent, bg="#ffffff")
        field_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label
        label = ModernLabel(
            field_frame,
            text=label_text,
            style="heading4",
            bg="#ffffff"
        )
        label.pack(anchor="w", pady=(0, 5))
        
        # Entry
        entry = ModernEntry(
            field_frame,
            textvariable=variable,
            placeholder=placeholder,
            validate_func=validate_func
        )
        entry.pack(fill=tk.X, pady=(0, 5))
        
        # Bind validation
        variable.trace("w", lambda *args: self.validate_form())
        
        # Error message
        field_key = label_text.lower().replace(" *", "").replace(" ", "_")
        if field_key in self.validation_errors:
            error_label = ModernLabel(
                field_frame,
                text=self.validation_errors[field_key],
                style="small",
                bg="#ffffff",
                fg="#ef4444"
            )
            error_label.pack(anchor="w")
    
    def create_booking_summary(self, parent):
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
        
        # Service details
        if self.booking_data.service:
            service_frame = tk.Frame(summary_frame, bg="#f8fafc", padx=15, pady=15)
            service_frame.pack(fill=tk.X, pady=(0, 15))
            
            service_title = ModernLabel(
                service_frame,
                text=self.booking_data.service.title,
                style="heading4",
                bg="#f8fafc"
            )
            service_title.pack(anchor="w")
            
            service_price = ModernLabel(
                service_frame,
                text=f"${self.booking_data.service.price:.0f}",
                style="body",
                bg="#f8fafc",
                fg="#10b981"
            )
            service_price.pack(anchor="w", pady=(5, 0))
        
        # Date and time
        if self.booking_data.date and self.booking_data.time:
            datetime_frame = tk.Frame(summary_frame, bg="#f8fafc", padx=15, pady=15)
            datetime_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Format date
            from datetime import datetime
            date_obj = datetime.strptime(self.booking_data.date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            
            date_label = ModernLabel(
                datetime_frame,
                text="Date & Time",
                style="heading4",
                bg="#f8fafc"
            )
            date_label.pack(anchor="w")
            
            date_value = ModernLabel(
                datetime_frame,
                text=formatted_date,
                style="body",
                bg="#f8fafc"
            )
            date_value.pack(anchor="w", pady=(5, 0))
            
            time_value = ModernLabel(
                datetime_frame,
                text=self.booking_data.time,
                style="body",
                bg="#f8fafc"
            )
            time_value.pack(anchor="w")
        
        # Pet info preview
        pet_frame = tk.Frame(summary_frame, bg="#f8fafc", padx=15, pady=15)
        pet_frame.pack(fill=tk.X, pady=(0, 15))
        
        pet_title = ModernLabel(
            pet_frame,
            text="Pet Information",
            style="heading4",
            bg="#f8fafc"
        )
        pet_title.pack(anchor="w")
        
        if self.pet_name_var.get():
            pet_name = ModernLabel(
                pet_frame,
                text=f"Name: {self.pet_name_var.get()}",
                style="body",
                bg="#f8fafc"
            )
            pet_name.pack(anchor="w", pady=(5, 0))
        
        if self.pet_type_var.get():
            pet_type = ModernLabel(
                pet_frame,
                text=f"Type: {self.pet_type_var.get()}",
                style="body",
                bg="#f8fafc"
            )
            pet_type.pack(anchor="w")
    
    def create_navigation(self, parent):
        """Create navigation buttons"""
        nav_frame = ModernFrame(parent, bg_color="#ffffff")
        nav_frame.pack(fill=tk.X, padx=20, pady=(30, 20))
        
        button_frame = tk.Frame(nav_frame, bg="#ffffff")
        button_frame.pack(expand=True, pady=20)
        
        # Back button
        back_btn = ModernButton(
            button_frame,
            text="← Back to Schedule",
            command=self.on_back,
            style="secondary"
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Continue button
        self.continue_btn = ModernButton(
            button_frame,
            text="Continue to Review →",
            command=self.continue_to_review,
            style="primary"
        )
        self.continue_btn.pack(side=tk.LEFT)
        
        # Initial validation
        self.validate_form()
    
    def validate_age(self, value: str) -> bool:
        """Validate age input"""
        if not value:
            return True
        try:
            age = int(value)
            return 0 <= age <= 30
        except ValueError:
            return False
    
    def validate_form(self, *args):
        """Validate entire form"""
        self.validation_errors.clear()
        
        # Required fields
        if not self.pet_name_var.get().strip():
            self.validation_errors["pet_name"] = "Pet name is required"
        
        if not self.pet_type_var.get():
            self.validation_errors["pet_type"] = "Pet type is required"
        
        # Age validation
        if self.pet_age_var.get():
            try:
                age = int(self.pet_age_var.get())
                if age < 0 or age > 30:
                    self.validation_errors["pet_age"] = "Age must be between 0 and 30"
            except ValueError:
                self.validation_errors["pet_age"] = "Age must be a number"
        
        # Update continue button state
        is_valid = len(self.validation_errors) == 0
        if hasattr(self, 'continue_btn'):
            self.continue_btn.configure(state="normal" if is_valid else "disabled")
        
        return is_valid
    
    def continue_to_review(self):
        """Continue to review step"""
        if self.validate_form():
            # Update booking data
            pet_data = {
                "pet_name": self.pet_name_var.get().strip(),
                "pet_type": self.pet_type_var.get(),
                "pet_age": int(self.pet_age_var.get()) if self.pet_age_var.get() else None,
                "pet_weight": self.pet_weight_var.get(),
                "notes": self.notes_var.get().strip()
            }
            
            self.booking_data.update(pet_data)
            self.on_complete(BookingStep.REVIEW)
