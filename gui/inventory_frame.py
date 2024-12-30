import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class InventoryFrame(ttk.Frame):
    def __init__(self, parent, inventory):
        super().__init__(parent)
        self.inventory = inventory
        
        # Create treeview
        self.tree = ttk.Treeview(self, 
            columns=('Date', 'Name', 'PrevStock', 'Entries', 'Outputs', 'Price', 'FinalQty', 'Comment'),
            show='headings',
            style='Modern.Treeview')
        
        self.tree.heading('Date', text='Date')
        self.tree.heading('Name', text='Marques')
        self.tree.heading('PrevStock', text='Stock Précédent')
        self.tree.heading('Entries', text='Entrées')
        self.tree.heading('Outputs', text='Sorties')
        self.tree.heading('Price', text='Prix')
        self.tree.heading('FinalQty', text='Quantité Finale')
        self.tree.heading('Comment', text='Commentaire')
        
        # Configure column widths
        self.tree.column('Date', width=100)
        self.tree.column('Name', width=150)
        self.tree.column('PrevStock', width=120)
        self.tree.column('Entries', width=80)
        self.tree.column('Outputs', width=80)
        self.tree.column('Price', width=100)
        self.tree.column('FinalQty', width=120)
        self.tree.column('Comment', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout with grid
        self.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        scrollbar.grid(row=0, column=1, sticky='ns', pady=10)
        
        # Add stock form
        self.add_frame = ttk.LabelFrame(self, text="Ajouter/Modifier Stock", style='Modern.TLabelframe')
        self.add_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=5)
        
        # Form grid
        form_frame = ttk.Frame(self.add_frame)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Date
        ttk.Label(form_frame, text="Date:", style='Modern.TLabel').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(form_frame, width=12, background='#007bff',
                                  foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Name
        ttk.Label(form_frame, text="Nom:", style='Modern.TLabel').grid(row=0, column=2, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, style='Modern.TEntry')
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Entries
        ttk.Label(form_frame, text="Entrées:", style='Modern.TLabel').grid(row=0, column=4, padx=5, pady=5)
        self.entries_var = tk.StringVar()
        self.entries_entry = ttk.Entry(form_frame, textvariable=self.entries_var, style='Modern.TEntry')
        self.entries_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Price
        ttk.Label(form_frame, text="Prix:", style='Modern.TLabel').grid(row=0, column=6, padx=5, pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(form_frame, textvariable=self.price_var, style='Modern.TEntry')
        self.price_entry.grid(row=0, column=7, padx=5, pady=5)
        
        # Comment
        ttk.Label(form_frame, text="Commentaire:", style='Modern.TLabel').grid(row=1, column=0, padx=5, pady=5)
        self.comment_var = tk.StringVar()
        self.comment_entry = ttk.Entry(form_frame, textvariable=self.comment_var, style='Modern.TEntry', width=50)
        self.comment_entry.grid(row=1, column=1, columnspan=7, sticky='ew', padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.add_frame)
        buttons_frame.pack(fill='x', padx=5, pady=10)
        
        # Add button
        ttk.Button(buttons_frame, text="Ajouter", style='Modern.TButton',
                  command=self.add_stock).pack(side=tk.LEFT, padx=5)
        
        # Update button
        ttk.Button(buttons_frame, text="Modifier", style='Modern.TButton',
                  command=self.update_stock).pack(side=tk.LEFT, padx=5)
        
        # Delete button
        ttk.Button(buttons_frame, text="Supprimer", style='Modern.TButton',
                  command=self.delete_stock).pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        ttk.Button(buttons_frame, text="Rafraîchir", style='Modern.TButton',
                  command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        
        # Clear database button
        ttk.Button(buttons_frame, text="Nettoyer Base", style='Modern.TButton',
                  command=self.clear_database).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Bind tree selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.refresh_inventory()

    def add_stock(self):
        try:
            name = self.name_var.get()
            entries = int(self.entries_var.get() or 0)
            price = float(self.price_var.get() or 0)
            comment = self.comment_var.get()
            date = self.date_entry.get_date()

            if not name:
                messagebox.showerror("Erreur", "Veuillez entrer un nom de moto!")
                return

            self.inventory.add_movement(name, date, entries=entries, price=price, comment=comment)
            self.clear_form()
            self.refresh_inventory()
            messagebox.showinfo("Succès", "Stock ajouté avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides!")

    def update_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à modifier!")
            return
        
        try:
            item = self.tree.item(selected[0])
            name = self.name_var.get()
            entries = int(self.entries_var.get() or 0)
            price = float(self.price_var.get() or 0)
            comment = self.comment_var.get()
            date = self.date_entry.get_date()

            # Mettre à jour le mouvement existant
            for movement in self.inventory.movements:
                if (movement.motorcycle_name == item['values'][1] and 
                    movement.date.strftime("%Y-%m-%d") == item['values'][0]):
                    movement.entries = entries
                    movement.price = price
                    movement.comment = comment
                    movement.date = date
                    break

            self.clear_form()
            self.refresh_inventory()
            messagebox.showinfo("Succès", "Stock mis à jour avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides!")

    def delete_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à supprimer!")
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément?"):
            item = self.tree.item(selected[0])
            # Supprimer le mouvement
            self.inventory.movements = [m for m in self.inventory.movements 
                                     if not (m.motorcycle_name == item['values'][1] and 
                                           m.date.strftime("%Y-%m-%d") == item['values'][0])]
            self.clear_form()
            self.refresh_inventory()
            messagebox.showinfo("Succès", "Stock supprimé avec succès!")

    def clear_database(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment nettoyer toute la base de données? Cette action est irréversible!"):
            self.inventory.movements.clear()
            self.refresh_inventory()
            messagebox.showinfo("Succès", "Base de données nettoyée avec succès!")

    def refresh_inventory(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        movements = self.inventory.get_daily_movements()
        for movement in movements:
            self.tree.insert('', 'end', values=(
                movement['date'],
                movement['motorcycle'],
                movement['prev_stock'],
                movement['entries'],
                movement['outputs'],
                f"{movement['price']:.2f}",
                movement['balance'],
                movement['comment']
            ))

    def clear_form(self):
        self.name_var.set('')
        self.entries_var.set('')
        self.price_var.set('')
        self.comment_var.set('')
        self.date_entry.set_date(datetime.now())

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.name_var.set(item['values'][1])
            self.entries_var.set(item['values'][3])
            self.price_var.set(item['values'][5])
            self.comment_var.set(item['values'][7])
            self.date_entry.set_date(datetime.strptime(item['values'][0], "%Y-%m-%d"))