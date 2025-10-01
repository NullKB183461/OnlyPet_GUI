import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
from PIL import Image
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PetAdoptionSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OnlyPets - Pet Adoption & Service Management System")
        self.geometry("1440x900")
        self.configure(fg_color="#17120E")
        
        self.current_user = None
        self.cart = []
        self.favorites = []
        self.bookings = []
        
        self.pets_data = []
        self.products_data = []
        self.users_data = []
        self.applications_data = []
        self.bookings_data = []
        
        self.main_container = None
        self.carousel_index = 0
        self.carousel_frame = None
        self.signin_modal = None
        self.signup_modal = None
        self.selected_category = None
        self.pets_display_frame = None
        self.selected_product_category = None
        self.products_display_frame = None
        
        self.pet_images = {
            1: "attached_assets/stock_images/golden_retriever_dog_a7247182.jpg",
            2: "attached_assets/stock_images/persian_cat_white_b3c7d5f4.jpg",
            3: "attached_assets/stock_images/labrador_dog_black_8c443e19.jpg",
            4: "attached_assets/stock_images/siamese_cat_63ef7d8c.jpg",
            5: "attached_assets/stock_images/german_shepherd_dog_1b92d0c8.jpg",
            6: "attached_assets/stock_images/canary_bird_yellow_602645ea.jpg",
            7: "attached_assets/stock_images/goldfish_orange_aqua_3219360d.jpg",
            8: "attached_assets/stock_images/beagle_dog_e6a00047.jpg",
            9: "attached_assets/stock_images/maine_coon_cat_857b9e89.jpg",
            10: "attached_assets/stock_images/cockatiel_bird_532dd605.jpg",
            11: "attached_assets/stock_images/clownfish_aquarium_e04c3cc7.jpg",
            12: "attached_assets/stock_images/poodle_dog_white_60b40c1e.jpg",
            13: "attached_assets/stock_images/british_shorthair_ca_be32d836.jpg",
            14: "attached_assets/stock_images/rabbit_holland_lop_6b304f11.jpg",
            15: "attached_assets/stock_images/hedgehog_pet_bba047fd.jpg"
        }
        
        self.product_images = {
            "Food": "attached_assets/stock_images/dog_food_bowl_c2f443f4.jpg",
            "Medications": "attached_assets/stock_images/pet_medication_suppl_db6f0ab6.jpg",
            "Toys": "attached_assets/stock_images/pet_toys_collection_c578af83.jpg",
            "Essentials": "attached_assets/stock_images/pet_bed_luxury_6ffccdd3.jpg"
        }
        
        self.init_data()
        self.create_main_container()
        self.show_landing_page()
    
    def init_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
                self.pets_data = data.get("pets", [])
                self.products_data = data.get("products", [])
                self.users_data = data.get("users", [])
                self.applications_data = data.get("applications", [])
                self.bookings_data = data.get("bookings", [])
        else:
            self.init_default_data()
            self.save_data()
    
    def init_default_data(self):
        self.pets_data = [
            {
                "id": 1, "name": "Max", "category": "Dogs", "breed": "Golden Retriever",
                "age": "2 years", "gender": "Male", "markings": "Golden coat with white chest",
                "neutered": "Yes", "dewormed": "Yes", 
                "medical_notes": "Healthy, vaccinated, loves to play fetch"
            },
            {
                "id": 2, "name": "Luna", "category": "Cats", "breed": "Persian",
                "age": "1 year", "gender": "Female", "markings": "White with grey patches",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Healthy, enjoys quiet spaces"
            },
            {
                "id": 3, "name": "Charlie", "category": "Dogs", "breed": "Labrador",
                "age": "3 years", "gender": "Male", "markings": "Black coat",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Very energetic, great with kids"
            },
            {
                "id": 4, "name": "Bella", "category": "Cats", "breed": "Siamese",
                "age": "2 years", "gender": "Female", "markings": "Cream with dark points",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Vocal, loves attention"
            },
            {
                "id": 5, "name": "Rocky", "category": "Dogs", "breed": "German Shepherd",
                "age": "4 years", "gender": "Male", "markings": "Black and tan",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Trained, excellent guard dog"
            },
            {
                "id": 6, "name": "Tweety", "category": "Birds", "breed": "Canary",
                "age": "1 year", "gender": "Male", "markings": "Bright yellow",
                "neutered": "N/A", "dewormed": "N/A",
                "medical_notes": "Beautiful singer, healthy"
            },
            {
                "id": 7, "name": "Bubbles", "category": "Fish", "breed": "Goldfish",
                "age": "6 months", "gender": "Unknown", "markings": "Orange and white",
                "neutered": "N/A", "dewormed": "N/A",
                "medical_notes": "Healthy, easy to care for"
            },
            {
                "id": 8, "name": "Daisy", "category": "Dogs", "breed": "Beagle",
                "age": "1.5 years", "gender": "Female", "markings": "Tri-color",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Friendly, loves food"
            },
            {
                "id": 9, "name": "Whiskers", "category": "Cats", "breed": "Maine Coon",
                "age": "3 years", "gender": "Male", "markings": "Brown tabby",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Large, gentle giant"
            },
            {
                "id": 10, "name": "Coco", "category": "Birds", "breed": "Cockatiel",
                "age": "2 years", "gender": "Female", "markings": "Grey with yellow crest",
                "neutered": "N/A", "dewormed": "N/A",
                "medical_notes": "Tame, enjoys head scratches"
            },
            {
                "id": 11, "name": "Nemo", "category": "Fish", "breed": "Clownfish",
                "age": "1 year", "gender": "Male", "markings": "Orange with white stripes",
                "neutered": "N/A", "dewormed": "N/A",
                "medical_notes": "Active swimmer, healthy"
            },
            {
                "id": 12, "name": "Buddy", "category": "Dogs", "breed": "Poodle",
                "age": "2 years", "gender": "Male", "markings": "White curly coat",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Hypoallergenic, smart"
            },
            {
                "id": 13, "name": "Mittens", "category": "Cats", "breed": "British Shorthair",
                "age": "1 year", "gender": "Female", "markings": "Grey blue",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Calm, loves cuddles"
            },
            {
                "id": 14, "name": "Hoppy", "category": "Others", "breed": "Holland Lop Rabbit",
                "age": "1 year", "gender": "Male", "markings": "Brown and white",
                "neutered": "Yes", "dewormed": "Yes",
                "medical_notes": "Friendly, litter trained"
            },
            {
                "id": 15, "name": "Spike", "category": "Others", "breed": "Hedgehog",
                "age": "6 months", "gender": "Male", "markings": "Brown quills",
                "neutered": "No", "dewormed": "Yes",
                "medical_notes": "Nocturnal, quiet"
            }
        ]
        
        self.products_data = [
            {
                "id": 1, "name": "Premium Dog Food - Chicken & Rice", "category": "Food",
                "price": 2575.44, "description": "High-quality nutrition for adult dogs. Made with real chicken and brown rice.",
                "rating": 4.8
            },
            {
                "id": 2, "name": "Cat Food - Salmon Delight", "category": "Food",
                "price": 2183.44, "description": "Delicious salmon-based cat food with essential vitamins and minerals.",
                "rating": 4.7
            },
            {
                "id": 3, "name": "Bird Seed Mix - Premium Blend", "category": "Food",
                "price": 895.44, "description": "Nutritious seed blend for all bird species.",
                "rating": 4.6
            },
            {
                "id": 4, "name": "Fish Flakes - Tropical Formula", "category": "Food",
                "price": 727.44, "description": "Complete nutrition for tropical fish.",
                "rating": 4.5
            },
            {
                "id": 5, "name": "Flea & Tick Prevention", "category": "Medications",
                "price": 3135.44, "description": "Monthly treatment for dogs and cats. Prevents fleas, ticks, and heartworm.",
                "rating": 4.9
            },
            {
                "id": 6, "name": "Probiotic Supplement", "category": "Medications",
                "price": 1679.44, "description": "Supports digestive health for dogs and cats.",
                "rating": 4.7
            },
            {
                "id": 7, "name": "Joint Support Tablets", "category": "Medications",
                "price": 2407.44, "description": "Helps maintain healthy joints in senior pets.",
                "rating": 4.8
            },
            {
                "id": 8, "name": "Interactive Puzzle Toy", "category": "Toys",
                "price": 1399.44, "description": "Keeps dogs mentally stimulated and entertained.",
                "rating": 4.6
            },
            {
                "id": 9, "name": "Feather Wand for Cats", "category": "Toys",
                "price": 727.44, "description": "Interactive toy for active play with your cat.",
                "rating": 4.7
            },
            {
                "id": 10, "name": "Chew Rope Toy", "category": "Toys",
                "price": 559.44, "description": "Durable rope toy for dogs of all sizes.",
                "rating": 4.5
            },
            {
                "id": 11, "name": "Catnip Mouse Set (3 pack)", "category": "Toys",
                "price": 839.44, "description": "Soft plush mice filled with premium catnip.",
                "rating": 4.8
            },
            {
                "id": 12, "name": "Bird Mirror with Bell", "category": "Toys",
                "price": 503.44, "description": "Keeps birds entertained for hours.",
                "rating": 4.4
            },
            {
                "id": 13, "name": "Luxury Pet Bed - Large", "category": "Essentials",
                "price": 4479.44, "description": "Orthopedic memory foam bed with washable cover.",
                "rating": 4.9
            },
            {
                "id": 14, "name": "Stainless Steel Food Bowls", "category": "Essentials",
                "price": 1119.44, "description": "Set of 2 non-slip bowls for food and water.",
                "rating": 4.7
            },
            {
                "id": 15, "name": "Adjustable Dog Collar", "category": "Essentials",
                "price": 951.44, "description": "Comfortable nylon collar with quick-release buckle.",
                "rating": 4.6
            },
            {
                "id": 16, "name": "Cat Litter Box - Self-Cleaning", "category": "Essentials",
                "price": 7279.44, "description": "Automatic litter box with odor control.",
                "rating": 4.8
            },
            {
                "id": 17, "name": "Pet Carrier - Medium", "category": "Essentials",
                "price": 2799.44, "description": "Airline-approved carrier with ventilation.",
                "rating": 4.7
            },
            {
                "id": 18, "name": "Grooming Brush Set", "category": "Essentials",
                "price": 1287.44, "description": "Complete set for all coat types.",
                "rating": 4.6
            },
            {
                "id": 19, "name": "Aquarium Filter System", "category": "Essentials",
                "price": 3359.44, "description": "Quiet and efficient filtration for tanks up to 50 gallons.",
                "rating": 4.8
            },
            {
                "id": 20, "name": "Dental Chews for Dogs", "category": "Medications",
                "price": 1063.44, "description": "Helps reduce tartar and freshen breath.",
                "rating": 4.7
            },
            {
                "id": 21, "name": "Premium Puppy Food", "category": "Food",
                "price": 2967.44, "description": "Complete nutrition for growing puppies.",
                "rating": 4.9
            },
            {
                "id": 22, "name": "Senior Cat Food", "category": "Food",
                "price": 2351.44, "description": "Specially formulated for cats 7+ years.",
                "rating": 4.8
            },
            {
                "id": 23, "name": "Hamster Pellets", "category": "Food",
                "price": 615.44, "description": "Balanced diet for hamsters and small animals.",
                "rating": 4.5
            },
            {
                "id": 24, "name": "Scratching Post Tower", "category": "Toys",
                "price": 5039.44, "description": "Multi-level cat tree with scratching posts and perches.",
                "rating": 4.9
            },
            {
                "id": 25, "name": "Dog Training Treats", "category": "Food",
                "price": 783.44, "description": "Low-calorie treats perfect for training sessions.",
                "rating": 4.7
            }
        ]
        
        self.users_data = []
        self.applications_data = []
        self.bookings_data = []
    
    def save_data(self):
        data = {
            "pets": self.pets_data,
            "products": self.products_data,
            "users": self.users_data,
            "applications": self.applications_data,
            "bookings": self.bookings_data
        }
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def create_main_container(self):
        self.main_container = ctk.CTkFrame(self, fg_color="#17120E")
        self.main_container.pack(fill="both", expand=True)
    
    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def load_pet_image(self, pet_id, size=(200, 200)):
        if pet_id in self.pet_images and os.path.exists(self.pet_images[pet_id]):
            try:
                image = Image.open(self.pet_images[pet_id])
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ctk.CTkImage(light_image=image, dark_image=image, size=size)
            except:
                return None
        return None
    
    def load_product_image(self, category, size=(150, 150)):
        if category in self.product_images and os.path.exists(self.product_images[category]):
            try:
                image = Image.open(self.product_images[category])
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ctk.CTkImage(light_image=image, dark_image=image, size=size)
            except:
                return None
        return None
    
    def create_header(self, parent, show_user=False):
        header_frame = ctk.CTkFrame(parent, fg_color="#1C130B", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        nav_items = [
            ("Home", 98, self.show_landing_page),
            ("Adoption", 272, self.show_adoption_page),
            ("Service", 447, self.show_service_page),
            ("Products", 894, self.show_products_page),
            ("Contact", 1069, self.show_contact_page)
        ]
        
        for text, x_pos, command in nav_items:
            btn = ctk.CTkButton(
                header_frame, text=text, fg_color="transparent",
                hover_color="#603C1E", text_color="#FFFFFF",
                font=("Microsoft JhengHei UI", 16), command=command,
                width=100, height=40
            )
            btn.place(x=x_pos, y=20)
        
        logo_label = ctk.CTkLabel(
            header_frame, text="🐾 OnlyPets",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 24, "bold")
        )
        logo_label.place(x=650, y=20)
        
        if show_user and self.current_user:
            user_label = ctk.CTkLabel(
                header_frame, text=f"Hello, {self.current_user}",
                text_color="#D7A765", font=("Microsoft JhengHei UI", 14)
            )
            user_label.place(x=1250, y=28)
        else:
            signin_btn = ctk.CTkButton(
                header_frame, text="Signup/SignIn", fg_color="#603C1E",
                hover_color="#D7A765", text_color="#FFFFFF",
                font=("Microsoft JhengHei UI", 16), command=self.show_signin_modal,
                width=120, height=40
            )
            signin_btn.place(x=1250, y=20)
        
        return header_frame
    
    def check_login(self, action_name):
        if not self.current_user:
            messagebox.showwarning("Login Required", f"Please sign in to {action_name}")
            self.show_signin_modal()
            return False
        return True
    
    def show_landing_page(self):
        self.clear_main_container()
        
        canvas = ctk.CTkCanvas(self.main_container, bg="#17120E", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#17120E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.create_header(scrollable_frame, show_user=self.current_user is not None)
        
        hero_section = ctk.CTkFrame(scrollable_frame, fg_color="#17120E", height=857, width=1440)
        hero_section.pack(fill="x", pady=0)
        hero_section.pack_propagate(False)
        
        hero_label = ctk.CTkLabel(
            hero_section,
            text="FIND YOUR NEW BEST FRIEND\nAND GIVE THEM A FOREVER HOME,\nWHILE WE CARE FOR ALL YOUR PET'S NEEDS",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 48, "bold"),
            justify="center"
        )
        hero_label.pack(pady=(200, 30))
        
        get_started_btn = ctk.CTkButton(
            hero_section, text="Get Started", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 20, "bold"),
            width=200, height=60, corner_radius=30,
            command=self.show_adoption_page
        )
        get_started_btn.pack(pady=20)
        
        about_section = ctk.CTkFrame(scrollable_frame, fg_color="#1B1612", height=481, width=1440)
        about_section.pack(fill="x", pady=20)
        about_section.pack_propagate(False)
        
        about_title = ctk.CTkLabel(
            about_section, text="About Our Shelter",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 36, "bold")
        )
        about_title.pack(pady=(40, 20))
        
        about_text = ctk.CTkLabel(
            about_section,
            text="We are devoted to enriching the bond between pets and their owners by offering\n"
                 "carefully selected products and services designed with their well-being in mind.\n"
                 "From nourishing food and premium accessories to expert grooming and healthcare,\n"
                 "everything we do is centered on providing the best for your furry, feathered, or finned friends.\n\n"
                 "With OnlyPets, you can trust that every choice you make for your beloved companions\n"
                 "is one that prioritizes their happiness, comfort, and care.",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16),
            justify="center"
        )
        about_text.pack(pady=20)
        
        pets_section = ctk.CTkFrame(scrollable_frame, fg_color="#17120E", height=848, width=1440)
        pets_section.pack(fill="x", pady=20)
        pets_section.pack_propagate(False)
        
        pets_title = ctk.CTkLabel(
            pets_section, text="Our friends who are looking for a house",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 32, "bold")
        )
        pets_title.pack(pady=(40, 30))
        
        self.carousel_index = 0
        self.carousel_frame = ctk.CTkFrame(pets_section, fg_color="transparent")
        self.carousel_frame.pack(pady=20)
        
        self.update_carousel()
        
        donation_section = ctk.CTkFrame(scrollable_frame, fg_color="#1B1612", height=480, width=1440)
        donation_section.pack(fill="x", pady=20)
        donation_section.pack_propagate(False)
        
        donation_title = ctk.CTkLabel(
            donation_section, text="You can make a donation",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 32, "bold")
        )
        donation_title.pack(pady=(40, 20))
        
        bank_info = ctk.CTkLabel(
            donation_section,
            text="Name of Bank / Bank Account Number\nOnlyPets Animal Care Foundation - 1234-5678-9012",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 18)
        )
        bank_info.pack(pady=10)
        
        donation_text = ctk.CTkLabel(
            donation_section,
            text="Through your support, we aim to extend love and care to animals in need.\n"
                 "By making a donation, you help us provide food, shelter, and medical assistance\n"
                 "to stray and abandoned pets. Every contribution, big or small, makes a difference—\n"
                 "because together, we can create a better world for our furry friends.",
            text_color="#DEDEDE", font=("Microsoft JhengHei UI", 14),
            justify="center"
        )
        donation_text.pack(pady=20)
        
        contact_frame = ctk.CTkFrame(scrollable_frame, fg_color="#1C130B", height=400, width=1440)
        contact_frame.pack(fill="x", pady=(20, 0))
        contact_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            contact_frame, text="Contact Us",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 28, "bold")
        )
        title.pack(pady=(30, 20))
        
        info_text = ctk.CTkLabel(
            contact_frame,
            text="OnlyPets Animal Care Foundation\nEmail: info@onlypets.com\nPhone: +63 (917) 123-4567\nAddress: 123 Pet Street, Manila, Philippines",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14),
            justify="center"
        )
        info_text.pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def update_carousel(self):
        for widget in self.carousel_frame.winfo_children():
            widget.destroy()
        
        left_arrow = ctk.CTkButton(
            self.carousel_frame, text="◀", fg_color="#603C1E",
            hover_color="#D7A765", width=50, height=400,
            font=("Arial", 24), command=self.carousel_prev
        )
        left_arrow.grid(row=0, column=0, padx=20)
        
        display_pets = self.pets_data[self.carousel_index:self.carousel_index+3]
        
        for i, pet in enumerate(display_pets):
            pet_card = ctk.CTkFrame(self.carousel_frame, fg_color="#261E18", width=300, height=480, corner_radius=15)
            pet_card.grid(row=0, column=i+1, padx=20)
            pet_card.pack_propagate(False)
            
            pet_img = self.load_pet_image(pet['id'], size=(200, 200))
            if pet_img:
                pet_img_label = ctk.CTkLabel(pet_card, image=pet_img, text="")
                pet_img_label.pack(pady=(20, 10))
            else:
                pet_img_label = ctk.CTkLabel(
                    pet_card, text=f"🐾", text_color="#D7A765",
                    font=("Microsoft JhengHei UI", 48)
                )
                pet_img_label.pack(pady=(40, 10))
            
            pet_name = ctk.CTkLabel(
                pet_card, text=pet['name'], text_color="#D7A765",
                font=("Microsoft JhengHei UI", 24, "bold")
            )
            pet_name.pack(pady=10)
            
            pet_info = ctk.CTkLabel(
                pet_card, text=f"{pet['breed']}\n{pet['age']} • {pet['gender']}",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14)
            )
            pet_info.pack(pady=10)
            
            adopt_btn = ctk.CTkButton(
                pet_card, text="Adopt Pet", fg_color="#D7A765",
                hover_color="#FFB774", text_color="#1C130B",
                font=("Microsoft JhengHei UI", 16, "bold"),
                command=lambda p=pet: self.show_pet_details_modal(p)
            )
            adopt_btn.pack(pady=20)
        
        right_arrow = ctk.CTkButton(
            self.carousel_frame, text="▶", fg_color="#603C1E",
            hover_color="#D7A765", width=50, height=400,
            font=("Arial", 24), command=self.carousel_next
        )
        right_arrow.grid(row=0, column=4, padx=20)
    
    def carousel_next(self):
        if self.carousel_index + 3 < len(self.pets_data):
            self.carousel_index += 1
            self.update_carousel()
    
    def carousel_prev(self):
        if self.carousel_index > 0:
            self.carousel_index -= 1
            self.update_carousel()
    
    def show_signin_modal(self):
        self.signin_modal = ctk.CTkToplevel(self)
        self.signin_modal.title("Sign In")
        self.signin_modal.geometry("500x650")
        self.signin_modal.configure(fg_color="#17120E")
        self.signin_modal.transient(self)
        self.signin_modal.grab_set()
        
        title = ctk.CTkLabel(
            self.signin_modal, text="Sign In to OnlyPets",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 28, "bold")
        )
        title.pack(pady=(40, 30))
        
        fullname_label = ctk.CTkLabel(self.signin_modal, text="Full Name:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        fullname_label.pack(pady=(10, 5))
        
        fullname_entry = ctk.CTkEntry(
            self.signin_modal, width=350, height=40,
            font=("Microsoft JhengHei UI", 14)
        )
        fullname_entry.pack(pady=5)
        
        password_label = ctk.CTkLabel(self.signin_modal, text="Password:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        password_label.pack(pady=(10, 5))
        
        password_entry = ctk.CTkEntry(
            self.signin_modal, width=350, height=40, show="*",
            font=("Microsoft JhengHei UI", 14)
        )
        password_entry.pack(pady=5)
        
        forgot_btn = ctk.CTkButton(
            self.signin_modal, text="Forgot Password?",
            fg_color="transparent", hover_color="#603C1E",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 12)
        )
        forgot_btn.pack(pady=10)
        
        signin_btn = ctk.CTkButton(
            self.signin_modal, text="Sign In", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 16, "bold"),
            width=350, height=45,
            command=lambda: self.do_signin(fullname_entry.get(), password_entry.get())
        )
        signin_btn.pack(pady=20)
        
        or_label = ctk.CTkLabel(self.signin_modal, text="— Or sign in with —", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 12))
        or_label.pack(pady=10)
        
        social_frame = ctk.CTkFrame(self.signin_modal, fg_color="transparent")
        social_frame.pack(pady=10)
        
        for social in ["Facebook", "Apple", "Gmail"]:
            social_btn = ctk.CTkButton(
                social_frame, text=social, fg_color="#603C1E",
                hover_color="#D7A765", width=100, height=35,
                font=("Microsoft JhengHei UI", 12)
            )
            social_btn.pack(side="left", padx=10)
        
        signup_label = ctk.CTkLabel(self.signin_modal, text="Don't have an account?", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 12))
        signup_label.pack(pady=(20, 5))
        
        signup_link = ctk.CTkButton(
            self.signin_modal, text="Sign Up Here",
            fg_color="transparent", hover_color="#603C1E",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 12, "bold"),
            command=self.show_signup_modal
        )
        signup_link.pack()
    
    def show_signup_modal(self):
        if hasattr(self, 'signin_modal') and self.signin_modal:
            self.signin_modal.destroy()
        
        self.signup_modal = ctk.CTkToplevel(self)
        self.signup_modal.title("Sign Up")
        self.signup_modal.geometry("500x750")
        self.signup_modal.configure(fg_color="#17120E")
        self.signup_modal.transient(self)
        self.signup_modal.grab_set()
        
        title = ctk.CTkLabel(
            self.signup_modal, text="Create Your Account",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 28, "bold")
        )
        title.pack(pady=(40, 30))
        
        email_label = ctk.CTkLabel(self.signup_modal, text="Email:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        email_label.pack(pady=(10, 5))
        
        email_entry = ctk.CTkEntry(
            self.signup_modal, width=350, height=40,
            font=("Microsoft JhengHei UI", 14)
        )
        email_entry.pack(pady=5)
        
        fullname_label = ctk.CTkLabel(self.signup_modal, text="Full Name:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        fullname_label.pack(pady=(10, 5))
        
        fullname_entry = ctk.CTkEntry(
            self.signup_modal, width=350, height=40,
            font=("Microsoft JhengHei UI", 14)
        )
        fullname_entry.pack(pady=5)
        
        password_label = ctk.CTkLabel(self.signup_modal, text="Password:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        password_label.pack(pady=(10, 5))
        
        password_entry = ctk.CTkEntry(
            self.signup_modal, width=350, height=40, show="*",
            font=("Microsoft JhengHei UI", 14)
        )
        password_entry.pack(pady=5)
        
        confirm_password_label = ctk.CTkLabel(self.signup_modal, text="Confirm Password:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        confirm_password_label.pack(pady=(10, 5))
        
        confirm_password_entry = ctk.CTkEntry(
            self.signup_modal, width=350, height=40, show="*",
            font=("Microsoft JhengHei UI", 14)
        )
        confirm_password_entry.pack(pady=5)
        
        signup_btn = ctk.CTkButton(
            self.signup_modal, text="Sign Up", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 16, "bold"),
            width=350, height=45,
            command=lambda: self.do_signup(email_entry.get(), fullname_entry.get(), password_entry.get(), confirm_password_entry.get())
        )
        signup_btn.pack(pady=20)
        
        or_label = ctk.CTkLabel(self.signup_modal, text="— Or sign up with —", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 12))
        or_label.pack(pady=10)
        
        social_frame = ctk.CTkFrame(self.signup_modal, fg_color="transparent")
        social_frame.pack(pady=10)
        
        for social in ["Facebook", "Apple", "Gmail"]:
            social_btn = ctk.CTkButton(
                social_frame, text=social, fg_color="#603C1E",
                hover_color="#D7A765", width=100, height=35,
                font=("Microsoft JhengHei UI", 12)
            )
            social_btn.pack(side="left", padx=10)
        
        signin_label = ctk.CTkLabel(self.signup_modal, text="Already have an account?", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 12))
        signin_label.pack(pady=(20, 5))
        
        signin_link = ctk.CTkButton(
            self.signup_modal, text="Sign In Here",
            fg_color="transparent", hover_color="#603C1E",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 12, "bold"),
            command=self.show_signin_modal
        )
        signin_link.pack()
    
    def do_signin(self, fullname, password):
        if not fullname or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        self.current_user = fullname
        if hasattr(self, 'signin_modal') and self.signin_modal:
            self.signin_modal.destroy()
        messagebox.showinfo("Success", f"Welcome back, {fullname}!")
        self.show_dashboard()
    
    def do_signup(self, email, fullname, password, confirm_password):
        if not all([email, fullname, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        self.users_data.append({
            "email": email,
            "fullname": fullname,
            "password": password
        })
        self.save_data()
        
        self.current_user = fullname
        if hasattr(self, 'signup_modal') and self.signup_modal:
            self.signup_modal.destroy()
        messagebox.showinfo("Success", f"Account created! Welcome, {fullname}!")
        self.show_dashboard()
    
    def show_dashboard(self):
        self.clear_main_container()
        
        self.create_header(self.main_container, show_user=True)
        
        content_frame = ctk.CTkFrame(self.main_container, fg_color="#17120E")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            content_frame, text=f"Welcome to Your Dashboard",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 32, "bold")
        )
        title.pack(pady=(20, 30))
        
        sections_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        sections_frame.pack(fill="both", expand=True)
        
        favorites_frame = ctk.CTkFrame(sections_frame, fg_color="#1B1612", corner_radius=15)
        favorites_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        fav_title = ctk.CTkLabel(favorites_frame, text="⭐ Favorites", text_color="#D7A765", font=("Microsoft JhengHei UI", 20, "bold"))
        fav_title.pack(pady=20)
        
        if self.favorites:
            for fav in self.favorites[:5]:
                fav_label = ctk.CTkLabel(favorites_frame, text=f"• {fav}", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
                fav_label.pack(pady=5)
        else:
            no_fav = ctk.CTkLabel(favorites_frame, text="No favorites yet", text_color="#838383", font=("Microsoft JhengHei UI", 14))
            no_fav.pack(pady=20)
        
        bookings_frame = ctk.CTkFrame(sections_frame, fg_color="#1B1612", corner_radius=15)
        bookings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        book_title = ctk.CTkLabel(bookings_frame, text="📅 Upcoming Bookings", text_color="#D7A765", font=("Microsoft JhengHei UI", 20, "bold"))
        book_title.pack(pady=20)
        
        if self.bookings:
            for booking in self.bookings[:5]:
                book_label = ctk.CTkLabel(bookings_frame, text=f"• {booking.get('service_type')} - {booking.get('date')}", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
                book_label.pack(pady=5)
        else:
            no_book = ctk.CTkLabel(bookings_frame, text="No bookings yet", text_color="#838383", font=("Microsoft JhengHei UI", 14))
            no_book.pack(pady=20)
        
        cart_frame = ctk.CTkFrame(sections_frame, fg_color="#1B1612", corner_radius=15)
        cart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        cart_title = ctk.CTkLabel(cart_frame, text="🛒 Shopping Cart", text_color="#D7A765", font=("Microsoft JhengHei UI", 20, "bold"))
        cart_title.pack(pady=20)
        
        if self.cart:
            for item in self.cart[:5]:
                cart_label = ctk.CTkLabel(cart_frame, text=f"• {item}", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
                cart_label.pack(pady=5)
        else:
            no_cart = ctk.CTkLabel(cart_frame, text="Cart is empty", text_color="#838383", font=("Microsoft JhengHei UI", 14))
            no_cart.pack(pady=20)
        
        hotpicks_frame = ctk.CTkFrame(sections_frame, fg_color="#1B1612", corner_radius=15)
        hotpicks_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        hot_title = ctk.CTkLabel(hotpicks_frame, text="🔥 Hot Picks", text_color="#D7A765", font=("Microsoft JhengHei UI", 20, "bold"))
        hot_title.pack(pady=20)
        
        hot_products = sorted(self.products_data, key=lambda x: x.get('rating', 0), reverse=True)[:3]
        for product in hot_products:
            hot_label = ctk.CTkLabel(hotpicks_frame, text=f"• {product['name']} (₱{product['price']:.2f})", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
            hot_label.pack(pady=5)
        
        sections_frame.grid_columnconfigure(0, weight=1)
        sections_frame.grid_columnconfigure(1, weight=1)
        sections_frame.grid_rowconfigure(0, weight=1)
        sections_frame.grid_rowconfigure(1, weight=1)
    
    def show_adoption_page(self):
        self.clear_main_container()
        
        canvas = ctk.CTkCanvas(self.main_container, bg="#17120E", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#17120E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.create_header(scrollable_frame, show_user=self.current_user is not None)
        
        title_label = ctk.CTkLabel(
            scrollable_frame, text="FIND YOUR NEW FRIEND",
            text_color="#FFFFFF", font=("Arial", 64, "bold")
        )
        title_label.pack(pady=(40, 30), padx=66, anchor="w")
        
        categories_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        categories_frame.pack(pady=20)
        
        categories = ["All", "Dogs", "Cats", "Birds", "Fish", "Others"]
        self.selected_category = tk.StringVar(value="All")
        
        for category in categories:
            cat_btn = ctk.CTkRadioButton(
                categories_frame, text=category, variable=self.selected_category,
                value=category, fg_color="#D7A765", hover_color="#FFB774",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16),
                command=self.filter_pets
            )
            cat_btn.pack(side="left", padx=15)
        
        self.pets_display_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.pets_display_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.filter_pets()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def filter_pets(self):
        for widget in self.pets_display_frame.winfo_children():
            widget.destroy()
        
        category = self.selected_category.get()
        
        if category == "All":
            filtered_pets = self.pets_data
        else:
            filtered_pets = [pet for pet in self.pets_data if pet['category'] == category]
        
        row = 0
        col = 0
        for pet in filtered_pets:
            pet_card = ctk.CTkFrame(self.pets_display_frame, fg_color="#261E18", width=320, height=400, corner_radius=15)
            pet_card.grid(row=row, column=col, padx=15, pady=15)
            pet_card.pack_propagate(False)
            
            pet_img = self.load_pet_image(pet['id'], size=(180, 180))
            if pet_img:
                pet_img_label = ctk.CTkLabel(pet_card, image=pet_img, text="")
                pet_img_label.pack(pady=(20, 10))
            else:
                pet_img_label = ctk.CTkLabel(
                    pet_card, text=f"🐾", text_color="#D7A765",
                    font=("Microsoft JhengHei UI", 36)
                )
                pet_img_label.pack(pady=(30, 10))
            
            pet_name = ctk.CTkLabel(
                pet_card, text=pet['name'],
                text_color="#D7A765", font=("Microsoft JhengHei UI", 22, "bold")
            )
            pet_name.pack(pady=5)
            
            pet_info = ctk.CTkLabel(
                pet_card,
                text=f"Breed: {pet['breed']}\nAge: {pet['age']}\nGender: {pet['gender']}",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 13),
                justify="left"
            )
            pet_info.pack(pady=10)
            
            adopt_btn = ctk.CTkButton(
                pet_card, text="View Details", fg_color="#D7A765",
                hover_color="#FFB774", text_color="#1C130B",
                font=("Microsoft JhengHei UI", 14, "bold"),
                command=lambda p=pet: self.show_pet_details_modal(p)
            )
            adopt_btn.pack(pady=15)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def show_pet_details_modal(self, pet):
        if not self.check_login("adopt a pet"):
            return
        
        modal = ctk.CTkToplevel(self)
        modal.title(f"{pet['name']} - Details")
        modal.geometry("600x700")
        modal.configure(fg_color="#17120E")
        modal.transient(self)
        modal.grab_set()
        
        pet_img = self.load_pet_image(pet['id'], size=(250, 250))
        if pet_img:
            img_label = ctk.CTkLabel(modal, image=pet_img, text="")
            img_label.pack(pady=(20, 10))
        
        title = ctk.CTkLabel(
            modal, text=f"🐾 {pet['name']}",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 32, "bold")
        )
        title.pack(pady=(30, 20))
        
        details_frame = ctk.CTkFrame(modal, fg_color="#1B1612", corner_radius=15)
        details_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        details = [
            ("Name:", pet['name']),
            ("Breed:", pet['breed']),
            ("Age:", pet['age']),
            ("Gender:", pet['gender']),
            ("Markings:", pet['markings']),
            ("Neutered/Spayed:", pet['neutered']),
            ("Dewormed:", pet['dewormed']),
            ("Medical Notes:", pet['medical_notes'])
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            detail_frame.pack(fill="x", pady=8, padx=20)
            
            label_widget = ctk.CTkLabel(
                detail_frame, text=label, text_color="#D7A765",
                font=("Microsoft JhengHei UI", 14, "bold"), width=150, anchor="w"
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                detail_frame, text=value, text_color="#FFFFFF",
                font=("Microsoft JhengHei UI", 14), anchor="w"
            )
            value_widget.pack(side="left", fill="x", expand=True)
        
        adopt_btn = ctk.CTkButton(
            modal, text="Adopt This Pet", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 18, "bold"),
            width=300, height=50,
            command=lambda: self.show_applicant_modal(pet, modal)
        )
        adopt_btn.pack(pady=20)
    
    def show_applicant_modal(self, pet, previous_modal):
        previous_modal.destroy()
        
        modal = ctk.CTkToplevel(self)
        modal.title("Adoption Application")
        modal.geometry("1098x800")
        modal.configure(fg_color="#17120E")
        modal.transient(self)
        modal.grab_set()
        
        canvas = ctk.CTkCanvas(modal, bg="#17120E", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(modal, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#17120E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        title = ctk.CTkLabel(
            scrollable_frame,
            text="Thank you for choosing to adopt!\nPlease fill out this form so we can ensure\nthe best match between you and your future pet.",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 18, "bold"),
            justify="center"
        )
        title.pack(pady=(30, 20))
        
        form_frame = ctk.CTkFrame(scrollable_frame, fg_color="#1B1612", corner_radius=15)
        form_frame.pack(fill="both", padx=40, pady=20)
        
        section_title = ctk.CTkLabel(
            form_frame, text="Applicant Information",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 22, "bold")
        )
        section_title.pack(pady=(20, 15))
        
        fields = {}
        
        for field in ["Full Name", "Complete Address", "Age", "Contact Number", "Email Address"]:
            field_label = ctk.CTkLabel(form_frame, text=f"{field}:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
            field_label.pack(pady=(10, 5), padx=40, anchor="w")
            
            field_entry = ctk.CTkEntry(form_frame, width=900, height=40, font=("Microsoft JhengHei UI", 14))
            field_entry.pack(pady=5, padx=40)
            fields[field] = field_entry
        
        care_label = ctk.CTkLabel(
            form_frame, text="Care Commitment - Who will take care of the pet?",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 16, "bold")
        )
        care_label.pack(pady=(20, 10), padx=40, anchor="w")
        
        care_entry = ctk.CTkEntry(form_frame, width=900, height=40, font=("Microsoft JhengHei UI", 14))
        care_entry.pack(pady=5, padx=40)
        fields["Caretaker"] = care_entry
        
        provide_label = ctk.CTkLabel(
            form_frame, text="Can you provide food, vet care, and a safe home?",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14)
        )
        provide_label.pack(pady=(15, 10), padx=40, anchor="w")
        
        provide_var = tk.StringVar(value="Yes")
        yes_radio = ctk.CTkRadioButton(form_frame, text="Yes", variable=provide_var, value="Yes", fg_color="#D7A765", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        yes_radio.pack(pady=5, padx=40, anchor="w")
        no_radio = ctk.CTkRadioButton(form_frame, text="No", variable=provide_var, value="No", fg_color="#D7A765", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        no_radio.pack(pady=5, padx=40, anchor="w")
        
        agreement_label = ctk.CTkLabel(
            form_frame, text="Agreement",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 16, "bold")
        )
        agreement_label.pack(pady=(20, 10), padx=40, anchor="w")
        
        agree1_var = tk.BooleanVar()
        agree1 = ctk.CTkCheckBox(
            form_frame, text="I understand that adopting a pet is a lifelong responsibility.",
            variable=agree1_var, fg_color="#D7A765", text_color="#FFFFFF",
            font=("Microsoft JhengHei UI", 13)
        )
        agree1.pack(pady=5, padx=40, anchor="w")
        
        agree2_var = tk.BooleanVar()
        agree2 = ctk.CTkCheckBox(
            form_frame, text="I promise to give love and proper care to my adopted pet.",
            variable=agree2_var, fg_color="#D7A765", text_color="#FFFFFF",
            font=("Microsoft JhengHei UI", 13)
        )
        agree2.pack(pady=5, padx=40, anchor="w")
        
        submit_btn = ctk.CTkButton(
            scrollable_frame, text="Submit Application", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 18, "bold"),
            width=300, height=50,
            command=lambda: self.submit_application(pet, fields, provide_var, agree1_var, agree2_var, modal)
        )
        submit_btn.pack(pady=30)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def submit_application(self, pet, fields, provide_var, agree1_var, agree2_var, modal):
        for field_name, field_entry in fields.items():
            if not field_entry.get():
                messagebox.showerror("Error", f"Please fill in {field_name}")
                return
        
        if not agree1_var.get() or not agree2_var.get():
            messagebox.showerror("Error", "Please agree to both commitments")
            return
        
        application = {
            "pet_id": pet['id'],
            "pet_name": pet['name'],
            "applicant": {field: entry.get() for field, entry in fields.items()},
            "can_provide": provide_var.get(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending"
        }
        
        self.applications_data.append(application)
        self.save_data()
        
        modal.destroy()
        messagebox.showinfo("Success", f"Application submitted for {pet['name']}!\n\nYour application is now pending review. We will contact you soon!")
    
    def show_service_page(self):
        if not self.check_login("book a service"):
            return
        
        self.clear_main_container()
        
        canvas = ctk.CTkCanvas(self.main_container, bg="#17120E", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#17120E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.create_header(scrollable_frame, show_user=self.current_user is not None)
        
        title = ctk.CTkLabel(
            scrollable_frame, text="Pet Care Services",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 42, "bold")
        )
        title.pack(pady=(40, 30))
        
        services_label = ctk.CTkLabel(
            scrollable_frame, text="Choose from our premium services:",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 18)
        )
        services_label.pack(pady=10)
        
        services_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        services_frame.pack(pady=30)
        
        services = [
            ("Grooming", "🧼"),
            ("Health Care", "⚕️"),
            ("Daycare", "🏠"),
            ("Training", "🎓"),
            ("Hygienic Care", "✨")
        ]
        
        for service, emoji in services:
            service_btn = ctk.CTkButton(
                services_frame, text=f"{emoji} {service}",
                fg_color="#603C1E", hover_color="#D7A765",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16, "bold"),
                width=250, height=60, corner_radius=30
            )
            service_btn.pack(side="left", padx=15)
        
        booking_frame = ctk.CTkFrame(scrollable_frame, fg_color="#1B1612", corner_radius=15)
        booking_frame.pack(fill="both", padx=60, pady=30)
        
        booking_title = ctk.CTkLabel(
            booking_frame, text="Service Booking Form",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 28, "bold")
        )
        booking_title.pack(pady=(30, 20))
        
        form_fields = {}
        
        pet_name_label = ctk.CTkLabel(booking_frame, text="Pet's Name:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        pet_name_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        pet_name_entry = ctk.CTkEntry(booking_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14))
        pet_name_entry.pack(pady=5, padx=40)
        form_fields["pet_name"] = pet_name_entry
        
        service_label = ctk.CTkLabel(booking_frame, text="Service Type:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        service_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        service_var = tk.StringVar(value="Grooming")
        service_menu = ctk.CTkOptionMenu(
            booking_frame, values=["Grooming", "Health Care", "Daycare", "Training", "Hygienic Care"],
            variable=service_var, fg_color="#603C1E", button_color="#D7A765",
            width=600, height=40, font=("Microsoft JhengHei UI", 14)
        )
        service_menu.pack(pady=5, padx=40)
        form_fields["service_type"] = service_var
        
        date_label = ctk.CTkLabel(booking_frame, text="Date:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        date_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        date_entry = ctk.CTkEntry(booking_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14), placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=5, padx=40)
        form_fields["date"] = date_entry
        
        time_label = ctk.CTkLabel(booking_frame, text="Time:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        time_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        time_entry = ctk.CTkEntry(booking_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14), placeholder_text="HH:MM")
        time_entry.pack(pady=5, padx=40)
        form_fields["time"] = time_entry
        
        staff_label = ctk.CTkLabel(booking_frame, text="Preferred Staff:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        staff_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        staff_var = tk.StringVar(value="Any Available")
        staff_menu = ctk.CTkOptionMenu(
            booking_frame, values=["Any Available", "Dr. Sarah Johnson", "Dr. Mike Chen", "Emily Rodriguez", "James Wilson"],
            variable=staff_var, fg_color="#603C1E", button_color="#D7A765",
            width=600, height=40, font=("Microsoft JhengHei UI", 14)
        )
        staff_menu.pack(pady=5, padx=40)
        form_fields["staff"] = staff_var
        
        instructions_label = ctk.CTkLabel(booking_frame, text="Special Instructions:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        instructions_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        instructions_text = ctk.CTkTextbox(booking_frame, width=600, height=100, font=("Microsoft JhengHei UI", 14))
        instructions_text.pack(pady=5, padx=40)
        form_fields["instructions"] = instructions_text
        
        submit_btn = ctk.CTkButton(
            booking_frame, text="Book Service", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 18, "bold"),
            width=300, height=50,
            command=lambda: self.submit_booking(form_fields)
        )
        submit_btn.pack(pady=30)
        
        calendar_label = ctk.CTkLabel(
            scrollable_frame, text="Your Bookings Calendar",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 28, "bold")
        )
        calendar_label.pack(pady=(20, 10))
        
        if self.bookings:
            bookings_display = ctk.CTkFrame(scrollable_frame, fg_color="#1B1612", corner_radius=15)
            bookings_display.pack(fill="both", padx=60, pady=20)
            
            for booking in self.bookings:
                booking_item = ctk.CTkLabel(
                    bookings_display,
                    text=f"📅 {booking['date']} at {booking['time']} - {booking['service_type']} for {booking['pet_name']}",
                    text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14)
                )
                booking_item.pack(pady=10, padx=20, anchor="w")
        else:
            no_bookings = ctk.CTkLabel(
                scrollable_frame, text="No bookings yet",
                text_color="#838383", font=("Microsoft JhengHei UI", 16)
            )
            no_bookings.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def submit_booking(self, form_fields):
        pet_name = form_fields["pet_name"].get()
        service_type = form_fields["service_type"].get()
        date = form_fields["date"].get()
        time = form_fields["time"].get()
        staff = form_fields["staff"].get()
        instructions = form_fields["instructions"].get("1.0", "end-1c")
        
        if not pet_name or not date or not time:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        booking = {
            "pet_name": pet_name,
            "service_type": service_type,
            "date": date,
            "time": time,
            "staff": staff,
            "instructions": instructions,
            "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.bookings.append(booking)
        self.bookings_data.append(booking)
        self.save_data()
        
        messagebox.showinfo("Success", f"Service booked!\n\n{service_type} for {pet_name}\n{date} at {time}")
        self.show_service_page()
    
    def show_products_page(self):
        if not self.check_login("buy products"):
            return
        
        self.clear_main_container()
        
        canvas = ctk.CTkCanvas(self.main_container, bg="#17120E", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#17120E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.create_header(scrollable_frame, show_user=self.current_user is not None)
        
        title = ctk.CTkLabel(
            scrollable_frame, text="Premium Pet Products",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 42, "bold")
        )
        title.pack(pady=(40, 20))
        
        subtitle = ctk.CTkLabel(
            scrollable_frame,
            text="Curated selection of high-quality products for your beloved pets",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16)
        )
        subtitle.pack(pady=10)
        
        categories_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        categories_frame.pack(pady=20)
        
        categories = ["All", "Food", "Medications", "Toys", "Essentials"]
        self.selected_product_category = tk.StringVar(value="All")
        
        for category in categories:
            cat_btn = ctk.CTkRadioButton(
                categories_frame, text=category, variable=self.selected_product_category,
                value=category, fg_color="#D7A765", hover_color="#FFB774",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16),
                command=self.filter_products
            )
            cat_btn.pack(side="left", padx=15)
        
        self.products_display_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.products_display_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.filter_products()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def filter_products(self):
        for widget in self.products_display_frame.winfo_children():
            widget.destroy()
        
        category = self.selected_product_category.get()
        
        if category == "All":
            filtered_products = self.products_data
        else:
            filtered_products = [p for p in self.products_data if p['category'] == category]
        
        row = 0
        col = 0
        for product in filtered_products:
            product_card = ctk.CTkFrame(self.products_display_frame, fg_color="#1B1612", width=320, height=420, corner_radius=15)
            product_card.grid(row=row, column=col, padx=15, pady=15)
            product_card.pack_propagate(False)
            
            prod_img = self.load_product_image(product['category'], size=(150, 150))
            if prod_img:
                img_label = ctk.CTkLabel(product_card, image=prod_img, text="")
                img_label.pack(pady=(20, 10))
            
            product_name = ctk.CTkLabel(
                product_card, text=product['name'][:30] + "..." if len(product['name']) > 30 else product['name'],
                text_color="#D7A765", font=("Microsoft JhengHei UI", 16, "bold"),
                wraplength=280
            )
            product_name.pack(pady=(20, 10))
            
            product_price = ctk.CTkLabel(
                product_card, text=f"₱{product['price']:.2f}",
                text_color="#FFB774", font=("Microsoft JhengHei UI", 20, "bold")
            )
            product_price.pack(pady=5)
            
            product_desc = ctk.CTkLabel(
                product_card, text=product['description'][:80] + "..." if len(product['description']) > 80 else product['description'],
                text_color="#DEDEDE", font=("Microsoft JhengHei UI", 11),
                wraplength=280
            )
            product_desc.pack(pady=10)
            
            rating = ctk.CTkLabel(
                product_card, text=f"⭐ {product.get('rating', 4.5)}",
                text_color="#FFFFFF", font=("Microsoft JhengHei UI", 12)
            )
            rating.pack(pady=5)
            
            buttons_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            buttons_frame.pack(pady=10)
            
            cart_btn = ctk.CTkButton(
                buttons_frame, text="Add to Cart", fg_color="#D7A765",
                hover_color="#FFB774", text_color="#1C130B",
                font=("Microsoft JhengHei UI", 12, "bold"),
                width=120, height=35,
                command=lambda p=product: self.add_to_cart(p)
            )
            cart_btn.pack(side="left", padx=5)
            
            fav_btn = ctk.CTkButton(
                buttons_frame, text="♥", fg_color="#603C1E",
                hover_color="#D7A765", text_color="#FFFFFF",
                font=("Microsoft JhengHei UI", 16), width=40, height=35,
                command=lambda p=product: self.add_to_favorites(p)
            )
            fav_btn.pack(side="left", padx=5)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def add_to_cart(self, product):
        self.cart.append(product['name'])
        messagebox.showinfo("Added to Cart", f"{product['name']} has been added to your cart!")
    
    def add_to_favorites(self, product):
        if product['name'] not in self.favorites:
            self.favorites.append(product['name'])
            messagebox.showinfo("Added to Favorites", f"{product['name']} has been added to your favorites!")
        else:
            messagebox.showinfo("Already in Favorites", f"{product['name']} is already in your favorites!")
    
    def show_contact_page(self):
        self.clear_main_container()
        
        self.create_header(self.main_container, show_user=self.current_user is not None)
        
        content_frame = ctk.CTkFrame(self.main_container, fg_color="#17120E")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = ctk.CTkLabel(
            content_frame, text="Get In Touch With Us",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 42, "bold")
        )
        title.pack(pady=(20, 30))
        
        contact_info_frame = ctk.CTkFrame(content_frame, fg_color="#1B1612", corner_radius=15)
        contact_info_frame.pack(fill="x", pady=20)
        
        info_title = ctk.CTkLabel(
            contact_info_frame, text="Contact Information",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 24, "bold")
        )
        info_title.pack(pady=(20, 15))
        
        info_text = ctk.CTkLabel(
            contact_info_frame,
            text="📍 Address: 123 Pet Street, Manila, Philippines\n"
                 "📞 Phone: +63 (917) 123-4567\n"
                 "📧 Email: info@onlypets.com\n"
                 "🕒 Hours: Mon-Fri 9:00 AM - 6:00 PM, Sat-Sun 10:00 AM - 4:00 PM",
            text_color="#FFFFFF", font=("Microsoft JhengHei UI", 16),
            justify="left"
        )
        info_text.pack(pady=20, padx=40)
        
        message_frame = ctk.CTkFrame(content_frame, fg_color="#1B1612", corner_radius=15)
        message_frame.pack(fill="both", expand=True, pady=20)
        
        message_title = ctk.CTkLabel(
            message_frame, text="Send Us a Message",
            text_color="#D7A765", font=("Microsoft JhengHei UI", 24, "bold")
        )
        message_title.pack(pady=(20, 15))
        
        name_label = ctk.CTkLabel(message_frame, text="Your Name:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        name_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        name_entry = ctk.CTkEntry(message_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14))
        name_entry.pack(pady=5, padx=40)
        
        email_label = ctk.CTkLabel(message_frame, text="Your Email:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        email_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        email_entry = ctk.CTkEntry(message_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14))
        email_entry.pack(pady=5, padx=40)
        
        subject_label = ctk.CTkLabel(message_frame, text="Subject:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        subject_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        subject_entry = ctk.CTkEntry(message_frame, width=600, height=40, font=("Microsoft JhengHei UI", 14))
        subject_entry.pack(pady=5, padx=40)
        
        message_label = ctk.CTkLabel(message_frame, text="Message:", text_color="#FFFFFF", font=("Microsoft JhengHei UI", 14))
        message_label.pack(pady=(10, 5), padx=40, anchor="w")
        
        message_text = ctk.CTkTextbox(message_frame, width=600, height=150, font=("Microsoft JhengHei UI", 14))
        message_text.pack(pady=5, padx=40)
        
        send_btn = ctk.CTkButton(
            message_frame, text="Send Message", fg_color="#D7A765",
            hover_color="#FFB774", text_color="#1C130B",
            font=("Microsoft JhengHei UI", 18, "bold"),
            width=250, height=50,
            command=lambda: self.send_message(name_entry, email_entry, subject_entry, message_text)
        )
        send_btn.pack(pady=30)
    
    def send_message(self, name_entry, email_entry, subject_entry, message_text):
        name = name_entry.get()
        email = email_entry.get()
        subject = subject_entry.get()
        message = message_text.get("1.0", "end-1c")
        
        if not all([name, email, subject, message]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        messagebox.showinfo("Message Sent", f"Thank you, {name}!\n\nYour message has been sent successfully. We will get back to you soon!")
        
        name_entry.delete(0, "end")
        email_entry.delete(0, "end")
        subject_entry.delete(0, "end")
        message_text.delete("1.0", "end")

if __name__ == "__main__":
    app = PetAdoptionSystem()
    app.mainloop()
