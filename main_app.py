"""
Main Application - Pet Service Booking System
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from data_models import BookingData, BookingStep
from ui_components import ModernFrame

# Import all screens
from service_discovery import ServiceDiscoveryFrame
from service_selection import ServiceSelectionFrame
from date_time_scheduling import DateTimeSchedulingFrame
from pet_information import PetInformationFrame
from review_confirmation import ReviewConfirmationFrame
from booking_success import BookingSuccessFrame
from booking_management import BookingManagementFrame

class PetBookingApp:
    """Main application class for pet service booking"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Application state
        self.booking_data = BookingData()
        self.current_step = BookingStep.DISCOVERY
        self.current_frame: Optional[tk.Widget] = None
        
        # Start the application
        self.show_current_step()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("OnlyPets - Pet Service Booking")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8fafc")
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Configure window properties
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
    
    def show_current_step(self):
        """Display the current booking step"""
        # Clear current frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create new frame based on current step
        if self.current_step == BookingStep.DISCOVERY:
            self.current_frame = ServiceDiscoveryFrame(
                self.root,
                self.booking_data,
                self.on_step_complete
            )
        
        elif self.current_step == BookingStep.SELECTION:
            self.current_frame = ServiceSelectionFrame(
                self.root,
                self.booking_data,
                self.on_step_complete,
                self.on_step_back
            )
        
        elif self.current_step == BookingStep.SCHEDULING:
            self.current_frame = DateTimeSchedulingFrame(
                self.root,
                self.booking_data,
                self.on_step_complete,
                self.on_step_back
            )
        
        elif self.current_step == BookingStep.PET_INFO:
            self.current_frame = PetInformationFrame(
                self.root,
                self.booking_data,
                self.on_step_complete,
                self.on_step_back
            )
        
        elif self.current_step == BookingStep.REVIEW:
            self.current_frame = ReviewConfirmationFrame(
                self.root,
                self.booking_data,
                self.on_step_complete,
                self.on_step_back,
                self.on_edit_step
            )
        
        elif self.current_step == BookingStep.SUCCESS:
            self.current_frame = BookingSuccessFrame(
                self.root,
                self.booking_data,
                self.on_step_complete
            )
        
        elif self.current_step == BookingStep.MANAGEMENT:
            self.current_frame = BookingManagementFrame(
                self.root,
                self.booking_data,
                self.on_step_complete
            )
        
        # Pack the frame
        if self.current_frame:
            self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def on_step_complete(self, next_step: BookingStep):
        """Handle step completion"""
        self.current_step = next_step
        self.show_current_step()
    
    def on_step_back(self):
        """Handle back navigation"""
        # Define the step sequence
        step_sequence = [
            BookingStep.DISCOVERY,
            BookingStep.SELECTION,
            BookingStep.SCHEDULING,
            BookingStep.PET_INFO,
            BookingStep.REVIEW,
            BookingStep.SUCCESS
        ]
        
        try:
            current_index = step_sequence.index(self.current_step)
            if current_index > 0:
                self.current_step = step_sequence[current_index - 1]
                self.show_current_step()
        except ValueError:
            # If current step not in sequence, go to discovery
            self.current_step = BookingStep.DISCOVERY
            self.show_current_step()
    
    def on_edit_step(self, step: BookingStep):
        """Handle editing a specific step from review"""
        self.current_step = step
        self.show_current_step()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = PetBookingApp()
    app.run()

if __name__ == "__main__":
    main()
