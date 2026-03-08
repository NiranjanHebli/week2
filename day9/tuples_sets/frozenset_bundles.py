import timeit
from collections import namedtuple
"""
 1. WHAT IS FROZENSET?

 A frozenset is an immutable version of a Python set. Like a regular set, it
 stores unique, unordered elements and supports the full range of set
 operations (union, intersection, difference, etc.). The key distinction is
 that once a frozenset is created it cannot be modified -- you cannot add,
 remove, or update its elements.

 set vs frozenset
 ----------------
 set:
   - Mutable: supports .add(), .remove(), .discard(), .update(), etc.
   - Unhashable: cannot be used as a dictionary key or placed inside another set.
   - Use when you need a collection that changes over time.

 frozenset:
   - Immutable: no mutation methods available after creation.
   - Hashable: can be used as a dictionary key or as an element of another set.
   - Use when the collection must be fixed and you need it to act as a key
     or to be stored inside another set.

 When to use frozenset in real systems
 --------------------------------------
 1. Dictionary keys that represent combinations -- e.g. bundle deals, feature
    flags, permission groups -- where the combination itself is the lookup key.
 2. Caching / memoisation: pass a frozenset of arguments as a cache key since
    regular sets are unhashable and cannot be cached.
 3. Graph algorithms: represent edges or node groups as frozensets so they can
    be stored in sets of edges without duplication.
 4. Configuration management: store a fixed set of allowed roles or tags per
    resource and compare against user-supplied sets at runtime.
 5. Database query building: represent a fixed set of selected columns or
    filter conditions that must not change mid-query.
"""
Product = namedtuple("Product", ["id", "name", "category", "price"])

catalog = [
    Product(1, "Laptop", "Electronics", 75000),
    Product(2, "Smartphone", "Electronics", 45000),
    Product(3, "Wireless Headphones", "Electronics", 8500),
    Product(4, "Smartwatch", "Electronics", 12000),
    Product(5, "Tablet", "Electronics", 30000),
    Product(6, "Running Shoes", "Clothing", 3200),
    Product(7, "Denim Jacket", "Clothing", 2800),
    Product(8, "Cotton T-Shirt", "Clothing", 599),
    Product(9, "Formal Trousers", "Clothing", 1800),
    Product(10, "Clean Code", "Books", 799),
    Product(11, "Python Crash Course", "Books", 649),
    Product(12, "The Pragmatic Programmer", "Books", 899),
    Product(13, "Designing Data-Intensive Applications", "Books", 1199),
    Product(14, "Air Purifier", "Home", 9999),
    Product(15, "Coffee Maker", "Home", 4500),
    Product(16, "Desk Lamp", "Home", 1299),
]

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


 # Bundle discounts defined as frozensets of categories mapping to discount percentages.
bundle_discounts = {
    frozenset({"Electronics", "Books"}): 10, #  tech + learning
    frozenset({"Electronics", "Home"}): 12,  # smart home setup
    frozenset({"Clothing", "Books"}): 8,  # lifestyle bundle
    frozenset({"Electronics", "Clothing"}): 7,  # wearable tech
    frozenset({"Books", "Home"}): 6,  # work-from-home
    frozenset({"Electronics", "Books", "Home"}): 18,  # premium bundle
    frozenset({"Electronics", "Clothing", "Books"}): 15,  # student bundle
}


# Check if a cart qualifies for any bundle discount by comparing the cart's
def check_bundle_discount(cart):
    """Given a set of Product namedtuples representing a customer's cart, determine
    which bundle discounts apply based on the categories of products in the cart.
    Returns a dict with matched bundles, best discount, and other details for display.
    """
    cart_categories = frozenset(p.category for p in cart)

    matched_bundles = []
    for bundle, discount in bundle_discounts.items():
        # A bundle matches when every category it requires is present in cart.
        if bundle.issubset(cart_categories):
            matched_bundles.append((bundle, discount))

    # Sort matched bundles by discount descending for clean display.
    matched_bundles.sort(key=lambda x: x[1], reverse=True)

    if matched_bundles:
        best_bundle, best_discount = matched_bundles[0]
    else:
        best_bundle, best_discount = None, 0

    return {
        "cart_categories": cart_categories,
        "matched_bundles": matched_bundles,
        "best_discount": best_discount,
        "best_bundle": best_bundle,
    }


# Sample customers for testing the bundle checker and performance benchmark.
def apply_discount(cart, discount_pct):
    """Return the total cart value after applying a percentage discount."""
    total = sum(p.price for p in cart)
    saving = total * discount_pct / 100
    return total, saving, total - saving


#  Sample customers for testing the bundle checker and performance benchmark.
ITERATIONS = 100_000

SET_STMT = "s = set(['Electronics', 'Books', 'Home', 'Clothing'])"
FROZENSET_STMT = "fs = frozenset(['Electronics', 'Books', 'Home', 'Clothing'])"

# Also benchmark using a frozenset as a dict key (only possible with frozenset)
FROZENSET_KEY_STMT = """
d = {frozenset(['Electronics', 'Books']): 10}
_ = d[frozenset(['Electronics', 'Books'])]
"""

# Sample customer carts for testing the bundle checker and performance benchmark.
def run_benchmark():
    """Run timeit comparisons and return results as a dict."""
    set_time = timeit.timeit(SET_STMT, number=ITERATIONS)
    frozenset_time = timeit.timeit(FROZENSET_STMT, number=ITERATIONS)
    key_time = timeit.timeit(FROZENSET_KEY_STMT, number=ITERATIONS)

    return {
        "set_total": set_time,
        "frozenset_total": frozenset_time,
        "frozenset_key_total": key_time,
        "set_per_call_us": (set_time / ITERATIONS) * 1_000_000,
        "frozenset_per_call_us": (frozenset_time / ITERATIONS) * 1_000_000,
        "key_per_call_us": (key_time / ITERATIONS) * 1_000_000,
        "difference_pct": abs(set_time - frozenset_time) / set_time * 100,
        "faster": "frozenset" if frozenset_time < set_time else "set",
    }


# format a frozenset of categories for display (e.g. {"Books", "Electronics"})

def fmt_categories(fset):
    return "{" + ", ".join(sorted(fset)) + "}"


# Helper function to format bundle check results for display.
def print_bundle_result(label, cart, result):
    separator = "-" * 68
    total, saving, final = apply_discount(cart, result["best_discount"])

    print(f"\n  {label}")
    print(f"  Cart categories : {fmt_categories(result['cart_categories'])}")

    if result["matched_bundles"]:
        print(f"  Matched bundles :")
        for bundle, disc in result["matched_bundles"]:
            print(f"    {fmt_categories(bundle):<45} {disc}% off")
        print(
            f"  Best discount   : {result['best_discount']}%"
            f"  (bundle: {fmt_categories(result['best_bundle'])})"
        )
        print(f"  Cart total      : Rs.{total:>8,}")
        print(f"  You save        : Rs.{saving:>8,.0f}")
        print(f"  Final price     : Rs.{final:>8,.0f}")
    else:
        print(f"  No bundle discount applies.")
        print(f"  Cart total      : Rs.{total:>8,}")

    print(f"  {separator}")


# main function to run all analyses and print results.
def main():
    separator = "=" * 70

    print("\n" + separator)
    print("  FROZENSET BUNDLE DISCOUNT SYSTEM")
    print(separator)

    # Display defined bundles and their discounts.
    print("\nDEFINED BUNDLE DISCOUNTS")
    print("-" * 68)
    print(f"  {'Bundle (categories)':<48} {'Discount'}")
    print("-" * 68)
    for bundle, disc in sorted(bundle_discounts.items(), key=lambda x: x[1]):
        print(f"  {fmt_categories(bundle):<48} {disc}%")

    # Sample carts to test the bundle checker with various category combinations.
    sample_carts = [
        ("Cart A -- Electronics + Books", {laptop, clean_code, python_book}),
        (
            "Cart B -- Electronics + Home",
            {smartphone, headphones, coffee_maker, desk_lamp},
        ),
        (
            "Cart C -- Electronics + Books + Home (premium)",
            {tablet, pragmatic, air_purifier},
        ),
        (
            "Cart D -- Electronics + Clothing + Books (student)",
            {smartwatch, tshirt, ddia},
        ),
        ("Cart E -- Clothing only (no bundle)", {shoes, jacket, trousers}),
        ("Cart F -- All four categories", {laptop, tshirt, clean_code, coffee_maker}),
    ]

    print("\n\nBUNDLE DISCOUNT CHECKER RESULTS")
    print("-" * 68)
    for label, cart in sample_carts:
        result = check_bundle_discount(cart)
        print_bundle_result(label, cart, result)

    #  Performance benchmark for set vs frozenset creation speed
    print("\nPERFORMANCE BENCHMARK -- set vs frozenset")
    print(f"Iterations: {ITERATIONS:,}")
    print("-" * 68)
    print("Running benchmark, please wait...")

    bm = run_benchmark()

    print(f"\n  Operation                              Total (s)    Per call (us)")
    print(f"  {'-'*64}")
    print(
        f"  set creation                          "
        f"  {bm['set_total']:>8.4f}        {bm['set_per_call_us']:>8.4f}"
    )
    print(
        f"  frozenset creation                    "
        f"  {bm['frozenset_total']:>8.4f}        {bm['frozenset_per_call_us']:>8.4f}"
    )
    print(
        f"  frozenset as dict key (create+lookup) "
        f"  {bm['frozenset_key_total']:>8.4f}        {bm['key_per_call_us']:>8.4f}"
    )
    print(
        f"\n  Speed difference (creation): {bm['difference_pct']:.2f}%"
        f"     -- {bm['faster']} is faster to create"
    )
    print(f"\n  Note: set cannot be used as a dict key (unhashable).")
    print(f"  frozenset enables the entire bundle lookup pattern above.")

    print("\n" + separator)
    print("  Analysis complete.")
    print(separator + "\n")


if __name__ == "__main__":
    main()
