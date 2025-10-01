"""
Analytics module for OnlyPets
Provides data analysis and visualization using Pandas
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import Dict, List, Tuple

class AnalyticsManager:
    """Manages analytics and reporting for OnlyPets"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_adoption_statistics(self) -> Dict:
        """Get adoption statistics"""
        conn = self.get_connection()
        
        # Total pets available
        total_pets = pd.read_sql_query("SELECT COUNT(*) as count FROM pets WHERE available = 1", conn)
        
        # Adoption applications by status
        adoption_stats = pd.read_sql_query("""
            SELECT status, COUNT(*) as count 
            FROM adoption_applications 
            GROUP BY status
        """, conn)
        
        # Pets by species
        species_stats = pd.read_sql_query("""
            SELECT species, COUNT(*) as count 
            FROM pets 
            WHERE available = 1 
            GROUP BY species
        """, conn)
        
        # Recent applications (last 30 days)
        recent_applications = pd.read_sql_query("""
            SELECT COUNT(*) as count 
            FROM adoption_applications 
            WHERE created_at >= date('now', '-30 days')
        """, conn)
        
        conn.close()
        
        return {
            'total_pets': total_pets['count'].iloc[0] if not total_pets.empty else 0,
            'adoption_stats': adoption_stats.to_dict('records'),
            'species_stats': species_stats.to_dict('records'),
            'recent_applications': recent_applications['count'].iloc[0] if not recent_applications.empty else 0
        }
    
    def get_service_statistics(self) -> Dict:
        """Get service booking statistics"""
        conn = self.get_connection()
        
        # Service bookings by type
        service_stats = pd.read_sql_query("""
            SELECT s.name, COUNT(sb.id) as bookings, SUM(s.price) as revenue
            FROM services s
            LEFT JOIN service_bookings sb ON s.id = sb.service_id
            GROUP BY s.id, s.name, s.price
        """, conn)
        
        # Monthly service revenue
        monthly_revenue = pd.read_sql_query("""
            SELECT strftime('%Y-%m', sb.created_at) as month, 
                   SUM(s.price) as revenue
            FROM service_bookings sb
            JOIN services s ON sb.service_id = s.id
            WHERE sb.created_at >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', sb.created_at)
            ORDER BY month
        """, conn)
        
        # Popular services
        popular_services = pd.read_sql_query("""
            SELECT s.name, COUNT(sb.id) as booking_count
            FROM services s
            LEFT JOIN service_bookings sb ON s.id = sb.service_id
            GROUP BY s.id, s.name
            ORDER BY booking_count DESC
        """, conn)
        
        conn.close()
        
        return {
            'service_stats': service_stats.to_dict('records'),
            'monthly_revenue': monthly_revenue.to_dict('records'),
            'popular_services': popular_services.to_dict('records')
        }
    
    def get_product_statistics(self) -> Dict:
        """Get product sales statistics"""
        conn = self.get_connection()
        
        # Products by category
        category_stats = pd.read_sql_query("""
            SELECT category, COUNT(*) as product_count, 
                   SUM(stock_quantity) as total_stock
            FROM products
            GROUP BY category
        """, conn)
        
        # Low stock products
        low_stock = pd.read_sql_query("""
            SELECT name, category, stock_quantity
            FROM products
            WHERE stock_quantity < 10
            ORDER BY stock_quantity ASC
        """, conn)
        
        conn.close()
        
        return {
            'category_stats': category_stats.to_dict('records'),
            'low_stock': low_stock.to_dict('records')
        }
    
    def get_donation_statistics(self) -> Dict:
        """Get donation statistics"""
        conn = self.get_connection()
        
        # Total donations
        total_donations = pd.read_sql_query("""
            SELECT COUNT(*) as count, SUM(amount) as total_amount
            FROM donations
        """, conn)
        
        # Monthly donations
        monthly_donations = pd.read_sql_query("""
            SELECT strftime('%Y-%m', created_at) as month, 
                   COUNT(*) as donation_count,
                   SUM(amount) as total_amount
            FROM donations
            WHERE created_at >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', created_at)
            ORDER BY month
        """, conn)
        
        conn.close()
        
        return {
            'total_donations': total_donations.to_dict('records')[0] if not total_donations.empty else {'count': 0, 'total_amount': 0},
            'monthly_donations': monthly_donations.to_dict('records')
        }
    
    def create_adoption_chart(self, parent_frame: tk.Frame) -> FigureCanvasTkAgg:
        """Create adoption statistics chart"""
        stats = self.get_adoption_statistics()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#1a1a1a')
        
        # Species distribution
        if stats['species_stats']:
            species_data = pd.DataFrame(stats['species_stats'])
            ax1.pie(species_data['count'], labels=species_data['species'], autopct='%1.1f%%')
            ax1.set_title('Pets by Species', color='white')
            ax1.set_facecolor('#1a1a1a')
        
        # Application status
        if stats['adoption_stats']:
            status_data = pd.DataFrame(stats['adoption_stats'])
            ax2.bar(status_data['status'], status_data['count'], color='#FFD700')
            ax2.set_title('Adoption Applications by Status', color='white')
            ax2.set_facecolor('#1a1a1a')
            ax2.tick_params(colors='white')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        return canvas
    
    def create_service_chart(self, parent_frame: tk.Frame) -> FigureCanvasTkAgg:
        """Create service statistics chart"""
        stats = self.get_service_statistics()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#1a1a1a')
        
        # Service popularity
        if stats['popular_services']:
            service_data = pd.DataFrame(stats['popular_services'])
            ax1.bar(service_data['name'], service_data['booking_count'], color='#FFD700')
            ax1.set_title('Service Bookings', color='white')
            ax1.set_facecolor('#1a1a1a')
            ax1.tick_params(colors='white', rotation=45)
        
        # Monthly revenue
        if stats['monthly_revenue']:
            revenue_data = pd.DataFrame(stats['monthly_revenue'])
            ax2.plot(revenue_data['month'], revenue_data['revenue'], color='#FFD700', marker='o')
            ax2.set_title('Monthly Service Revenue', color='white')
            ax2.set_facecolor('#1a1a1a')
            ax2.tick_params(colors='white', rotation=45)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        return canvas
    
    def get_dashboard_summary(self) -> Dict:
        """Get comprehensive dashboard summary"""
        adoption_stats = self.get_adoption_statistics()
        service_stats = self.get_service_statistics()
        product_stats = self.get_product_statistics()
        donation_stats = self.get_donation_statistics()
        
        return {
            'adoption': adoption_stats,
            'services': service_stats,
            'products': product_stats,
            'donations': donation_stats
        }
