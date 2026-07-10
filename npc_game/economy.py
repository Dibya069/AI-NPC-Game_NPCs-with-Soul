"""
Economy System
Dynamic economy with supply, demand, and prices
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import random


@dataclass
class Item:
    """A tradeable item"""
    name: str
    base_price: float
    current_price: float = 0.0
    supply: int = 100  # Available quantity
    demand: int = 100  # How much people want it
    
    def __post_init__(self):
        if self.current_price == 0.0:
            self.current_price = self.base_price
    
    def update_price(self):
        """Update price based on supply and demand"""
        if self.supply == 0:
            self.current_price = self.base_price * 3.0  # Scarcity!
            return
        
        # Price = base_price * (demand / supply)
        ratio = self.demand / max(1, self.supply)
        self.current_price = self.base_price * (0.5 + ratio)
        
        # Clamp to reasonable range
        self.current_price = max(
            self.base_price * 0.3,
            min(self.current_price, self.base_price * 3.0)
        )
    
    def buy(self, quantity: int = 1) -> float:
        """Buy item, returns cost"""
        if self.supply >= quantity:
            self.supply -= quantity
            self.demand = max(1, self.demand - quantity // 2)
            cost = self.current_price * quantity
            self.update_price()
            return cost
        return -1  # Not enough supply
    
    def sell(self, quantity: int = 1) -> float:
        """Sell item, returns payment"""
        self.supply += quantity
        self.demand = min(200, self.demand + quantity // 2)
        payment = self.current_price * quantity * 0.7  # Merchants buy at 70%
        self.update_price()
        return payment


@dataclass
class Economy:
    """Manages the world economy"""
    
    items: Dict[str, Item] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize with common items"""
        if not self.items:
            self.items = {
                "food": Item("Food", base_price=5.0, supply=150, demand=120),
                "water": Item("Water", base_price=2.0, supply=200, demand=150),
                "weapon": Item("Weapon", base_price=50.0, supply=30, demand=40),
                "armor": Item("Armor", base_price=80.0, supply=20, demand=35),
                "potion": Item("Potion", base_price=20.0, supply=50, demand=60),
                "book": Item("Book", base_price=15.0, supply=40, demand=20),
                "tools": Item("Tools", base_price=30.0, supply=60, demand=50),
                "cloth": Item("Cloth", base_price=10.0, supply=100, demand=80),
            }
    
    def get_item(self, item_name: str) -> Optional[Item]:
        """Get an item by name"""
        return self.items.get(item_name.lower())
    
    def buy_item(self, item_name: str, quantity: int = 1) -> tuple[bool, float]:
        """Buy an item, returns (success, cost)"""
        item = self.get_item(item_name)
        if item:
            cost = item.buy(quantity)
            if cost >= 0:
                return True, cost
        return False, 0.0
    
    def sell_item(self, item_name: str, quantity: int = 1) -> tuple[bool, float]:
        """Sell an item, returns (success, payment)"""
        item = self.get_item(item_name)
        if item:
            payment = item.sell(quantity)
            return True, payment
        return False, 0.0
    
    def update_market(self):
        """Simulate market changes"""
        for item in self.items.values():
            # Random fluctuations in supply/demand
            if random.random() < 0.3:
                item.supply += random.randint(-5, 10)
                item.supply = max(0, min(300, item.supply))
            
            if random.random() < 0.3:
                item.demand += random.randint(-5, 10)
                item.demand = max(10, min(200, item.demand))
            
            item.update_price()
    
    def apply_event_effect(self, event_description: str):
        """Apply economic effects from world events"""
        event_lower = event_description.lower()
        
        if "crop" in event_lower or "harvest" in event_lower:
            # Affects food supply
            if "poor" in event_lower or "shortage" in event_lower:
                self.items["food"].supply = max(20, self.items["food"].supply - 50)
                self.items["food"].demand += 30
            else:
                self.items["food"].supply += 50
                self.items["food"].demand -= 20
        
        if "merchant" in event_lower or "caravan" in event_lower:
            # General supply increase
            for item in self.items.values():
                item.supply += random.randint(5, 20)
        
        if "war" in event_lower or "conflict" in event_lower:
            # Weapons in demand
            self.items["weapon"].demand += 40
            self.items["armor"].demand += 40
        
        # Update all prices
        for item in self.items.values():
            item.update_price()
    
    def get_price_list(self) -> str:
        """Get formatted price list"""
        lines = ["💰 Market Prices:"]
        for name, item in sorted(self.items.items()):
            trend = "📈" if item.current_price > item.base_price else "📉"
            lines.append(
                f"  {trend} {item.name.capitalize()}: "
                f"{item.current_price:.1f} gold "
                f"(Supply: {item.supply}, Demand: {item.demand})"
            )
        return "\n".join(lines)
    
    def get_affordable_items(self, budget: float) -> list[str]:
        """Get list of items within budget"""
        return [name for name, item in self.items.items() 
                if item.current_price <= budget]


@dataclass  
class Inventory:
    """NPC's inventory"""
    
    items: Dict[str, int] = field(default_factory=dict)
    gold: float = 50.0
    
    def add_item(self, item_name: str, quantity: int = 1):
        """Add item to inventory"""
        self.items[item_name] = self.items.get(item_name, 0) + quantity
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory"""
        if self.has_item(item_name, quantity):
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            return True
        return False
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """Check if has item"""
        return self.items.get(item_name, 0) >= quantity
    
    def get_summary(self) -> str:
        """Get inventory summary"""
        lines = [f"💰 Gold: {self.gold:.1f}"]
        if self.items:
            lines.append("🎒 Items:")
            for item, qty in self.items.items():
                lines.append(f"  - {item.capitalize()} x{qty}")
        else:
            lines.append("🎒 No items")
        return "\n".join(lines)
