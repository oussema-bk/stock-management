# 📦 Stock Management System Guide

## ✅ What's New

### **Automatic Stock Integration with Sales**
- Sales now **automatically reduce stock** when completed
- Stock is **automatically restored** when sales are cancelled
- **Stock validation** prevents negative inventory
- Complete **audit trail** with stock movements

---

## 🔄 How It Works

### **1. Creating a Sale (PENDING Status)**

When you create a new sale:
1. Sale starts with status: **PENDING**
2. You add items to the sale
3. **Stock is NOT reduced yet** - it's just reserved
4. You can see if enough stock is available

### **2. Completing a Sale**

When you click "Complete Sale":
1. System checks if all items have sufficient stock
2. If OK: 
   - Stock is **reduced automatically**
   - Sale status → **COMPLETED**
   - **Stock movements created** for audit trail
3. If NOT OK:
   - Error message shows which products have insufficient stock
   - Sale remains PENDING

### **3. Cancelling a Sale**

When you cancel a completed sale:
1. If sale was COMPLETED:
   - Stock is **automatically restored**
   - **IN movements** created to track restoration
2. Sale status → **CANCELLED**

---

## 🛡️ Stock Protection

### **Negative Stock Prevention**

The system **prevents stock from going below 0** in these scenarios:

1. **Manual Stock Movements**
   - You can't remove more stock than available
   - Error message shows current vs. requested quantity

2. **Sales**
   - Can't add items to sale if stock insufficient
   - Can't complete sale without enough stock

3. **Adjustments**
   - Setting stock to negative values is blocked

---

## 📊 Stock Levels Explained

### **Stock Actuel** (Current Stock)
- The **real-time quantity** you have in inventory
- Updates automatically when:
  - Sales are completed (decreases)
  - Sales are cancelled (increases)
  - Stock movements are added

### **Stock Minimum** (Minimum Stock)
- Your **reorder threshold**
- When `Stock Actuel ≤ Stock Minimum`:
  - **Alert shown** on dashboard
  - Status: "Stock faible" 🟠
- When `Stock Actuel = 0`:
  - Status: "Rupture de stock" 🔴

### **Stock Maximum**
- Your warehouse capacity limit
- Helps plan restocking

---

## 🎯 Typical Workflow

### **Scenario: Selling Products**

```
1. Create Sale (PENDING)
   └─ Customer: TechSolutions SARL
   
2. Add Items
   ├─ Arduino Uno x5 (checks: stock available? ✓)
   ├─ LED Rouge x50 (checks: stock available? ✓)
   └─ Breadboard x3 (checks: stock available? ✓)
   
3. Complete Sale
   ├─ Validates all stock levels
   ├─ Reduces stock:
   │  ├─ Arduino Uno: 50 → 45
   │  ├─ LED Rouge: 800 → 750
   │  └─ Breadboard: 75 → 72
   └─ Creates stock movements (OUT)
   
Result: ✅ Sale completed, stock updated, movements logged
```

### **Scenario: Restocking**

```
1. Go to Stock → Movements
2. Add Stock Movement
   ├─ Type: IN (Entrée)
   ├─ Product: Arduino Uno
   ├─ Quantity: 20
   ├─ Reference: PO-2025-001
   └─ Notes: Restock from supplier XYZ
   
3. Submit
   └─ Stock updated: 45 → 65
   
Result: ✅ Stock increased, movement logged
```

---

## 📈 Sample Data

The database is now populated with:
- **20 products** across 6 categories
- **5 customers**
- **4 sales** (3 completed, 1 pending)
- **28 stock movements** (initial stock + sales)
- Logical pricing and realistic quantities

### To Re-populate Sample Data:
```bash
python3 manage.py populate_sample_data
```
⚠️ **Warning**: This clears ALL existing data!

---

## 🎨 UI Features

### **Sale Detail Page**
- Shows sale status badge (PENDING/COMPLETED/CANCELLED)
- **Complete Sale** button (visible on PENDING sales)
- **Cancel Sale** button (visible on all sales)
- Real-time stock availability check

### **Stock Dashboard**
- Low stock alerts
- Out of stock warnings
- Stock movements history

### **Products**
- Current stock levels
- Stock status indicators
- Quick stock adjustment

---

## 🔍 Stock Movement Types

| Type | French | When to Use | Effect |
|------|--------|-------------|--------|
| **IN** | Entrée de stock | Receiving shipments, returns | Increases stock |
| **OUT** | Sortie de stock | Manual removals, damages | Decreases stock |
| **ADJUSTMENT** | Ajustement | Inventory counts, corrections | Sets exact value |
| **TRANSFER** | Transfert | Between warehouses (future) | Not implemented |

---

## ⚡ Quick Reference

### **Stock Actuel (Current Stock)**
✅ Real-time inventory quantity
✅ Auto-updates with sales and movements
✅ Cannot go below 0

### **Stock Minimum (Minimum Stock)**
✅ Reorder threshold
✅ Triggers low stock alerts
✅ Helps prevent stockouts

### **Sales & Stock**
✅ PENDING sales don't reduce stock
✅ COMPLETED sales reduce stock
✅ CANCELLED sales restore stock
✅ Full audit trail maintained

---

## 🎯 Best Practices

1. **Set realistic minimum stock levels**
   - Based on average sales per week
   - Include safety margin

2. **Complete sales promptly**
   - Don't leave sales in PENDING too long
   - Stock isn't actually reserved until completed

3. **Use references in movements**
   - Purchase order numbers
   - Supplier names
   - Helps with auditing

4. **Regular stock adjustments**
   - Periodic inventory counts
   - Reconcile physical vs. system stock

5. **Monitor alerts**
   - Check low stock dashboard daily
   - Reorder before stockout

---

## 🆘 Troubleshooting

### **"Stock insuffisant" error**
- Check current stock on product page
- Verify pending sales haven't reserved stock
- Consider adjusting stock or reducing quantity

### **Stock seems wrong**
- Check stock movements history
- Look for unauthorized OUT movements
- Do physical inventory count
- Use ADJUSTMENT to correct

### **Can't complete sale**
- Verify all products have sufficient stock
- Check for negative stock values
- Review error message for specific product

---

**Need help?** Check the Stock Movements page for complete history of all stock changes.
