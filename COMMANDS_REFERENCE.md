# Django Management Commands Reference

## Data Management Commands

### 1. Clear All Data (Except Users)
```bash
python3 manage.py clear_data
```
**What it does:**
- Deletes ALL sales, customers, products, stock levels, and stock movements
- **Preserves all users** (including admin)
- Useful when you want to start fresh but keep your login credentials

**Output:**
```
Deleting all data (keeping users)...
✅ Data deleted successfully!

Deleted:
  • SaleItems: 150
  • Sales: 100
  • Customers: 20
  • StockMovements: 200
  • StockLevels: 50
  • Products: 50
  • Categories: 10

⚠️  Users were preserved
```

---

### 2. Generate Fake Data
```bash
python3 manage.py generate_fake_data
```

**Options:**
```bash
# Generate with custom quantities
python3 manage.py generate_fake_data --categories 5 --products 30 --customers 10 --sales 50
```

**What it does:**
- Creates realistic fake data for testing
- All sales use the **new automatic stock logic**:
  - Sales start as PENDING
  - 75% are randomly completed (stock reduced automatically)
  - 25% stay pending
- Creates admin user if doesn't exist (username: admin, password: admin123)
- Validates stock availability before completing sales

**New Logic:**
- ✅ Only uses active products with stock > 0
- ✅ Limits sale quantities to available stock
- ✅ Uses `sale.complete_sale(user)` method for automatic stock reduction
- ✅ Creates proper stock movements for completed sales
- ✅ No negative stock possible

**Default quantities:**
- 10 categories
- 50 products
- 20 customers
- 100 sales

---

### 3. Populate Sample Data (Logical)
```bash
python3 manage.py populate_sample_data
```

**What it does:**
- **Clears ALL existing data** (including users)
- Creates 20 electrical component products
- Creates 5 business customers
- Creates 4 realistic sales scenarios
- All with logical pricing and stock levels

**⚠️ Warning:** This deletes EVERYTHING including users!

---

## Comparison

| Command | Deletes Users? | Creates Users? | Stock Logic | Use Case |
|---------|---------------|----------------|-------------|----------|
| `clear_data` | ❌ No | ❌ No | N/A | Clean slate, keep login |
| `generate_fake_data` | ❌ No | ✅ If needed | ✅ New automatic | Generate test data |
| `populate_sample_data` | ✅ Yes | ✅ Admin only | ✅ New automatic | Complete reset with examples |

---

## Typical Workflow

### Scenario 1: Testing with Fresh Data
```bash
# Keep your user, delete all data
python3 manage.py clear_data

# Generate fresh test data
python3 manage.py generate_fake_data --products 20 --sales 30

# Now you can test with clean data
```

### Scenario 2: Demo/Presentation
```bash
# Get clean, realistic demo data
python3 manage.py populate_sample_data

# Login with: admin / admin123
```

### Scenario 3: Large Dataset Testing
```bash
python3 manage.py clear_data
python3 manage.py generate_fake_data --categories 20 --products 200 --customers 50 --sales 500
```

---

## Migration Commands (Standard Django)

### Create migrations
```bash
python3 manage.py makemigrations
```

### Apply migrations
```bash
python3 manage.py migrate
```

### Create superuser
```bash
python3 manage.py createsuperuser
```

---

## Quick Reference: Data Cleanup

| Situation | Command |
|-----------|---------|
| "I want to test with fresh data but keep my login" | `clear_data` then `generate_fake_data` |
| "I want realistic demo data" | `populate_sample_data` |
| "I want to delete everything" | `populate_sample_data` |
| "I want lots of test data" | `generate_fake_data --sales 1000` |
| "I just want to remove products" | Use Django admin or shell |

---

## Notes

- All commands use the **new automatic stock management system**
- Stock can never go negative
- Completed sales automatically reduce stock
- Cancelled sales automatically restore stock
- All operations are logged in stock movements
