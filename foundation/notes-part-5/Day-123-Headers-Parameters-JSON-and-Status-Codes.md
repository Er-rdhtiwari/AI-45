# Day 123: API Request and Response Details

## 1. Day number

**Day 123**

## 2. Topic name

**Headers, Path Parameters, Query Parameters, JSON, and Status Codes**

Today you will look inside an API request and response and learn what additional information can travel between the client and server.

---

## 3. Connection

Yesterday, on **Day 122**, you learned how HTTP methods describe what a client wants to do:

```text
GET    → Read
POST   → Create
PUT    → Update
DELETE → Delete
```

Today, you will go one level deeper.

An API request may contain more than just:

```text
GET /products
```

It can also contain things such as:

```text
Headers
Path parameters
Query parameters
JSON body
```

And the server's response can contain:

```text
Status code
Headers
JSON response body
```

The basic picture becomes:

```text
Client
   |
   | HTTP request
   | - method
   | - URL
   | - parameters
   | - headers
   | - possibly JSON body
   ↓
Server
   |
   | HTTP response
   | - status code
   | - headers
   | - possibly JSON body
   ↓
Client
```

---

# 4. Important topics

Today you will focus on:

```text
Headers
Path parameter
Query parameter
JSON request body
JSON response
HTTP status code
```

You do **not** need to memorize every possible HTTP detail.

The goal is simply to recognize the main parts of a typical API request and response.

---

# 5. Foundational notes

Think of an API request as a message containing several pieces of information.

For example:

```text
POST /products

Content-Type: application/json

{
    "name": "Keyboard",
    "price": 1200
}
```

This request contains:

```text
Method → POST
Path   → /products
Header → Content-Type: application/json
Body   → product data
```

The server may respond:

```text
201 Created

{
    "id": 10,
    "name": "Keyboard",
    "price": 1200
}
```

This response contains:

```text
Status code → 201
JSON body   → created product
```

So HTTP communication is not just:

```text
request → response
```

It is more like:

```text
Request
├── method
├── URL
├── parameters
├── headers
└── body

Response
├── status code
├── headers
└── body
```

---

# 6. Headers

A **header** contains extra information about an HTTP request or response.

Think of headers as small pieces of **metadata**.

They describe the message rather than being the main data itself.

For example:

```text
Content-Type: application/json
```

This tells the receiver:

> The body contains JSON data.

Imagine sending a parcel.

```text
Parcel contents → actual data

Label on parcel → extra information about the parcel
```

Similarly:

```text
JSON body → actual API data

HTTP header → information about the request/response
```

For today, you only need to understand the general idea.

Do not worry about learning many different HTTP headers yet.

---

# 7. Path parameter

A **path parameter** is a value that appears directly inside the URL path.

Example:

```text
GET /products/25
```

Here:

```text
25
```

can be treated as a path parameter representing a particular product.

You could imagine the API route as:

```text
/products/{product_id}
```

Then:

```text
/products/25
```

means:

```text
product_id = 25
```

Another example:

```text
/users/7
```

could mean:

```text
user_id = 7
```

The path parameter normally helps identify a **specific resource**.

Simple mental model:

```text
/products/25
          ↑
     path parameter
```

---

# 8. Query parameter

A **query parameter** is extra information added after a `?` in the URL.

Example:

```text
GET /products?category=electronics
```

Here:

```text
category=electronics
```

is a query parameter.

Another example:

```text
GET /products?limit=10
```

Here:

```text
limit=10
```

is a query parameter.

It might mean:

> Return at most 10 products.

Query parameters are commonly useful for things like:

```text
filtering
searching
sorting
limiting results
```

You only need the basic idea today.

---

# 9. Path parameter vs query parameter

This distinction is important.

## Path parameter

A path parameter is part of the URL path.

Example:

```text
/products/25
```

Here:

```text
25
```

identifies a particular product.

Think:

```text
Which exact resource?
```

---

## Query parameter

A query parameter appears after `?`.

Example:

```text
/products?category=electronics
```

Here:

```text
category=electronics
```

modifies or filters the request.

Think:

```text
How should I search/filter the resources?
```

---

### Easy comparison

| Type | Example | Beginner meaning |
|---|---|---|
| Path parameter | `/products/25` | Give me product 25 |
| Query parameter | `/products?category=electronics` | Give me products matching electronics |

A simple memory trick:

```text
Path parameter
    ↓
Which resource?

Query parameter
    ↓
Which options or filters?
```

For example:

```text
/products/25
```

means:

```text
specific product → 25
```

while:

```text
/products?category=books
```

means:

```text
products filtered by category → books
```

---

# 10. JSON request body

Sometimes the client needs to send structured data to the server.

For example, to create a product:

```text
POST /products
```

The client could send:

```json
{
  "name": "Mouse",
  "price": 500
}
```

This is the **JSON request body**.

It contains the actual data being sent to the server.

Conceptually:

```text
Client
   |
   | POST /products
   |
   | JSON body:
   | {
   |   "name": "Mouse",
   |   "price": 500
   | }
   ↓
Server
```

Remember that JSON often uses:

```text
key : value
```

pairs.

For example:

```json
{
  "name": "Mouse",
  "price": 500
}
```

contains:

```text
name  → Mouse
price → 500
```

---

# 11. JSON response

The server can also send JSON back to the client.

For example:

```json
{
  "id": 25,
  "name": "Mouse",
  "price": 500
}
```

This is a **JSON response body**.

So JSON can travel in both directions.

```text
Client
   |
   | JSON request
   ↓
Server
   |
   | JSON response
   ↓
Client
```

For example:

```text
POST /products
```

Request body:

```json
{
  "name": "Mouse",
  "price": 500
}
```

Response body:

```json
{
  "id": 25,
  "name": "Mouse",
  "price": 500
}
```

The server might have generated the new ID:

```text
25
```

---

# 12. HTTP status code

An **HTTP status code** is a number in the server's response that tells the client what happened.

For example:

```text
200
```

generally means the request succeeded.

Another example:

```text
404
```

means the requested resource was not found.

Think of a status code as a short result message:

```text
Request
   ↓
Server processes it
   ↓
Status code tells client what happened
```

You only need six common codes today.

---

# 13. Status code 200 — OK

```text
200 OK
```

means that the request succeeded.

Example:

```text
GET /products/25
```

If product 25 exists, the server might return:

```text
200 OK
```

with:

```json
{
  "id": 25,
  "name": "Mouse",
  "price": 500
}
```

Beginner meaning:

```text
200 → Success
```

---

# 14. Status code 201 — Created

```text
201 Created
```

usually means that a new resource was successfully created.

Example:

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

The server creates the product and might respond:

```text
201 Created
```

with:

```json
{
  "id": 26,
  "name": "Monitor",
  "price": 8000
}
```

Beginner meaning:

```text
201 → New resource successfully created
```

---

# 15. Status code 400 — Bad Request

```text
400 Bad Request
```

generally means something is wrong with the request sent by the client.

For example, imagine the API expects:

```json
{
  "name": "Keyboard",
  "price": 1200
}
```

but receives invalid data.

Conceptually:

```text
Client
   |
   | incorrect request
   ↓
Server
   |
   | cannot correctly process it
   ↓
400
```

Beginner meaning:

```text
400 → Client sent an invalid request
```

---

# 16. Status code 401 — Unauthorized

```text
401 Unauthorized
```

generally means authentication is required or the provided authentication information is not valid.

Imagine an API resource that requires the client to identify itself properly.

```text
Client
   |
   | request without valid authentication
   ↓
Server
   |
   ↓
401
```

Beginner meaning:

```text
401 → Authentication problem
```

Do not worry about login tokens or detailed authentication systems yet.

You will only remember the basic meaning today.

---

# 17. Status code 404 — Not Found

```text
404 Not Found
```

means that the requested resource could not be found.

Example:

```text
GET /products/999
```

Suppose product `999` does not exist.

The server might respond:

```text
404 Not Found
```

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
   | Not found
   ↓
404
```

Beginner meaning:

```text
404 → Requested resource not found
```

---

# 18. Status code 500 — Internal Server Error

```text
500 Internal Server Error
```

means something went wrong inside the server while processing the request.

Example:

```text
Client sends valid request
        ↓
Server begins processing
        ↓
Unexpected server problem
        ↓
500
```

The important distinction is:

```text
400 → something wrong with the client's request

500 → something went wrong on the server
```

Beginner meaning:

```text
500 → Server-side problem
```

---

# 19. Common status codes summary

For Day 123, remember:

| Code | Name | Simple meaning |
|---:|---|---|
| `200` | OK | Request succeeded |
| `201` | Created | New resource created |
| `400` | Bad Request | Invalid client request |
| `401` | Unauthorized | Authentication problem |
| `404` | Not Found | Resource not found |
| `500` | Internal Server Error | Server problem |

A useful pattern is:

```text
2xx → generally successful

4xx → generally client/request problem

5xx → generally server problem
```

You do not need to learn other codes yet.

---

# 20. Easy example

Imagine this request:

```text
POST /products?notify=true

Content-Type: application/json
```

Body:

```json
{
  "name": "Webcam",
  "price": 2500
}
```

Let's identify its parts.

### Method

```text
POST
```

The intention is to create something.

### URL/path

```text
/products
```

The resource is products.

### Query parameter

```text
notify=true
```

It appears after:

```text
?
```

### Header

```text
Content-Type: application/json
```

This tells the server that the request body contains JSON.

### JSON body

```json
{
  "name": "Webcam",
  "price": 2500
}
```

This is the new product information.

If the product is successfully created, the server might respond:

```text
201 Created
```

with:

```json
{
  "id": 30,
  "name": "Webcam",
  "price": 2500
}
```

---

# 21. Another example with a path parameter

Suppose the client sends:

```text
GET /products/25
```

We can identify:

```text
Method         → GET
Resource       → products
Path parameter → 25
JSON body      → none needed for this simple example
```

If product `25` exists:

```text
Status → 200
```

Response:

```json
{
  "id": 25,
  "name": "Mouse",
  "price": 500
}
```

If product `25` does not exist:

```text
Status → 404
```

Notice how the same request method can produce different status codes depending on what happens.

---

# 22. Problem statement

Examine this API request:

```text
POST /products?notify=true

Content-Type: application/json
```

Request body:

```json
{
  "name": "Laptop Stand",
  "price": 1500
}
```

Assume the request is valid and the server successfully creates the product.

Identify:

```text
1. HTTP method
2. URL/path
3. Query parameter
4. Header
5. JSON request body
6. Expected success status code
7. Possible JSON response
```

Do not write Python or FastAPI code.

Focus only on recognizing the different pieces of the HTTP request and response.

---

# 23. Concepts used

The exercise combines everything from today's lesson:

```text
HTTP method
URL
Header
Path parameter
Query parameter
JSON request body
JSON response
HTTP status code
```

It also uses your Day 121 and Day 122 knowledge:

```text
Client
   ↓
HTTP request
   ↓
Server
   ↓
HTTP response
   ↓
Client
```

---

# 24. Thought process

When examining an API request, go through it in a consistent order.

### Step 1: Find the HTTP method

Look for:

```text
GET
POST
PUT
DELETE
```

Example:

```text
POST /products
```

means:

```text
method = POST
```

---

### Step 2: Find the URL or path

Example:

```text
/products/25
```

This tells you which resource is being accessed.

---

### Step 3: Look for path parameters

Ask:

> Is a value embedded directly inside the path?

Example:

```text
/products/25
```

Then:

```text
25 → path parameter
```

---

### Step 4: Look for `?`

If you see:

```text
?
```

the information after it may contain query parameters.

Example:

```text
/products?category=electronics
```

Then:

```text
category=electronics
```

is a query parameter.

---

### Step 5: Look for headers

Example:

```text
Content-Type: application/json
```

This is extra metadata about the HTTP message.

---

### Step 6: Look for a JSON body

Example:

```json
{
  "name": "Mouse",
  "price": 500
}
```

Ask:

> Is the client sending actual structured data to the server?

If yes, that may be the request body.

---

### Step 7: Determine what happened

Look at the server's status code.

For example:

```text
200 → successful request
201 → successfully created something
400 → bad request
401 → authentication problem
404 → resource not found
500 → server problem
```

---

# 25. Beginner-friendly request structure

You can imagine a request using this simple template:

```text
HTTP REQUEST
│
├── Method
│     POST
│
├── URL
│     /products?notify=true
│
├── Query parameter
│     notify=true
│
├── Headers
│     Content-Type: application/json
│
└── Body
      {
          "name": "Mouse",
          "price": 500
      }
```

The server might respond:

```text
HTTP RESPONSE
│
├── Status code
│     201
│
├── Headers
│     ...
│
└── Body
      {
          "id": 25,
          "name": "Mouse",
          "price": 500
      }
```

At this stage, you should be able to look at a simple request and identify its major parts.

---

# 26. Easy edge case: missing parameter

Suppose an API expects a particular product ID.

For example:

```text
/products/{product_id}
```

A valid request might be:

```text
GET /products/25
```

But suppose the client sends something incomplete that does not provide the required product identifier.

The server may not be able to determine which product the client wants.

Conceptually:

```text
Client
   |
   | Missing required information
   ↓
Server
   |
   | Cannot correctly process request
   ↓
Error response
```

Depending on the API design, this may produce an error.

The key lesson is:

> If the server requires information, the client must provide it in the expected place and format.

---

# 27. Easy edge case: malformed JSON

Correct JSON might look like:

```json
{
  "name": "Mouse",
  "price": 500
}
```

Malformed data might be missing important JSON syntax.

Conceptually:

```text
Client
   |
   | malformed JSON
   ↓
Server
   |
   | cannot understand request data
   ↓
Error response
```

A request problem like this may result in a client-error response.

For your beginner mental model:

```text
Malformed request data
        ↓
Could lead to a 400-type client error
```

You do not need to study JSON parsing errors in depth today.

---

# 28. Expected response

For the problem:

```text
POST /products?notify=true
```

with:

```json
{
  "name": "Laptop Stand",
  "price": 1500
}
```

you should eventually be able to explain the interaction like this:

```text
The client sends a POST request.

The resource is /products.

The request contains the query parameter:
notify=true

The Content-Type header indicates JSON data.

The JSON request body contains the new product information.

If the server successfully creates the product,
a 201 status code is expected.

The server may return the newly created product
as a JSON response.
```

Conceptually:

```text
Client
   |
   | POST /products?notify=true
   |
   | Content-Type: application/json
   |
   | {
   |   "name": "Laptop Stand",
   |   "price": 1500
   | }
   ↓
Server
   |
   | Create product
   ↓
201 Created
   |
   | {
   |   "id": 31,
   |   "name": "Laptop Stand",
   |   "price": 1500
   | }
   ↓
Client
```

---

# 29. Hint only

For the exercise, inspect the request from top to bottom.

Start with:

```text
POST
```

Ask:

```text
What does POST represent?
```

Then inspect:

```text
/products?notify=true
```

Look carefully at what comes after:

```text
?
```

Next inspect:

```text
Content-Type: application/json
```

Ask whether this is actual product data or information **about** the request.

Finally inspect:

```json
{
  "name": "Laptop Stand",
  "price": 1500
}
```

Then think about which success code is normally associated with:

```text
Create
```

Use only today's codes:

```text
200
201
400
401
404
500
```

---

# Day 123 key takeaway

Over the last three days, your API mental model has grown.

### Day 121

```text
Client → Request → Server
Client ← Response ← Server
```

### Day 122

You added HTTP methods:

```text
GET    → Read
POST   → Create
PUT    → Update
DELETE → Delete
```

### Day 123

Now you can inspect the contents of requests and responses:

```text
Client
   |
   | REQUEST
   | Method
   | URL
   | Path/query parameters
   | Headers
   | JSON body
   ↓
Server
   |
   | RESPONSE
   | Status code
   | Headers
   | JSON body
   ↓
Client
```

The most important distinctions to remember are:

```text
Path parameter  → identifies something in the URL path
Query parameter → provides options/filtering after ?

JSON body       → actual structured data being sent
Header          → extra information about the HTTP message

200 → success
201 → created
400 → bad request
401 → authentication problem
404 → not found
500 → server problem
```

This gives you the foundation needed to understand what you are actually seeing when you begin sending requests to real APIs or building API endpoints later.

By the way, ChatGPT Images 2.5 can turn a rough idea into a finished image, with richer textures and details you can refine. Want me to create an image of a beginner-friendly infographic showing the anatomy of an API request and response?