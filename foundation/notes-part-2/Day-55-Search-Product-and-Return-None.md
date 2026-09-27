# Day 55: Search Product and Return None
# Day 55: Search Product and Return `None`

## 1. Day Number

**Day 55**

## 2. Topic Name

**Search method and `None`**

Today you will learn how to search through a list of objects and:

* return the matching object when found
* return `None` when nothing matches

---

## 3. Connection

Previously, you removed products from a cart by searching for a product name.

Today, instead of removing the product, you will **return the product object itself**.

The idea is:

```text
Search product
      |
      v
Found?
 /   \
Yes   No
 |     |
return return
object None
```

This pattern is extremely common in Python applications.

---

## 4. Important Topics

Today's main concepts are:

* `for` loop
* `return`
* `None`
* list of objects
* object attributes
* search logic
* method/function

---

# 5. Foundational Notes

## What does searching mean?

Suppose your program contains three products:

```text
Laptop
Mouse
Keyboard
```

The user searches for:

```text
Mouse
```

Your program checks each product one by one.

```text
Laptop == Mouse?    No
Mouse == Mouse?     Yes
```

Once the product is found, the program can immediately return it.

---

## What is `return`?

`return` sends a value back from a function or method.

Simple example:

```python
def get_number():
    return 10
```

Then:

```python
number = get_number()
```

Now:

```text
number = 10
```

---

## What is `None`?

`None` represents **no value / nothing found / no result**.

For example:

```python
result = None
```

It does not mean:

```python
0
```

It does not mean:

```python
""
```

It means:

```text
there is currently no object/value here
```

---

## Why return `None` when searching?

Suppose you search for:

```text
Phone
```

but your product list contains only:

```text
Laptop
Mouse
Keyboard
```

There is no product object to return.

So returning:

```python
None
```

clearly tells the caller:

> No matching product was found.

---

## List of objects

Instead of storing simple strings:

```python
products = ["Laptop", "Mouse"]
```

you may have objects:

```text
Product object
    name = Laptop
    price = 50000

Product object
    name = Mouse
    price = 500
```

The list contains the **objects themselves**.

Conceptually:

```text
products
   |
   +--> Product("Laptop")
   |
   +--> Product("Mouse")
   |
   +--> Product("Keyboard")
```

When searching, you check an attribute such as:

```python
product.name
```

---

# 6. Easy Example

Before using Product objects, understand the same idea with numbers.

Suppose:

```python
numbers = [10, 20, 30]
```

You want to search for:

```text
20
```

The logic is:

```text
Start loop

10 == 20?
No

20 == 20?
Yes

Return 20
```

If searching for:

```text
50
```

then:

```text
10 == 50? No
20 == 50? No
30 == 50? No

Loop finished

Return None
```

The important pattern is:

```text
FOR each item
    IF item matches
        RETURN item

RETURN None
```

Notice that `return None` happens **after the loop finishes**.

---

# 7. Problem Statement

Create a product list.

Each product should be represented using a `Product` object.

Write a function or method that:

1. accepts a product name to search for
2. loops through the product list
3. compares the requested name with each product's name
4. returns the matching `Product` object if found
5. returns `None` if no matching product exists

For example:

```text
Products:

Laptop
Mouse
Keyboard
```

Search:

```text
Mouse
```

Result:

```text
Mouse product object
```

Search:

```text
Phone
```

Result:

```python
None
```

---

# 8. Concepts Used

### Class

Represents a product.

Conceptually:

```text
Product
 ├── name
 ├── price
 └── stock
```

### Object

An individual product created from the class.

For example:

```text
Laptop Product object
```

### List of objects

Store multiple Product objects together.

```text
products
 ├── laptop_object
 ├── mouse_object
 └── keyboard_object
```

### Loop

Visit every product.

```python
for product in products:
```

### Attribute access

Check the product's name.

```python
product.name
```

### `if`

Compare the current product against the requested name.

### `return`

Immediately send the matching product back.

### `None`

Represent the situation where no product was found.

---

# 9. Thought Process

Think about the problem in this order.

### Step 1: What am I searching?

A product name.

For example:

```text
Mouse
```

### Step 2: Where are the products?

Inside a list.

Conceptually:

```text
products = [
    Laptop object,
    Mouse object,
    Keyboard object
]
```

### Step 3: How can I inspect every product?

Use a loop.

```text
for every product in products
```

### Step 4: What should I compare?

Compare:

```text
current product name
```

with:

```text
requested product name
```

### Step 5: What happens if they match?

Return the current Product object.

```text
Laptop -> no
Mouse -> yes

RETURN Mouse object
```

The search can stop immediately.

### Step 6: What if the loop finishes without finding anything?

Return:

```python
None
```

Overall flow:

```text
Search "Mouse"
      |
      v
+-------------+
| Laptop      |
+-------------+
      |
   no match
      |
      v
+-------------+
| Mouse       |
+-------------+
      |
    match
      |
      v
Return Mouse object
```

Not-found flow:

```text
Search "Phone"
      |
      v
Laptop -> no
      |
Mouse -> no
      |
Keyboard -> no
      |
Loop finished
      |
      v
Return None
```

---

# 10. Pseudocode

OOP-style pseudocode:

```text
CREATE Product class

CREATE Cart or ProductManager class

STORE Product objects in a list

DEFINE search_product(product_name)

    FOR each product in product list

        IF product.name equals product_name
            RETURN product

    RETURN None
```

Notice this important structure:

```text
FOR ...
    IF ...
        RETURN product

RETURN None
```

The final `RETURN None` should usually be **outside the loop**.

---

# 11. Suggested Solving Approach

## Preferred: OOP-Based Approach

Since you are already working with `Product` and `Cart`, continue using OOP.

A possible design is:

```text
Product
 ├── name
 ├── price
 └── stock

Cart
 ├── items
 ├── add_product()
 ├── remove_product()
 ├── calculate_total()
 └── search_product()
```

Conceptually:

```text
cart.search_product("Mouse")
```

may return:

```text
<Product object for Mouse>
```

while:

```text
cart.search_product("Phone")
```

may return:

```python
None
```

This approach fits naturally with your previous cart exercises.

---

## Functional Approach

A standalone function is also acceptable.

Conceptually:

```text
search_product(products, product_name)
```

The function receives:

```text
product list
+
name being searched
```

and returns:

```text
Product object
```

or:

```python
None
```

For this learning sequence, the **OOP approach is preferred**.

---

# 12. Easy Edge Cases

## Edge Case 1: Product Not Found

Products:

```text
Laptop
Mouse
Keyboard
```

Search:

```text
Phone
```

No product matches.

Expected result:

```python
None
```

---

## Edge Case 2: Empty Product List

Suppose:

```python
products = []
```

Search:

```text
Laptop
```

The loop has nothing to inspect.

Therefore, the result should be:

```python
None
```

This is useful because you don't need special complicated logic for an empty list.

Conceptually:

```text
Empty list
   |
FOR loop runs 0 times
   |
RETURN None
```

---

# 13. Expected Input

Example products:

```text
Product 1:
Name: Laptop
Price: 50000
Stock: 5

Product 2:
Name: Mouse
Price: 500
Stock: 20

Product 3:
Name: Keyboard
Price: 1500
Stock: 10
```

Search input:

```text
Enter product name: Mouse
```

Another possible input:

```text
Enter product name: Phone
```

---

# 14. Expected Output

When the product exists:

```text
Enter product name: Mouse
Product found: Mouse
```

You may also display other attributes:

```text
Product found
Name: Mouse
Price: 500
Stock: 20
```

Internally, however, your search function/method should return the **Product object**, not just print the name.

For a missing product:

```text
Enter product name: Phone
Product not found
```

Internally:

```python
None
```

A useful calling pattern is conceptually:

```text
result = search for product

IF result is None
    print product not found
ELSE
    print result's details
```

---

# 15. Hint Only

Think about these three lines of logic:

```python
for product in ...:
```

Then compare:

```python
product.name
```

with the searched name.

If they match:

```python
return ...
```

After the **entire loop finishes**, think about:

```python
return None
```

The key structure is:

```text
loop
    |
    +-- match? --> return Product object
    |
loop ends
    |
    v
return None
```

**Important beginner point:** don't put `return None` inside the loop too early. Otherwise, your method might check only the first product and stop before searching the rest.
