import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry

class ReportsFrame(ttk.Frame):
    def __init__(self, parent, sales_manager):
        super().__init__(parent)
        self.sales_manager = sales_manager
        
        # Filter frame
        filter_frame = ttk.LabelFrame(self, text="Filtres", style='Modern.TLabelframe')
        filter_frame.pack(padx=10, pady=5, fill='x')
        
        # Date filter
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(padx=10, pady=5, fill='x')
        
        ttk.Label(date_frame, text="Date:", style='Modern.TLabel').pack(side='left', padx=5)
        self.date_filter = DateEntry(date_frame, width=12, background='#007bff',
                                   foreground='white', borderwidth=2)
        self.date_filter.pack(side='left', padx=5)
        
        ttk.Button(date_frame, text="Filtrer", 
                  style='Modern.TButton',
                  command=self.refresh_report).pack(side='left', padx=5)
        
        # Create treeview
        self.tree = ttk.Treeview(self, 
                                columns=('Date', 'Motorcycle', 'Quantity', 'Price', 'Total'),
                                show='headings',
                                style='Modern.Treeview')
        
        self.tree.heading('Date', text='Date')
        self.tree.heading('Motorcycle', text='Moto')
        self.tree.heading('Quantity', text='Quantité')
        self.tree.heading('Price', text='Prix unitaire')
        self.tree.heading('Total', text='Total')
        
        # Configure column widths
        self.tree.column('Date', width=150)
        self.tree.column('Motorcycle', width=200)
        self.tree.column('Quantity', width=100)
        self.tree.column('Price', width=100)
        self.tree.column('Total', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(padx=10, pady=10, fill='both', expand=True, side='left')
        scrollbar.pack(pady=10, fill='y', side='right')
        
        self.refresh_report()
    
    def refresh_report(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        selected_date = self.date_filter.get_date()
        
        for sale in self.sales_manager.get_sales_report():
            sale_date = datetime.strptime(sale['date'], "%Y-%m-%d %H:%M")
            if sale_date.date() == selected_date:
                self.tree.insert('', 'end', values=(
                    sale['date'],
                    sale['motorcycle'],
                    sale['quantity'],
                    f"{sale['price']:.2f}",
                    f"{sale['total']:.2f}"
                ))