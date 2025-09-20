"""
Booking Management Screen - View and manage existing bookings
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, List
from datetime import datetime, timedelta
from ui_components import ModernFrame, ModernButton, ModernLabel, ModernCard, ModernScrollableFrame
from data_models import BookingStep, Service, SAMPLE_SERVICES
import json
import os

class BookingManagementFrame(ModernScrollableFrame):
    """Booking management interface"""
    
    def __init__(self, parent, booking_data, on_complete: Callable):
        super().__init__(parent, bg="#f8fafc")
        
        self.booking_data = booking_data
        self.on_complete = on_complete
        
        # Mock bookings data
        self.bookings = self.load_mock_bookings()
        
        # Current tab
        self.current_tab = "upcoming"
        
        self.create_content()
    
    def load_mock_bookings(self) -> List[Dict[str, Any]]:
        """Load mock bookings data"""
        # Add current booking if it exists
        bookings = []
        
        if self.booking_data.is_complete():
            current_booking = {
                "id": self.booking_data.booking_id or "CURRENT",
                "service": self.booking_data.service.__dict__ if self.booking_data.service else None,
                "date": self.booking_data.date,
                "time": self.booking_data.time,
                "pet_name": self.booking_data.pet_name,
                "pet_type": self.booking_data.pet_type,
                "status": "confirmed",
                "created_at": datetime.now().isoformat()
            }
            bookings.append(current_booking)
        
        # Add some mock historical bookings
        mock_bookings = [
            {
                "id": "BOOK001",
                "service": SAMPLE_SERVICES[0].__dict__,
                "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "time": "10:00 AM",
                "pet_name": "Buddy",
                "pet_type": "Dog",
                "status": "confirmed",
                "created_at": (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                "id": "BOOK002",
                "service": SAMPLE_SERVICES[1].__dict__,
                "date": (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
                "time": "2:00 PM",
                "pet_name": "Whiskers",
                "pet_type": "Cat",
                "status": "completed",
                "created_at": (datetime.now() - timedelta(days=16)).isoformat()
            },
            {
                "id": "BOOK003",
                "service": SAMPLE_SERVICES[2].__dict__,
                "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "time": "11:00 AM",
                "pet_name": "Max",
                "pet_type": "Dog",
                "status": "completed",
                "created_at": (datetime.now() - timedelta(days=32)).isoformat()
            }
        ]
        
        bookings.extend(mock_bookings)
        return bookings
    
    def create_content(self):
        """Create booking management content"""
        container = self.scrollable_frame
        
        # Header
        self.create_header(container)
        
        # Tab navigation
        self.create_tab_navigation(container)
        
        # Bookings list
        self.create_bookings_list(container)
        
        # Action buttons
        self.create_action_buttons(container)
    
    def create_header(self, parent):
        """Create page header"""
        header_frame = ModernFrame(parent, bg_color="#ffffff")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        content = tk.Frame(header_frame, bg="#ffffff")
        content.pack(expand=True, pady=30)
        
        title = ModernLabel(
            content,
            text="My Bookings",
            style="heading2",
            bg="#ffffff"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ModernLabel(
            content,
            text="Manage your pet service appointments",
            style="body",
            bg="#ffffff"
        )
        subtitle.pack()
    
    def create_tab_navigation(self, parent):
        """Create tab navigation"""
        tab_frame = ModernFrame(parent, bg_color="#ffffff")
        tab_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tab_container = tk.Frame(tab_frame, bg="#ffffff")
        tab_container.pack(expand=True, pady=20)
        
        # Upcoming tab
        upcoming_btn = tk.Button(
            tab_container,
            text="Upcoming",
            font=("Segoe UI", 12, "bold" if self.current_tab == "upcoming" else "normal"),
            bg="#3b82f6" if self.current_tab == "upcoming" else "#f3f4f6",
            fg="white" if self.current_tab == "upcoming" else "#374151",
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self.switch_tab("upcoming")
        )
        upcoming_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Past tab
        past_btn = tk.Button(
            tab_container,
            text="Past",
            font=("Segoe UI", 12, "bold" if self.current_tab == "past" else "normal"),
            bg="#3b82f6" if self.current_tab == "past" else "#f3f4f6",
            fg="white" if self.current_tab == "past" else "#374151",
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self.switch_tab("past")
        )
        past_btn.pack(side=tk.LEFT)
        
        # Booking count
        upcoming_count = len(self.get_upcoming_bookings())
        past_count = len(self.get_past_bookings())
        
        count_text = f"{upcoming_count} upcoming, {past_count} completed"
        count_label = ModernLabel(
            tab_container,
            text=count_text,
            style="caption",
            bg="#ffffff"
        )
        count_label.pack(side=tk.RIGHT, padx=(20, 0))
    
    def create_bookings_list(self, parent):
        """Create bookings list based on current tab"""
        list_frame = ModernFrame(parent, bg_color="#f8fafc")
        list_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Get bookings for current tab
        if self.current_tab == "upcoming":
            bookings = self.get_upcoming_bookings()
            empty_message = "No upcoming bookings"
        else:
            bookings = self.get_past_bookings()
            empty_message = "No past bookings"
        
        if not bookings:
            # Empty state
            empty_frame = tk.Frame(list_frame, bg="#f8fafc")
            empty_frame.pack(expand=True, pady=60)
            
            empty_label = ModernLabel(
                empty_frame,
                text=empty_message,
                style="body",
                bg="#f8fafc"
            )
            empty_label.pack()
            
            if self.current_tab == "upcoming":
                book_btn = ModernButton(
                    empty_frame,
                    text="Book a Service",
                    command=lambda: self.on_complete(BookingStep.DISCOVERY),
                    style="primary"
                )
                book_btn.pack(pady=(20, 0))
        else:
            # Bookings list
            bookings_container = tk.Frame(list_frame, bg="#f8fafc")
            bookings_container.pack(fill=tk.X, padx=20, pady=20)
            
            for booking in bookings:
                booking_card = self.create_booking_card(bookings_container, booking)
                booking_card.pack(fill=tk.X, pady=(0, 15))
    
    def create_booking_card(self, parent, booking: Dict[str, Any]):
        """Create individual booking card"""
        card = ModernCard(parent)
        
        # Status badge
        status_color = {
            "confirmed": "#10b981",
            "completed": "#6b7280",
            "cancelled": "#ef4444"
        }.get(booking["status"], "#6b7280")
        
        status_badge = tk.Label(
            card,
            text=booking["status"].upper(),
            font=("Segoe UI", 9, "bold"),
            bg=status_color,
            fg="white",
            padx=10,
            pady=4
        )
        status_badge.pack(anchor="ne", pady=(0, 15))
        
        # Main content
        content_frame = tk.Frame(card, bg="#ffffff")
        content_frame.pack(fill=tk.X)
        
        # Left side - Service info
        left_frame = tk.Frame(content_frame, bg="#ffffff")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Service title
        service_title = booking["service"]["title"] if booking["service"] else "Unknown Service"
        title = ModernLabel(
            left_frame,
            text=service_title,
            style="heading4",
            bg="#ffffff"
        )
        title.pack(anchor="w", pady=(0, 5))
        
        # Date and time
        if booking["date"] and booking["time"]:
            date_obj = datetime.strptime(booking["date"], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            
            datetime_text = f"{formatted_date} at {booking['time']}"
            datetime_label = ModernLabel(
                left_frame,
                text=datetime_text,
                style="body",
                bg="#ffffff"
            )
            datetime_label.pack(anchor="w", pady=(0, 5))
        
        # Pet info
        if booking["pet_name"] and booking["pet_type"]:
            pet_text = f"Pet: {booking['pet_name']} ({booking['pet_type']})"
            pet_label = ModernLabel(
                left_frame,
                text=pet_text,
                style="caption",
                bg="#ffffff"
            )
            pet_label.pack(anchor="w", pady=(0, 5))
        
        # Booking ID
        booking_id = ModernLabel(
            left_frame,
            text=f"ID: {booking['id']}",
            style="small",
            bg="#ffffff"
        )
        booking_id.pack(anchor="w")
        
        # Right side - Price and actions
        right_frame = tk.Frame(content_frame, bg="#ffffff")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Price
        if booking["service"]:
            price = ModernLabel(
                right_frame,
                text=f"${booking['service']['price']:.0f}",
                style="heading4",
                bg="#ffffff",
                fg="#10b981"
            )
            price.pack(anchor="e", pady=(0, 15))
        
        # Action buttons
        if booking["status"] == "confirmed":
            # Upcoming booking actions
            reschedule_btn = ModernButton(
                right_frame,
                text="Reschedule",
                command=lambda b=booking: self.reschedule_booking(b),
                style="secondary"
            )
            reschedule_btn.pack(fill=tk.X, pady=(0, 5))
            
            cancel_btn = ModernButton(
                right_frame,
                text="Cancel",
                command=lambda b=booking: self.cancel_booking(b),
                style="danger"
            )
            cancel_btn.pack(fill=tk.X)
        
        elif booking["status"] == "completed":
            # Past booking actions
            rebook_btn = ModernButton(
                right_frame,
                text="Book Again",
                command=lambda b=booking: self.rebook_service(b),
                style="primary"
            )
            rebook_btn.pack(fill=tk.X, pady=(0, 5))
            
            review_btn = ModernButton(
                right_frame,
                text="Leave Review",
                command=lambda b=booking: self.leave_review(b),
                style="secondary"
            )
            review_btn.pack(fill=tk.X)
        
        return card
    
    def create_action_buttons(self, parent):
        """Create main action buttons"""
        actions_frame = ModernFrame(parent, bg_color="#ffffff")
        actions_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_container = tk.Frame(actions_frame, bg="#ffffff")
        button_container.pack(expand=True, pady=30)
        
        # Book new service
        book_btn = ModernButton(
            button_container,
            text="Book New Service",
            command=lambda: self.on_complete(BookingStep.DISCOVERY),
            style="primary"
        )
        book_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Export bookings
        export_btn = ModernButton(
            button_container,
            text="Export Bookings",
            command=self.export_bookings,
            style="secondary"
        )
        export_btn.pack(side=tk.LEFT)
    
    def get_upcoming_bookings(self) -> List[Dict[str, Any]]:
        """Get upcoming bookings"""
        today = datetime.now().date()
        upcoming = []
        
        for booking in self.bookings:
            if booking["status"] == "confirmed" and booking["date"]:
                booking_date = datetime.strptime(booking["date"], "%Y-%m-%d").date()
                if booking_date >= today:
                    upcoming.append(booking)
        
        # Sort by date
        upcoming.sort(key=lambda x: x["date"])
        return upcoming
    
    def get_past_bookings(self) -> List[Dict[str, Any]]:
        """Get past bookings"""
        today = datetime.now().date()
        past = []
        
        for booking in self.bookings:
            if booking["status"] in ["completed", "cancelled"]:
                past.append(booking)
            elif booking["date"]:
                booking_date = datetime.strptime(booking["date"], "%Y-%m-%d").date()
                if booking_date < today:
                    past.append(booking)
        
        # Sort by date (most recent first)
        past.sort(key=lambda x: x["date"], reverse=True)
        return past
    
    def switch_tab(self, tab: str):
        """Switch between tabs"""
        self.current_tab = tab
        
        # Refresh content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_content()
    
    def reschedule_booking(self, booking: Dict[str, Any]):
        """Reschedule a booking"""
        messagebox.showinfo(
            "Reschedule Booking",
            f"Rescheduling booking {booking['id']}.\n\n"
            "This would open the scheduling interface with the current booking pre-selected."
        )
    
    def cancel_booking(self, booking: Dict[str, Any]):
        """Cancel a booking"""
        result = messagebox.askyesno(
            "Cancel Booking",
            f"Are you sure you want to cancel booking {booking['id']}?\n\n"
            "This action cannot be undone."
        )
        
        if result:
            # Update booking status
            for b in self.bookings:
                if b["id"] == booking["id"]:
                    b["status"] = "cancelled"
                    break
            
            # Refresh display
            self.switch_tab(self.current_tab)
            
            messagebox.showinfo("Booking Cancelled", "Your booking has been cancelled.")
    
    def rebook_service(self, booking: Dict[str, Any]):
        """Rebook the same service"""
        if booking["service"]:
            # Create service object from booking data
            service_data = booking["service"]
            from data_models import Service
            
            try:
                service = Service(
                    id=service_data["id"],
                    title=service_data["title"],
                    description=service_data["description"],
                    price=service_data["price"],
                    duration=service_data["duration"],
                    image=service_data["image"],
                    features=service_data.get("features", []),
                    popular=service_data.get("popular", False)
                )
                
                # Pre-select the service and go to scheduling
                self.booking_data.update({"service": service})
                self.on_complete(BookingStep.SCHEDULING)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Unable to rebook service: {str(e)}"
                )
    
    def leave_review(self, booking: Dict[str, Any]):
        """Leave a review for completed service"""
        messagebox.showinfo(
            "Leave Review",
            f"Review interface for booking {booking['id']} would open here.\n\n"
            "This would allow rating the service and leaving feedback."
        )
    
    def export_bookings(self):
        """Export bookings data"""
        messagebox.showinfo(
            "Export Bookings",
            "Booking data would be exported to CSV/PDF format.\n\n"
            f"Total bookings: {len(self.bookings)}\n"
            f"Upcoming: {len(self.get_upcoming_bookings())}\n"
            f"Completed: {len(self.get_past_bookings())}"
        )
