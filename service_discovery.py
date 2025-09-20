"""
Service Discovery Screen - Landing page with service showcase
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard, ModernScrollableFrame
from data_models import BookingStep, SAMPLE_SERVICES

class ServiceDiscoveryFrame(ModernScrollableFrame):
    """Service discovery landing page"""
    
    def __init__(self, parent, booking_data, on_complete: Callable):
        super().__init__(parent, bg="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        
        self.create_content()
    
    def create_content(self):
        """Create the service discovery content"""
        container = self.scrollable_frame
        
        # Hero Section
        self.create_hero_section(container)
        
        # Services Grid
        self.create_services_section(container)
        
        # Trust Indicators
        self.create_trust_section(container)
        
        # Call to Action
        self.create_cta_section(container)
    
    def create_hero_section(self, parent):
        """Create hero section with main call-to-action"""
        hero_frame = ModernFrame(parent, bg_color="#ffffff")
        hero_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Hero content
        hero_content = tk.Frame(hero_frame, bg="#ffffff")
        hero_content.pack(expand=True, pady=40)
        
        # Main heading
        heading = ModernLabel(
            hero_content,
            text="Professional Pet Care Services",
            style="heading1"
        )
        heading.pack(pady=(0, 10))
        
        # Subheading
        subheading = ModernLabel(
            hero_content,
            text="Book trusted, professional pet services with just a few clicks.\nYour furry friends deserve the best care.",
            style="body",
            justify=tk.CENTER
        )
        subheading.pack(pady=(0, 30))
        
        # CTA Buttons
        button_frame = tk.Frame(hero_content, bg="#ffffff")
        button_frame.pack()
        
        book_btn = ModernButton(
            button_frame,
            text="Book a Service",
            command=lambda: self.on_complete(BookingStep.SELECTION),
            style="primary"
        )
        book_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        manage_btn = ModernButton(
            button_frame,
            text="Manage Bookings",
            command=lambda: self.on_complete(BookingStep.MANAGEMENT),
            style="secondary"
        )
        manage_btn.pack(side=tk.LEFT)
    
    def create_services_section(self, parent):
        """Create services showcase grid"""
        services_frame = ModernFrame(parent, bg_color="#f8fafc")
        services_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Section header
        header_frame = tk.Frame(services_frame, bg="#f8fafc")
        header_frame.pack(fill=tk.X, pady=(30, 20))
        
        title = ModernLabel(
            header_frame,
            text="Our Services",
            style="heading2"
        )
        title.pack()
        
        subtitle = ModernLabel(
            header_frame,
            text="Choose from our range of professional pet care services",
            style="body"
        )
        subtitle.pack(pady=(5, 0))
        
        # Services grid
        grid_frame = tk.Frame(services_frame, bg="#f8fafc")
        grid_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Create service cards in a 3-column grid
        for i, service in enumerate(SAMPLE_SERVICES):
            row = i // 3
            col = i % 3
            
            service_card = self.create_service_card(grid_frame, service)
            service_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
    
    def create_service_card(self, parent, service):
        """Create individual service card"""
        card = ModernCard(parent)
        card.configure(width=300, height=350)
        
        # Popular badge
        if service.popular:
            badge = ModernLabel(
                card,
                text="POPULAR",
                style="small",
                font=("Segoe UI", 8, "bold"),
                fg="white"
            )
            badge.configure(bg="#10b981", padx=8, pady=2)
            badge.pack(anchor="ne", pady=(0, 10))
        
        # Service image placeholder
        image_frame = tk.Frame(card, bg="#e5e7eb", height=120)
        image_frame.pack(fill=tk.X, pady=(0, 15))
        image_frame.pack_propagate(False)
        
        image_label = ModernLabel(
            image_frame,
            text="🐾 Service Image",
            style="caption"
        )
        image_label.configure(bg="#e5e7eb")
        image_label.pack(expand=True)
        
        # Service title
        title = ModernLabel(
            card,
            text=service.title,
            style="heading4"
        )
        title.pack(anchor="w", pady=(0, 5))
        
        # Service description
        desc = ModernLabel(
            card,
            text=service.description,
            style="caption",
            wraplength=250,
            justify=tk.LEFT
        )
        desc.pack(anchor="w", pady=(0, 10))
        
        # Features
        if service.features:
            features_text = " • ".join(service.features[:3])
            if len(service.features) > 3:
                features_text += f" • +{len(service.features) - 3} more"
            
            features = ModernLabel(
                card,
                text=features_text,
                style="small",
                wraplength=250,
                justify=tk.LEFT
            )
            features.pack(anchor="w", pady=(0, 15))
        
        # Price and duration
        price_frame = tk.Frame(card, bg="#ffffff")
        price_frame.pack(fill=tk.X, pady=(0, 15))
        
        price = ModernLabel(
            price_frame,
            text=f"${service.price:.0f}",
            style="heading4"
        )
        price.pack(side=tk.LEFT)
        
        duration = ModernLabel(
            price_frame,
            text=service.duration,
            style="caption"
        )
        duration.pack(side=tk.RIGHT)
        
        # Book button
        book_btn = ModernButton(
            card,
            text="Select Service",
            command=lambda s=service: self.select_service(s),
            style="primary"
        )
        book_btn.pack(fill=tk.X)
        
        return card
    
    def create_trust_section(self, parent):
        """Create trust indicators section"""
        trust_frame = ModernFrame(parent, bg_color="#ffffff")
        trust_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Section content
        content_frame = tk.Frame(trust_frame, bg="#ffffff")
        content_frame.pack(expand=True, pady=30)
        
        # Title
        title = ModernLabel(
            content_frame,
            text="Trusted by Pet Owners",
            style="heading3"
        )
        title.pack(pady=(0, 20))
        
        # Stats grid
        stats_frame = tk.Frame(content_frame, bg="#ffffff")
        stats_frame.pack()
        
        stats = [
            ("5,000+", "Happy Pets"),
            ("4.9/5", "Average Rating"),
            ("24/7", "Support Available"),
            ("100%", "Insured Services")
        ]
        
        for i, (number, label) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg="#ffffff")
            stat_frame.grid(row=0, column=i, padx=30, pady=10)
            
            num_label = ModernLabel(
                stat_frame,
                text=number,
                style="heading2"
            )
            num_label.pack()
            
            desc_label = ModernLabel(
                stat_frame,
                text=label,
                style="caption"
            )
            desc_label.pack()
    
    def create_cta_section(self, parent):
        """Create final call-to-action section"""
        cta_frame = ModernFrame(parent, bg_color="#3b82f6")
        cta_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # CTA content
        content_frame = tk.Frame(cta_frame, bg="#3b82f6")
        content_frame.pack(expand=True, pady=40)
        
        # Heading
        heading = ModernLabel(
            content_frame,
            text="Ready to Book?",
            style="heading2",
            fg="white"
        )
        heading.configure(bg="#3b82f6")
        heading.pack(pady=(0, 10))
        
        # Description
        desc = ModernLabel(
            content_frame,
            text="Join thousands of satisfied pet owners who trust us with their furry friends.",
            style="body",
            fg="white"
        )
        desc.configure(bg="#3b82f6")
        desc.pack(pady=(0, 20))
        
        # CTA Button
        cta_btn = ModernButton(
            content_frame,
            text="Start Booking Now",
            command=lambda: self.on_complete(BookingStep.SELECTION),
            style="secondary"
        )
        cta_btn.pack()
    
    def select_service(self, service):
        """Handle service selection"""
        self.booking_data.update({"service": service})
        self.on_complete(BookingStep.SCHEDULING)
