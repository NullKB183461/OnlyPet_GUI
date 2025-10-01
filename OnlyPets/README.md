# OnlyPets - Pet Adoption & Service Management System

A comprehensive Python tkinter-based application for pet adoption and care services, featuring a sleek black-and-gold design theme.

## Features

### 🏠 Landing Page
- Modern black-and-gold color scheme
- Intuitive navigation with Home, Adoption, Service, Products, Contact, and Sign Up/Sign In
- Hero section with mission statement
- About section highlighting shelter values
- Service showcase with horizontal buttons
- Product categories display
- Donation support section

### 🔐 User Authentication
- Sign Up/Sign In modal with dual tabs
- Support for Apple, Facebook, Google, and email/password registration
- Secure password hashing
- User session management

### 🐾 Pet Adoption System
- Browse pets by category (Dogs, Cats, Birds, Fish, Other)
- Detailed pet information including:
  - Species, breed, age, gender
  - Markings and medical status
  - Vaccine, neutering/spaying, and deworming status
- Comprehensive adoption application form
- Care commitment questions
- Application tracking and management

### 🛠️ Service Management
- Five service types: Grooming, Health Care, Daycare, Training, Hygienic Care
- Service booking form with:
  - Pet name and service selection
  - Date and time scheduling
  - Staff member preferences
  - Special instructions
- Calendar view for appointment management

### 🛒 Products Catalog
- Categorized products: Food, Medications, Toys, Other essentials
- Product details with pricing and stock information
- Purchase interest tracking
- Category filtering system

### 📊 Analytics Dashboard
- Comprehensive analytics powered by Pandas
- Adoption statistics and trends
- Service usage analytics
- Revenue tracking
- Donation statistics
- Interactive charts and visualizations

### 💰 Donation System
- Secure donation processing
- Donor information collection
- Message support for donors
- Donation tracking and reporting

### 📞 Contact & Support
- Contact information display
- Business hours and location
- Support request handling

## Technical Features

### Database
- SQLite database with comprehensive schema
- User management with secure authentication
- Pet information and adoption tracking
- Service bookings and scheduling
- Product catalog management
- Donation tracking
- Analytics data collection

### Analytics
- Pandas-powered data analysis
- Matplotlib chart generation
- Real-time statistics
- Trend analysis
- Revenue tracking
- Adoption metrics

### User Interface
- Pure Python tkinter implementation
- Responsive design with scrollable content
- Modal windows for forms
- Tabbed interfaces for organization
- Consistent black-and-gold theming
- Professional typography and spacing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd OnlyPets
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **First Time Setup**: The application will automatically create the database and populate it with sample data.

2. **User Registration**: Click "Sign Up / Sign In" to create an account or log in.

3. **Browse Pets**: Navigate to the Adoption section to view available pets by category.

4. **Adopt a Pet**: Click "View Details" on any pet, then "Adopt This Pet" to fill out the adoption application.

5. **Book Services**: Go to the Service section to book grooming, health care, daycare, training, or hygienic care services.

6. **Shop Products**: Browse the Products section to view available pet supplies and essentials.

7. **View Analytics**: Logged-in users can access the Dashboard to view comprehensive analytics and statistics.

8. **Make Donations**: Visit the Contact section to make donations to support the shelter.

## Database Schema

The application uses SQLite with the following main tables:
- `users`: User accounts and authentication
- `pets`: Pet information and availability
- `adoption_applications`: Adoption request tracking
- `services`: Available service types
- `service_bookings`: Service appointment scheduling
- `products`: Product catalog
- `donations`: Donation tracking

## File Structure

```
OnlyPets/
├── main.py                 # Main application file
├── analytics.py           # Analytics and reporting module
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
└── onlypets.db           # SQLite database (created automatically)
```

## Features in Detail

### Authentication System
- Secure user registration and login
- Password hashing for security
- Session management
- User profile information

### Pet Adoption Workflow
1. Browse available pets by category
2. View detailed pet information
3. Fill out comprehensive adoption application
4. Submit application for review
5. Track application status

### Service Booking Process
1. Select service type
2. Choose date and time
3. Specify pet information
4. Add special instructions
5. Book appointment

### Analytics Dashboard
- Real-time adoption statistics
- Service usage trends
- Revenue analytics
- Donation tracking
- Interactive charts and graphs

## Customization

The application uses a consistent color scheme defined in the `colors` dictionary:
- Background: `#1a1a1a` (Dark)
- Gold: `#FFD700` (Primary accent)
- Light Gold: `#FFF8DC` (Secondary accent)
- White: `#FFFFFF` (Text)
- Dark Gray: `#333333` (Secondary background)

## Contributing

This is a pure Python tkinter application designed for educational and demonstration purposes. The codebase is structured for easy understanding and modification.

## License

This project is created for educational purposes and demonstrates a comprehensive pet adoption and service management system using Python tkinter.
