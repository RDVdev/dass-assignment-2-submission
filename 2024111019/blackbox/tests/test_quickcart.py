"""Rigorous black-box API tests for QuickCart based only on the published API contract."""

import os

import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    """Return base URL for QuickCart API."""
    return os.getenv("QUICKCART_BASE_URL", "http://127.0.0.1:8080/api/v1")


@pytest.fixture(scope="session")
def roll_number():
    """Return roll number used in test headers."""
    return os.getenv("QUICKCART_ROLL", "2024111019")


@pytest.fixture(scope="session")
def request_timeout():
    """Central timeout so all tests use the same request budget."""
    return 10


@pytest.fixture(scope="session")
def admin_headers(roll_number):
    """Headers for admin-scoped endpoints."""
    return {"X-Roll-Number": roll_number}


@pytest.fixture(scope="session")
def user_id(base_url, admin_headers, request_timeout):
    """Pick an existing user_id from admin users list."""
    response = requests.get(
        f"{base_url}/admin/users", headers=admin_headers, timeout=request_timeout
    )
    response.raise_for_status()
    users = response.json()
    if not users:
        raise RuntimeError("No users found in QuickCart dataset.")
    return users[0]["user_id"]


@pytest.fixture(scope="session")
def user_headers(admin_headers, user_id):
    """Headers for user-scoped endpoints."""
    headers = dict(admin_headers)
    headers["X-User-ID"] = str(user_id)
    return headers


@pytest.fixture(scope="session")
def active_products(base_url, user_headers, request_timeout):
    """Fetch active products once for stable product-based tests."""
    response = requests.get(f"{base_url}/products", headers=user_headers, timeout=request_timeout)
    response.raise_for_status()
    products = response.json()
    if len(products) < 2:
        raise RuntimeError("Need at least two active products for cart coverage.")
    return products


@pytest.fixture(autouse=True)
def ensure_clean_cart(base_url, user_headers, request_timeout):
    """Clear cart before each test for stable black-box assertions."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers, timeout=request_timeout)


PROFILE_KEYS = {
    "user_id",
    "name",
    "email",
    "phone",
    "wallet_balance",
    "loyalty_points",
}

PRODUCT_KEYS = {"product_id", "name", "price", "category", "stock", "is_active"}


def assert_error_response(response, expected_status):
    """Validate common error-response structure for negative tests."""
    assert response.status_code == expected_status
    body = response.json()
    assert isinstance(body, dict)
    assert "error" in body


def add_to_cart(base_url, user_headers, request_timeout, product_id, quantity):
    """Helper for cart setup in pricing and checkout scenarios."""
    return requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": product_id, "quantity": quantity},
        timeout=request_timeout,
    )


def update_cart(base_url, user_headers, request_timeout, product_id, quantity):
    """Helper for exercising cart update validations."""
    return requests.post(
        f"{base_url}/cart/update",
        headers=user_headers,
        json={"product_id": product_id, "quantity": quantity},
        timeout=request_timeout,
    )


def get_cart(base_url, user_headers, request_timeout):
    """Fetch cart and assert success for follow-up assertions."""
    response = requests.get(f"{base_url}/cart", headers=user_headers, timeout=request_timeout)
    assert response.status_code == 200
    return response.json()


def create_address(base_url, user_headers, request_timeout, payload):
    """Create address and return created address object."""
    response = requests.post(
        f"{base_url}/addresses",
        headers=user_headers,
        json=payload,
        timeout=request_timeout,
    )
    assert response.status_code == 200
    body = response.json()
    assert "address" in body
    return body["address"]


def create_support_ticket(base_url, user_headers, request_timeout, subject, message):
    """Create a ticket and return its id for workflow tests."""
    response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": subject, "message": message},
        timeout=request_timeout,
    )
    assert response.status_code == 200
    body = response.json()
    assert "ticket_id" in body
    return body["ticket_id"]


def get_product_stock(product):
    """Return stock field value across possible API field names."""
    if "stock" in product:
        return product["stock"]
    if "stock_quantity" in product:
        return product["stock_quantity"]
    raise AssertionError("Product payload missing both stock and stock_quantity fields")


def test_missing_roll_header_returns_401(base_url, request_timeout):
    response = requests.get(f"{base_url}/admin/users", timeout=request_timeout)
    assert_error_response(response, 401)


def test_invalid_roll_header_returns_400(base_url, request_timeout):
    response = requests.get(
        f"{base_url}/admin/users",
        headers={"X-Roll-Number": "invalid-roll"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_missing_user_header_on_user_endpoint(base_url, admin_headers, request_timeout):
    response = requests.get(
        f"{base_url}/profile", headers=admin_headers, timeout=request_timeout
    )
    assert_error_response(response, 400)


@pytest.mark.parametrize(
    "candidate_user_id", ["abc", "0", "-3"], ids=["nondigit", "zero", "negative"]
)
def test_invalid_user_header_on_user_endpoint(
    base_url, admin_headers, request_timeout, candidate_user_id
):
    headers = dict(admin_headers)
    headers["X-User-ID"] = candidate_user_id
    response = requests.get(f"{base_url}/profile", headers=headers, timeout=request_timeout)
    assert_error_response(response, 400)


def test_profile_get_valid_structure(base_url, user_headers, request_timeout):
    response = requests.get(f"{base_url}/profile", headers=user_headers, timeout=request_timeout)
    assert response.status_code == 200
    body = response.json()
    assert PROFILE_KEYS.issubset(body.keys())
    assert isinstance(body["user_id"], int)
    assert isinstance(body["name"], str) and body["name"].strip()
    assert isinstance(body["email"], str) and "@" in body["email"]
    assert isinstance(body["phone"], str)


@pytest.mark.parametrize(
    ("payload", "case_name"),
    [
        ({"name": "A", "phone": "1234567890"}, "name too short"),
        ({"name": "Valid Name", "phone": "12345"}, "phone too short"),
        ({"name": "Valid Name", "phone": "12345abcde"}, "phone has non-digits"),
    ],
    ids=["short-name", "short-phone", "nondigit-phone"],
)
def test_profile_update_rejects_invalid_payloads(
    base_url, user_headers, request_timeout, payload, case_name
):
    response = requests.put(
        f"{base_url}/profile",
        headers=user_headers,
        json=payload,
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_address_create_missing_pincode_rejected(base_url, user_headers, request_timeout):
    response = requests.post(
        f"{base_url}/addresses",
        headers=user_headers,
        json={"label": "HOME", "street": "12345 Main Street", "city": "Pune"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


@pytest.mark.parametrize(
    ("payload", "case_name"),
    [
        (
            {
                "label": "WORK",
                "street": "12345 Main Street",
                "city": "Pune",
                "pincode": "411001",
                "is_default": False,
            },
            "invalid label",
        ),
        (
            {
                "label": "HOME",
                "street": "12345 Main Street",
                "city": "Pune",
                "pincode": "41100",
                "is_default": False,
            },
            "short pincode",
        ),
    ],
    ids=["invalid-label", "short-pincode"],
)
def test_address_create_rejects_invalid_payloads(
    base_url, user_headers, request_timeout, payload, case_name
):
    response = requests.post(
        f"{base_url}/addresses",
        headers=user_headers,
        json=payload,
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_address_update_rejects_attempt_to_modify_label_city_or_pincode(
    base_url, user_headers, request_timeout
):
    created = create_address(
        base_url,
        user_headers,
        request_timeout,
        {
            "label": "HOME",
            "street": "55 Original Street",
            "city": "Pune",
            "pincode": "411001",
            "is_default": False,
        },
    )

    response = requests.put(
        f"{base_url}/addresses/{created['address_id']}",
        headers=user_headers,
        json={
            "label": "OFFICE",
            "city": "Mumbai",
            "pincode": "400001",
            "street": "77 Updated Street",
            "is_default": True,
        },
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_address_create_default_keeps_only_one_default(base_url, user_headers, request_timeout):
    first = create_address(
        base_url,
        user_headers,
        request_timeout,
        {
            "label": "HOME",
            "street": "11 First Default Street",
            "city": "Pune",
            "pincode": "411001",
            "is_default": True,
        },
    )
    second = create_address(
        base_url,
        user_headers,
        request_timeout,
        {
            "label": "OFFICE",
            "street": "22 Second Default Street",
            "city": "Pune",
            "pincode": "411002",
            "is_default": True,
        },
    )

    addresses_response = requests.get(
        f"{base_url}/addresses", headers=user_headers, timeout=request_timeout
    )
    assert addresses_response.status_code == 200
    addresses = addresses_response.json()
    defaults = [address for address in addresses if address["is_default"]]
    assert len(defaults) == 1
    assert defaults[0]["address_id"] == second["address_id"]
    assert first["address_id"] != second["address_id"]


def test_products_returns_active_products_with_expected_fields(
    base_url, user_headers, request_timeout
):
    response = requests.get(f"{base_url}/products", headers=user_headers, timeout=request_timeout)
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert products
    for product in products:
        assert PRODUCT_KEYS.issubset(product.keys())
        assert product["is_active"] is True
        assert product["price"] >= 0


def test_product_lookup_nonexistent_id_returns_404(base_url, user_headers, request_timeout):
    response = requests.get(
        f"{base_url}/products/999999",
        headers=user_headers,
        timeout=request_timeout,
    )
    assert_error_response(response, 404)


def test_cart_add_with_nonexistent_product_returns_404(
    base_url, user_headers, request_timeout
):
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers,
        json={"product_id": 999999, "quantity": 1},
        timeout=request_timeout,
    )
    assert_error_response(response, 404)


@pytest.mark.parametrize("quantity", [0, -1], ids=["zero", "negative"])
def test_cart_add_rejects_non_positive_quantities(
    base_url, user_headers, request_timeout, active_products, quantity
):
    response = add_to_cart(
        base_url,
        user_headers,
        request_timeout,
        active_products[0]["product_id"],
        quantity,
    )
    assert_error_response(response, 400)


def test_cart_add_rejects_quantity_above_stock(
    base_url, user_headers, request_timeout, active_products
):
    product = next((item for item in active_products if get_product_stock(item) > 0), None)
    if product is None:
        pytest.skip("No in-stock product available for stock-boundary check")

    product_stock = get_product_stock(product)
    response = add_to_cart(
        base_url,
        user_headers,
        request_timeout,
        product["product_id"],
        product_stock + 1,
    )
    assert_error_response(response, 400)


def test_cart_add_same_product_accumulates_quantity(
    base_url, user_headers, request_timeout, active_products
):
    product_id = active_products[0]["product_id"]

    first = add_to_cart(base_url, user_headers, request_timeout, product_id, 2)
    second = add_to_cart(base_url, user_headers, request_timeout, product_id, 3)
    assert first.status_code == 200
    assert second.status_code == 200

    cart = get_cart(base_url, user_headers, request_timeout)
    item = next(item for item in cart["items"] if item["product_id"] == product_id)
    assert item["quantity"] == 5


@pytest.mark.parametrize("quantity", [0, -2], ids=["zero", "negative"])
def test_cart_update_rejects_non_positive_quantities(
    base_url, user_headers, request_timeout, active_products, quantity
):
    product_id = active_products[0]["product_id"]
    assert add_to_cart(base_url, user_headers, request_timeout, product_id, 2).status_code == 200

    response = update_cart(
        base_url, user_headers, request_timeout, product_id=product_id, quantity=quantity
    )
    assert_error_response(response, 400)


def test_cart_remove_nonexistent_item_returns_404(base_url, user_headers, request_timeout):
    response = requests.post(
        f"{base_url}/cart/remove",
        headers=user_headers,
        json={"product_id": 999999},
        timeout=request_timeout,
    )
    assert_error_response(response, 404)


def test_cart_subtotal_equals_qty_times_unit_price(
    base_url, user_headers, request_timeout, active_products
):
    product_id = active_products[0]["product_id"]

    add_response = add_to_cart(base_url, user_headers, request_timeout, product_id, 2)
    assert add_response.status_code == 200

    cart = get_cart(base_url, user_headers, request_timeout)
    item = next(item for item in cart["items"] if item["product_id"] == product_id)
    assert item["subtotal"] == item["quantity"] * item["unit_price"]


def test_cart_total_equals_sum_of_all_subtotals(
    base_url, user_headers, request_timeout, active_products
):
    first_product_id = active_products[0]["product_id"]
    second_product_id = active_products[1]["product_id"]

    assert add_to_cart(
        base_url, user_headers, request_timeout, first_product_id, 2
    ).status_code == 200
    assert add_to_cart(
        base_url, user_headers, request_timeout, second_product_id, 3
    ).status_code == 200

    cart = get_cart(base_url, user_headers, request_timeout)
    expected_total = sum(item["subtotal"] for item in cart["items"])
    assert cart["total"] == expected_total


@pytest.mark.parametrize("amount", [0, 100001], ids=["zero", "above-max"])
def test_wallet_add_rejects_out_of_range_amounts(
    base_url, user_headers, request_timeout, amount
):
    response = requests.post(
        f"{base_url}/wallet/add",
        headers=user_headers,
        json={"amount": amount},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_wallet_add_valid_amount_increases_balance(base_url, user_headers, request_timeout):
    profile_before = requests.get(
        f"{base_url}/profile", headers=user_headers, timeout=request_timeout
    )
    assert profile_before.status_code == 200
    balance_before = profile_before.json()["wallet_balance"]

    top_up_response = requests.post(
        f"{base_url}/wallet/add",
        headers=user_headers,
        json={"amount": 250},
        timeout=request_timeout,
    )
    assert top_up_response.status_code == 200

    profile_after = requests.get(
        f"{base_url}/profile", headers=user_headers, timeout=request_timeout
    )
    assert profile_after.status_code == 200
    balance_after = profile_after.json()["wallet_balance"]
    assert balance_after >= balance_before + 250


def test_checkout_rejects_invalid_payment_method(
    base_url, user_headers, request_timeout, active_products
):
    add_response = add_to_cart(
        base_url, user_headers, request_timeout, active_products[0]["product_id"], 1
    )
    assert add_response.status_code == 200

    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "UPI"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_checkout_rejects_empty_cart(base_url, user_headers, request_timeout):
    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_checkout_cod_rejects_order_above_5000(
    base_url, user_headers, request_timeout, active_products
):
    candidate = None
    for product in sorted(active_products, key=lambda item: item["price"], reverse=True):
        product_stock = get_product_stock(product)
        if product_stock <= 0 or product["price"] <= 0:
            continue
        quantity = min(product_stock, int(5000 // product["price"]) + 1)
        if quantity >= 1 and (product["price"] * quantity) > 5000:
            candidate = (product["product_id"], quantity)
            break

    if candidate is None:
        pytest.skip("Dataset cannot build cart total above COD threshold")

    product_id, quantity = candidate
    add_response = add_to_cart(base_url, user_headers, request_timeout, product_id, quantity)
    assert add_response.status_code == 200

    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "COD"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_checkout_card_sets_paid_status(
    base_url, user_headers, request_timeout, active_products
):
    add_response = add_to_cart(
        base_url, user_headers, request_timeout, active_products[0]["product_id"], 1
    )
    assert add_response.status_code == 200

    response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
        timeout=request_timeout,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["payment_status"] == "PAID"


@pytest.mark.parametrize("rating", [0, 6], ids=["too-low", "too-high"])
def test_review_rejects_rating_outside_allowed_range(
    base_url, user_headers, request_timeout, active_products, rating
):
    response = requests.post(
        f"{base_url}/products/{active_products[0]['product_id']}/reviews",
        headers=user_headers,
        json={"rating": rating, "comment": f"invalid rating {rating}"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


@pytest.mark.parametrize(
    "comment",
    ["", "x" * 201],
    ids=["empty-comment", "comment-too-long"],
)
def test_review_rejects_comment_outside_allowed_range(
    base_url, user_headers, request_timeout, active_products, comment
):
    response = requests.post(
        f"{base_url}/products/{active_products[0]['product_id']}/reviews",
        headers=user_headers,
        json={"rating": 4, "comment": comment},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


@pytest.mark.parametrize(
    ("subject", "message"),
    [
        ("Help", "valid body"),
        ("Valid subject", ""),
        ("S" * 101, "valid body"),
        ("Valid subject", "M" * 501),
    ],
    ids=["short-subject", "empty-message", "subject-too-long", "message-too-long"],
)
def test_support_ticket_creation_rejects_invalid_lengths(
    base_url, user_headers, request_timeout, subject, message
):
    response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers,
        json={"subject": subject, "message": message},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_support_ticket_transition_open_to_closed_rejected(
    base_url, user_headers, request_timeout
):
    ticket_id = create_support_ticket(
        base_url,
        user_headers,
        request_timeout,
        "Need help with order",
        "Please check order 1",
    )

    response = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=request_timeout,
    )
    assert_error_response(response, 400)


def test_support_ticket_transition_open_to_in_progress_allowed(
    base_url, user_headers, request_timeout
):
    ticket_id = create_support_ticket(
        base_url,
        user_headers,
        request_timeout,
        "Need support quickly",
        "Issue in checkout",
    )

    response = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=request_timeout,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_support_ticket_transition_in_progress_to_closed_allowed(
    base_url, user_headers, request_timeout
):
    ticket_id = create_support_ticket(
        base_url,
        user_headers,
        request_timeout,
        "Escalating ongoing issue",
        "Status transition test",
    )

    first = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=request_timeout,
    )
    assert first.status_code == 200

    second = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=request_timeout,
    )
    assert second.status_code == 200
    assert second.json()["status"] == "CLOSED"
