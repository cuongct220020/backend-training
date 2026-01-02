---
layout: default
title: "Python OOP Conventions"
---

# Python OOP Conventions (Modern Typing)

## Table of Contents
1. [Goals](#goals)
2. [Naming Conventions](#1-naming-conventions)
3. [Modern Type Hints](#2-modern-type-hints-python-311)
4. [Standard Class Structure](#3-standard-class-structure)
5. [General Principles](#4-general-principles)
6. [Docstrings](#5-docstrings-google-style)
7. [Code Organization](#6-code-organization)
8. [Inheritance & Composition](#7-inheritance--composition)
9. [SOLID Principles](#8-solid-principles-summary)
10. [Type Checking Setup](#9-type-checking-setup)
11. [Team Standards Checklist](#10-team-standards-checklist)

## Goals
- Write readable, maintainable code
- Ensure consistency across the project  
- Follow Python 3.11+ typing standards
- Support effective team collaboration

## 1. Naming Conventions

<table>
    <thead>
        <tr>
            <th>Component</th>
            <th>Convention</th>
            <th>Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Class</td>
            <td>PascalCase</td>
            <td><code>ShoppingList</code>, <code>FoodItem</code></td>
        </tr>
        <tr>
            <td>Method/Function</td>
            <td>snake_case</td>
            <td><code>add_item()</code>, <code>check_expiry()</code></td>
        </tr>
        <tr>
            <td>Attribute</td>
            <td>snake_case</td>
            <td><code>expiry_date</code>, <code>total_items</code></td>
        </tr>
        <tr>
            <td>Private</td>
            <td><code>_prefix</code></td>
            <td><code>_password_hash</code></td>
        </tr>
        <tr>
            <td>Constant</td>
            <td>UPPER_CASE</td>
            <td><code>MAX_ITEMS = 100</code></td>
        </tr>
        <tr>
            <td>Type Alias</td>
            <td>PascalCase</td>
            <td><code>UserId</code>, <code>JsonDict</code></td>
        </tr>
        <tr>
            <td>Module/Package</td>
            <td>snake_case</td>
            <td><code>food_storage.py</code>, <code>shopping_system/</code></td>
        </tr>
    </tbody>
</table>

**Rules**: Class names are nouns, method names are verbs. Avoid vague names (`Manager`, `Helper`) and unclear abbreviations (`fd` → `food`).

## 2. Modern Type Hints (Python 3.11+)

### Built-in Generic Types (Python 3.9+)
```python
# ✅ Modern (use this)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ Deprecated (don't use)
from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:
    ...
```

### Union with `|` Operator (Python 3.10+)
```python
# ✅ Modern
def find_user(user_id: int) -> User | None:
    return database.get(user_id)

# ❌ Old
from typing import Optional, Union
def find_user(user_id: int) -> Optional[User]:
    ...
```

### Type Aliases with `TypeAlias`
```python
from typing import TypeAlias

UserId: TypeAlias = int
JsonDict: TypeAlias = dict[str, any]
OptionalUser: TypeAlias = User | None
```

### `Self` Type (Python 3.11+)
```python
from typing import Self

class FoodItem:
    def set_quantity(self, qty: float) -> Self:
        """Method chaining returns instance of same class."""
        self.quantity = qty
        return self
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Factory method."""
        return cls(**data)
```

### Protocol for Structural Typing
```python
from typing import Protocol

class Drawable(Protocol):
    """Duck-typing interface without inheritance."""
    def draw(self) -> None: ...

class Closeable(Protocol):
    def close(self) -> None: ...

def cleanup(resource: Closeable) -> None:
    """Works with any object that has close()."""
    resource.close()
```

### TypedDict for Structured Data
```python
from typing import TypedDict, NotRequired

class FoodItemData(TypedDict):
    """Type-safe dictionary structure."""
    name: str
    quantity: float
    unit: str
    category: NotRequired[str]  # Optional field

def create_food(data: FoodItemData) -> FoodItem:
    return FoodItem(**data)
```

### Avoid `Any` Without Documentation
```python
# ❌ Bad
def process(data: Any) -> Any:
    return data

# ✅ Good - document why Any is needed
def legacy_api_call(payload: any) -> any:
    """Call legacy API with arbitrary JSON.
    
    TODO(typing): Replace with Protocol when API schema is available.
    """
    return requests.post("/api", json=payload).json()
```

### ClassVar for Class Attributes
```python
from typing import ClassVar

class FoodItem:
    EXPIRY_WARNING_DAYS: ClassVar[int] = 3
    _total_items: ClassVar[int] = 0
    
    def __init__(self, name: str) -> None:
        self.name = name  # Instance attribute (no ClassVar)
```

### Final for Constants
```python
from typing import Final

MAX_ITEMS: Final = 100
API_URL: Final[str] = "https://api.example.com"

@final
def validate_item(item: FoodItem) -> bool:
    """This method cannot be overridden."""
    return item.quantity > 0
```

## 3. Standard Class Structure

```python
from datetime import datetime
from typing import Self, ClassVar

class FoodItem:
    """
    Represents a food item.
    
    Attributes:
        EXPIRY_WARNING_DAYS: Days before expiration warning
        name: Item name
        quantity: Amount available
    """
    
    # 1. Class attributes with ClassVar
    EXPIRY_WARNING_DAYS: ClassVar[int] = 3
    _total_items: ClassVar[int] = 0
    
    # 2. Constructor with type hints
    def __init__(
        self,
        name: str,
        quantity: float,
        expiry_date: datetime
    ) -> None:
        """Initialize food item."""
        self.name = name
        self._quantity = quantity
        self.expiry_date = expiry_date
        FoodItem._total_items += 1
    
    # 3. Magic methods
    def __str__(self) -> str:
        return f"{self.name} ({self._quantity})"
    
    def __repr__(self) -> str:
        return f"FoodItem(name='{self.name}')"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FoodItem):
            return NotImplemented
        return self.name == other.name
    
    # 4. Properties
    @property
    def quantity(self) -> float:
        """Get quantity."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: float) -> None:
        """Set quantity with validation."""
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value
    
    @property
    def is_expired(self) -> bool:
        """Check if expired."""
        return datetime.now() > self.expiry_date
    
    # 5. Public methods
    def use(self, amount: float) -> None:
        """Use food amount."""
        if amount > self._quantity:
            raise ValueError(f"Insufficient quantity: {self._quantity}")
        self._quantity -= amount
    
    # 6. Class methods with Self
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from dictionary."""
        return cls(
            name=data['name'],
            quantity=data['quantity'],
            expiry_date=datetime.fromisoformat(data['expiry_date'])
        )
    
    # 7. Static methods
    @staticmethod
    def calculate_shelf_life(
        start: datetime,
        end: datetime
    ) -> int:
        """Calculate shelf life in days."""
        return (end - start).days
    
    # 8. Private methods
    def _validate(self) -> bool:
        """Internal validation."""
        return self._quantity >= 0
```

## 4. General Principles

### Properties over Getters/Setters
```python
# ❌ Java style
def get_total_items(self) -> int:
    return self._total_items

# ✅ Pythonic
@property
def total_items(self) -> int:
    return len(self._items)
```

### Composition over Inheritance
```python
# ❌ Deep inheritance chain
class Food: pass
class PerishableFood(Food): pass
class Vegetable(PerishableFood): pass

# ✅ Composition
class ExpiryTracker:
    def check_status(self, food: FoodItem) -> str:
        return "Expired" if food.is_expired else "Good"

class Refrigerator:
    def __init__(self) -> None:
        self.tracker = ExpiryTracker()  # Has-a relationship
        self._items: list[FoodItem] = []
```

### Visibility Levels
```python
class UserAccount:
    def __init__(self, username: str) -> None:
        self.username = username             # Public
        self._password_hash = "..."          # Private
        self._pin_code = "0000"              # Private
```

## 5. Docstrings (Google Style)

```python
def suggest_recipes(
    self,
    refrigerator: 'Refrigerator',
    min_ingredients: int = 3
) -> list[str]:
    """
    Suggest recipes based on fridge contents.
    
    Args:
        refrigerator: Refrigerator with available food
        min_ingredients: Minimum required ingredients (default 3)
    
    Returns:
        List of recipe names
    
    Raises:
        ValueError: If min_ingredients < 1
        EmptyFridgeError: If refrigerator empty
    
    Note:
        Prioritizes recipes using soon-to-expire ingredients.
    """
    if min_ingredients < 1:
        raise ValueError("min_ingredients must be >= 1")
    return self._find_recipes(refrigerator, min_ingredients)
```

## 6. Code Organization

### Import Order (PEP 8)
```python
# 1. Standard library
import json
from datetime import datetime
from typing import TypeAlias, Protocol
from collections.abc import Iterator

# 2. Third-party
import requests
from sqlalchemy import create_engine

# 3. Internal modules
from .models import FoodItem
from .config import MAX_ITEMS
```

### Class Member Order
1. Class attributes (with `ClassVar`)
2. `__init__`
3. Magic methods (`__str__`, `__repr__`, `__eq__`, etc.)
4. Properties (`@property`)
5. Public methods
6. Class methods (`@classmethod`)
7. Static methods (`@staticmethod`)
8. Private methods (`_method`)


## 7. Inheritance & Composition

### Abstract Base Classes
```python
from abc import ABC, abstractmethod

class Storage(ABC):
    """Abstract base class for storage."""
    
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: list[FoodItem] = []
    
    @abstractmethod
    def add_item(self, item: FoodItem) -> bool:
        """Must implement in subclass."""
        ...

class Refrigerator(Storage):
    def add_item(self, item: FoodItem) -> bool:
        if item.category not in ["Meat", "Vegetables"]:
            return False
        self._items.append(item)
        return True
```

### Composition Example
```python
class NotificationService:
    def notify(self, user_id: str, message: str) -> None:
        print(f"[{user_id}] {message}")

class SmartRefrigerator:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.notifier = NotificationService()  # Composition
        self._items: list[FoodItem] = []
    
    def check_expiry(self) -> None:
        expired = [i for i in self._items if i.is_expired]
        if expired:
            self.notifier.notify(self.user_id, "Items expiring!")
```

## 8. SOLID Principles (Summary)

### S - Single Responsibility
```python
# Each class has ONE reason to change
class FoodRepository:
    """Only handles food storage."""
    def save(self, food: FoodItem) -> None: ...

class NotificationService:
    """Only handles notifications."""
    def send_alert(self, msg: str) -> None: ...
```

### O - Open/Closed
```python
# Open for extension, closed for modification
class PriceCalculator(ABC):
    @abstractmethod
    def calculate(self, price: float, qty: float) -> float: ...

class StandardCalculator(PriceCalculator):
    def calculate(self, price: float, qty: float) -> float:
        return price * qty

class DiscountCalculator(PriceCalculator):
    def __init__(self, discount: float) -> None:
        self.discount = discount
    
    def calculate(self, price: float, qty: float) -> float:
        total = price * qty
        return total * (1 - self.discount)
```

### L - Liskov Substitution
```python
# Subclass replaces base class seamlessly
class Storage(ABC):
    @abstractmethod
    def add_item(self, item: FoodItem) -> bool: ...

def store_items(storage: Storage, items: list[FoodItem]) -> None:
    """Works with ANY Storage subclass."""
    for item in items:
        storage.add_item(item)
```

### I - Interface Segregation
```python
# Use small Protocols instead of large interfaces
class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class TextEditor:
    """Only needs what it uses."""
    def edit(self, doc: Writable) -> None: ...
```

### D - Dependency Inversion
```python
# Depend on abstractions, not concrete classes
class Database(Protocol):
    def save(self, data: dict) -> bool: ...

class FoodManager:
    def __init__(self, db: Database) -> None:  # Inject abstraction
        self.db = db

# Can swap implementations
manager = FoodManager(PostgreSQL())
manager = FoodManager(MongoDB())
```

## 9. Type Checking Setup

### mypy Configuration (`pyproject.toml`)
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_any_generics = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

### Pyright Configuration (`pyrightconfig.json`)
```json
{
  "include": ["src"],
  "typeCheckingMode": "strict",
  "pythonVersion": "3.11",
  "reportMissingTypeStubs": false
}
```

### Run Type Checking
```bash
mypy src/           # Run mypy
pyright src/        # Or use pyright
mypy --strict src/  # Enforce strict mode
```

## 10. Team Standards Checklist

### Must Follow
- Target Python 3.11+ minimum
- Use built-in generics (`list`, `dict`, not `List`, `Dict`)
- Use `|` for unions (not `Optional`, `Union`)
- Annotate all public functions/methods
- Use `Self` for methods returning instance
- Use `Protocol` for duck typing
- Use `TypedDict` for structured dicts
- Use `Final` for constants
- Enable mypy/pyright strict mode in CI
- Document any use of `Any` with comment

### Code Review Checklist
- [ ] All public functions typed
- [ ] Modern syntax (`list`, `dict`, `|` operators)
- [ ] Using `Self` for method chaining
- [ ] No `Any` without explanation
- [ ] Type aliases use `TypeAlias`
- [ ] Constants marked `Final`
- [ ] Passes `mypy --strict`
- [ ] Protocols used for interfaces
- [ ] Google-style docstrings

**Last Updated**: October 2025 (Python 3.11+ standards)