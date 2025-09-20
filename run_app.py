#!/usr/bin/env python3
"""
Run the Pet Booking Application
"""

if __name__ == "__main__":
    try:
        from main_app import main
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all required files are in the scripts directory")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
