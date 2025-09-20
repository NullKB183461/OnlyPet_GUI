"""
Service Selection Screen - Detailed service comparison and selection
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, Optional
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard, ModernScrollableFrame
from data_models import BookingStep, SAMPLE_SERVICES, Service

class ServiceSelectionFrame(ModernScrollableFrame):
    """Service selection with detailed comparison"""
    
    def __init__(self, parent, booking_data, on_complete: Callable, on_back: Callable):
        super().__init__(parent, bg="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        self.on_back = on_back
        self.selected_service = booking_data.service
        
        self.create_content()
    
    def create_content(self):
        """Create the service selection content"""
        container = self.scrollable_frame
        
        # Header
        self.create_header(container)
        
        # Services comparison
        self.create_services_comparison(container)
        
        # Navigation
        self.create_navigation(container)
    
    def create_header(self, parent):
        """Create page header"""
        header_frame = ModernFrame(parent, bg="#ffffff")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(header_frame, bg="#ffffff")
        content.pack(expand=True, pady=30)
        
        # Title
        title = ModernLabel(
            content,
            text="Choose Your Service",
            style="heading2",
            bg="#ffffff"
        )
        title.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = ModernLabel(
            content,
            text="Compare our services and select the one that best fits your pet's needs",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
    
    def create_services_comparison(self, parent):
        """Create detailed service comparison"""
        comparison_frame = ModernFrame(parent, bg="#f8fafc")
        comparison_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Services grid
        grid_frame = tk.Frame(comparison_frame, bg="#f8fafc")
        grid_frame.pack(fill=tk.X, padx=20, pady=30)
        
        # Create detailed service cards
        for i, service in enumerate(SAMPLE_SERVICES):
            row = i // 2
            col = i % 2
            
            service_card = self.create_detailed_service_card(grid_frame, service)
            service_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configure grid weights
        for i in range(2):
            grid_frame.columnconfigure(i, weight=1)
    
    def create_detailed_service_card(self, parent, service: Service):
        """Create detailed service card with selection"""
        is_selected = self.selected_service and self.selected_service.id == service.id
        
        card_bg = "#eff6ff" if is_selected else "#ffffff"
        border_color = "#3b82f6" if is_selected else "#e5e7eb"
        
        card = ModernCard(parent, bg_color=card_bg, border_color=border_color)
        
        # Selection indicator
        if is_selected:
            selected_badge = tk.Label(
                card,
                text="✓ SELECTED",
                font=("Segoe UI", 9, "bold"),
                bg="#3b82f6",
                fg="white",
                padx=10,
                pady=4
            )
            selected_badge.pack(anchor="ne", pady=(0, 15))
        
        # Popular badge
        if service.popular:
            popular_badge = tk.Label(
                card,
                text="MOST POPULAR",
                font=("Segoe UI", 8, "bold"),
                bg="#10b981",
                fg="white",
                padx=8,
                pady=2
            )
            popular_badge.pack(anchor="nw" if not is_selected else "n", pady=(0, 10))
        
        # Service image placeholder
        image_frame = tk.Frame(card, bg="#e5e7eb", height=150)
        image_frame.pack(fill=tk.X, pady=(0, 20))
        image_frame.pack_propagate(False)
        
        image_label = ModernLabel(
            image_frame,
            text=f"🐾 {service.title}",
            style="body",
            bg="#e5e7eb"
        )
        image_label.pack(expand=True)
        
        # Service details
        details_frame = tk.Frame(card, bg=card_bg)
        details_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title and price
        title_frame = tk.Frame(details_frame, bg=card_bg)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title = ModernLabel(
            title_frame,
            text=service.title,
            style="heading3",
            bg=card_bg
        )
        title.pack(side=tk.LEFT)
        
        price = ModernLabel(
            title_frame,
            text=f"${service.price:.0f}",
            style="heading3",
            bg=card_bg,
            fg="#10b981"
        )
        price.pack(side=tk.RIGHT)
        
        # Duration
        duration = ModernLabel(
            details_frame,
            text=f"Duration: {service.duration}",
            style="caption",
            bg=card_bg
        )
        duration.pack(anchor="w", pady=(0, 10))
        
        # Description
        desc = ModernLabel(
            details_frame,
            text=service.description,
            style="body",
            bg=card_bg,
            wraplength=350,
            justify=tk.LEFT
        )
        desc.pack(anchor="w", pady=(0, 15))
        
        # Features list
        if service.features:
            features_label = ModernLabel(
                details_frame,
                text="What's included:",
                style="heading4",
                bg=card_bg
            )
            features_label.pack(anchor="w", pady=(0, 5))
            
            for feature in service.features:
                feature_frame = tk.Frame(details_frame, bg=card_bg)
                feature_frame.pack(fill=tk.X, pady=2)
                
                bullet = ModernLabel(
                    feature_frame,
                    text="✓",
                    style="body",
                    bg=card_bg,
                    fg="#10b981"
                )
                bullet.pack(side=tk.LEFT, padx=(0, 8))
                
                feature_text = ModernLabel(
                    feature_frame,
                    text=feature,
                    style="body",
                    bg=card_bg
                )
                feature_text.pack(side=tk.LEFT)
        
        # Selection button
        button_text = "Selected" if is_selected else "Select This Service"
        button_style = "success" if is_selected else "primary"
        
        select_btn = ModernButton(
            card,
            text=button_text,
            command=lambda s=service: self.select_service(s),
            style=button_style
        )
        select_btn.pack(fill=tk.X, pady=(20, 0))
        
        return card
    
    def create_navigation(self, parent):
        """Create navigation buttons"""
        nav_frame = ModernFrame(parent, bg="#ffffff")
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_frame = tk.Frame(nav_frame, bg="#ffffff")
        button_frame.pack(expand=True, pady=20)
        
        # Back button
        back_btn = ModernButton(
            button_frame,
            text="← Back",
            command=self.on_back,
            style="secondary"
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Continue button
        continue_btn = ModernButton(
            button_frame,
            text="Continue to Scheduling →",
            command=self.continue_to_scheduling,
            style="primary"
        )
        continue_btn.pack(side=tk.LEFT)
        
        # Update button state
        if not self.selected_service:
            continue_btn.configure(state="disabled")
    
    def select_service(self, service: Service):
        """Handle service selection"""
        self.selected_service = service
        self.booking_data.update({"service": service})
        
        # Refresh the display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_content()
    
    def continue_to_scheduling(self):
        """Continue to scheduling step"""
        if self.selected_service:
            self.on_complete(BookingStep.SCHEDULING)
