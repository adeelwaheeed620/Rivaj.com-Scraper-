import requests
import json
import math

# 1️⃣ List of available categories (56+58 cleaned):
categories = [
    # (list all 58 slug strings)
    "blush-on", "bundle", "cleanser", "concealer", "contour", "contour-hd",
    "developer", "blonder", "eye-brows", "eye-care", "eye-lashes",
    "eye-liner", "eye-palette", "eye-pencil", "lip-eye-pencil",
    "eye-shadow", "eyes-accessories", "face-accessories", "face-serum",
    "fixer", "foundation", "gel", "cream", "gift", "hair-accessories",
    "hair-color", "hair-comb", "hair-oil", "hair-serum", "hair-spray",
    "hand-mask", "hands-accessories", "highlighter", "kajal", "lip-care",
    "lip-gloss", "lip-pencil", "lipstick", "makeup-brush", "makeup-fixer",
    "makeup-remover", "mascara", "mask", "men-perfume", "women-perfume",
    "unisex-perfume", "nail-polish", "nail-polish-remover", "nails",
    "oral-care", "pedicure-kit", "powder", "primer", "razor", "scrub",
    "sunblock", "wax", "strips"
]

# Show the menu
print("Available Categories:")
for idx, slug in enumerate(categories, start=1):
    print(f"{idx}. {slug.replace('-', ' ').title()}")

try:
    choice = int(input("\nEnter category number: "))
    slug = categories[choice - 1]
except Exception:
    print("Invalid choice! Please run again.")
    exit()

print(f"\n🔍 Scraping '{slug}' category...")

# 2️⃣ Fetch all products via Shopify JSON
products = []
limit = 250  # Shopify maximum products per page
page = 1

while True:
    url = (f"https://rivaj-uk.com/collections/{slug}/products.json"
           f"?page={page}&limit={limit}")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json().get("products", [])
    if not data:
        break

    for p in data:
        variant = p.get("variants", [{}])[0]
        products.append({
            "name": p.get("title", ""),
            "original_price": f"Rs.{variant.get('compare_at_price', variant.get('price', ''))}",
            "sale_price": f"Rs.{variant.get('price', '')}",
            "url": f"https://rivaj-uk.com/products/{p.get('handle', '')}"
        })
    page += 1

print(f"✅ Total products found: {len(products)}")

# 3️⃣ Save results
filename = f"{slug}_products.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"📦 Saved output to {filename}")