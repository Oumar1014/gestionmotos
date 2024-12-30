import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SalesFrame(ttk.Frame):
    def __init__(self, parent, inventory, sales_manager):
        super().__init__(parent)
        self.inventory = inventory
        self.sales_manager = sales_manager
        
        # Sales form
        form_frame = ttk.LabelFrame(self, text="Enregistrer une vente", style='Modern.TLabelframe')
        form_frame.pack(padx=10, pady=5, fill='x')
        
        # Grid for form elements
        grid_frame = ttk.Frame(form_frame)
        grid_frame.pack(padx=10, pady=5, fill='x')
        
        # Motorcycle selection
        ttk.Label(grid_frame, text="Moto:", style='Modern.TLabel').grid(row=0, column=0, padx=5, pady=5)
        self.moto_var = tk.StringVar()
        self.moto_combo = ttk.Combobox(grid_frame, textvariable=self.moto_var, style='Modern.TCombobox')
        self.moto_combo['values'] = [m.name for m in inventory.get_stock()]
        self.moto_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Quantity
        ttk.Label(grid_frame, text="Quantité:", style='Modern.TLabel').grid(row=0, column=2, padx=5, pady=5)
        self.qty_var = tk.StringVar()
        ttk.Entry(grid_frame, textvariable=self.qty_var, style='Modern.TEntry').grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        # Price
        ttk.Label(grid_frame, text="Prix unitaire:", style='Modern.TLabel').grid(row=0, column=4, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(grid_frame, textvariable=self.price_var, style='Modern.TEntry').grid(row=0, column=5, padx=5, pady=5, sticky='ew')
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(pady=10, fill='x')
        
        # Submit button
        ttk.Button(buttons_frame, text="Enregistrer la vente", 
                  style='Modern.TButton',
                  command=self.record_sale).pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        ttk.Button(buttons_frame, text="Rafraîchir", 
                  style='Modern.TButton',
                  command=self.refresh_motos).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(3, weight=1)
        grid_frame.columnconfigure(5, weight=1)
    
    def refresh_motos(self):
        self.moto_combo['values'] = [m.name for m in self.inventory.get_stock()]
    
    def record_sale(self):
        try:
            name = self.moto_var.get()
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
            
            if not name:
                messagebox.showerror("Erreur", "Veuillez sélectionner une moto!")
                return
            
            if self.inventory.remove_motorcycle(name, qty):
                self.sales_manager.record_sale(name, qty, price)
                self.moto_var.set('')
                self.qty_var.set('')
                self.price_var.set('')
                self.refresh_motos()
                messagebox.showinfo("Succès", "Vente enregistrée avec succès!")
            else:
                messagebox.showerror("Erreur", "Stock insuffisant!")
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides!")