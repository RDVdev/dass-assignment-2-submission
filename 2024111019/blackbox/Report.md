# QuickCart REST API Black Box Testing Report

## 1. Scope

This report covers black-box testing of QuickCart API using only documentation in QuickCart System.md.

- Roll number: 2024111019
- Tools: pytest, requests
- Base URL: http://127.0.0.1:8080/api/v1
- Test files:
  - quickcart_blackbox/test_quickcart_api.py (self-contained: fixtures + tests)

## 2. Test Case Design Approach

Test design includes all required categories:

- Valid requests
- Invalid inputs
- Missing fields/headers
- Wrong data types
- Boundary values

The suite validates:

- Correct HTTP status codes
- Proper JSON response structure
- Returned data correctness against API specification

Observed summary:

- Total: 45
- Passed: 33
- Failed: 12

## 4. Test Case Inventory (Input, Expected Output, Justification)

Legend:

- V = Valid request
- I = Invalid input
- M = Missing field/header
- T = Wrong type/format
- B = Boundary

| ID | Endpoint | Type | Input | Expected Output | Justification |
|---|---|---|---|---|---|
| BB-01 | GET /admin/users | M | No X-Roll-Number | 401 + error JSON | Validates mandatory roll header check |
| BB-02 | GET /admin/users | T | X-Roll-Number=invalid-roll | 400 + error JSON | Validates roll number type validation |
| BB-03 | GET /profile | M | Missing X-User-ID | 400 + error JSON | Validates user header requirement |
| BB-04 | GET /profile | T | X-User-ID=abc | 400 + error JSON | Reject non-numeric user IDs |
| BB-05 | GET /profile | B | X-User-ID=0 | 400 + error JSON | Reject lower-bound invalid positive-int IDs |
| BB-06 | GET /profile | B | X-User-ID=-3 | 400 + error JSON | Reject negative IDs |
| BB-07 | GET /profile | V | Valid headers | 200 + required profile keys | Validates core profile retrieval contract |
| BB-08 | PUT /profile | B | name='A' | 400 + error JSON | Name lower boundary validation |
| BB-09 | PUT /profile | B | phone='12345' | 400 + error JSON | Phone length boundary validation |
| BB-10 | PUT /profile | T | phone='12345abcde' | 400 + error JSON | Phone digit-only validation |
| BB-11 | POST /addresses | M | Missing pincode | 400 + error JSON | Required field validation |
| BB-12 | POST /addresses | I | label='WORK' | 400 + error JSON | Label enum validation |
| BB-13 | POST /addresses | B | pincode='41100' | 400 + error JSON | Pincode length boundary |
| BB-14 | PUT /addresses/{id} | I | Modify immutable fields | 400 + error JSON | Validates update restrictions |
| BB-15 | POST /addresses + GET /addresses | V | Add default twice | Exactly one default | Validates default uniqueness rule |
| BB-16 | GET /products | V | Valid headers | 200 + required product fields | Validates product schema and active-only listing |
| BB-17 | GET /products/{id} | I | product_id=999999 | 404 + error JSON | Nonexistent resource handling |
| BB-18 | POST /cart/add | I | bad product id | 404 + error JSON | Product existence validation |
| BB-19 | POST /cart/add | B | quantity=0 | 400 + error JSON | Quantity lower boundary |
| BB-20 | POST /cart/add | B | quantity=-1 | 400 + error JSON | Negative quantity rejection |
| BB-21 | POST /cart/add | B | quantity=stock+1 | 400 + error JSON | Stock upper-bound validation |
| BB-22 | POST /cart/add twice | V | same product 2 then 3 | quantity accumulates to 5 | Merge behavior validation |
| BB-23 | POST /cart/update | B | quantity=0 | 400 + error JSON | Update boundary validation |
| BB-24 | POST /cart/update | B | quantity=-2 | 400 + error JSON | Update negative validation |
| BB-25 | POST /cart/remove | I | remove absent product | 404 + error JSON | Missing cart-item handling |
| BB-26 | GET /cart | V | known qty and unit price | subtotal=qty*unit_price | Financial correctness (item level) |
| BB-27 | GET /cart | V | multi-item cart | total=sum(subtotals) | Financial correctness (aggregate) |
| BB-28 | POST /wallet/add | B | amount=0 | 400 + error JSON | Lower wallet boundary |
| BB-29 | POST /wallet/add | B | amount=100001 | 400 + error JSON | Upper wallet boundary |
| BB-30 | POST /wallet/add then GET /profile | V | amount=250 | wallet increases | Valid state update after top-up |
| BB-31 | POST /checkout | I | payment_method='UPI' | 400 + error JSON | Payment method domain validation |
| BB-32 | POST /checkout | M | checkout with empty cart | 400 + error JSON | Empty cart precondition check |
| BB-33 | POST /checkout | B | COD total > 5000 | 400 + error JSON | COD threshold validation |
| BB-34 | POST /checkout | V | payment_method='CARD' | 200 + payment_status=PAID | Payment-state correctness |
| BB-35 | POST /products/{id}/reviews | B | rating=0 | 400 + error JSON | Lower rating boundary |
| BB-36 | POST /products/{id}/reviews | B | rating=6 | 400 + error JSON | Upper rating boundary |
| BB-37 | POST /products/{id}/reviews | B | comment='' | 400 + error JSON | Comment minimum length boundary |
| BB-38 | POST /products/{id}/reviews | B | comment length 201 | 400 + error JSON | Comment maximum length boundary |
| BB-39 | POST /support/ticket | B | short subject | 400 + error JSON | Subject lower boundary |
| BB-40 | POST /support/ticket | B | empty message | 400 + error JSON | Message lower boundary |
| BB-41 | POST /support/ticket | B | subject > 100 chars | 400 + error JSON | Subject upper boundary |
| BB-42 | POST /support/ticket | B | message > 500 chars | 400 + error JSON | Message upper boundary |
| BB-43 | PUT /support/tickets/{id} | I | OPEN->CLOSED | 400 + error JSON | Invalid transition rejection |
| BB-44 | PUT /support/tickets/{id} | V | OPEN->IN_PROGRESS | 200 + updated status | Valid transition acceptance |
| BB-45 | PUT /support/tickets/{id} | V | IN_PROGRESS->CLOSED | 200 + updated status | Final transition validation |

## 6. Detailed Bug Reports (Observed)

### BR-01: Profile accepts non-digit phone

- Endpoint tested: PUT /api/v1/profile
- Request payload:
  - Method: PUT
  - URL: http://127.0.0.1:8080/api/v1/profile
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body: {"name":"Valid Name","phone":"12345abcde"}
- Expected result: 400 error (phone must be exactly 10 digits)
- Actual result observed: 200, {"message":"Profile updated successfully"}

### BR-02: Address creation allows missing pincode

- Endpoint tested: POST /api/v1/addresses
- Request payload:
  - Method: POST
  - URL: http://127.0.0.1:8080/api/v1/addresses
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body: {"label":"HOME","street":"12345 Main Street","city":"Pune"}
- Expected result: 400 error (pincode required, exactly 6 digits)
- Actual result observed: 200 with created address and empty pincode field

### BR-03: Address creation allows short pincode

- Endpoint tested: POST /api/v1/addresses
- Request payload:
  - Method: POST
  - URL: http://127.0.0.1:8080/api/v1/addresses
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body: {"label":"HOME","street":"12345 Main Street","city":"Pune","pincode":"41100","is_default":false}
- Expected result: 400 error (pincode must be 6 digits)
- Actual result observed: 200 with created address

### BR-04: Address creation rejects documented valid pincode length

- Endpoint tested: POST /api/v1/addresses
- Request payload:
  - Method: POST
  - URL: http://127.0.0.1:8080/api/v1/addresses
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body: {"label":"HOME","street":"55 Original Street","city":"Pune","pincode":"411001","is_default":false}
- Expected result: 200 success (valid documented payload)
- Actual result observed: 400, {"error":"Invalid pincode"}

### BR-05: Product schema mismatch for stock field

- Endpoint tested: GET /api/v1/products
- Request payload:
  - Method: GET
  - URL: http://127.0.0.1:8080/api/v1/products
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body: None
- Expected result: each product includes stock field per spec
- Actual result observed: field returned as stock_quantity instead of stock

### BR-06: Cart add accepts non-positive quantities

- Endpoint tested: POST /api/v1/cart/add
- Request payload:
  - Method: POST
  - URL: http://127.0.0.1:8080/api/v1/cart/add
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body A: {"product_id":1,"quantity":0}
  - Body B: {"product_id":1,"quantity":-1}
- Expected result: 400 for both (quantity must be >= 1)
- Actual result observed: 200 for both, {"message":"Item added to cart"}

### BR-07: Cart item subtotal computed incorrectly

- Endpoint tested: GET /api/v1/cart
- Request payload:
  - Method: GET
  - URL: http://127.0.0.1:8080/api/v1/cart
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Setup: added product_id=1 quantity=2 (unit_price=120)
- Expected result: subtotal = 2 * 120 = 240
- Actual result observed: subtotal = -16

### BR-08: Cart total does not equal sum of item subtotals

- Endpoint tested: GET /api/v1/cart
- Request payload:
  - Method: GET
  - URL: http://127.0.0.1:8080/api/v1/cart
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Setup: added product 1 qty 2 and product 2 qty 3
- Expected result: total equals sum of all item subtotals
- Actual result observed: subtotals were -16 and -122 (sum -138), but total returned -16

### BR-09: Review endpoint accepts out-of-range ratings

- Endpoint tested: POST /api/v1/products/{product_id}/reviews
- Request payload:
  - Method: POST
  - URL: http://127.0.0.1:8080/api/v1/products/1/reviews
  - Headers: X-Roll-Number=2024111019, X-User-ID=1
  - Body A: {"rating":0,"comment":"invalid rating"}
  - Body B: {"rating":6,"comment":"invalid rating"}
- Expected result: 400 for both (rating allowed only 1..5)
- Actual result observed: 200 for both, review added successfully

## 7. Conclusion

The black-box suite is comprehensive and satisfies assignment coverage requirements.

Final observed run summary:

- Total: 45
- Passed: 33
- Failed: 12

All 12 failures are mapped to 9 reproducible API defects documented in Section 6.
