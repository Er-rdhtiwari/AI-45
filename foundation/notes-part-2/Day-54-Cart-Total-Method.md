# Day 54: Cart Total Method
# Day 54: Cart Total Method

## 1. Day Number

**Day 54**

## 2. Topic Name

**Method with Accumulator**

Today you will learn how a method can:

* loop through a list of objects
* collect values from those objects
* keep adding them into a variable
* return the final result

The variable that keeps collecting the total is called an **accumulator**.

---

## 3. Connection

You can already add products to a cart.

A cart may contain products like:

```text
Laptop   → 50000
Mouse    → 1000
Keyboard → 2000
```

Today you will make the `Cart` class calculate:

```text
50000 + 1000 + 2000 = 53000
```

You will add a method called:

```python
calculate_total()
```

The important difference today is that the method should **return** the total instead of only printing it.

---

# 4. Important Topics

### Loop

A loop lets us visit every product stored in the cart.

Conceptually:

```python
for product in cart_items:
    ...
```

---

### List of Objects

Your cart contains `Product` objects.

For example:

```text
Cart
 |
 +-- Product object
 +-- Product object
 +-- Product object
```

Each product may contain attributes such as:

```text
name
price
stock
```

So while looping, you can access:

```python
product.price
```

---

### Accumulator

An accumulator is a variable that keeps a running total.

For example:

```python
total = 0
```

Then:

```text
total = 0

add 100
total = 100

add 200
total = 300

add 50
total = 350
```

Here, `total` is the accumulator.

---

### Return Value

A method can calculate something and send the result back using:

```python
return
```

Conceptually:

```python
def some_method(self):
    result = ...
    return result
```

Then the returned value can be stored:

```python
answer = object.some_method()
```

---

# 5. Foundational Notes

## A. Start the accumulator at zero

When calculating a sum, normally begin with:

```python
total = 0
```

Why zero?

Because initially nothing has been added.

---

## B. Visit every object

Suppose the cart contains:

```text
Product("Book", 500)
Product("Pen", 20)
Product("Bag", 1000)
```

The loop should examine each product one at a time.

```text
First product  → Book
Second product → Pen
Third product  → Bag
```

---

## C. Access the object's price

Because each item is a `Product` object, its price can be accessed through its attribute.

Concept:

```python
product.price
```

---

## D. Add price to the accumulator

For every product:

```text
total = total + product price
```

A shorter Python form is:

```python
total += product_price
```

Both mean the same basic thing.

---

## E. Return after the loop

The total should be returned **after all products have been processed**.

Conceptually:

```text
start total

loop:
    add product price

return total
```

Be careful not to return too early.

If `return` happens inside the loop, the method may stop after the first product.

---

# 6. Easy Example

Before applying this idea to objects, consider a simple list of numbers:

```python
prices = [100, 200, 50]

total = 0

for price in prices:
    total += price

print(total)
```

Output:

```text
350
```

The important pattern is:

```text
Initialize
    ↓
Loop
    ↓
Accumulate
    ↓
Use final result
```

With your cart, the pattern will be similar, except the list contains **Product objects instead of numbers**.

For example:

```text
items
 |
 +-- Product → price = 100
 +-- Product → price = 200
 +-- Product → price = 50
```

So instead of adding the item itself, you use the object's price.

---

# 7. Problem Statement

Add a:

```python
calculate_total()
```

method to the `Cart` class.

The method should:

1. Start a total at `0`.
2. Loop through every Product object in the cart's `items` list.
3. Get each product's price.
4. Add the price to the total.
5. Return the final total.

Example cart:

```text
Book     ₹500
Pen      ₹20
Notebook ₹100
```

The method should calculate:

```text
500 + 20 + 100
```

and return:

```text
620
```

---

# 8. Concepts Used

You will use:

* `class`
* object
* method
* `self`
* list attribute
* list of objects
* `for` loop
* object attributes
* accumulator variable
* `return`
* method call

The central idea is:

```text
Cart object
   |
   | items
   v
[Product, Product, Product]
   |
   | loop
   v
read each .price
   |
   v
add into total
   |
   v
return total
```

---

# 9. Thought Process

Before writing code, think through the problem.

### Step 1: Where are the products?

Inside the cart's:

```text
items list
```

---

### Step 2: What information do I need from each product?

Its:

```text
price
```

---

### Step 3: How do I examine every product?

Use a:

```text
for loop
```

---

### Step 4: Where do I keep the running sum?

Create:

```text
total = 0
```

---

### Step 5: What happens for each product?

Add its price:

```text
total = total + product price
```

---

### Step 6: What happens after every product has been processed?

Return:

```text
total
```

So the overall thinking is:

```text
Create total
     |
     v
Loop through items
     |
     v
Read product.price
     |
     v
Add price to total
     |
     v
More products?
  /       \
Yes        No
 |          |
loop      return total
```

---

# 10. Pseudocode

```text
CLASS Cart

    CONSTRUCTOR
        create empty items list

    METHOD calculate_total

        set total to 0

        FOR each product in items
            add product price to total

        RETURN total
```

Notice that this is only pseudocode, not the complete Python solution.

---

# 11. Suggested Solving Approach

Use an **OOP-based approach** because both `Product` and `Cart` represent real objects.

Your structure can conceptually look like:

```text
Product class
    |
    +-- name
    +-- price
    +-- stock


Cart class
    |
    +-- items
    |
    +-- add_product()
    |
    +-- remove_product()
    |
    +-- calculate_total()
```

The responsibility of each class is becoming clearer:

```text
Product
    stores product information

Cart
    manages products
    adds products
    removes products
    calculates total
```

This is one of the important ideas in OOP: **put related behavior with the object responsible for it.**

---

# 12. Easy Edge Cases

## Edge Case 1: Empty Cart

Suppose:

```text
items = []
```

There are no products.

Your accumulator starts as:

```text
total = 0
```

The loop runs zero times.

Therefore the method should naturally return:

```text
0
```

You do not necessarily need a special condition for this.

---

## Edge Case 2: Product Price is `0`

Suppose:

```text
Product A → 100
Product B → 0
Product C → 50
```

Calculation:

```text
100 + 0 + 50
```

Result:

```text
150
```

A zero-price product should not cause an error.

---

## Small Mental Test

Imagine:

```text
Cart items:

Apple  → 50
Milk   → 60
Bread  → 40
```

Trace the accumulator:

```text
Starting total = 0

Apple:
0 + 50 = 50

Milk:
50 + 60 = 110

Bread:
110 + 40 = 150
```

Final result:

```text
150
```

---

# 13. Expected Input

You may create products such as:

```text
Product 1:
name  = "Book"
price = 500

Product 2:
name  = "Pen"
price = 20

Product 3:
name  = "Bag"
price = 1000
```

Add them to the cart.

Then call:

```text
cart.calculate_total()
```

There does not need to be keyboard input for this exercise unless you want to extend it later.

---

# 14. Expected Output

For:

```text
Book = 500
Pen  = 20
Bag  = 1000
```

Expected total:

```text
1520
```

You could eventually display something like:

```text
Cart Total: 1520
```

For an empty cart:

```text
Cart Total: 0
```

---

# 15. Hint Only

Inside `calculate_total()`:

```text
1. Create a variable starting at 0.
2. Loop through self.items.
3. Each item is a Product object.
4. Read the item's price attribute.
5. Add that price to your accumulator.
6. After the loop finishes, return the accumulator.
```

Think about this skeleton without filling in the missing parts:

```python
def calculate_total(self):
    total = ___

    for product in ___:
        total = total + ___

    return ___
```

The key question is:

**What attribute of each `product` object contains the value you need to add?**
