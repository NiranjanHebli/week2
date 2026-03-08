from collections import defaultdict


# PRODUCT CATALOG
# Structure: catalog maps each SKU string to a product dict with name, price, category, stock, rating, and tags

catalog = {
    "SKU001": {
        "name": "Laptop Pro 15",
        "price": 85000,
        "category": "electronics",
        "stock": 12,
        "rating": 4.7,
        "tags": ["computer", "work", "portable"]
    },
    "SKU002": {
        "name": "Wireless Earbuds",
        "price": 4500,
        "category": "electronics",
        "stock": 0,
        "rating": 4.2,
        "tags": ["audio", "wireless", "portable"]
    },
    "SKU003": {
        "name": "Smart TV 55 inch",
        "price": 55000,
        "category": "electronics",
        "stock": 5,
        "rating": 4.5,
        "tags": ["display", "streaming", "home"]
    },
    "SKU004": {
        "name": "Mechanical Keyboard",
        "price": 8500,
        "category": "electronics",
        "stock": 20,
        "rating": 4.6,
        "tags": ["computer", "work", "gaming"]
    },
    "SKU005": {
        "name": "Smartphone X12",
        "price": 62000,
        "category": "electronics",
        "stock": 0,
        "rating": 4.4,
        "tags": ["mobile", "portable", "work"]
    },
    "SKU006": {
        "name": "Cotton Kurta",
        "price": 1200,
        "category": "clothing",
        "stock": 50,
        "rating": 4.1,
        "tags": ["traditional", "cotton", "casual"]
    },
    "SKU007": {
        "name": "Denim Jeans Slim Fit",
        "price": 2500,
        "category": "clothing",
        "stock": 35,
        "rating": 3.9,
        "tags": ["casual", "denim", "everyday"]
    },
    "SKU008": {
        "name": "Formal Blazer",
        "price": 4800,
        "category": "clothing",
        "stock": 0,
        "rating": 4.3,
        "tags": ["formal", "work", "occasion"]
    },
    "SKU009": {
        "name": "Sports Sneakers",
        "price": 3200,
        "category": "clothing",
        "stock": 18,
        "rating": 4.0,
        "tags": ["sports", "casual", "comfortable"]
    },
    "SKU010": {
        "name": "Python Mastery Book",
        "price": 750,
        "category": "books",
        "stock": 100,
        "rating": 4.8,
        "tags": ["programming", "learning", "tech"]
    },
    "SKU011": {
        "name": "The Lean Startup",
        "price": 499,
        "category": "books",
        "stock": 60,
        "rating": 4.5,
        "tags": ["business", "startup", "learning"]
    },
    "SKU012": {
        "name": "Deep Learning Guide",
        "price": 1100,
        "category": "books",
        "stock": 0,
        "rating": 4.7,
        "tags": ["ai", "programming", "tech"]
    },
    "SKU013": {
        "name": "Sapiens",
        "price": 599,
        "category": "books",
        "stock": 45,
        "rating": 4.6,
        "tags": ["history", "science", "popular"]
    },
    "SKU014": {
        "name": "Organic Honey 500g",
        "price": 380,
        "category": "food",
        "stock": 200,
        "rating": 4.3,
        "tags": ["organic", "natural", "healthy"]
    },
    "SKU015": {
        "name": "Arabica Coffee Beans",
        "price": 850,
        "category": "food",
        "stock": 0,
        "rating": 4.6,
        "tags": ["coffee", "premium", "morning"]
    },
    "SKU016": {
        "name": "Mixed Nuts Pack",
        "price": 650,
        "category": "food",
        "stock": 80,
        "rating": 4.2,
        "tags": ["snack", "healthy", "natural"]
    },
    "SKU017": {
        "name": "Green Tea 100 Bags",
        "price": 290,
        "category": "food",
        "stock": 150,
        "rating": 4.0,
        "tags": ["tea", "healthy", "morning"]
    }
}


# Build a tag index using defaultdict, then look up the given tag
def search_by_tag(tag):
    """Search products by a single tag. Returns a dict of matching SKUs and their product details."""
    tag_index = defaultdict(dict)

    for sku, product in catalog.items():
        for t in product.get("tags", []):
            tag_index[t][sku] = product

    return tag_index.get(tag, {})


# Filter catalog using dict comprehension where stock is exactly zero
def out_of_stock():
    """Return all products that are currently out of stock (stock equals 0)."""
    return {
        sku: product
        for sku, product in catalog.items()
        if product.get("stock", 1) == 0
    }


# Guard against None inputs before applying the price filter
def price_range(min_price, max_price):
    """Return products whose price falls inclusively between min_price and max_price."""
    if min_price is None or max_price is None:
        return {}

    return {
        sku: product
        for sku, product in catalog.items()
        if min_price <= product.get("price", 0) <= max_price
    }


# Accumulate prices and ratings per category, then compute averages in one pass
def category_summary():
    """Summarize each category with product count, average price, and average rating."""
    prices_by_cat = defaultdict(list)
    ratings_by_cat = defaultdict(list)

    for product in catalog.values():
        cat = product.get("category", "unknown")
        price = product.get("price")
        rating = product.get("rating")

        if price is not None:
            prices_by_cat[cat].append(price)
        if rating is not None:
            ratings_by_cat[cat].append(rating)

    summary = {}

    for cat in prices_by_cat:
        prices = prices_by_cat[cat]
        ratings = ratings_by_cat[cat]

        avg_price = round(sum(prices) / len(prices), 2) if prices else 0
        avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

        summary[cat] = {
            "count": len(prices),
            "avg_price": avg_price,
            "avg_rating": avg_rating
        }

    return summary


# Compute the price multiplier once, then apply it only to the matching category
def apply_discount(category, percent):
    """Apply a percentage discount to all products in the given category. Returns updated catalog."""
    if not category or percent is None:
        return catalog

    if percent < 0 or percent > 100:
        print("Percent must be between 0 and 100")
        return catalog

    multiplier = 1 - (percent / 100)

    return {
        sku: dict(product, price=round(product.get("price", 0) * multiplier, 2))
        if product.get("category") == category
        else product
        for sku, product in catalog.items()
    }


# Detect conflicts first, then merge with dict unpacking so catalog2 wins on duplicates
def merge_catalogs(catalog1, catalog2):
    """Merge two catalogs into one. Where SKUs clash, catalog2 values take priority."""
    conflicts = [sku for sku in catalog1 if sku in catalog2]

    if conflicts:
        print("Duplicate SKUs found. catalog2 values will overwrite catalog1:")
        for sku in conflicts:
            print("  Conflict on", sku)

    merged = {**catalog1, **catalog2}
    return merged


# DEMO RUNS

def print_section(title):
    print()
    print("=" * 55)
    print(title)
    print("=" * 55)


def print_products(products):
    if not products:
        print("  No products found.")
        return
    for sku, p in products.items():
        name = p.get("name", "Unknown")
        price = p.get("price", 0)
        stock = p.get("stock", 0)
        rating = p.get("rating", 0)
        category = p.get("category", "N/A")
        print(f"  {sku}  {name}")
        print(f"        Category : {category}")
        print(f"        Price    : {price}")
        print(f"        Stock    : {stock}")
        print(f"        Rating   : {rating}")
        print()


if __name__ == "__main__":

    print_section("1. SEARCH BY TAG  portable")
    results = search_by_tag("portable")
    print_products(results)

    print_section("2. OUT OF STOCK PRODUCTS")
    oos = out_of_stock()
    print_products(oos)

    print_section("3. PRICE RANGE  500 to 5000")
    in_range = price_range(500, 5000)
    print_products(in_range)

    print_section("4. CATEGORY SUMMARY")
    summary = category_summary()
    for cat, data in summary.items():
        print(f"  {cat}")
        print(f"    count      : {data.get('count')}")
        print(f"    avg price  : {data.get('avg_price')}")
        print(f"    avg rating : {data.get('avg_rating')}")
        print()

    print_section("5. APPLY DISCOUNT  10 percent off books")
    discounted = apply_discount("books", 10)
    books_only = {
        sku: p
        for sku, p in discounted.items()
        if p.get("category") == "books"
    }
    print_products(books_only)

    print_section("6. MERGE CATALOGS")
    extra_catalog = {
        "SKU018": {
            "name": "USB C Hub",
            "price": 3200,
            "category": "electronics",
            "stock": 25,
            "rating": 4.3,
            "tags": ["computer", "portable", "work"]
        },
        "SKU001": {
            "name": "Laptop Pro 15 Version 2",
            "price": 87000,
            "category": "electronics",
            "stock": 8,
            "rating": 4.8,
            "tags": ["computer", "work", "portable"]
        }
    }
    merged = merge_catalogs(catalog, extra_catalog)
    print(f"  Total products after merge : {len(merged)}")
    print()
    print("  Updated SKU001 after merge :")
    sku001 = merged.get("SKU001", {})
    print(f"    name  : {sku001.get('name')}")
    print(f"    price : {sku001.get('price')}")