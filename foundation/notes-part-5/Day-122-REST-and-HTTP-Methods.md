# Day 122: REST APIs and HTTP Methods

## 1. Day number

**Day 122**

## 2. Topic name

**REST, GET, POST, PUT, and DELETE**

Today you will learn how APIs commonly use different HTTP methods for different kinds of operations.

---

## 3. Connection

Yesterday, on **Day 121**, you learned the basic HTTP flow:

```text
Client
  ↓ request
Server
  ↓ response
Client
```

You learned that a client sends an HTTP request to a server, and the server sends back a response.

Today, you will add one important idea:

> Different HTTP methods usually represent different intentions.

For example:

```text
GET    → read data
POST   → create data
PUT    → update data
DELETE → delete data
```

These ideas are commonly used when designing **REST APIs**.

---

# 4. Important topics

## REST API

**REST** stands for:

```text
Representational State Transfer
```

You do not need to memorize the full definition yet.

At a beginner level, think of a REST API as:

> An API that organizes data as resources and commonly uses HTTP methods to perform operations on those resources.

For example, an online store may have a product resource:

```text
/products
```

and an individual product:

```text
/products/10
```

A client might use different HTTP methods with those URLs.

```text
GET    /products/10
PUT    /products/10
DELETE /products/10
```

The URL identifies the resource.

The HTTP method describes what the client wants to do with it.

---

## Resource

A **resource** is something that the API manages.

Examples:

```text
product
customer
order
book
student
employee
```

In a products API, one product could look like:

```json
{
  "id": 10,
  "name": "Keyboard",
  "price": 1200
}
```

Here:

```text
Product = resource
```

A collection of products might be represented by:

```text
/products
```

A specific product might be represented by:

```text
/products/10
```

---

## Endpoint

An **endpoint** is a location in an API that a client can send requests to.

Example:

```text
https://api.example.com/products
```

Another endpoint might be:

```text
https://api.example.com/products/10
```

You can think of an endpoint as an API address.

For example:

```text
/products
```

could represent all products.

And:

```text
/products/10
```

could represent product number 10.

---

# 5. Foundational notes

The main idea today is very simple.

Suppose an API manages products.

The client might want to:

```text
Read a product
Create a product
Update a product
Delete a product
```

REST-style APIs often represent those intentions using HTTP methods.

```text
GET
POST
PUT
DELETE
```

Think of the HTTP method as the **verb**.

Think of the resource as the **thing being acted upon**.

For example:

```text
GET /products/10
```

can be read approximately as:

```text
GET product 10
```

Similarly:

```text
DELETE /products/10
```

can be understood as:

```text
DELETE product 10
```

This is a useful beginner mental model.

---

# 6. CRUD and HTTP methods

A very common software concept is **CRUD**.

CRUD stands for:

```text
C → Create
R → Read
U → Update
D → Delete
```

These are four basic operations that many applications perform on data.

For example, with products:

```text
Create a new product
Read an existing product
Update an existing product
Delete an existing product
```

REST APIs often connect CRUD operations with HTTP methods like this:

| CRUD operation | HTTP method | Meaning |
|---|---|---|
| Create | `POST` | Create a new resource |
| Read | `GET` | Retrieve a resource |
| Update | `PUT` | Update a resource |
| Delete | `DELETE` | Delete a resource |

A simple memory trick is:

```text
CRUD

Create → POST
Read   → GET
Update → PUT
Delete → DELETE
```

---

# 7. GET

`GET` is commonly used to **read or retrieve data**.

Example:

```text
GET /products/10
```

Meaning:

```text
"Give me product 10."
```

The server might return:

```json
{
  "id": 10,
  "name": "Keyboard",
  "price": 1200
}
```

Conceptually:

```text
Client
   |
   | GET /products/10
   ↓
Server
   |
   | Find product 10
   ↓
Product data
```

You can also imagine:

```text
GET /products
```

meaning:

```text
"Give me the products."
```

For today, remember:

```text
GET → Read
```

---

# 8. POST

`POST` is commonly used to **create a new resource**.

Suppose the client wants to create a new product.

It might send:

```text
POST /products
```

along with product information:

```json
{
  "name": "Mouse",
  "price": 500
}
```

Conceptually:

```text
Client
   |
   | POST /products
   |
   | new product data
   ↓
Server
   |
   | Create product
   ↓
Response
```

The server might assign the product an ID:

```json
{
  "id": 11,
  "name": "Mouse",
  "price": 500
}
```

For today, remember:

```text
POST → Create
```

---

# 9. PUT

`PUT` is commonly used to **update an existing resource**.

Suppose product 10 currently contains:

```json
{
  "id": 10,
  "name": "Keyboard",
  "price": 1200
}
```

You want to update it.

The request could conceptually be:

```text
PUT /products/10
```

with new information:

```json
{
  "name": "Mechanical Keyboard",
  "price": 1500
}
```

Meaning:

```text
"Update product 10 with this information."
```

The flow looks like:

```text
Client
   |
   | PUT /products/10
   | updated product data
   ↓
Server
   |
   | Update product 10
   ↓
Updated result
```

For today, remember:

```text
PUT → Update
```

Do not worry yet about more detailed rules surrounding partial versus complete updates.

---

# 10. DELETE

`DELETE` is commonly used to **delete a resource**.

Example:

```text
DELETE /products/10
```

Meaning:

```text
"Delete product 10."
```

Conceptually:

```text
Client
   |
   | DELETE /products/10
   ↓
Server
   |
   | Delete product 10
   ↓
Response
```

The server may return a confirmation that the operation succeeded.

For today, remember:

```text
DELETE → Delete
```

---

# 11. Easy products API example

Imagine an API with this base endpoint:

```text
https://api.example.com/products
```

The server currently has:

```text
Product 1 → Laptop
Product 2 → Keyboard
Product 3 → Mouse
```

Now let's perform different operations.

## Read product 2

```text
GET /products/2
```

Meaning:

```text
Retrieve product 2.
```

---

## Create a new product

```text
POST /products
```

with:

```json
{
  "name": "Monitor",
  "price": 8000
}
```

Meaning:

```text
Create a new product.
```

---

## Update product 2

```text
PUT /products/2
```

with:

```json
{
  "name": "Wireless Keyboard",
  "price": 1500
}
```

Meaning:

```text
Update product 2.
```

---

## Delete product 3

```text
DELETE /products/3
```

Meaning:

```text
Delete product 3.
```

---

# 12. Simple mapping

This is the main mapping to remember today:

```text
GET    → read product
POST   → create product
PUT    → update product
DELETE → delete product
```

Or with CRUD:

```text
Create → POST
Read   → GET
Update → PUT
Delete → DELETE
```

You can visualize the whole idea like this:

```text
                 Products API
                      |
        +-------------+-------------+
        |             |             |
       GET           POST          PUT
        |             |             |
       Read          Create        Update
                                      |
                                   DELETE
                                      |
                                    Delete
```

A cleaner version is:

```text
Client wants to...
        |
        +-- Read ------> GET
        |
        +-- Create ----> POST
        |
        +-- Update ----> PUT
        |
        +-- Delete ----> DELETE
```

---

# 13. Resource + method thinking

When working with REST APIs, try to separate two questions.

First:

```text
What resource am I working with?
```

Example:

```text
product
```

Second:

```text
What do I want to do with that resource?
```

Example:

```text
read
create
update
delete
```

Then choose the HTTP method.

Example:

```text
Resource:
product 8

Operation:
read

Method:
GET
```

Result:

```text
GET /products/8
```

Another example:

```text
Resource:
product 8

Operation:
delete

Method:
DELETE
```

Result:

```text
DELETE /products/8
```

---

# 14. Problem statement

Suppose you have this products API:

```text
https://api.example.com/products
```

Choose the correct HTTP method for each operation.

### Operation 1

Retrieve product number 20.

```text
/products/20
```

Which HTTP method should you use?

---

### Operation 2

Create a new product:

```json
{
  "name": "Webcam",
  "price": 2500
}
```

Which HTTP method should you use?

---

### Operation 3

Update product number 20 with a new price.

Which HTTP method should you use?

---

### Operation 4

Remove product number 20.

Which HTTP method should you use?

Your job is only to identify:

```text
GET
POST
PUT
or
DELETE
```

Do not write FastAPI or Python code.

---

# 15. Concepts used

This exercise uses:

```text
REST API
Resource
Endpoint
HTTP method
GET
POST
PUT
DELETE
CRUD
```

The most important connection is:

```text
Resource + desired operation
            ↓
      HTTP method
```

For example:

```text
Product + Read
      ↓
     GET
```

---

# 16. Thought process

When you see an API operation, ask:

### Step 1: What resource am I working with?

Example:

```text
Product
```

### Step 2: What does the client want to do?

Ask whether the operation is:

```text
Create
Read
Update
Delete
```

### Step 3: Map the operation to an HTTP method

Use:

```text
Create → POST
Read   → GET
Update → PUT
Delete → DELETE
```

### Step 4: Identify the endpoint

For example:

```text
/products
```

or:

```text
/products/20
```

### Step 5: Combine method and endpoint

Example:

```text
Read product 20
```

becomes:

```text
GET /products/20
```

You do not need to think about programming syntax yet.

---

# 17. Beginner-friendly pseudocode

Imagine a client wants to interact with products.

```text
START

choose the product operation

IF operation is "read"
    use GET

ELSE IF operation is "create"
    use POST

ELSE IF operation is "update"
    use PUT

ELSE IF operation is "delete"
    use DELETE

send request to the products API

server processes the request

server sends a response

END
```

For one product:

```text
IF user wants product information
    GET /products/product_id

IF user wants to update product
    PUT /products/product_id

IF user wants to delete product
    DELETE /products/product_id
```

For creating a product:

```text
POST /products
send new product data
```

---

# 18. Suggested solving approach: REST-style thinking

Use this simple three-step approach.

### Step A: Find the noun

The noun is usually the **resource**.

Example:

```text
product
```

### Step B: Find the action

Example:

```text
retrieve
create
update
remove
```

Translate these into CRUD:

```text
retrieve → Read
create   → Create
update   → Update
remove   → Delete
```

### Step C: Choose the method

```text
Read   → GET
Create → POST
Update → PUT
Delete → DELETE
```

Example:

```text
"Remove product 5"

Resource:
product 5

Operation:
Delete

HTTP method:
DELETE
```

So conceptually:

```text
DELETE /products/5
```

---

# 19. Easy edge case: product does not exist

Imagine the client sends:

```text
GET /products/999
```

But product `999` does not exist.

The server cannot return that product.

Conceptually:

```text
Client
   |
   | GET /products/999
   ↓
Server
   |
   | Search for product 999
   |
   | Product not found
   ↓
Error response
```

The important lesson is:

> Using the correct HTTP method does not guarantee that the requested resource exists.

The request itself may be logically correct, but the requested product may not exist.

You will learn proper HTTP error status codes later.

---

# 20. Easy edge case: invalid operation

Suppose someone says:

```text
"I want to create a new product using GET."
```

That does not match the simple REST mapping you are learning.

For today's model:

```text
GET → read
```

Creating a resource normally maps to:

```text
POST
```

So first identify the actual intention:

```text
Create new product
```

Then choose:

```text
POST
```

Similarly:

```text
Read product
```

should make you think:

```text
GET
```

and not:

```text
DELETE
```

---

# 21. Quick comparison

| Method | Main beginner meaning | Example |
|---|---|---|
| `GET` | Read | Get product 10 |
| `POST` | Create | Add a new product |
| `PUT` | Update | Change product 10 |
| `DELETE` | Delete | Remove product 10 |

A useful memory sentence is:

```text
GET gets data.
POST creates data.
PUT updates data.
DELETE deletes data.
```

---

# 22. Hint only

For the problem, first translate each sentence into one CRUD word.

For example:

```text
Retrieve → Read
Add      → Create
Change   → Update
Remove   → Delete
```

Then use:

```text
Create → ?
Read   → ?
Update → ?
Delete → ?
```

Your four choices are:

```text
GET
POST
PUT
DELETE
```

Do not think about code yet.

---

## Day 122 key takeaway

Yesterday you learned:

```text
Client → Request → Server
Client ← Response ← Server
```

Today you added the idea that the **HTTP method communicates the intention of the request**.

Remember:

```text
          REST-style API
                |
      Resource: Product
                |
    +-----------+-----------+
    |           |           |
 Create       Read        Update       Delete
    |           |           |            |
   POST        GET         PUT         DELETE
```

The most important mapping for Day 122 is:

```text
GET    → Read
POST   → Create
PUT    → Update
DELETE → Delete
```

Once this feels natural, concepts such as API endpoints, request bodies, status codes, and FastAPI routes will be much easier to understand.