"""
Modern UI components for the pet booking system
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Any

class ModernFrame(tk.Frame):
    """Modern styled frame with rounded corners effect"""
    
    def __init__(self, parent, bg_color=None, bg="#ffffff", border_color="#e5e7eb", **kwargs):
        if bg_color is not None:
            bg = bg_color
        super().__init__(parent, bg=bg, relief=tk.FLAT, bd=1, **kwargs)
        self.configure(highlightbackground=border_color, highlightthickness=1)

class ModernButton(tk.Button):
    """Modern styled button with hover effects"""
    
    def __init__(self, parent, text="", command=None, style="primary", **kwargs):
        # Define styles
        styles = {
            "primary": {
                "bg": "#3b82f6",
                "fg": "white",
                "activebackground": "#2563eb",
                "activeforeground": "white"
            },
            "secondary": {
                "bg": "#e5e7eb",
                "fg": "#374151",
                "activebackground": "#d1d5db",
                "activeforeground": "#374151"
            },
            "success": {
                "bg": "#10b981",
                "fg": "white",
                "activebackground": "#059669",
                "activeforeground": "white"
            },
            "danger": {
                "bg": "#ef4444",
                "fg": "white",
                "activebackground": "#dc2626",
                "activeforeground": "white"
            }
        }
        
        style_config = styles.get(style, styles["primary"])
        
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            **style_config,
            **kwargs
        )
        
        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self.default_bg = style_config["bg"]
        self.hover_bg = style_config["activebackground"]
    
    def _on_enter(self, event):
        self.configure(bg=self.hover_bg)
    
    def _on_leave(self, event):
        self.configure(bg=self.default_bg)

class ModernLabel(tk.Label):
    """Modern styled label with typography options"""
    
    def __init__(self, parent, text="", style="body", **kwargs):
        # Define typography styles
        styles = {
            "heading1": {"font": ("Segoe UI", 32, "bold"), "fg": "#1f2937"},
            "heading2": {"font": ("Segoe UI", 24, "bold"), "fg": "#1f2937"},
            "heading3": {"font": ("Segoe UI", 18, "bold"), "fg": "#1f2937"},
            "heading4": {"font": ("Segoe UI", 16, "bold"), "fg": "#1f2937"},
            "body": {"font": ("Segoe UI", 11), "fg": "#374151"},
            "caption": {"font": ("Segoe UI", 10), "fg": "#6b7280"},
            "small": {"font": ("Segoe UI", 9), "fg": "#6b7280"}
        }
        
        style_config = styles.get(style, styles["body"])
        
        default_bg = kwargs.pop("bg", "#ffffff")
        
        # Merge style config with kwargs, giving priority to kwargs
        final_config = {**style_config}
        final_config.update(kwargs)
        
        super().__init__(
            parent,
            text=text,
            bg=default_bg,
            **final_config
        )

class ModernEntry(tk.Entry):
    """Modern styled entry field with validation"""
    
    def __init__(self, parent, placeholder="", validate_func=None, **kwargs):
        super().__init__(
            parent,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bd=1,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb",
            **kwargs
        )
        
        self.placeholder = placeholder
        self.validate_func = validate_func
        self.is_placeholder = True
        
        if placeholder:
            self.insert(0, placeholder)
            self.configure(fg="#9ca3af")
        
        # Bind events
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        if validate_func:
            self.bind("<KeyRelease>", self._on_validate)
    
    def _on_focus_in(self, event):
        if self.is_placeholder:
            self.delete(0, tk.END)
            self.configure(fg="#374151")
            self.is_placeholder = False
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg="#9ca3af")
            self.is_placeholder = True
    
    def _on_validate(self, event):
        if self.validate_func and not self.is_placeholder:
            is_valid = self.validate_func(self.get())
            self.configure(
                highlightcolor="#10b981" if is_valid else "#ef4444"
            )
    
    def get_value(self):
        """Get the actual value (not placeholder)"""
        return "" if self.is_placeholder else self.get()

class ModernCard(ModernFrame):
    """Card component with shadow effect"""
    
    def __init__(self, parent, bg_color='#ffffff', border_color='#e5e7eb', **kwargs):
        super().__init__(
            parent,
            bg_color=bg_color,
            border_color=border_color,
            **kwargs
        )
        self.configure(padx=20, pady=20)
        
        self.bg_color = bg_color
    
    def cget(self, option):
        """Override cget to handle bg_color requests"""
        if option == "bg" or option == "bg_color":
            return self.bg_color
        return super().cget(option)

class ModernScrollableFrame(tk.Frame):
    """Scrollable frame for long content"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack components
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
