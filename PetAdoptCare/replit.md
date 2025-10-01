# OnlyPets - Pet Adoption & Service Management System

## Overview

OnlyPets is a comprehensive Pet Adoption & Service Management System built with Python and CustomTkinter. The application provides a complete platform for pet adoption, service booking, product purchasing, and donation management. It features a modern GUI with a warm color palette (browns, creams, and oranges) designed to create a welcoming experience for users looking to adopt pets or access pet care services.

The system manages multiple user workflows including browsing available pets, applying for adoption, booking services (grooming, healthcare, daycare, training, hygiene), purchasing pet products, and making donations to support animal care.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Updates (October 1, 2025)

1. **Currency Conversion**: All product prices converted from USD to PHP (Philippine Peso) using exchange rate of 56
2. **Authentication Requirements**: Added login requirement - users must sign in before:
   - Adopting pets
   - Purchasing products  
   - Booking services
3. **Branding Enhancement**: Added "🐾 OnlyPets" company logo/name centered in header navigation (x=650)
4. **Real Images Integration**: Downloaded and integrated 15 real stock images for pets and 4 category images for products using PIL
5. **Code Quality**: Fixed all LSP issues - moved instance attributes to __init__, removed unused imports, fixed image references
6. **Contact Information**: Updated phone number format to Philippine format (+63)

## System Architecture

### Frontend Architecture

**GUI Framework: CustomTkinter**
- The application uses CustomTkinter (ctk) as the primary GUI framework, providing modern, customizable widgets with a consistent look and feel
- Light appearance mode with blue color theme as defaults
- Custom color palette implementation using hex colors (#17120E primary background, #FFFFFF, #FEEBD9, #603C1E, etc.)
- Main window dimensions: 1440x900 pixels for optimal desktop viewing

**Layout Structure:**
- Container-based architecture with a main container managing different page views
- Modal popup system for authentication (sign in/sign up) and forms (adoption applications, service bookings)
- Multi-page navigation: Landing Page, Adoption Page, Services Page, Products Page, Dashboard, Contact
- Responsive frame dimensions designed for specific content areas (e.g., 1440x3141 for landing page, 1440x1777 for adoption frame)

**Key UI Components:**
- Header navigation bar with consistent positioning (Home X98 Y38, Adoption X272 Y38, etc.)
- Image carousel/slider for pet browsing with arrow navigation
- Card-based displays for pets and products with images, descriptions, and action buttons
- Calendar widget integration using tkcalendar for booking services
- Shopping cart and favorites system with persistent state management

**Typography:**
- Primary font: Microsoft JhengHei UI
- Secondary font: Poppins for headers and navigation

### Backend Architecture

**Data Management:**
- JSON-based file storage (data.json) for persistent data
- In-memory data structures during runtime for performance
- Lazy loading pattern: Data initialized on application startup from file or defaults

**Core Data Models:**
1. **Pets Data**: id, name, category (Dogs/Cats), breed, age, gender, markings, neutered status, dewormed status, medical notes
2. **Products Data**: Categorized into food, medications, toys, and other essentials
3. **Users Data**: Authentication and profile information
4. **Applications Data**: Pet adoption applications with applicant information
5. **Bookings Data**: Service bookings for grooming, healthcare, daycare, training, hygiene care

**State Management:**
- User session tracking (current_user)
- Shopping cart state (cart array)
- Favorites tracking (favorites array)
- Booking history (bookings array)
- Data synchronized between memory and disk via save_data() method

**Authentication System:**
- Multi-provider login support planned (Facebook, Apple, Gmail integration)
- Traditional email/password authentication
- Password recovery functionality ("Forgot Password" flow)
- Session persistence across application lifecycle

**Business Logic Flows:**

1. **Adoption Workflow:**
   - Browse pets → View pet details (modal) → Click "Adopt" → Fill adoption application form (1098x1348 modal) → Submit → Approval queue
   - Application form includes: Applicant info, care commitment questionnaire, agreement acknowledgment

2. **Service Booking Workflow:**
   - Select service type (5 horizontal button options) → Fill service booking form with calendar integration → Confirm booking → Booking confirmation

3. **Product Purchase Workflow:**
   - Browse products by category → Add to cart → Checkout process → Order confirmation

4. **Donation Workflow:**
   - View donation section (1440x480 frame) → Bank account details displayed (OnlyPets Animal Care Foundation - 1234) → Process donation

### Design Patterns

**Singleton Pattern**: Main application class (PetAdoptionSystem) manages global state

**Observer Pattern**: Implicit in cart, favorites, and bookings tracking where UI updates based on state changes

**Factory Pattern**: Default data initialization when data.json doesn't exist

**Modal Pattern**: Popup overlays for forms and authentication to maintain context while collecting user input

## External Dependencies

### Python Libraries

1. **customtkinter** - Modern UI framework for creating the GUI with enhanced styling capabilities
2. **tkinter** - Base GUI framework (comes with Python)
3. **tkcalendar** - Calendar widget for service booking date selection
4. **PIL (Pillow)** - Image processing for pet and product photos (ImageTk integration)
5. **json** - Data serialization and deserialization for persistent storage
6. **os** - File system operations for checking data.json existence
7. **datetime** - Date/time handling for bookings and timestamps

### Planned Third-Party Integrations

1. **Social Authentication Providers:**
   - Facebook Login API
   - Apple Sign-In
   - Google OAuth (Gmail login)

2. **Payment Processing** (Implied by donation and product features):
   - Bank transfer integration for donations
   - Payment gateway for product purchases

### Data Storage

**File-based JSON Storage:**
- Single data.json file storing all application data
- No external database currently implemented
- Structure supports future migration to relational or NoSQL database

### Asset Management

- Image assets for pets and products stored locally
- Image loading via PIL/Pillow with tkinter PhotoImage conversion
- Asset organization follows attached_assets directory pattern