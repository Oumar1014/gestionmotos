from datetime import datetime
from typing import List

class Sale:
    def __init__(self, motorcycle_name: str, quantity: int, price: float):
        self.motorcycle_name = motorcycle_name
        self.quantity = quantity
        self.price = price
        self.date = datetime.now()
        
class SalesManager:
    def __init__(self):
        self.sales: List[Sale] = []
    
    def record_sale(self, motorcycle_name: str, quantity: int, price: float) -> None:
        sale = Sale(motorcycle_name, quantity, price)
        self.sales.append(sale)
    
    def get_sales_report(self) -> List[dict]:
        return [
            {
                "date": sale.date.strftime("%Y-%m-%d %H:%M"),
                "motorcycle": sale.motorcycle_name,
                "quantity": sale.quantity,
                "price": sale.price,
                "total": sale.quantity * sale.price
            }
            for sale in self.sales
        ]