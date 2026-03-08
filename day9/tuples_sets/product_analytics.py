from collections import namedtuple


Product = namedtuple("Product", ["id", "name", "category", "price"])

# Sample product catalog -- 16 products across 4 categories, with varying prices.
catalog = [
    # Electronics
    Product(1, "Laptop", "Electronics", 75000),
    Product(2, "Smartphone", "Electronics", 45000),
    Product(3, "Wireless Headphones", "Electronics", 8500),
    Product(4, "Smartwatch", "Electronics", 12000),
    Product(5, "Tablet", "Electronics", 30000),
    # Clothing
    Product(6, "Running Shoes", "Clothing", 3200),
    Product(7, "Denim Jacket", "Clothing", 2800),
    Product(8, "Cotton T-Shirt", "Clothing", 599),
    Product(9, "Formal Trousers", "Clothing", 1800),
    # Books
    Product(10, "Clean Code", "Books", 799),
    Product(11, "Python Crash Course", "Books", 649),
    Product(12, "The Pragmatic Programmer", "Books", 899),
    Product(13, "Designing Data-Intensive Applications", "Books", 1199),
    # Home
    Product(14, "Air Purifier", "Home", 9999),
    Product(15, "Coffee Maker", "Home", 4500),
    Product(16, "Desk Lamp", "Home", 1299),
]

# Quick lookup by id
catalog_by_id = {p.id: p for p in catalog}

# Unpack frequently used products for cart construction
(
    laptop,
    smartphone,
    headphones,
    smartwatch,
    tablet,
    shoes,
    jacket,
    tshirt,
    trousers,
    clean_code,
    python_book,
    pragmatic,
    ddia,
    air_purifier,
    coffee_maker,
    desk_lamp,
) = catalog


# Sample customer carts -- sets of Product namedtuples.
customer_1_cart = {laptop, headphones, clean_code, coffee_maker, tshirt}
customer_2_cart = {smartphone, headphones, python_book, desk_lamp, jacket}
customer_3_cart = {laptop, tablet, headphones, air_purifier, shoes}
customer_4_cart = {smartwatch, headphones, clean_code, coffee_maker, trousers}
customer_5_cart = {laptop, smartphone, headphones, ddia, desk_lamp}

# List of all carts for easy iteration in analyses.
all_carts = [
    customer_1_cart,
    customer_2_cart,
    customer_3_cart,
    customer_4_cart,
    customer_5_cart,
]

# Labels for display purposes.
customer_labels = [
    "Customer 1",
    "Customer 2",
    "Customer 3",
    "Customer 4",
    "Customer 5",
]


# (a) Bestsellers -- products in ALL carts (intersection)
def bestsellers(carts):
    """Products appearing in ALL carts via set intersection."""
    result = carts[0].copy()
    for cart in carts[1:]:
        result = result.intersection(cart)
    return result


#  (b) Catalog reach -- products in ANY cart (union)
def catalog_reach(carts):
    """Products appearing in ANY cart via set union."""
    result = set()
    for cart in carts:
        result = result.union(cart)
    return result


# (c) Exclusive purchases for a target customer -- difference against all others
def exclusive_purchases(target_cart, other_carts):
    """Products only the target customer bought, via set difference against all other carts."""
    others_combined = set()
    for cart in other_carts:
        others_combined = others_combined.union(cart)
    return target_cart.difference(others_combined)


# (d) Recommendations based on community purchases -- union of all carts
def recommend_products(customer_cart, carts):
    """Suggest products the community bought that this customer has not, via set difference."""
    community_purchases = set()
    for cart in carts:
        community_purchases = community_purchases.union(cart)
    return community_purchases.difference(customer_cart)


# (e) Category summary -- dict mapping category to set of product names
def category_summary(products):
    """Return a dict mapping each category to a set of product names, using set comprehension."""
    categories = {p.category for p in products}
    return {
        category: {p.name for p in products if p.category == category}
        for category in categories
    }


# Helper function to format a set of products for display.
def format_product_set(product_set):
    if not product_set:
        return "  (none)"
    lines = []
    for p in sorted(product_set, key=lambda x: x.id):
        lines.append(f"  [{p.id:>2}] {p.name:<40} {p.category:<15} Rs.{p.price:>7,}")
    return "\n".join(lines)


# Main function to run all analyses and print results.
def main():
    separator = "-" * 70

    print(
        "\n+------------------------------------------------------------------------------+"
    )
    print(
        "|                         PRODUCT ANALYTICS TOOL                               |"
    )
    print(
        "+------------------------------------------------------------------------------+\n"
    )

    print("\nFULL PRODUCT CATALOG")
    print(separator)
    print(f"  {'ID':<4} {'Name':<40} {'Category':<15} {'Price (Rs.)'}")
    print(separator)
    for p in catalog:
        print(f"  [{p.id:>2}] {p.name:<40} {p.category:<15} Rs.{p.price:>7,}")

    print("\n\nCUSTOMER CARTS")
    print(separator)
    for label, cart in zip(customer_labels, all_carts):
        names = ", ".join(sorted(p.name for p in cart))
        print(f"  {label}: {names}")

    print("\n\nBESTSELLERS")
    print(separator)
    hits = bestsellers(all_carts)
    print(format_product_set(hits))

    print("\n\nCATALOG REACH")
    print(separator)
    reached = catalog_reach(all_carts)
    print(format_product_set(reached))
    unsold = set(catalog) - reached
    print(
        f"\n  Products never added to any cart: "
        f"{', '.join(p.name for p in unsold) if unsold else 'none'}"
    )

    print("\n\nEXCLUSIVE PURCHASES FOR CUSTOMER 1")
    print(separator)
    others = [c for c in all_carts if c is not customer_1_cart]
    exclusives = exclusive_purchases(customer_1_cart, others)
    print(format_product_set(exclusives))

    print("\n\nPRODUCT RECOMMENDATIONS")
    print(separator)
    for label, cart in zip(customer_labels, all_carts):
        recs = recommend_products(cart, all_carts)
        rec_names = ", ".join(sorted(p.name for p in recs)) if recs else "none"
        print(f"  {label}: {rec_names}")

    print("\n\nCATEGORY SUMMARY")
    print(separator)
    summary = category_summary(catalog)
    for category in sorted(summary):
        names = ", ".join(sorted(summary[category]))
        print(f"  {category}: {{{names}}}")

    print("\n" + "=" * 70)
    print("Analysis complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()