import tkinter as tk
from tkinter import ttk
from models.inventory import Inventory
from models.sales import SalesManager
from gui.inventory_frame import InventoryFrame
from gui.sales_frame import SalesFrame
from gui.reports_frame import ReportsFrame

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.inventory = Inventory()
        self.sales_manager = SalesManager()
        
        # Header frame avec style moderne
        header_frame = ttk.Frame(master, style='Header.TFrame')
        header_frame.pack(fill='x', padx=10, pady=5)
        
        # Company info avec style moderne
        company_frame = ttk.LabelFrame(header_frame, style='Header.TLabelframe')
        company_frame.pack(fill='x')
        
        # Titre principal
        title_label = ttk.Label(
            company_frame,
            text="GESTION DE MOTOS",
            style='HeaderTitle.TLabel'
        )
        title_label.pack(pady=(10, 5))
        
        # Info de contact
        contact_label = ttk.Label(
            company_frame,
            text="Chez Nouhoum Bama\nTél : +223 77873789",
            style='HeaderInfo.TLabel',
            justify='center'
        )
        contact_label.pack(pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create frames
        self.inventory_frame = InventoryFrame(self.notebook, self.inventory)
        self.sales_frame = SalesFrame(self.notebook, self.inventory, self.sales_manager)
        self.reports_frame = ReportsFrame(self.notebook, self.sales_manager)
        
        # Add frames to notebook
        self.notebook.add(self.inventory_frame, text='Inventaire')
        self.notebook.add(self.sales_frame, text='Ventes')
        self.notebook.add(self.reports_frame, text='Rapports')
        
        # Footer frame
        footer_frame = ttk.Frame(master, style='Footer.TFrame')
        footer_frame.pack(fill='x', side='bottom', padx=5, pady=2)
        
        # Footer text
        footer_label = ttk.Label(
            footer_frame,
            text="Développé par Cheick Oumar Cisse | Tél : +223 73505832",
            style='Footer.TLabel',
            justify='center'
        )
        footer_label.pack(side='right', padx=5)