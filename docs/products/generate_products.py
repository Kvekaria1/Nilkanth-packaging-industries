#!/usr/bin/env python3
"""Generate static product catalogue and detail pages from catalog.json."""

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
CATALOG_FILE = PRODUCTS / "catalog.json"
PHONE = "+919428526059"
EMAIL = "nilkanthpackaging09@gmail.com"
WHATSAPP = "919428526059"
ACCENT = "#b63338"


def escape(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_catalog():
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    seen = set()
    for category in catalog["categories"]:
        for product in category["products"]:
            slug = slugify(product)
            if slug in seen:
                raise ValueError(f"Duplicate product slug: {slug}")
            seen.add(slug)
    return catalog


def photo(catalog, filename):
    return catalog["photos"][filename]


def photo_path(filename, depth):
    return "../" * depth + "images/products/" + filename


def product_link(product, depth):
    if depth == 0:
        return "products/" + slugify(product) + "/"
    return "../" * (depth - 1) + slugify(product) + "/"


def category_link(category, depth):
    if depth == 0:
        return "products/index.html#" + category["slug"]
    return "../" * (depth - 1) + "index.html#" + category["slug"]


def category_icon(index):
    shapes = [
        '<path d="m3 8 9-5 9 5-9 5zM3 8v9l9 5 9-5V8M12 13v9"/>',
        '<path d="m3 8 9-5 9 5-9 5zM3 8v9l9 5 9-5V8M12 13v9M7 6l10 5"/>',
        '<path d="M3 7c3-5 6 5 9 0s6 5 9 0M3 12c3-5 6 5 9 0s6 5 9 0M3 17c3-5 6 5 9 0s6 5 9 0"/>',
        '<path d="M4 4h16v16H4zM8 8h8M8 12h8M8 16h5"/>',
        '<path d="m4 5 16-2-2 16-15 2zM7 17l10-10"/>',
        '<path d="M4 4h16v4H4zM4 10h16v4H4zM4 16h16v4H4z"/>',
        '<path d="M3 4h18v16H3zM12 4v16M3 12h18"/>',
        '<path d="M3 10h18v10H3zM2 10l10-7 10 7M8 20v-6h8v6"/>',
        '<path d="M3 21V10l6 3V8l6 4V5h6v16zM17 8h1"/>',
        '<path d="M20 4C10 4 5 8 5 14a6 6 0 0 0 6 6c6 0 9-6 9-16ZM4 21c3-5 7-8 12-11"/>',
    ]
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shapes[index]}</svg>'
    )


def mega_menu(catalog, depth):
    groups = []
    for index in range(0, len(catalog["categories"]), 2):
        pair = catalog["categories"][index:index + 2]
        chunks = []
        for category in pair:
            category_index = catalog["categories"].index(category)
            links = "".join(
                f'<a href="{escape(product_link(product, depth))}">{escape(product)}</a>'
                for product in category["products"]
            )
            chunks.append(
                '<section class="mega-group">'
                f'<h3><span class="mega-icon">{category_icon(category_index)}</span><a href="{escape(category_link(category, depth))}">'
                f'{escape(category["name"])}</a></h3>'
                f'<p>{escape(category["description"])}</p>{links}</section>'
            )
        groups.append('<div class="mega-column">' + "".join(chunks) + "</div>")
    return "".join(groups)


def header(catalog, depth):
    prefix = "../" * depth
    return f"""
<div class="topline"><div class="shell topline-inner">
  <span>Vapi, Gujarat, India <span class="dot">/</span> Corrugated packaging manufacturer</span>
  <span><a href="tel:{PHONE}">+91 94285 26059</a><span class="dot">/</span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></div>
<header class="site-header"><div class="shell nav-inner">
  <a class="brand" href="{prefix}index.html" aria-label="Nilkanth Packaging Industries home">
    <img src="{prefix}images/nilkanth-logo.png" alt="Nilkanth Packaging Industries logo"><span>Packaging Industries<small>Vapi, Gujarat</small></span>
  </a>
  <nav aria-label="Main navigation">
    <a class="nav-link" href="{prefix}index.html">Home</a>
    <div class="nav-products"><a class="nav-link" href="{prefix}products/index.html">Products <span aria-hidden="true">⌄</span></a>
      <div class="mega" aria-label="Product categories">{mega_menu(catalog, depth)}</div>
    </div>
    <a class="nav-link" href="{prefix}index.html#why">Why Nilkanth</a>
    <a class="nav-cta" href="{prefix}products/index.html#quote">Request a Quote</a>
  </nav>
</div></header>"""


def page_styles():
    return """
<style>
:root{{--ink:#20282d;--muted:#66727a;--line:#e4e8e9;--paper:#f5f6f5;--red:__ACCENT__;--red-dark:#8f252b;--green:#294e43;--white:#fff;--gold:#c7a86c}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;color:var(--ink);background:var(--white);font:16px/1.65 Inter,Arial,sans-serif}}a{{color:inherit;text-decoration:none}}img{{max-width:100%}}h1,h2,h3{{font-family:"Space Grotesk",Inter,Arial,sans-serif;line-height:1.13;letter-spacing:-.025em;margin:0 0 14px}}h1{{font-size:clamp(2.2rem,4vw,3.8rem)}}h2{{font-size:clamp(1.7rem,3vw,2.5rem)}}h3{{font-size:1.2rem}}p{{margin:0 0 16px}}.shell{{width:min(1200px,calc(100% - 48px));margin:auto}}.topline{{background:#20282d;color:#e2e5e6;font-size:12px}}.topline-inner{{min-height:36px;display:flex;justify-content:space-between;align-items:center;gap:12px}}.topline a:hover{{color:#fff}}.dot{{padding:0 9px;color:#859095}}.site-header{{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line)}}.nav-inner{{height:78px;display:flex;align-items:center;justify-content:space-between;gap:30px}}.brand{{display:flex;align-items:center;gap:12px;color:#243037;font-weight:800;letter-spacing:.04em;text-transform:uppercase;font-size:12px;line-height:1.3}}.brand img{{width:64px;height:48px;object-fit:contain}}.brand small{{display:block;color:var(--muted);font-size:10px;font-weight:600;letter-spacing:.15em;margin-top:3px}}nav{{display:flex;align-items:center;gap:25px;font-size:13px;font-weight:700}}.nav-link{{padding:12px 0}}.nav-link:hover{{color:var(--red)}}.nav-cta,.button{{display:inline-flex;align-items:center;justify-content:center;padding:12px 19px;background:var(--red);color:#fff;font-size:13px;font-weight:800;border:1px solid var(--red);transition:transform .18s,background .18s}}.nav-cta:hover,.button:hover{{background:var(--red-dark);transform:translateY(-2px)}}.nav-products{{position:relative}}.mega{{display:none;position:fixed;top:116px;left:50%;transform:translateX(-50%);width:min(1180px,calc(100vw - 32px));max-height:82vh;overflow:auto;background:#fff;border:1px solid var(--line);box-shadow:0 24px 60px #18242a2b;padding:24px;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px}}
.mega-column{{min-width:0}}.mega-group+.mega-group{{border-top:1px solid var(--line);margin-top:16px;padding-top:14px}}.mega-group h3{{font-size:12px;color:var(--red);text-transform:uppercase;letter-spacing:.03em;margin:0 0 7px}}.mega-group h3 a{{color:var(--red)}}.mega-group p{{font-size:11px;line-height:1.45;color:var(--muted);margin:0 0 7px}}.mega-group>a{{display:block;padding:3px 0;font-size:11px;line-height:1.4;font-weight:500}}.mega-group>a:hover{{color:var(--red);text-decoration:underline}}.nav-products:hover .mega,.nav-products:focus-within .mega{{display:grid}}
.eyebrow{{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--red);margin-bottom:12px}}.crumbs{{padding:22px 0;color:var(--muted);font-size:13px}}.crumbs a:hover,.text-link:hover,.footer-links a:hover{{color:var(--red)}}.actions{{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}}.button.whatsapp{{background:#294e43;border-color:#294e43}}.button.whatsapp:hover{{background:#1d3d34}}
.product-hero{{padding:32px 0 58px}}.product-hero-grid{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.92fr);align-items:center;gap:56px}}.product-photo{{margin:0;min-width:0;background:var(--paper)}}.product-photo img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}}.product-photo figcaption,.photo-credit{{padding:8px 12px;color:var(--muted);font-size:11px;line-height:1.45}}.product-photo figcaption a{{text-decoration:underline}}.product-intro,.catalog-hero p,.copy{{color:#4d5a61;font-size:16px;line-height:1.75}}.product-tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}}.product-tags span{{background:#f5f6f5;border:1px solid var(--line);padding:7px 10px;font-size:11px;font-weight:700;color:#4d5a61}}
.content-section{{padding:62px 0}}.content-section.muted{{background:var(--paper)}}.two-col{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:start}}.feature-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.feature{{padding:18px;background:var(--paper);border:1px solid var(--line)}}.feature strong,.feature span{{display:block}}.feature strong{{margin-bottom:7px;font-size:14px}}.feature span{{font-size:13px;line-height:1.55;color:var(--muted)}}.spec-table{{width:100%;border-collapse:collapse;margin:18px 0}}.spec-table td{{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13px}}.spec-table td:first-child{{width:34%;font-weight:700}}.form-note{{color:var(--muted);font-size:12px;line-height:1.5}}.why-panel{{margin-top:26px;padding:26px;background:#20282d;color:#fff}}.why-panel h2{{font-size:1.6rem}}.why-panel p,.why-panel li{{color:#d7dfe1;font-size:13px}}.why-panel ul{{margin:14px 0 0;padding-left:18px}}.why-panel li{{margin:7px 0}}.related-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:22px}}.related-card{{display:block;border:1px solid var(--line);background:#fff;transition:transform .18s,box-shadow .18s}}.related-card:hover,.catalog-card:hover{{transform:translateY(-3px);box-shadow:0 12px 28px #18242a14}}.related-card img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}}.related-card span{{display:block;padding:14px;font-weight:700;font-size:14px}}
.quote-section{{padding:68px 0;background:#f4f5f4}}.quote-grid{{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:48px;align-items:start}}.quote-aside h2{{font-size:clamp(1.8rem,3vw,2.5rem)}}.quote-card{{padding:26px;background:#fff;border:1px solid var(--line);box-shadow:0 14px 36px #18242a0d}}.form-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.field{{min-width:0}}.field.full{{grid-column:1/-1}}.field label{{display:block;font-size:12px;font-weight:700;margin-bottom:6px}}.field input,.field textarea{{width:100%;min-height:44px;padding:10px 12px;border:1px solid #cbd2d5;border-radius:0;background:#fff;color:var(--ink);font:inherit;font-size:14px}}.field textarea{{min-height:100px;resize:vertical}}.field input:focus,.field textarea:focus{{outline:2px solid #b6333844;border-color:var(--red)}}.field button{{cursor:pointer}}.field .form-note{{margin:10px 0 0}}
.catalog-hero{{padding:56px 0;background:#20282d;color:#fff}}.catalog-hero .eyebrow{{color:#e4b7a5}}.catalog-hero h1{{max-width:14ch;color:#fff}}.catalog-hero p{{color:#d7dfe1;max-width:62ch}}.catalog-hero-grid{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.88fr);align-items:center;gap:48px}}.catalog-hero-grid>img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}}.catalog-section{{padding:64px 0;border-bottom:1px solid var(--line)}}.category-heading{{display:flex;justify-content:space-between;align-items:end;gap:32px;margin-bottom:26px}}.category-heading>p{{max-width:460px;margin:0;color:var(--muted);font-size:14px}}.catalog-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.catalog-card{{min-width:0;border:1px solid var(--line);background:#fff;display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}}.catalog-card>img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--paper)}}.catalog-card-body{{padding:18px;display:flex;flex:1;flex-direction:column}}.catalog-card-body h3{{font-size:17px}}.catalog-card-body p{{color:var(--muted);font-size:13px;line-height:1.55;flex:1}}.text-link{{font-size:12px;font-weight:800;color:var(--red)}}.catalog-card .photo-credit{{border-top:1px solid var(--line)}}.photo-credit a{{text-decoration:underline}}.site-footer{{padding:34px 0;background:#20282d;color:#fff}}.footer-inner{{display:flex;justify-content:space-between;gap:28px;align-items:center}}.footer-inner strong{{font-size:14px}}.footer-inner p{{max-width:560px;margin:8px 0 0;color:#c5ced1;font-size:12px}}.footer-links{{display:flex;gap:18px;flex-wrap:wrap;font-size:12px}}
@media(max-width:900px){{.nav-inner{{gap:18px}}nav{{gap:16px}}.product-hero-grid,.catalog-hero-grid{{gap:30px}}.catalog-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.mega{{padding:16px;gap:12px}}}}
@media(max-width:760px){{.shell{{width:min(100% - 32px,620px)}}.topline-inner{{justify-content:center;flex-wrap:wrap;padding:6px 0;text-align:center}}.nav-inner{{height:auto;min-height:72px;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px 0}}.brand{{margin:0 auto}}.nav-inner nav{{width:100%;justify-content:center;gap:18px;font-size:12px}}.nav-inner nav>a.nav-link:nth-of-type(2){{display:none}}.nav-cta{{padding:9px 12px;font-size:12px}}.mega{{position:fixed;top:126px;left:12px;right:12px;transform:none;width:auto;max-height:calc(100vh - 140px);grid-template-columns:repeat(2,minmax(0,1fr));padding:14px;gap:12px}}.product-hero-grid,.catalog-hero-grid,.two-col,.quote-grid{{grid-template-columns:1fr;gap:28px}}.product-hero{{padding-top:18px}}.product-hero-grid>div{{order:-1}}.category-heading{{display:block}}.category-heading>p{{margin-top:12px}}.catalog-hero{{padding:38px 0}}.catalog-section,.content-section{{padding:44px 0}}.quote-section{{padding:46px 0}}.footer-inner{{align-items:flex-start;flex-direction:column}}}}
@media(max-width:520px){{.shell{{width:calc(100% - 28px)}}.catalog-grid,.related-grid{{grid-template-columns:1fr}}.feature-grid,.form-grid{{grid-template-columns:1fr}}.field.full{{grid-column:auto}}.quote-card{{padding:18px}}.product-tags{{gap:6px}}.product-tags span{{font-size:10px;padding:6px 8px}}.actions{{gap:8px}}.actions .button{{flex:1 1 145px;padding:11px 12px;text-align:center}}.mega{{grid-template-columns:1fr;top:126px;max-height:calc(100vh - 140px)}}.mega-column{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.mega-group+.mega-group{{border-top:0;border-left:1px solid var(--line);margin:0;padding:0 0 0 12px}}}}
</style>""".replace("{{", "{").replace("}}", "}").replace("__ACCENT__", ACCENT) + (
        "\n<style>.mega-icon{display:inline-flex;vertical-align:middle;margin-right:6px;color:var(--red)}"
        ".mega-icon svg{width:15px;height:15px}</style>"
    )


def head(title, description, canonical_path, structured_data=None):
    structured = ""
    if structured_data:
        structured = '<script type="application/ld+json">' + json.dumps(
            structured_data, ensure_ascii=False
        ).replace("</", "<\\/") + "</script>"
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="{ACCENT}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{page_styles()}
{structured}
</head><body>"""


def category_for_product(catalog, product):
    for category in catalog["categories"]:
        if product in category["products"]:
            return category
    raise ValueError(f"Product missing category: {product}")


def products(catalog):
    for category in catalog["categories"]:
        for product in category["products"]:
            yield category, product


def item_intro(category, product):
    lower = product.lower()
    return (
        f"{product} are specified around the product being packed, how it is handled, "
        f"and where it needs to go. Nilkanth Packaging Industries works with businesses "
        f"in Vapi, Gujarat to plan {lower} with practical dimensions, board construction "
        f"and print options for the intended packing and distribution conditions."
    )


def item_detail(category, product):
    return (
        f"Our {product.lower()} can be developed as part of a complete secondary packaging "
        f"requirement. We review the product measurements, packed weight, orientation, "
        f"stacking pattern, storage environment and transport route before recommending a "
        f"board and box format. This helps align the packaging with your packing line and "
        f"handling needs rather than relying on a one-size-fits-all specification."
    )


def specification_rows(category, product):
    name = product.lower()
    ply = "3, 5, 7, 9 and 11 ply, as applicable to the selected product and confirmed specification"
    flute = "A, B, C, E, F, BC and EB flute profiles where suitable for the construction"
    if "3 ply" in name:
        ply = "3 ply, single-wall construction"
    elif "5 ply" in name:
        ply = "5 ply, double-wall construction"
    elif "7 ply" in name:
        ply = "7 ply, triple-wall construction"
    elif "9 ply" in name:
        ply = "9 ply, subject to engineering and order confirmation"
    elif "11 ply" in name:
        ply = "11 ply, subject to engineering and order confirmation"
    elif "double wall" in name:
        ply = "Double-wall construction; ply build confirmed against the application"
    elif "triple wall" in name:
        ply = "Triple-wall construction; ply build confirmed against the application"
    elif "2 ply" in name:
        ply = "2 ply, single-face corrugated board"
    if "bc flute" in name or "eb flute" in name:
        flute = f"{product.split()[0]} flute combination"
    elif "flute" in name and name[0:1] in "abcef":
        flute = f"{product.split()[0]} flute profile"
    elif "single face" in name:
        flute = "Single-face corrugated roll; profile and roll size confirmed to order"
    elif "sheet" in name or "roll" in name:
        flute = "Flute profile selected for the required sheet or roll construction"
    return [
        ("Dimensions", "Made to customer-supplied internal or external box dimensions"),
        ("Ply / wall", ply),
        ("Flute", flute),
        ("Paper GSM", "Selected liner and medium GSM finalized against strength and weight requirements"),
        ("Printing", "Plain or printed options discussed during quotation, where applicable"),
        ("Order details", "Minimum order, production schedule and delivery confirmed against specification"),
    ]


def features(category, product):
    name = product.lower()
    items = [
        ("Application-led specification", "Box style and board build planned around the product and route."),
        ("Made-to-order dimensions", "Share internal or external dimensions for a fit-for-purpose quotation."),
        ("Material and print choices", "Discuss liner, medium, flute and print requirements with the team."),
    ]
    if "print" in name or "barcode" in name or "logo" in name or "qr" in name or "fmcg" in name:
        items[2] = ("Brand and information printing", "Artwork, marks and codes can be reviewed for print feasibility.")
    if "insert" in name or "partition" in name or "divider" in name or "bottle" in name:
        items[0] = ("Product separation", "Internal components can help separate products and limit contact.")
    if "export" in name or "heavy" in name or "industrial" in name or "triple" in name or "11 ply" in name or "9 ply" in name:
        items[0] = ("Transit-focused construction", "Discuss board strength, stacking and handling for longer routes.")
    return items


def use_case(category, product):
    return (
        f"{product} are considered for packing, storing, shipping or presenting products "
        f"where a paper-based format can meet the application. The correct specification "
        f"depends on packed weight, product fragility, stacking, handling frequency and "
        f"transport conditions; share these details when requesting a quotation."
    )


def related_products(catalog, product):
    category = category_for_product(catalog, product)
    related = [item for item in category["products"] if item != product][:3]
    if len(related) < 3:
        for other in catalog["categories"]:
            if other["slug"] == category["slug"]:
                continue
            related.extend(other["products"][:3 - len(related)])
            if len(related) >= 3:
                break
    return related


def breadcrumb_data(product):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "../../index.html"},
            {"@type": "ListItem", "position": 2, "name": "Products", "item": "../index.html"},
            {"@type": "ListItem", "position": 3, "name": product},
        ],
    }


def product_jsonld(product, category, image):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product,
        "description": item_intro(category, product),
        "image": "../../images/products/" + image,
        "brand": {"@type": "Brand", "name": "Nilkanth Packaging Industries"},
        "manufacturer": {
            "@type": "Organization",
            "name": "Nilkanth Packaging Industries",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Vapi",
                "addressRegion": "Gujarat",
                "addressCountry": "IN",
            },
        },
        "category": category["name"],
    }


def quote_form(product):
    return f"""
<section class="quote-section" id="quote"><div class="shell quote-grid">
  <div class="quote-aside"><div class="eyebrow">Talk to our team</div><h2>Request a quote for {escape(product)}</h2>
    <p>Share the packaging details you have. Our team can follow up to confirm dimensions, board construction and the information needed for a quotation. Pricing is quoted to specification; no fixed online prices.</p>
    <div class="actions"><a class="button whatsapp" href="https://wa.me/{WHATSAPP}?text={escape('Hello Nilkanth Packaging Industries, I would like to discuss ' + product + '.')}" target="_blank" rel="noopener">WhatsApp our team</a></div>
    <p style="margin-top:18px"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE}">+91 94285 26059</a></p>
  </div>
  <form class="quote-card" data-product="{escape(product)}">
    <div class="form-grid">
      <div class="field"><label for="customer-name">Customer name *</label><input id="customer-name" name="customerName" autocomplete="name" required></div>
      <div class="field"><label for="company-name">Company name</label><input id="company-name" name="companyName" autocomplete="organization"></div>
      <div class="field"><label for="customer-email">Email address</label><input id="customer-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="customer-phone">Phone number *</label><input id="customer-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div class="field full"><label for="product-name">Product name</label><input id="product-name" name="productName" value="{escape(product)}" readonly></div>
      <div class="field"><label for="quantity">Required quantity</label><input id="quantity" name="quantity" placeholder="e.g. 5,000 boxes"></div>
      <div class="field"><label for="dimensions">Box dimensions</label><input id="dimensions" name="dimensions" placeholder="L × W × H and unit"></div>
      <div class="field"><label for="ply">Ply requirement</label><input id="ply" name="ply" placeholder="If known"></div>
      <div class="field"><label for="gsm">GSM requirement</label><input id="gsm" name="gsm" placeholder="If known"></div>
      <div class="field full"><label for="requirements">Additional requirements</label><textarea id="requirements" name="requirements" placeholder="Printing, flute, use case, delivery location or other details"></textarea></div>
      <div class="field full"><button class="button" type="submit">Send quote request on WhatsApp</button><p class="form-note">Submitting opens WhatsApp with your enquiry for review. Your browser will not transmit this form to the website.</p></div>
    </div>
  </form>
</div></section>"""


def script():
    return """
<script>
document.querySelectorAll('.quote-card').forEach(function(form) {
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    if (!form.reportValidity()) return;
    var labels = {
      customerName: 'Customer name',
      companyName: 'Company name',
      email: 'Email',
      phone: 'Phone',
      productName: 'Product',
      quantity: 'Quantity',
      dimensions: 'Dimensions',
      ply: 'Ply requirement',
      gsm: 'GSM requirement',
      requirements: 'Additional requirements'
    };
    var lines = ['Hello Nilkanth Packaging Industries, I would like to request a quotation:'];
    new FormData(form).forEach(function(value, key) {
      if (String(value).trim()) lines.push(labels[key] + ': ' + String(value).trim());
    });
    window.open('https://wa.me/919428526059?text=' + encodeURIComponent(lines.join('\\n')), '_blank', 'noopener');
  });
});
</script>"""


def catalogue_page(catalog):
    intro = (
        "Browse corrugated box styles, board constructions, flute profiles, printed cartons, "
        "sheets, partitions and industry-specific packaging. Each product page explains "
        "the available choices and gives you a direct route to request a specification-based quote."
    )
    structured = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Corrugated Packaging Products",
        "description": intro,
        "publisher": {"@type": "Organization", "name": catalog["company"]},
    }
    sections = []
    for category in catalog["categories"]:
        cards = []
        for index, product in enumerate(category["products"]):
            image = category["photos"][index % len(category["photos"])]
            asset = photo(catalog, image)
            cards.append(
                f'<article class="catalog-card"><img loading="lazy" src="../images/products/{escape(image)}" '
                f'alt="{escape(asset["alt"])}"><div class="catalog-card-body"><h3>{escape(product)}</h3>'
                f'<p>{escape(item_intro(category, product))}</p>'
                f'<a class="text-link" href="{escape(product_link(product, 1))}">View product details <span aria-hidden="true">→</span></a></div>'
                f'<div class="photo-credit">Illustrative photo: <a href="{escape(asset["url"])}" target="_blank" rel="noopener">{escape(asset["source"])}</a></div></article>'
            )
        sections.append(
            f'<section class="catalog-section" id="{escape(category["slug"])}"><div class="shell">'
            f'<div class="category-heading"><div><div class="eyebrow">Category {len(sections)+1:02d}</div>'
            f'<h2>{escape(category["name"])}</h2></div><p>{escape(category["description"])}</p></div>'
            f'<div class="catalog-grid">{"".join(cards)}</div></div></section>'
        )
    hero_photo = photo(catalog, "mailer-cartons.jpg")
    title = "Corrugated Packaging Products | Nilkanth Packaging Industries"
    html_page = head(title, intro, "products/", structured)
    html_page += header(catalog, 1)
    html_page += f"""
<main><section class="catalog-hero"><div class="shell catalog-hero-grid">
  <div><div class="eyebrow">Product catalogue / Vapi, Gujarat</div><h1>Packaging made for the way your products move.</h1>
    <p>{escape(intro)}</p><a class="button" href="#quote">Discuss a packaging requirement</a>
  </div><img src="../images/products/mailer-cartons.jpg" alt="{escape(hero_photo['alt'])}">
</div></section>
<div class="shell crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Product catalogue</div>
{"".join(sections)}
<section class="quote-section" id="quote"><div class="shell quote-grid"><div class="quote-aside"><div class="eyebrow">Specification-led service</div><h2>Need help selecting a box?</h2><p>Share your product dimensions, packed weight, handling conditions and order quantity. Nilkanth Packaging Industries can discuss the construction and options that fit the requirement.</p></div>
<div class="quote-card"><h3>Talk with our Vapi team</h3><p>For a quotation, call or email with your product and delivery details. There are no fixed catalogue prices; each quote depends on the final specification and quantity.</p><div class="actions"><a class="button" href="tel:{PHONE}">Call +91 94285 26059</a><a class="button whatsapp" href="https://wa.me/{WHATSAPP}?text=Hello%20Nilkanth%20Packaging%20Industries%2C%20I%20need%20help%20with%20a%20packaging%20specification." target="_blank" rel="noopener">WhatsApp enquiry</a></div><p class="form-note"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section></main>
<footer class="site-footer"><div class="shell footer-inner"><div><strong>Nilkanth Packaging Industries</strong><p>Corrugated boxes and packaging solutions from Vapi, Gujarat. Product specifications and pricing are confirmed against each enquiry.</p></div><div class="footer-links"><a href="../index.html">Home</a><a href="mailto:{EMAIL}">Email us</a><a href="tel:{PHONE}">Call us</a></div></div></footer>
</body></html>"""
    return html_page


def product_page(catalog, category, product):
    slug = slugify(product)
    index = category["products"].index(product)
    image = category["photos"][index % len(category["photos"])]
    asset = photo(catalog, image)
    intro = item_intro(category, product)
    description = (
        f"{product} from Nilkanth Packaging Industries in Vapi, Gujarat. "
        f"{category['description']} Request a packaging specification and quote."
    )
    structured = [
        product_jsonld(product, category, image),
        breadcrumb_data(product),
    ]
    title = f"{product} Manufacturer & Supplier in Vapi | Nilkanth Packaging"
    page_html = head(title, description, "products/" + slug + "/", structured)
    page_html += header(catalog, 2)
    related = related_products(catalog, product)
    related_cards = []
    for related_product in related:
        related_category = category_for_product(catalog, related_product)
        related_index = related_category["products"].index(related_product)
        related_image = related_category["photos"][related_index % len(related_category["photos"])]
        related_asset = photo(catalog, related_image)
        related_cards.append(
            f'<a class="related-card" href="{escape(product_link(related_product, 2))}">'
            f'<img loading="lazy" src="../../images/products/{escape(related_image)}" alt="{escape(related_asset["alt"])}">'
            f'<span>{escape(related_product)} →</span></a>'
        )
    specs = "".join(
        f"<tr><td>{escape(label)}</td><td>{escape(value)}</td></tr>"
        for label, value in specification_rows(category, product)
    )
    feature_markup = "".join(
        f'<div class="feature"><strong>{escape(title)}</strong><span>{escape(description)}</span></div>'
        for title, description in features(category, product)
    )
    uses = (
        f"{product} are used where the selected packaging format suits the product and handling conditions. "
        "Potential applications include secondary packaging, storage, picking, order fulfilment, "
        "retail presentation or transit, depending on the exact product design."
    )
    page_html += f"""
<main><div class="shell crumbs" aria-label="Breadcrumb"><a href="../../index.html">Home</a> / <a href="../index.html">Products</a> / {escape(product)}</div>
<section class="product-hero"><div class="shell product-hero-grid">
  <figure class="product-photo"><img src="../../images/products/{escape(image)}" alt="{escape(asset['alt'])}" fetchpriority="high"><figcaption>Illustrative packaging photograph · <a href="{escape(asset['url'])}" target="_blank" rel="noopener">{escape(asset['source'])} / Pexels</a></figcaption></figure>
  <div><div class="eyebrow">{escape(category['name'])} · Vapi, Gujarat</div><h1>{escape(product)}</h1><p class="product-intro">{escape(intro)}</p>
    <div class="product-tags"><span>Made to requirement</span><span>No fixed online prices</span><span>Specification-led quote</span></div>
    <div class="actions"><a class="button" href="#quote">Request a Quote</a><a class="button whatsapp" href="https://wa.me/{WHATSAPP}?text={escape('Hello Nilkanth Packaging Industries, I would like to enquire about ' + product + '.')}" target="_blank" rel="noopener">WhatsApp enquiry</a></div>
  </div>
</div></section>
<section class="content-section"><div class="shell two-col"><div><div class="eyebrow">Product overview</div><h2>Packaging tailored to the application</h2><p class="copy">{escape(category['description'])}</p><p class="copy">{escape(item_detail(category, product))}</p></div>
<div><div class="eyebrow">Key features and benefits</div><div class="feature-grid">{feature_markup}</div></div></div></section>
<section class="content-section muted"><div class="shell two-col"><div><div class="eyebrow">Specification options</div><h2>Sizes, paper and construction</h2><table class="spec-table"><tbody>{specs}</tbody></table><p class="form-note">Final specifications, production feasibility, minimum quantities and lead times are confirmed by the Nilkanth team before an order is accepted.</p></div>
<div><div class="eyebrow">Applications</div><h2>Where it may be used</h2><p class="copy">{escape(uses)}</p><div class="why-panel"><div class="eyebrow" style="color:#e4b7a5">Why Nilkanth Packaging Industries</div><h2>Packaging support from Vapi</h2><p>Work directly with the manufacturer to discuss dimensions, board selection and print needs for your application.</p><ul><li>Made-to-order specification discussion</li><li>Corrugated packaging expertise</li><li>Direct contact with the Vapi team</li><li>Quote based on your requirements—no fixed online prices</li></ul></div></div></div></section>
<section class="content-section"><div class="shell"><div class="eyebrow">Explore more</div><h2>Related products</h2><div class="related-grid">{"".join(related_cards)}</div></div></section>
{quote_form(product)}
</main><footer class="site-footer"><div class="shell footer-inner"><div><strong>Nilkanth Packaging Industries</strong><p>Corrugated boxes and packaging from Vapi, Gujarat. Specifications and pricing are confirmed for each order.</p></div><div class="footer-links"><a href="../index.html">Products</a><a href="../../index.html">Home</a><a href="mailto:{EMAIL}">Email</a><a href="tel:{PHONE}">Call us</a></div></div></footer>
{script()}</body></html>"""
    return page_html


def update_homepage(catalog):
    homepage = ROOT / "index.html"
    page = homepage.read_text(encoding="utf-8")
    menu = mega_menu(catalog, 0)
    if "<!-- PRODUCT_MEGA_MENU -->" in page:
        page = page.replace("<!-- PRODUCT_MEGA_MENU -->", menu)
    homepage.write_text(page, encoding="utf-8")


def legacy_redirect_page(target):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0;url={escape(target)}">
<link rel="canonical" href="{escape(target)}">
<title>Page moved | Nilkanth Packaging Industries</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;background:#f5f6f5;color:#20282d;font:16px/1.6 Arial,sans-serif}}main{{max-width:560px;padding:32px;background:#fff;border:1px solid #e4e8e9}}a{{color:#b63338;font-weight:700}}
</style>
</head><body><main><h1>This product page has moved</h1>
<p>We are taking you to the current Nilkanth Packaging Industries product catalogue.</p>
<p><a href="{escape(target)}">Continue to the product page</a></p>
<script>window.location.replace({json.dumps(target)});</script>
</main></body></html>"""


def update_legacy_routes():
    routes = {
        "3-ply-corrugated-boxes.html": "products/3-ply-corrugated-boxes/",
        "5-ply-corrugated-boxes.html": "products/5-ply-corrugated-boxes/",
        "7-ply-heavy-duty-boxes.html": "products/7-ply-corrugated-boxes/",
        "die-cut-custom-boxes.html": "products/die-cut-boxes/",
        "offset-printed-boxes.html": "products/offset-printed-boxes/",
        "mono-cartons.html": "products/index.html#printed-corrugated-boxes",
    }
    for filename, target in routes.items():
        (ROOT / filename).write_text(legacy_redirect_page(target), encoding="utf-8")


def main():
    catalog = read_catalog()
    PRODUCTS.mkdir(parents=True, exist_ok=True)
    (PRODUCTS / "index.html").write_text(catalogue_page(catalog), encoding="utf-8")
    count = 0
    for category, product in products(catalog):
        output = PRODUCTS / slugify(product) / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(product_page(catalog, category, product), encoding="utf-8")
        count += 1
    update_homepage(catalog)
    update_legacy_routes()
    print(f"Generated catalogue with {len(catalog['categories'])} categories and {count} product pages.")


if __name__ == "__main__":
    main()
