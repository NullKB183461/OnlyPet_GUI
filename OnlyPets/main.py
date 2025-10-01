#!/usr/bin/env python3
"""
OnlyPets - Pet Adoption & Service Management System
A comprehensive tkinter-based application for pet adoption and care services.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from analytics import AnalyticsManager

class OnlyPetsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OnlyPets - Pet Adoption & Service Management")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize database and analytics
        self.db = DatabaseManager()
        self.analytics = AnalyticsManager("onlypets.db")
        self.current_user = None
        
        # Initialize form attributes
        self.signup_entries = {}
        self.signin_entries = {}
        self.adoption_entries = {}
        self.care_vars = {}
        self.agreement_var = None
        self.selected_category = None
        self.selected_product_category = None
        self.pets_frame = None
        self.products_frame = None
        self.pet_name_entry = None
        self.service_var = None
        self.date_entry = None
        self.time_entry = None
        self.staff_entry = None
        self.instructions_text = None
        self.donor_name_entry = None
        self.donor_email_entry = None
        self.donation_amount_entry = None
        self.donation_message_text = None
        
        # Color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'gold': '#FFD700',
            'light_gold': '#FFF8DC',
            'dark_gold': '#B8860B',
            'white': '#FFFFFF',
            'light_gray': '#F5F5F5',
            'dark_gray': '#333333'
        }
        
        self.setup_styles()
        self.create_landing_page()
        
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Gold.TButton',
                       background=self.colors['gold'],
                       foreground=self.colors['bg'],
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Dark.TButton',
                       background=self.colors['dark_gray'],
                       foreground=self.colors['white'],
                       font=('Arial', 10),
                       padding=(8, 4))
        
        # Configure frame styles
        style.configure('Gold.TFrame',
                       background=self.colors['gold'])
        
        style.configure('Dark.TFrame',
                       background=self.colors['bg'])
    
    def create_landing_page(self):
        """Create the main landing page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Main content
        self.create_main_content(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create the application header with navigation"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header_frame.pack(fill='x', padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        title_frame.pack(side='left')
        
        logo_label = tk.Label(title_frame, text="🐾 OnlyPets", 
                             font=('Arial', 24, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        logo_label.pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        nav_frame.pack(side='right')
        
        nav_buttons = ['Home', 'Adoption', 'Service', 'Products', 'Contact']
        for nav in nav_buttons:
            btn = tk.Button(nav_frame, text=nav, 
                           command=lambda n=nav: self.navigate_to(n),
                           bg=self.colors['dark_gray'], fg=self.colors['white'],
                           font=('Arial', 10), relief='flat', padx=15, pady=5)
            btn.pack(side='left', padx=5)
        
        # Sign Up/Sign In button
        auth_btn = tk.Button(nav_frame, text="Sign Up / Sign In",
                           command=self.show_auth_modal,
                           bg=self.colors['gold'], fg=self.colors['bg'],
                           font=('Arial', 10, 'bold'), relief='flat', padx=15, pady=5)
        auth_btn.pack(side='left', padx=5)
    
    def create_main_content(self, parent):
        """Create the main content area"""
        content_frame = tk.Frame(parent, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Hero section
        hero_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        hero_frame.pack(fill='x', pady=20)
        
        hero_title = tk.Label(hero_frame, 
                             text="Find your new best friend and give them a forever home,\nwhile we care for all your pet's needs.",
                             font=('Arial', 18),
                             fg=self.colors['white'], bg=self.colors['bg'],
                             justify='center')
        hero_title.pack(pady=20)
        
        get_started_btn = tk.Button(hero_frame, text="Get Started",
                                  command=self.show_auth_modal,
                                  bg=self.colors['gold'], fg=self.colors['bg'],
                                  font=('Arial', 14, 'bold'),
                                  padx=30, pady=10)
        get_started_btn.pack(pady=10)
        
        # About section
        about_frame = tk.Frame(content_frame, bg=self.colors['dark_gray'])
        about_frame.pack(fill='x', pady=20)
        
        about_title = tk.Label(about_frame, text="About Our Shelter",
                              font=('Arial', 16, 'bold'),
                              fg=self.colors['gold'], bg=self.colors['dark_gray'])
        about_title.pack(pady=10)
        
        about_text = tk.Label(about_frame,
                             text="We are dedicated to providing loving homes for pets in need and offering comprehensive care services. Our mission is to create a community where every pet finds their perfect family.",
                             font=('Arial', 12),
                             fg=self.colors['white'], bg=self.colors['dark_gray'],
                             wraplength=800, justify='center')
        about_text.pack(pady=10, padx=20)
        
        # Services section
        services_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        services_frame.pack(fill='x', pady=20)
        
        services_title = tk.Label(services_frame, text="Our Services",
                                 font=('Arial', 16, 'bold'),
                                 fg=self.colors['gold'], bg=self.colors['bg'])
        services_title.pack(pady=10)
        
        services_buttons = ['Grooming', 'Health Care', 'Daycare', 'Training', 'Hygienic Care']
        services_btn_frame = tk.Frame(services_frame, bg=self.colors['bg'])
        services_btn_frame.pack(pady=10)
        
        for service in services_buttons:
            btn = tk.Button(services_btn_frame, text=service,
                           command=lambda s=service: self.show_service_info(s),
                           bg=self.colors['dark_gray'], fg=self.colors['white'],
                           font=('Arial', 10), padx=20, pady=5)
            btn.pack(side='left', padx=5)
    
    def create_footer(self, parent):
        """Create the application footer"""
        footer_frame = tk.Frame(parent, bg=self.colors['dark_gray'], height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_text = tk.Label(footer_frame, 
                              text="© 2024 OnlyPets - Where Every Paw Finds a Home",
                              font=('Arial', 10),
                              fg=self.colors['gold'], bg=self.colors['dark_gray'])
        footer_text.pack(pady=20)
    
    def navigate_to(self, section):
        """Navigate to different sections"""
        if section == 'Home':
            self.create_landing_page()
        elif section == 'Dashboard':
            if self.current_user:
                self.show_dashboard()
            else:
                self.show_auth_modal()
        elif section == 'Adoption':
            self.show_adoption_page()
        elif section == 'Service':
            self.show_service_page()
        elif section == 'Products':
            self.show_products_page()
        elif section == 'Contact':
            self.show_contact_page()
    
    def show_auth_modal(self):
        """Show authentication modal"""
        auth_window = tk.Toplevel(self.root)
        auth_window.title("Sign Up / Sign In")
        auth_window.geometry("500x600")
        auth_window.configure(bg=self.colors['bg'])
        auth_window.transient(self.root)
        auth_window.grab_set()
        
        # Center the window
        auth_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(auth_window)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sign Up tab
        signup_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(signup_frame, text="Sign Up")
        
        signup_title = tk.Label(signup_frame, text="Start your journey with us — pets are waiting for you!",
                               font=('Arial', 14, 'bold'),
                               fg=self.colors['gold'], bg=self.colors['bg'])
        signup_title.pack(pady=20)
        
        # Sign up form
        self.create_signup_form(signup_frame)
        
        # Sign In tab
        signin_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(signin_frame, text="Sign In")
        
        signin_title = tk.Label(signin_frame, text="Where Every Paw Finds a Home!",
                               font=('Arial', 14, 'bold'),
                               fg=self.colors['gold'], bg=self.colors['bg'])
        signin_title.pack(pady=20)
        
        # Sign in form
        self.create_signin_form(signin_frame)
    
    def create_signup_form(self, parent):
        """Create sign up form"""
        form_frame = tk.Frame(parent, bg=self.colors['bg'])
        form_frame.pack(pady=20)
        
        # Form fields
        fields = ['Full Name', 'Email', 'Password', 'Confirm Password', 'Phone']
        self.signup_entries = {}
        
        for field in fields:
            frame = tk.Frame(form_frame, bg=self.colors['bg'])
            frame.pack(pady=5)
            
            label = tk.Label(frame, text=field + ":", 
                           font=('Arial', 10),
                           fg=self.colors['white'], bg=self.colors['bg'])
            label.pack(side='left', padx=(0, 10))
            
            entry = tk.Entry(frame, font=('Arial', 10), width=30)
            entry.pack(side='left')
            self.signup_entries[field] = entry
        
        # Sign up button
        signup_btn = tk.Button(form_frame, text="Sign Up",
                              command=self.signup_user,
                              bg=self.colors['gold'], fg=self.colors['bg'],
                              font=('Arial', 12, 'bold'),
                              padx=20, pady=5)
        signup_btn.pack(pady=20)
    
    def create_signin_form(self, parent):
        """Create sign in form"""
        form_frame = tk.Frame(parent, bg=self.colors['bg'])
        form_frame.pack(pady=20)
        
        # Form fields
        fields = ['Email', 'Password']
        self.signin_entries = {}
        
        for field in fields:
            frame = tk.Frame(form_frame, bg=self.colors['bg'])
            frame.pack(pady=5)
            
            label = tk.Label(frame, text=field + ":", 
                           font=('Arial', 10),
                           fg=self.colors['white'], bg=self.colors['bg'])
            label.pack(side='left', padx=(0, 10))
            
            entry = tk.Entry(frame, font=('Arial', 10), width=30, show='*' if field == 'Password' else '')
            entry.pack(side='left')
            self.signin_entries[field] = entry
        
        # Sign in button
        signin_btn = tk.Button(form_frame, text="Sign In",
                              command=self.signin_user,
                              bg=self.colors['gold'], fg=self.colors['bg'],
                              font=('Arial', 12, 'bold'),
                              padx=20, pady=5)
        signin_btn.pack(pady=20)
    
    def signup_user(self):
        """Handle user sign up"""
        try:
            # Get form data
            name = self.signup_entries['Full Name'].get()
            email = self.signup_entries['Email'].get()
            password = self.signup_entries['Password'].get()
            confirm_password = self.signup_entries['Confirm Password'].get()
            phone = self.signup_entries['Phone'].get()
            
            # Validate form
            if not all([name, email, password, confirm_password, phone]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Create user
            user_id = self.db.create_user(name, email, password, phone)
            if user_id:
                messagebox.showinfo("Success", "Account created successfully!")
                self.current_user = self.db.get_user_by_email(email)
                self.update_header_for_logged_in_user()
            else:
                messagebox.showerror("Error", "Failed to create account")
                
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def signin_user(self):
        """Handle user sign in"""
        try:
            email = self.signin_entries['Email'].get()
            password = self.signin_entries['Password'].get()
            
            if not email or not password:
                messagebox.showerror("Error", "Please enter email and password")
                return
            
            user = self.db.authenticate_user(email, password)
            if user:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome back, {user['name']}!")
                self.update_header_for_logged_in_user()
            else:
                messagebox.showerror("Error", "Invalid email or password")
                
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_header_for_logged_in_user(self):
        """Update header to show user info and dashboard"""
        # Redirect to dashboard after login
        self.show_dashboard()
    
    @staticmethod
    def show_service_info(service):
        """Show information about a specific service"""
        messagebox.showinfo("Service Information", 
                           f"Learn more about our {service} services. "
                           f"Professional care for your beloved pets.")
    
    def show_adoption_page(self):
        """Show the adoption page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Adoption content
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Find Your New Friend",
                             font=('Arial', 20, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Category buttons
        category_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        category_frame.pack(pady=10)
        
        categories = ['All', 'Dogs', 'Cats', 'Birds', 'Fish', 'Other']
        self.selected_category = tk.StringVar(value='All')
        
        for category in categories:
            btn = tk.Radiobutton(category_frame, text=category, variable=self.selected_category,
                               value=category, command=self.filter_pets,
                               bg=self.colors['bg'], fg=self.colors['white'],
                               font=('Arial', 10), selectcolor=self.colors['gold'])
            btn.pack(side='left', padx=10)
        
        # Pets display area
        self.pets_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        self.pets_frame.pack(fill='both', expand=True, pady=20)
        
        # Load and display pets
        self.load_pets()
    
    def load_pets(self):
        """Load and display pets based on selected category"""
        # Clear existing pets
        for widget in self.pets_frame.winfo_children():
            widget.destroy()
        
        category = self.selected_category.get()
        pets = self.db.get_available_pets(category)
        
        if not pets:
            no_pets_label = tk.Label(self.pets_frame, text="No pets available in this category",
                                   font=('Arial', 14),
                                   fg=self.colors['white'], bg=self.colors['bg'])
            no_pets_label.pack(pady=50)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(self.pets_frame, bg=self.colors['bg'])
        scrollbar = tk.Scrollbar(self.pets_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display pets in grid
        row = 0
        col = 0
        for pet in pets:
            pet_frame = tk.Frame(scrollable_frame, bg=self.colors['dark_gray'], relief='raised', bd=2)
            pet_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Pet image placeholder
            image_label = tk.Label(pet_frame, text="🐾", font=('Arial', 30),
                                 bg=self.colors['dark_gray'], fg=self.colors['gold'])
            image_label.pack(pady=10)
            
            # Pet info
            info_frame = tk.Frame(pet_frame, bg=self.colors['dark_gray'])
            info_frame.pack(pady=5)
            
            name_label = tk.Label(info_frame, text=pet['name'], font=('Arial', 12, 'bold'),
                                fg=self.colors['gold'], bg=self.colors['dark_gray'])
            name_label.pack()
            
            species_label = tk.Label(info_frame, text=f"{pet['species']} - {pet['breed']}",
                                   font=('Arial', 10),
                                   fg=self.colors['white'], bg=self.colors['dark_gray'])
            species_label.pack()
            
            age_label = tk.Label(info_frame, text=f"Age: {pet['age']} years",
                               font=('Arial', 10),
                               fg=self.colors['white'], bg=self.colors['dark_gray'])
            age_label.pack()
            
            # View details button
            details_btn = tk.Button(pet_frame, text="View Details",
                                  command=lambda p=pet: self.show_pet_details(p),
                                  bg=self.colors['gold'], fg=self.colors['bg'],
                                  font=('Arial', 10, 'bold'), padx=10, pady=5)
            details_btn.pack(pady=10)
            
            col += 1
            if col >= 3:  # 3 pets per row
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def filter_pets(self):
        """Filter pets by selected category"""
        self.load_pets()
    
    def show_pet_details(self, pet):
        """Show detailed pet information in a modal"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Pet Details - {pet['name']}")
        details_window.geometry("500x600")
        details_window.configure(bg=self.colors['bg'])
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Center the window
        details_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 50))
        
        # Pet image
        image_label = tk.Label(details_window, text="🐾", font=('Arial', 50),
                             bg=self.colors['bg'], fg=self.colors['gold'])
        image_label.pack(pady=20)
        
        # Pet details
        details_frame = tk.Frame(details_window, bg=self.colors['bg'])
        details_frame.pack(fill='both', expand=True, padx=20)
        
        details = [
            ("Name", pet['name']),
            ("Species", pet['species']),
            ("Breed", pet['breed']),
            ("Age", f"{pet['age']} years"),
            ("Gender", pet['gender']),
            ("Markings", pet['markings']),
            ("Vaccine Status", pet['vaccine_status']),
            ("Neutered/Spayed", pet['neutered_spayed']),
            ("Dewormed", pet['dewormed']),
            ("Medical Notes", pet['medical_notes'])
        ]
        
        for label, value in details:
            frame = tk.Frame(details_frame, bg=self.colors['bg'])
            frame.pack(fill='x', pady=5)
            
            label_widget = tk.Label(frame, text=f"{label}:", font=('Arial', 10, 'bold'),
                                  fg=self.colors['gold'], bg=self.colors['bg'])
            label_widget.pack(side='left')
            
            value_widget = tk.Label(frame, text=value, font=('Arial', 10),
                                  fg=self.colors['white'], bg=self.colors['bg'])
            value_widget.pack(side='left', padx=(10, 0))
        
        # Adopt button
        if self.current_user:
            adopt_btn = tk.Button(details_window, text="Adopt This Pet",
                                command=lambda: self.show_adoption_form(pet),
                                bg=self.colors['gold'], fg=self.colors['bg'],
                                font=('Arial', 12, 'bold'), padx=20, pady=10)
            adopt_btn.pack(pady=20)
        else:
            login_btn = tk.Button(details_window, text="Sign In to Adopt",
                                 command=lambda: [details_window.destroy(), self.show_auth_modal()],
                                 bg=self.colors['dark_gray'], fg=self.colors['white'],
                                 font=('Arial', 12, 'bold'), padx=20, pady=10)
            login_btn.pack(pady=20)
    
    def show_adoption_form(self, pet):
        """Show adoption application form"""
        form_window = tk.Toplevel(self.root)
        form_window.title(f"Adoption Application - {pet['name']}")
        form_window.geometry("600x700")
        form_window.configure(bg=self.colors['bg'])
        form_window.transient(self.root)
        form_window.grab_set()
        
        # Center the window
        form_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(form_window, 
                             text="Thank you for choosing to adopt! Please fill out this form\nso we can ensure the best match between you and your future pet.",
                             font=('Arial', 12),
                             fg=self.colors['white'], bg=self.colors['bg'],
                             justify='center')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(form_window, bg=self.colors['bg'])
        form_frame.pack(fill='both', expand=True, padx=20)
        
        # Form fields
        self.adoption_entries = {}
        
        fields = [
            ('Full Name', 'entry'),
            ('Complete Address', 'text'),
            ('Age', 'entry'),
            ('Contact Number', 'entry'),
            ('Email Address', 'entry'),
            ('Care Commitment', 'text')
        ]
        
        for field_name, field_type in fields:
            frame = tk.Frame(form_frame, bg=self.colors['bg'])
            frame.pack(fill='x', pady=5)
            
            label = tk.Label(frame, text=f"{field_name}:", font=('Arial', 10, 'bold'),
                           fg=self.colors['gold'], bg=self.colors['bg'])
            label.pack(anchor='w')
            
            if field_type == 'entry':
                entry = tk.Entry(frame, font=('Arial', 10), width=50)
                entry.pack(fill='x', pady=2)
            else:  # text
                entry = tk.Text(frame, font=('Arial', 10), height=3, width=50)
                entry.pack(fill='x', pady=2)
            
            self.adoption_entries[field_name] = entry
        
        # Care questions
        care_frame = tk.Frame(form_frame, bg=self.colors['bg'])
        care_frame.pack(fill='x', pady=10)
        
        care_label = tk.Label(care_frame, text="Care Questions:", font=('Arial', 10, 'bold'),
                            fg=self.colors['gold'], bg=self.colors['bg'])
        care_label.pack(anchor='w')
        
        self.care_vars = {}
        care_questions = [
            "Can you provide food?",
            "Can you provide veterinary care?",
            "Can you provide a safe home?"
        ]
        
        for question in care_questions:
            q_frame = tk.Frame(care_frame, bg=self.colors['bg'])
            q_frame.pack(fill='x', pady=2)
            
            var = tk.StringVar(value="No")
            self.care_vars[question] = var
            
            tk.Label(q_frame, text=question, font=('Arial', 10),
                   fg=self.colors['white'], bg=self.colors['bg']).pack(side='left')
            
            tk.Radiobutton(q_frame, text="Yes", variable=var, value="Yes",
                          bg=self.colors['bg'], fg=self.colors['white'],
                          selectcolor=self.colors['gold']).pack(side='left', padx=(20, 10))
            tk.Radiobutton(q_frame, text="No", variable=var, value="No",
                          bg=self.colors['bg'], fg=self.colors['white'],
                          selectcolor=self.colors['gold']).pack(side='left')
        
        # Agreement
        agreement_frame = tk.Frame(form_frame, bg=self.colors['bg'])
        agreement_frame.pack(fill='x', pady=10)
        
        agreement_text = "I understand that adopting a pet is a lifelong responsibility. I promise to give love and proper care to my adopted pet."
        agreement_label = tk.Label(agreement_frame, text=agreement_text, font=('Arial', 10),
                                fg=self.colors['white'], bg=self.colors['bg'], wraplength=500)
        agreement_label.pack()
        
        self.agreement_var = tk.BooleanVar()
        agreement_check = tk.Checkbutton(agreement_frame, text="I agree to the above statement",
                                       variable=self.agreement_var,
                                       bg=self.colors['bg'], fg=self.colors['white'],
                                       selectcolor=self.colors['gold'])
        agreement_check.pack(pady=5)
        
        # Submit button
        submit_btn = tk.Button(form_frame, text="Submit Application",
                             command=lambda: self.submit_adoption_application(pet, form_window),
                             bg=self.colors['gold'], fg=self.colors['bg'],
                             font=('Arial', 12, 'bold'), padx=20, pady=10)
        submit_btn.pack(pady=20)
    
    def submit_adoption_application(self, pet, window):
        """Submit adoption application"""
        try:
            # Validate form
            required_fields = ['Full Name', 'Complete Address', 'Age', 'Contact Number', 'Email Address']
            for field in required_fields:
                if not self.adoption_entries[field].get().strip():
                    messagebox.showerror("Error", f"Please fill in {field}")
                    return
            
            if not self.agreement_var.get():
                messagebox.showerror("Error", "Please agree to the responsibility statement")
                return
            
            # Get form data
            application_data = {
                'user_id': self.current_user['id'],
                'pet_id': pet['id'],
                'full_name': self.adoption_entries['Full Name'].get(),
                'address': self.adoption_entries['Complete Address'].get(),
                'age': int(self.adoption_entries['Age'].get()),
                'contact_number': self.adoption_entries['Contact Number'].get(),
                'email': self.adoption_entries['Email Address'].get(),
                'care_commitment': self.adoption_entries['Care Commitment'].get(),
                'can_provide_food': self.care_vars["Can you provide food?"].get() == "Yes",
                'can_provide_vet_care': self.care_vars["Can you provide veterinary care?"].get() == "Yes",
                'can_provide_safe_home': self.care_vars["Can you provide a safe home?"].get() == "Yes",
                'agreement_accepted': True
            }
            
            # Submit application
            application_id = self.db.submit_adoption_application(application_data)
            if application_id:
                messagebox.showinfo("Success", "Your adoption application has been submitted successfully!")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to submit application")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def show_service_page(self):
        """Show the service booking page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Service content
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Our Services",
                             font=('Arial', 20, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Service buttons
        services_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        services_frame.pack(pady=10)
        
        services = ['Grooming', 'Health Care', 'Daycare', 'Training', 'Hygienic Care']
        for service in services:
            btn = tk.Button(services_frame, text=service,
                          command=lambda s=service: self.show_service_booking_form(s),
                          bg=self.colors['dark_gray'], fg=self.colors['white'],
                          font=('Arial', 10), padx=20, pady=5)
            btn.pack(side='left', padx=5)
        
        # Service booking form
        self.create_service_booking_form(content_frame)
    
    def create_service_booking_form(self, parent):
        """Create service booking form"""
        form_frame = tk.Frame(parent, bg=self.colors['dark_gray'])
        form_frame.pack(fill='x', pady=20, padx=20)
        
        form_title = tk.Label(form_frame, text="Service Booking Form",
                            font=('Arial', 16, 'bold'),
                            fg=self.colors['gold'], bg=self.colors['dark_gray'])
        form_title.pack(pady=10)
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg=self.colors['dark_gray'])
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Pet name
        pet_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        pet_frame.pack(fill='x', pady=5)
        
        tk.Label(pet_frame, text="Pet Name:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.pet_name_entry = tk.Entry(pet_frame, font=('Arial', 10), width=30)
        self.pet_name_entry.pack(side='left', padx=(10, 0))
        
        # Service type
        service_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        service_frame.pack(fill='x', pady=5)
        
        tk.Label(service_frame, text="Service Type:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.service_var = tk.StringVar(value="Grooming")
        service_combo = tk.OptionMenu(service_frame, self.service_var, *['Grooming', 'Health Care', 'Daycare', 'Training', 'Hygienic Care'])
        service_combo.pack(side='left', padx=(10, 0))
        
        # Date and time
        datetime_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        datetime_frame.pack(fill='x', pady=5)
        
        tk.Label(datetime_frame, text="Date:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.date_entry = tk.Entry(datetime_frame, font=('Arial', 10), width=15)
        self.date_entry.pack(side='left', padx=(10, 20))
        
        tk.Label(datetime_frame, text="Time:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.time_entry = tk.Entry(datetime_frame, font=('Arial', 10), width=15)
        self.time_entry.pack(side='left', padx=(10, 0))
        
        # Staff member
        staff_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        staff_frame.pack(fill='x', pady=5)
        
        tk.Label(staff_frame, text="Preferred Staff:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.staff_entry = tk.Entry(staff_frame, font=('Arial', 10), width=30)
        self.staff_entry.pack(side='left', padx=(10, 0))
        
        # Special instructions
        instructions_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        instructions_frame.pack(fill='x', pady=5)
        
        tk.Label(instructions_frame, text="Special Instructions:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(anchor='w')
        
        self.instructions_text = tk.Text(instructions_frame, font=('Arial', 10), height=3, width=50)
        self.instructions_text.pack(fill='x', pady=2)
        
        # Book service button
        if self.current_user:
            book_btn = tk.Button(form_frame, text="Book Service",
                               command=self.book_service,
                               bg=self.colors['gold'], fg=self.colors['bg'],
                               font=('Arial', 12, 'bold'), padx=20, pady=5)
            book_btn.pack(pady=10)
        else:
            login_btn = tk.Button(form_frame, text="Sign In to Book Service",
                                 command=self.show_auth_modal,
                                 bg=self.colors['dark_gray'], fg=self.colors['white'],
                                 font=('Arial', 12, 'bold'), padx=20, pady=5)
            login_btn.pack(pady=10)
    
    def show_service_booking_form(self, service):
        """Show service booking form for specific service"""
        self.service_var.set(service)
        messagebox.showinfo("Service Selected", f"You have selected {service} service. Please fill out the booking form below.")
    
    def book_service(self):
        """Book a service"""
        if not self.current_user:
            messagebox.showerror("Error", "Please sign in to book a service")
            return
        
        try:
            # Get form data
            pet_name = self.pet_name_entry.get()
            service_type = self.service_var.get()
            date = self.date_entry.get()
            time = self.time_entry.get()
            staff = self.staff_entry.get()
            instructions = self.instructions_text.get("1.0", tk.END).strip()
            
            if not all([pet_name, date, time]):
                messagebox.showerror("Error", "Please fill in pet name, date, and time")
                return
            
            # Get service ID
            services = self.db.get_services()
            service_id = None
            for service in services:
                if service['name'] == service_type:
                    service_id = service['id']
                    break
            
            if not service_id:
                messagebox.showerror("Error", "Service not found")
                return
            
            # Create booking data
            booking_data = {
                'user_id': self.current_user['id'],
                'service_id': service_id,
                'pet_name': pet_name,
                'booking_date': date,
                'booking_time': time,
                'staff_member': staff,
                'special_instructions': instructions
            }
            
            # Book service
            booking_id = self.db.book_service(booking_data)
            if booking_id:
                messagebox.showinfo("Success", "Service booked successfully!")
                # Clear form
                self.pet_name_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                self.time_entry.delete(0, tk.END)
                self.staff_entry.delete(0, tk.END)
                self.instructions_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Failed to book service")
                
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_products_page(self):
        """Show the products page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Products content
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Our Products",
                             font=('Arial', 20, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Category buttons
        category_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        category_frame.pack(pady=10)
        
        categories = ['All', 'Food', 'Medications', 'Toys', 'Other']
        self.selected_product_category = tk.StringVar(value='All')
        
        for category in categories:
            btn = tk.Radiobutton(category_frame, text=category, variable=self.selected_product_category,
                               value=category, command=self.filter_products,
                               bg=self.colors['bg'], fg=self.colors['white'],
                               font=('Arial', 10), selectcolor=self.colors['gold'])
            btn.pack(side='left', padx=10)
        
        # Products display area
        self.products_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        self.products_frame.pack(fill='both', expand=True, pady=20)
        
        # Load and display products
        self.load_products()
    
    def load_products(self):
        """Load and display products based on selected category"""
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        category = self.selected_product_category.get()
        products = self.db.get_products(category if category != 'All' else None)
        
        if not products:
            no_products_label = tk.Label(self.products_frame, text="No products available in this category",
                                       font=('Arial', 14),
                                       fg=self.colors['white'], bg=self.colors['bg'])
            no_products_label.pack(pady=50)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(self.products_frame, bg=self.colors['bg'])
        scrollbar = tk.Scrollbar(self.products_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display products in grid
        row = 0
        col = 0
        for product in products:
            product_frame = tk.Frame(scrollable_frame, bg=self.colors['dark_gray'], relief='raised', bd=2)
            product_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Product image placeholder
            image_label = tk.Label(product_frame, text="📦", font=('Arial', 30),
                                 bg=self.colors['dark_gray'], fg=self.colors['gold'])
            image_label.pack(pady=10)
            
            # Product info
            info_frame = tk.Frame(product_frame, bg=self.colors['dark_gray'])
            info_frame.pack(pady=5)
            
            name_label = tk.Label(info_frame, text=product['name'], font=('Arial', 12, 'bold'),
                                fg=self.colors['gold'], bg=self.colors['dark_gray'])
            name_label.pack()
            
            category_label = tk.Label(info_frame, text=f"Category: {product['category']}",
                                   font=('Arial', 10),
                                   fg=self.colors['white'], bg=self.colors['dark_gray'])
            category_label.pack()
            
            price_label = tk.Label(info_frame, text=f"Price: ${product['price']}",
                                font=('Arial', 10, 'bold'),
                                fg=self.colors['gold'], bg=self.colors['dark_gray'])
            price_label.pack()
            
            stock_label = tk.Label(info_frame, text=f"Stock: {product['stock_quantity']}",
                                font=('Arial', 10),
                                fg=self.colors['white'], bg=self.colors['dark_gray'])
            stock_label.pack()
            
            # Purchase button
            if self.current_user:
                purchase_btn = tk.Button(product_frame, text="Purchase",
                                       command=lambda p=product: self.purchase_product(p),
                                       bg=self.colors['gold'], fg=self.colors['bg'],
                                       font=('Arial', 10, 'bold'), padx=10, pady=5)
                purchase_btn.pack(pady=10)
            else:
                login_btn = tk.Button(product_frame, text="Sign In to Purchase",
                                     command=self.show_auth_modal,
                                     bg=self.colors['dark_gray'], fg=self.colors['white'],
                                     font=('Arial', 10, 'bold'), padx=10, pady=5)
                login_btn.pack(pady=10)
            
            col += 1
            if col >= 3:  # 3 products per row
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def filter_products(self):
        """Filter products by selected category"""
        self.load_products()
    
    @staticmethod
    def purchase_product(product):
        """Handle product purchase"""
        messagebox.showinfo("Purchase", f"Thank you for your interest in {product['name']}! "
                                       f"Please contact us to complete your purchase.")
    
    def show_contact_page(self):
        """Show the contact page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Contact content
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Contact Us",
                             font=('Arial', 20, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Contact info
        contact_frame = tk.Frame(content_frame, bg=self.colors['dark_gray'])
        contact_frame.pack(fill='x', pady=20, padx=20)
        
        contact_info = [
            ("Phone", "1-800-ONLYPETS"),
            ("Email", "info@onlypets.com"),
            ("Address", "123 Pet Street, Animal City, AC 12345"),
            ("Hours", "Monday - Friday: 9AM - 6PM\nSaturday - Sunday: 10AM - 4PM")
        ]
        
        for label, info in contact_info:
            info_frame = tk.Frame(contact_frame, bg=self.colors['dark_gray'])
            info_frame.pack(fill='x', pady=5)
            
            label_widget = tk.Label(info_frame, text=f"{label}:", font=('Arial', 12, 'bold'),
                                  fg=self.colors['gold'], bg=self.colors['dark_gray'])
            label_widget.pack(side='left')
            
            info_widget = tk.Label(info_frame, text=info, font=('Arial', 12),
                                 fg=self.colors['white'], bg=self.colors['dark_gray'])
            info_widget.pack(side='left', padx=(10, 0))
        
        # Donation section
        donation_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        donation_frame.pack(fill='x', pady=20)
        
        donation_title = tk.Label(donation_frame, text="Support Our Shelter",
                                font=('Arial', 16, 'bold'),
                                fg=self.colors['gold'], bg=self.colors['bg'])
        donation_title.pack(pady=10)
        
        donation_text = tk.Label(donation_frame,
                               text="Your donations help us provide care for animals in need and maintain our facilities.",
                               font=('Arial', 12),
                               fg=self.colors['white'], bg=self.colors['bg'],
                               wraplength=600, justify='center')
        donation_text.pack(pady=10)
        
        # Donation form
        self.create_donation_form(donation_frame)
    
    def create_donation_form(self, parent):
        """Create donation form"""
        form_frame = tk.Frame(parent, bg=self.colors['dark_gray'])
        form_frame.pack(fill='x', pady=20, padx=20)
        
        form_title = tk.Label(form_frame, text="Make a Donation",
                            font=('Arial', 14, 'bold'),
                            fg=self.colors['gold'], bg=self.colors['dark_gray'])
        form_title.pack(pady=10)
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg=self.colors['dark_gray'])
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Donor name
        name_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        name_frame.pack(fill='x', pady=5)
        
        tk.Label(name_frame, text="Name:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.donor_name_entry = tk.Entry(name_frame, font=('Arial', 10), width=30)
        self.donor_name_entry.pack(side='left', padx=(10, 0))
        
        # Email
        email_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        email_frame.pack(fill='x', pady=5)
        
        tk.Label(email_frame, text="Email:", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.donor_email_entry = tk.Entry(email_frame, font=('Arial', 10), width=30)
        self.donor_email_entry.pack(side='left', padx=(10, 0))
        
        # Amount
        amount_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        amount_frame.pack(fill='x', pady=5)
        
        tk.Label(amount_frame, text="Amount ($):", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(side='left')
        
        self.donation_amount_entry = tk.Entry(amount_frame, font=('Arial', 10), width=15)
        self.donation_amount_entry.pack(side='left', padx=(10, 0))
        
        # Message
        message_frame = tk.Frame(fields_frame, bg=self.colors['dark_gray'])
        message_frame.pack(fill='x', pady=5)
        
        tk.Label(message_frame, text="Message (optional):", font=('Arial', 10, 'bold'),
                fg=self.colors['gold'], bg=self.colors['dark_gray']).pack(anchor='w')
        
        self.donation_message_text = tk.Text(message_frame, font=('Arial', 10), height=3, width=50)
        self.donation_message_text.pack(fill='x', pady=2)
        
        # Submit donation button
        submit_btn = tk.Button(form_frame, text="Submit Donation",
                             command=self.submit_donation,
                             bg=self.colors['gold'], fg=self.colors['bg'],
                             font=('Arial', 12, 'bold'), padx=20, pady=5)
        submit_btn.pack(pady=10)
    
    def submit_donation(self):
        """Submit donation"""
        try:
            # Get form data
            donor_name = self.donor_name_entry.get()
            email = self.donor_email_entry.get()
            amount = self.donation_amount_entry.get()
            message = self.donation_message_text.get("1.0", tk.END).strip()
            
            if not all([donor_name, email, amount]):
                messagebox.showerror("Error", "Please fill in name, email, and amount")
                return
            
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    messagebox.showerror("Error", "Please enter a valid amount")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return
            
            # Create donation data
            donation_data = {
                'donor_name': donor_name,
                'amount': amount_float,
                'email': email,
                'message': message
            }
            
            # Submit donation
            donation_id = self.db.submit_donation(donation_data)
            if donation_id:
                messagebox.showinfo("Success", "Thank you for your donation! Your support helps us care for animals in need.")
                # Clear form
                self.donor_name_entry.delete(0, tk.END)
                self.donor_email_entry.delete(0, tk.END)
                self.donation_amount_entry.delete(0, tk.END)
                self.donation_message_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Failed to submit donation")
                
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_dashboard(self):
        """Show user dashboard with analytics"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Header with user info
        self.create_dashboard_header(main_frame)
        
        # Dashboard content
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(content_frame, 
                               text=f"Welcome back, {self.current_user['name']}!",
                               font=('Arial', 18, 'bold'),
                               fg=self.colors['gold'], bg=self.colors['bg'])
        welcome_label.pack(pady=20)
        
        # Analytics section
        analytics_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        analytics_frame.pack(fill='both', expand=True)
        
        # Create analytics charts
        self.create_analytics_dashboard(analytics_frame)
    
    def create_dashboard_header(self, parent):
        """Create dashboard header with user info"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header_frame.pack(fill='x', padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        title_frame.pack(side='left')
        
        logo_label = tk.Label(title_frame, text="🐾 OnlyPets Dashboard", 
                             font=('Arial', 20, 'bold'),
                             fg=self.colors['gold'], bg=self.colors['bg'])
        logo_label.pack()
        
        # User info
        user_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        user_frame.pack(side='right')
        
        user_label = tk.Label(user_frame, text=f"Welcome, {self.current_user['name']}",
                            font=('Arial', 12),
                            fg=self.colors['white'], bg=self.colors['bg'])
        user_label.pack(side='right', padx=10)
        
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        nav_frame.pack(side='right')
        
        nav_buttons = ['Dashboard', 'Adoption', 'Service', 'Products', 'Contact']
        for nav in nav_buttons:
            btn = tk.Button(nav_frame, text=nav, 
                           command=lambda n=nav: self.navigate_to(n),
                           bg=self.colors['dark_gray'], fg=self.colors['white'],
                           font=('Arial', 10), relief='flat', padx=15, pady=5)
            btn.pack(side='left', padx=5)
    
    def create_analytics_dashboard(self, parent):
        """Create analytics dashboard with charts"""
        # Get analytics data
        summary = self.analytics.get_dashboard_summary()
        
        # Create notebook for different analytics views
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True)
        
        # Adoption analytics tab
        adoption_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(adoption_frame, text="Adoption Analytics")
        
        adoption_chart = self.analytics.create_adoption_chart(adoption_frame)
        adoption_chart.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
        
        # Service analytics tab
        service_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(service_frame, text="Service Analytics")
        
        service_chart = self.analytics.create_service_chart(service_frame)
        service_chart.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
        
        # Summary statistics
        stats_frame = tk.Frame(parent, bg=self.colors['dark_gray'])
        stats_frame.pack(fill='x', pady=20)
        
        stats_title = tk.Label(stats_frame, text="Quick Statistics",
                              font=('Arial', 14, 'bold'),
                              fg=self.colors['gold'], bg=self.colors['dark_gray'])
        stats_title.pack(pady=10)
        
        # Display key statistics
        stats_text = f"""
        Total Available Pets: {summary['adoption']['total_pets']}
        Recent Applications (30 days): {summary['adoption']['recent_applications']}
        Total Donations: ${summary['donations']['total_donations']['total_amount']:.2f}
        """
        
        stats_label = tk.Label(stats_frame, text=stats_text, font=('Arial', 12),
                             fg=self.colors['white'], bg=self.colors['dark_gray'])
        stats_label.pack(pady=10)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


class DatabaseManager:
    """Database management class for OnlyPets"""
    
    def __init__(self):
        self.db_path = "onlypets.db"
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                age INTEGER,
                gender TEXT,
                markings TEXT,
                vaccine_status TEXT,
                neutered_spayed TEXT,
                dewormed TEXT,
                medical_notes TEXT,
                image_path TEXT,
                available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Adoption applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adoption_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                pet_id INTEGER,
                full_name TEXT NOT NULL,
                address TEXT NOT NULL,
                age INTEGER,
                contact_number TEXT,
                email TEXT,
                care_commitment TEXT,
                can_provide_food BOOLEAN,
                can_provide_vet_care BOOLEAN,
                can_provide_safe_home BOOLEAN,
                agreement_accepted BOOLEAN,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (pet_id) REFERENCES pets (id)
            )
        ''')
        
        # Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2),
                duration_minutes INTEGER
            )
        ''')
        
        # Service bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                service_id INTEGER,
                pet_name TEXT NOT NULL,
                booking_date DATE,
                booking_time TIME,
                staff_member TEXT,
                special_instructions TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2),
                stock_quantity INTEGER,
                image_path TEXT
            )
        ''')
        
        # Donations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_name TEXT,
                amount DECIMAL(10,2),
                email TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert sample data
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample data for demonstration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM pets")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Insert sample pets (25 per category = 125 total)
        # Dogs (25)
        dogs = [
            ('Buddy', 'Dog', 'Golden Retriever', 3, 'Male', 'Golden coat', 'Up to date', 'Yes', 'Yes', 'Healthy and friendly'),
            ('Max', 'Dog', 'Labrador', 2, 'Male', 'Black', 'Up to date', 'Yes', 'Yes', 'Energetic and playful'),
            ('Bella', 'Dog', 'German Shepherd', 4, 'Female', 'Brown and black', 'Up to date', 'Yes', 'Yes', 'Protective and loyal'),
            ('Rocky', 'Dog', 'Bulldog', 5, 'Male', 'White with brown spots', 'Up to date', 'Yes', 'Yes', 'Calm and gentle'),
            ('Luna', 'Dog', 'Husky', 2, 'Female', 'White and gray', 'Up to date', 'Yes', 'Yes', 'Active and intelligent'),
            ('Charlie', 'Dog', 'Beagle', 3, 'Male', 'Tri-color', 'Up to date', 'Yes', 'Yes', 'Friendly and curious'),
            ('Daisy', 'Dog', 'Poodle', 1, 'Female', 'White', 'Up to date', 'No', 'Yes', 'Smart and trainable'),
            ('Duke', 'Dog', 'Rottweiler', 4, 'Male', 'Black with brown', 'Up to date', 'Yes', 'Yes', 'Strong and protective'),
            ('Molly', 'Dog', 'Border Collie', 2, 'Female', 'Black and white', 'Up to date', 'Yes', 'Yes', 'Intelligent and active'),
            ('Toby', 'Dog', 'Chihuahua', 3, 'Male', 'Brown', 'Up to date', 'Yes', 'Yes', 'Small but brave'),
            ('Sadie', 'Dog', 'Boxer', 3, 'Female', 'Brindle', 'Up to date', 'Yes', 'Yes', 'Playful and energetic'),
            ('Zeus', 'Dog', 'Great Dane', 2, 'Male', 'Black', 'Up to date', 'Yes', 'Yes', 'Gentle giant'),
            ('Ruby', 'Dog', 'Cocker Spaniel', 4, 'Female', 'Golden', 'Up to date', 'Yes', 'Yes', 'Sweet and loving'),
            ('Jack', 'Dog', 'Jack Russell', 2, 'Male', 'White with brown', 'Up to date', 'Yes', 'Yes', 'Energetic and smart'),
            ('Mia', 'Dog', 'Shih Tzu', 1, 'Female', 'White and gray', 'Up to date', 'No', 'Yes', 'Gentle and affectionate'),
            ('Bruno', 'Dog', 'Mastiff', 5, 'Male', 'Fawn', 'Up to date', 'Yes', 'Yes', 'Calm and protective'),
            ('Lola', 'Dog', 'Dachshund', 3, 'Female', 'Brown', 'Up to date', 'Yes', 'Yes', 'Playful and loyal'),
            ('Sam', 'Dog', 'Siberian Husky', 2, 'Male', 'Gray and white', 'Up to date', 'Yes', 'Yes', 'Active and friendly'),
            ('Zoe', 'Dog', 'Australian Shepherd', 1, 'Female', 'Merle', 'Up to date', 'No', 'Yes', 'Intelligent and agile'),
            ('Rex', 'Dog', 'Doberman', 4, 'Male', 'Black and tan', 'Up to date', 'Yes', 'Yes', 'Loyal and alert'),
            ('Penny', 'Dog', 'Basset Hound', 3, 'Female', 'Tri-color', 'Up to date', 'Yes', 'Yes', 'Calm and friendly'),
            ('Oscar', 'Dog', 'French Bulldog', 2, 'Male', 'Brindle', 'Up to date', 'Yes', 'Yes', 'Playful and charming'),
            ('Nala', 'Dog', 'Maltese', 1, 'Female', 'White', 'Up to date', 'No', 'Yes', 'Gentle and elegant'),
            ('Thor', 'Dog', 'Saint Bernard', 3, 'Male', 'Brown and white', 'Up to date', 'Yes', 'Yes', 'Gentle and patient'),
            ('Lily', 'Dog', 'Yorkshire Terrier', 2, 'Female', 'Black and tan', 'Up to date', 'Yes', 'Yes', 'Spunky and loyal')
        ]
        
        # Cats (25)
        cats = [
            ('Whiskers', 'Cat', 'Persian', 2, 'Male', 'White and fluffy', 'Up to date', 'Yes', 'Yes', 'Calm and gentle'),
            ('Shadow', 'Cat', 'Maine Coon', 3, 'Male', 'Black', 'Up to date', 'Yes', 'Yes', 'Large and friendly'),
            ('Princess', 'Cat', 'Siamese', 1, 'Female', 'Seal point', 'Up to date', 'No', 'Yes', 'Vocal and social'),
            ('Tiger', 'Cat', 'Tabby', 4, 'Male', 'Orange stripes', 'Up to date', 'Yes', 'Yes', 'Playful and independent'),
            ('Snowball', 'Cat', 'Ragdoll', 2, 'Female', 'White', 'Up to date', 'Yes', 'Yes', 'Docile and affectionate'),
            ('Smokey', 'Cat', 'Russian Blue', 3, 'Male', 'Gray', 'Up to date', 'Yes', 'Yes', 'Quiet and reserved'),
            ('Ginger', 'Cat', 'Orange Tabby', 1, 'Female', 'Orange', 'Up to date', 'No', 'Yes', 'Energetic and curious'),
            ('Midnight', 'Cat', 'Bombay', 2, 'Male', 'Black', 'Up to date', 'Yes', 'Yes', 'Playful and social'),
            ('Luna', 'Cat', 'Calico', 3, 'Female', 'Tri-color', 'Up to date', 'Yes', 'Yes', 'Sweet and loving'),
            ('Felix', 'Cat', 'British Shorthair', 4, 'Male', 'Blue-gray', 'Up to date', 'Yes', 'Yes', 'Calm and dignified'),
            ('Bella', 'Cat', 'Sphynx', 1, 'Female', 'Hairless', 'Up to date', 'No', 'Yes', 'Social and warm'),
            ('Simba', 'Cat', 'Abyssinian', 2, 'Male', 'Ruddy', 'Up to date', 'Yes', 'Yes', 'Active and intelligent'),
            ('Cleo', 'Cat', 'Egyptian Mau', 3, 'Female', 'Spotted', 'Up to date', 'Yes', 'Yes', 'Elegant and athletic'),
            ('Oreo', 'Cat', 'Tuxedo', 1, 'Male', 'Black and white', 'Up to date', 'No', 'Yes', 'Playful and mischievous'),
            ('Pearl', 'Cat', 'Birman', 2, 'Female', 'Seal point', 'Up to date', 'Yes', 'Yes', 'Gentle and sweet'),
            ('Milo', 'Cat', 'Scottish Fold', 3, 'Male', 'Gray', 'Up to date', 'Yes', 'Yes', 'Calm and friendly'),
            ('Ruby', 'Cat', 'Manx', 4, 'Female', 'Orange', 'Up to date', 'Yes', 'Yes', 'Playful and tailless'),
            ('Jasper', 'Cat', 'Norwegian Forest', 2, 'Male', 'Brown tabby', 'Up to date', 'Yes', 'Yes', 'Large and fluffy'),
            ('Misty', 'Cat', 'Himalayan', 1, 'Female', 'Seal point', 'Up to date', 'No', 'Yes', 'Calm and beautiful'),
            ('Zeus', 'Cat', 'Savannah', 3, 'Male', 'Spotted', 'Up to date', 'Yes', 'Yes', 'Wild-looking and active'),
            ('Coco', 'Cat', 'Burmese', 2, 'Female', 'Brown', 'Up to date', 'Yes', 'Yes', 'Social and vocal'),
            ('Apollo', 'Cat', 'Bengal', 1, 'Male', 'Spotted', 'Up to date', 'No', 'Yes', 'Energetic and wild'),
            ('Stella', 'Cat', 'Munchkin', 3, 'Female', 'Black', 'Up to date', 'Yes', 'Yes', 'Short legs and playful'),
            ('Atlas', 'Cat', 'Maine Coon', 4, 'Male', 'Brown tabby', 'Up to date', 'Yes', 'Yes', 'Gentle giant'),
            ('Nova', 'Cat', 'Oriental Shorthair', 2, 'Female', 'Chocolate', 'Up to date', 'Yes', 'Yes', 'Sleek and vocal')
        ]
        
        # Birds (25)
        birds = [
            ('Tweety', 'Bird', 'Canary', 1, 'Male', 'Yellow', 'Up to date', 'N/A', 'Yes', 'Sweet singer'),
            ('Polly', 'Bird', 'Parrot', 3, 'Female', 'Green and red', 'Up to date', 'N/A', 'Yes', 'Very talkative'),
            ('Sunny', 'Bird', 'Sun Conure', 2, 'Male', 'Orange and yellow', 'Up to date', 'N/A', 'Yes', 'Colorful and social'),
            ('Blue', 'Bird', 'Blue and Gold Macaw', 4, 'Male', 'Blue and gold', 'Up to date', 'N/A', 'Yes', 'Large and intelligent'),
            ('Kiwi', 'Bird', 'Cockatiel', 1, 'Female', 'Gray with yellow', 'Up to date', 'N/A', 'Yes', 'Gentle and friendly'),
            ('Rio', 'Bird', 'Green Cheek Conure', 2, 'Male', 'Green with red', 'Up to date', 'N/A', 'Yes', 'Playful and small'),
            ('Rainbow', 'Bird', 'Rainbow Lorikeet', 3, 'Female', 'Multi-colored', 'Up to date', 'N/A', 'Yes', 'Very colorful'),
            ('Buddy', 'Bird', 'Budgerigar', 1, 'Male', 'Blue', 'Up to date', 'N/A', 'Yes', 'Small and active'),
            ('Scarlet', 'Bird', 'Scarlet Macaw', 5, 'Female', 'Red and blue', 'Up to date', 'N/A', 'Yes', 'Majestic and large'),
            ('Pepper', 'Bird', 'African Gray', 4, 'Male', 'Gray', 'Up to date', 'N/A', 'Yes', 'Very intelligent'),
            ('Luna', 'Bird', 'Lovebird', 1, 'Female', 'Green', 'Up to date', 'N/A', 'Yes', 'Small and affectionate'),
            ('Phoenix', 'Bird', 'Eclectus', 3, 'Male', 'Green', 'Up to date', 'N/A', 'Yes', 'Beautiful and calm'),
            ('Sapphire', 'Bird', 'Blue Parakeet', 2, 'Female', 'Blue', 'Up to date', 'N/A', 'Yes', 'Active and social'),
            ('Goldie', 'Bird', 'Goldfinch', 1, 'Male', 'Yellow and black', 'Up to date', 'N/A', 'Yes', 'Beautiful singer'),
            ('Emerald', 'Bird', 'Green Parakeet', 2, 'Female', 'Green', 'Up to date', 'N/A', 'Yes', 'Playful and curious'),
            ('Crimson', 'Bird', 'Crimson Rosella', 3, 'Male', 'Red and blue', 'Up to date', 'N/A', 'Yes', 'Colorful and active'),
            ('Pearl', 'Bird', 'Pearl Cockatiel', 1, 'Female', 'White with pearls', 'Up to date', 'N/A', 'Yes', 'Elegant and gentle'),
            ('Jade', 'Bird', 'Jade Ringneck', 2, 'Male', 'Green', 'Up to date', 'N/A', 'Yes', 'Talkative and smart'),
            ('Ruby', 'Bird', 'Red Factor Canary', 1, 'Female', 'Red', 'Up to date', 'N/A', 'Yes', 'Beautiful red color'),
            ('Azure', 'Bird', 'Blue Crown Conure', 3, 'Male', 'Blue crown', 'Up to date', 'N/A', 'Yes', 'Social and playful'),
            ('Amber', 'Bird', 'Yellow Canary', 1, 'Female', 'Yellow', 'Up to date', 'N/A', 'Yes', 'Sweet singer'),
            ('Onyx', 'Bird', 'Black Cockatoo', 4, 'Male', 'Black', 'Up to date', 'N/A', 'Yes', 'Rare and beautiful'),
            ('Coral', 'Bird', 'Coral Billed Toucan', 2, 'Female', 'Black with coral bill', 'Up to date', 'N/A', 'Yes', 'Unique and exotic'),
            ('Topaz', 'Bird', 'Yellow Naped Amazon', 3, 'Male', 'Green with yellow', 'Up to date', 'N/A', 'Yes', 'Great talker'),
            ('Violet', 'Bird', 'Violet Ringneck', 1, 'Female', 'Violet', 'Up to date', 'N/A', 'Yes', 'Rare and beautiful')
        ]
        
        # Fish (25)
        fish = [
            ('Nemo', 'Fish', 'Clownfish', 1, 'Male', 'Orange with white stripes', 'N/A', 'N/A', 'N/A', 'Easy to care for'),
            ('Dory', 'Fish', 'Blue Tang', 2, 'Female', 'Blue', 'N/A', 'N/A', 'N/A', 'Peaceful and active'),
            ('Bubbles', 'Fish', 'Goldfish', 1, 'Male', 'Orange', 'N/A', 'N/A', 'N/A', 'Classic and hardy'),
            ('Coral', 'Fish', 'Angelfish', 1, 'Female', 'Silver with black stripes', 'N/A', 'N/A', 'N/A', 'Graceful and beautiful'),
            ('Flash', 'Fish', 'Neon Tetra', 1, 'Male', 'Blue and red', 'N/A', 'N/A', 'N/A', 'Small and colorful'),
            ('Splash', 'Fish', 'Betta', 1, 'Male', 'Blue', 'N/A', 'N/A', 'N/A', 'Beautiful and territorial'),
            ('Rainbow', 'Fish', 'Rainbowfish', 2, 'Female', 'Multi-colored', 'N/A', 'N/A', 'N/A', 'Colorful and active'),
            ('Pearl', 'Fish', 'Pearl Gourami', 1, 'Male', 'Silver with pearls', 'N/A', 'N/A', 'N/A', 'Peaceful and elegant'),
            ('Sunny', 'Fish', 'Yellow Tang', 2, 'Male', 'Yellow', 'N/A', 'N/A', 'N/A', 'Bright and active'),
            ('Midnight', 'Fish', 'Black Molly', 1, 'Female', 'Black', 'N/A', 'N/A', 'N/A', 'Hardy and peaceful'),
            ('Ruby', 'Fish', 'Red Swordtail', 1, 'Male', 'Red', 'N/A', 'N/A', 'N/A', 'Colorful and active'),
            ('Emerald', 'Fish', 'Green Discus', 2, 'Female', 'Green', 'N/A', 'N/A', 'N/A', 'Beautiful and sensitive'),
            ('Goldie', 'Fish', 'Golden Barb', 1, 'Male', 'Gold', 'N/A', 'N/A', 'N/A', 'Active and schooling'),
            ('Azure', 'Fish', 'Blue Ram', 1, 'Female', 'Blue', 'N/A', 'N/A', 'N/A', 'Peaceful and colorful'),
            ('Crimson', 'Fish', 'Red Platy', 1, 'Male', 'Red', 'N/A', 'N/A', 'N/A', 'Easy to breed'),
            ('Silver', 'Fish', 'Silver Dollar', 2, 'Female', 'Silver', 'N/A', 'N/A', 'N/A', 'Large and peaceful'),
            ('Tiger', 'Fish', 'Tiger Barb', 1, 'Male', 'Orange with black stripes', 'N/A', 'N/A', 'N/A', 'Active and schooling'),
            ('Purple', 'Fish', 'Purple Emperor', 1, 'Female', 'Purple', 'N/A', 'N/A', 'N/A', 'Rare and beautiful'),
            ('Orange', 'Fish', 'Orange Platy', 1, 'Male', 'Orange', 'N/A', 'N/A', 'N/A', 'Bright and hardy'),
            ('White', 'Fish', 'White Cloud', 1, 'Female', 'White', 'N/A', 'N/A', 'N/A', 'Small and peaceful'),
            ('Pink', 'Fish', 'Pink Gourami', 1, 'Male', 'Pink', 'N/A', 'N/A', 'N/A', 'Gentle and beautiful'),
            ('Turquoise', 'Fish', 'Turquoise Rainbow', 2, 'Female', 'Turquoise', 'N/A', 'N/A', 'N/A', 'Colorful and active'),
            ('Lemon', 'Fish', 'Lemon Tetra', 1, 'Male', 'Yellow', 'N/A', 'N/A', 'N/A', 'Small and bright'),
            ('Cobalt', 'Fish', 'Cobalt Blue Discus', 2, 'Female', 'Cobalt blue', 'N/A', 'N/A', 'N/A', 'Stunning and peaceful'),
            ('Flame', 'Fish', 'Flame Angelfish', 1, 'Male', 'Red and orange', 'N/A', 'N/A', 'N/A', 'Beautiful and hardy')
        ]
        
        # Other (25)
        other_pets = [
            ('Thumper', 'Rabbit', 'Holland Lop', 1, 'Male', 'Brown and white', 'Up to date', 'Yes', 'Yes', 'Gentle and friendly'),
            ('Bunny', 'Rabbit', 'Netherland Dwarf', 1, 'Female', 'White', 'Up to date', 'Yes', 'Yes', 'Small and cute'),
            ('Hoppy', 'Rabbit', 'Flemish Giant', 2, 'Male', 'Gray', 'Up to date', 'Yes', 'Yes', 'Large and gentle'),
            ('Fluffy', 'Hamster', 'Syrian', 1, 'Male', 'Golden', 'N/A', 'N/A', 'N/A', 'Friendly and nocturnal'),
            ('Nibbles', 'Hamster', 'Dwarf', 1, 'Female', 'Gray', 'N/A', 'N/A', 'N/A', 'Small and active'),
            ('Squeaky', 'Guinea Pig', 'American', 1, 'Male', 'Brown and white', 'Up to date', 'N/A', 'Yes', 'Social and vocal'),
            ('Patches', 'Guinea Pig', 'Abyssinian', 1, 'Female', 'Tri-color', 'Up to date', 'N/A', 'Yes', 'Friendly and curious'),
            ('Spike', 'Hedgehog', 'African Pygmy', 1, 'Male', 'Brown', 'N/A', 'N/A', 'N/A', 'Unique and nocturnal'),
            ('Prickles', 'Hedgehog', 'European', 2, 'Female', 'Brown', 'N/A', 'N/A', 'N/A', 'Gentle when handled'),
            ('Slither', 'Snake', 'Corn Snake', 2, 'Male', 'Orange and red', 'N/A', 'N/A', 'N/A', 'Docile and easy care'),
            ('Python', 'Snake', 'Ball Python', 3, 'Female', 'Brown', 'N/A', 'N/A', 'N/A', 'Gentle and calm'),
            ('Lizard', 'Lizard', 'Bearded Dragon', 1, 'Male', 'Tan and brown', 'N/A', 'N/A', 'N/A', 'Friendly and hardy'),
            ('Gecko', 'Lizard', 'Leopard Gecko', 1, 'Female', 'Yellow with spots', 'N/A', 'N/A', 'N/A', 'Easy to handle'),
            ('Turtle', 'Turtle', 'Red-Eared Slider', 3, 'Male', 'Green with red ears', 'N/A', 'N/A', 'N/A', 'Long-lived and hardy'),
            ('Tortoise', 'Turtle', 'Russian Tortoise', 5, 'Female', 'Brown', 'N/A', 'N/A', 'N/A', 'Small and friendly'),
            ('Frog', 'Amphibian', 'Tree Frog', 1, 'Male', 'Green', 'N/A', 'N/A', 'N/A', 'Colorful and arboreal'),
            ('Tadpole', 'Amphibian', 'Fire-Bellied Toad', 1, 'Female', 'Green with red belly', 'N/A', 'N/A', 'N/A', 'Colorful and active'),
            ('Hermit', 'Crab', 'Hermit Crab', 1, 'Male', 'Brown shell', 'N/A', 'N/A', 'N/A', 'Interesting and low maintenance'),
            ('Crawler', 'Crab', 'Fiddler Crab', 1, 'Female', 'Brown', 'N/A', 'N/A', 'N/A', 'Active and interesting'),
            ('Spider', 'Arachnid', 'Tarantula', 2, 'Male', 'Brown', 'N/A', 'N/A', 'N/A', 'Docile and fascinating'),
            ('Scorpion', 'Arachnid', 'Emperor Scorpion', 1, 'Female', 'Black', 'N/A', 'N/A', 'N/A', 'Large and impressive'),
            ('Chinchilla', 'Rodent', 'Chinchilla', 2, 'Male', 'Gray', 'N/A', 'N/A', 'N/A', 'Soft and playful'),
            ('Ferret', 'Mustelid', 'Ferret', 1, 'Female', 'Brown and white', 'Up to date', 'Yes', 'Yes', 'Playful and curious'),
            ('Skunk', 'Mustelid', 'Domestic Skunk', 2, 'Male', 'Black and white', 'Up to date', 'Yes', 'Yes', 'Unique and friendly'),
            ('Sugar', 'Marsupial', 'Sugar Glider', 1, 'Female', 'Gray with stripes', 'N/A', 'N/A', 'N/A', 'Small and gliding')
        ]
        
        # Combine all pets
        sample_pets = dogs + cats + birds + fish + other_pets
        
        for pet in sample_pets:
            cursor.execute('''
                INSERT INTO pets (name, species, breed, age, gender, markings, vaccine_status, neutered_spayed, dewormed, medical_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', pet)
        
        # Insert sample services
        sample_services = [
            ('Grooming', 'Professional pet grooming services', 50.00, 60),
            ('Health Care', 'Veterinary health checkups', 75.00, 30),
            ('Daycare', 'Pet daycare services', 40.00, 480),
            ('Training', 'Pet training sessions', 60.00, 45),
            ('Hygienic Care', 'Specialized hygiene services', 35.00, 30)
        ]
        
        for service in sample_services:
            cursor.execute('''
                INSERT INTO services (name, description, price, duration_minutes)
                VALUES (?, ?, ?, ?)
            ''', service)
        
        # Insert sample products (50 total)
        sample_products = [
            # Food (15)
            ('Premium Dog Food', 'Food', 'High-quality dog food with real meat', 25.99, 50, ''),
            ('Grain-Free Cat Food', 'Food', 'Natural grain-free cat food', 22.99, 45, ''),
            ('Bird Seed Mix', 'Food', 'Nutritious seed mix for birds', 8.99, 60, ''),
            ('Fish Flakes', 'Food', 'Complete nutrition fish flakes', 6.99, 80, ''),
            ('Rabbit Pellets', 'Food', 'High-fiber rabbit food', 12.99, 35, ''),
            ('Hamster Mix', 'Food', 'Balanced hamster diet', 7.99, 40, ''),
            ('Guinea Pig Food', 'Food', 'Vitamin C enriched guinea pig food', 9.99, 30, ''),
            ('Reptile Pellets', 'Food', 'Complete reptile nutrition', 15.99, 25, ''),
            ('Puppy Formula', 'Food', 'Special formula for puppies', 18.99, 20, ''),
            ('Kitten Food', 'Food', 'High-protein kitten food', 16.99, 25, ''),
            ('Senior Dog Food', 'Food', 'Easy-to-digest senior dog food', 28.99, 15, ''),
            ('Senior Cat Food', 'Food', 'Joint support for senior cats', 24.99, 20, ''),
            ('Treats Variety Pack', 'Food', 'Mixed treats for all pets', 14.99, 50, ''),
            ('Freeze-Dried Raw', 'Food', 'Natural freeze-dried raw food', 35.99, 10, ''),
            ('Wet Cat Food', 'Food', 'Premium wet cat food variety', 19.99, 40, ''),
            
            # Medications (10)
            ('Flea Treatment', 'Medications', 'Monthly flea prevention', 24.99, 30, ''),
            ('Heartworm Prevention', 'Medications', 'Monthly heartworm protection', 29.99, 25, ''),
            ('Pet Vitamins', 'Medications', 'Essential pet vitamins', 19.99, 40, ''),
            ('Joint Supplements', 'Medications', 'Glucosamine for joint health', 22.99, 20, ''),
            ('Probiotics', 'Medications', 'Digestive health probiotics', 16.99, 35, ''),
            ('Antibiotic Ointment', 'Medications', 'Topical antibiotic for wounds', 12.99, 15, ''),
            ('Ear Cleaner', 'Medications', 'Gentle ear cleaning solution', 8.99, 25, ''),
            ('Eye Drops', 'Medications', 'Soothing eye drops for pets', 14.99, 20, ''),
            ('Deworming Tablets', 'Medications', 'Internal parasite treatment', 18.99, 30, ''),
            ('Pain Relief', 'Medications', 'Safe pain relief for pets', 26.99, 10, ''),
            
            # Toys (15)
            ('Interactive Dog Toys', 'Toys', 'Mental stimulation toys', 12.99, 25, ''),
            ('Catnip Mice', 'Toys', 'Catnip-filled mouse toys', 4.99, 50, ''),
            ('Bird Perches', 'Toys', 'Natural wood perches', 15.99, 20, ''),
            ('Fish Tank Decor', 'Toys', 'Colorful aquarium decorations', 8.99, 30, ''),
            ('Rabbit Chew Toys', 'Toys', 'Safe chewing toys for rabbits', 6.99, 40, ''),
            ('Hamster Exercise Wheel', 'Toys', 'Silent exercise wheel', 19.99, 15, ''),
            ('Guinea Pig Hideout', 'Toys', 'Cozy hideout for guinea pigs', 11.99, 25, ''),
            ('Dog Puzzle Feeder', 'Toys', 'Slow feeder puzzle toy', 24.99, 20, ''),
            ('Cat Scratching Post', 'Toys', 'Multi-level scratching post', 45.99, 10, ''),
            ('Bird Swings', 'Toys', 'Colorful bird swings', 9.99, 35, ''),
            ('Dog Rope Toys', 'Toys', 'Durable rope tug toys', 8.99, 30, ''),
            ('Cat Laser Pointer', 'Toys', 'Interactive laser pointer', 7.99, 40, ''),
            ('Fish Bubble Wand', 'Toys', 'Aquarium bubble wand', 5.99, 25, ''),
            ('Rabbit Tunnel', 'Toys', 'Play tunnel for rabbits', 16.99, 15, ''),
            ('Hamster Ball', 'Toys', 'Exercise ball for hamsters', 12.99, 20, ''),
            
            # Other (10)
            ('Cat Litter', 'Other', 'Premium clumping cat litter', 15.99, 30, ''),
            ('Dog Leash', 'Other', 'Durable nylon dog leash', 12.99, 25, ''),
            ('Pet Carrier', 'Other', 'Travel carrier for small pets', 35.99, 15, ''),
            ('Water Bottle', 'Other', 'Automatic water dispenser', 18.99, 20, ''),
            ('Food Bowl Set', 'Other', 'Stainless steel bowl set', 14.99, 30, ''),
            ('Pet Bed', 'Other', 'Orthopedic pet bed', 39.99, 12, ''),
            ('Grooming Brush', 'Other', 'Professional grooming brush', 9.99, 35, ''),
            ('Nail Clippers', 'Other', 'Safe pet nail clippers', 6.99, 25, ''),
            ('Pet Shampoo', 'Other', 'Gentle pet shampoo', 11.99, 40, ''),
            ('Training Pads', 'Other', 'House training pads', 16.99, 50, '')
        ]
        
        for product in sample_products:
            cursor.execute('''
                INSERT INTO products (name, category, description, price, stock_quantity, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', product)
        
        conn.commit()
        conn.close()
    
    def create_user(self, name, email, password, phone):
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, phone)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password_hash, phone))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                SELECT id, name, email, phone FROM users 
                WHERE email = ? AND password_hash = ?
            ''', (email, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'phone': user[3]
                }
            return None
        except Exception:
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, phone FROM users WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'phone': user[3]
                }
            return None
        except Exception:
            return None
    
    def get_available_pets(self, category='All'):
        """Get available pets by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category == 'All':
                cursor.execute('''
                    SELECT * FROM pets WHERE available = 1 ORDER BY created_at DESC
                ''')
            else:
                cursor.execute('''
                    SELECT * FROM pets WHERE available = 1 AND species = ? ORDER BY created_at DESC
                ''', (category,))
            
            pets = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            pet_list = []
            for pet in pets:
                pet_list.append({
                    'id': pet[0],
                    'name': pet[1],
                    'species': pet[2],
                    'breed': pet[3],
                    'age': pet[4],
                    'gender': pet[5],
                    'markings': pet[6],
                    'vaccine_status': pet[7],
                    'neutered_spayed': pet[8],
                    'dewormed': pet[9],
                    'medical_notes': pet[10],
                    'image_path': pet[11],
                    'available': pet[12],
                    'created_at': pet[13]
                })
            
            return pet_list
        except Exception:
            return []
    
    def submit_adoption_application(self, application_data):
        """Submit adoption application"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO adoption_applications 
                (user_id, pet_id, full_name, address, age, contact_number, email, 
                 care_commitment, can_provide_food, can_provide_vet_care, 
                 can_provide_safe_home, agreement_accepted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                application_data['user_id'],
                application_data['pet_id'],
                application_data['full_name'],
                application_data['address'],
                application_data['age'],
                application_data['contact_number'],
                application_data['email'],
                application_data['care_commitment'],
                application_data['can_provide_food'],
                application_data['can_provide_vet_care'],
                application_data['can_provide_safe_home'],
                application_data['agreement_accepted']
            ))
            
            application_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return application_id
        except Exception:
            return None
    
    def get_services(self):
        """Get all available services"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM services ORDER BY name')
            services = cursor.fetchall()
            conn.close()
            
            service_list = []
            for service in services:
                service_list.append({
                    'id': service[0],
                    'name': service[1],
                    'description': service[2],
                    'price': service[3],
                    'duration_minutes': service[4]
                })
            
            return service_list
        except Exception:
            return []
    
    def book_service(self, booking_data):
        """Book a service"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO service_bookings 
                (user_id, service_id, pet_name, booking_date, booking_time, 
                 staff_member, special_instructions)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                booking_data['user_id'],
                booking_data['service_id'],
                booking_data['pet_name'],
                booking_data['booking_date'],
                booking_data['booking_time'],
                booking_data['staff_member'],
                booking_data['special_instructions']
            ))
            
            booking_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return booking_id
        except Exception:
            return None
    
    def get_products(self, category=None):
        """Get products by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY name', (category,))
            else:
                cursor.execute('SELECT * FROM products ORDER BY category, name')
            
            products = cursor.fetchall()
            conn.close()
            
            product_list = []
            for product in products:
                product_list.append({
                    'id': product[0],
                    'name': product[1],
                    'category': product[2],
                    'description': product[3],
                    'price': product[4],
                    'stock_quantity': product[5],
                    'image_path': product[6]
                })
            
            return product_list
        except Exception:
            return []
    
    def submit_donation(self, donation_data):
        """Submit a donation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO donations (donor_name, amount, email, message)
                VALUES (?, ?, ?, ?)
            ''', (
                donation_data['donor_name'],
                donation_data['amount'],
                donation_data['email'],
                donation_data['message']
            ))
            
            donation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return donation_id
        except Exception:
            return None


if __name__ == "__main__":
    app = OnlyPetsApp()
    app.run()
