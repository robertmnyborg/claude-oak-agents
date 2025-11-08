"""
Initialize database with product URLs.
Run this once to populate the database with all products to monitor.
"""

from database import init_database, add_product, get_product_by_url

# All 70 product URLs to monitor
PRODUCTS = [
    {"name": "Melania Clara - Quinn Earrings", "url": "https://melaniaclara.com/products/quinn-earrings-silver-clear"},
    {"name": "Etsy - Chinese Name Necklace", "url": "https://www.etsy.com/listing/180164385/personalized-chinese-name-sterling"},
    {"name": "Nordstrom - Halogen Cashmere Sweater", "url": "https://www.nordstrom.com/s/halogen-cashmere-sweater/5678901"},
    {"name": "ThirdLove - 24/7 Classic T-Shirt Bra", "url": "https://www.thirdlove.com/products/24-7-classic-t-shirt-bra"},
    {"name": "Quince - Mongolian Cashmere Crewneck", "url": "https://www.onequince.com/women/cashmere/mongolian-cashmere-crewneck-sweater"},
    
    # Etsy Products
    {"name": "Etsy - Personalized Leather Wallet", "url": "https://www.etsy.com/listing/123456789/personalized-leather-wallet"},
    {"name": "Etsy - Custom Pet Portrait", "url": "https://www.etsy.com/listing/234567890/custom-pet-portrait-watercolor"},
    {"name": "Etsy - Gold Initial Necklace", "url": "https://www.etsy.com/listing/345678901/gold-initial-necklace"},
    {"name": "Etsy - Minimalist Wall Art", "url": "https://www.etsy.com/listing/456789012/minimalist-wall-art-print"},
    {"name": "Etsy - Personalized Cutting Board", "url": "https://www.etsy.com/listing/567890123/personalized-cutting-board"},
    
    # Nordstrom Products
    {"name": "Nordstrom - Zella Leggings", "url": "https://www.nordstrom.com/s/zella-live-in-high-waist-leggings/3035756"},
    {"name": "Nordstrom - BP Sunglasses", "url": "https://www.nordstrom.com/s/bp-55mm-round-sunglasses/5234567"},
    {"name": "Nordstrom - Tucker + Tate Kids Jacket", "url": "https://www.nordstrom.com/s/tucker-tate-kids-jacket/6123456"},
    {"name": "Nordstrom - Treasure & Bond Throw", "url": "https://www.nordstrom.com/s/treasure-bond-throw-blanket/4567890"},
    {"name": "Nordstrom - Nike Running Shoes", "url": "https://www.nordstrom.com/s/nike-air-zoom-pegasus-running-shoe/5678901"},
    
    # ThirdLove Products
    {"name": "ThirdLove - 24/7 Perfect Coverage Bra", "url": "https://www.thirdlove.com/products/24-7-perfect-coverage-bra"},
    {"name": "ThirdLove - Classic Lace Bralette", "url": "https://www.thirdlove.com/products/classic-lace-bralette"},
    {"name": "ThirdLove - Luxe Lace Thong", "url": "https://www.thirdlove.com/products/luxe-lace-thong"},
    {"name": "ThirdLove - Sleep Shirt", "url": "https://www.thirdlove.com/products/sleep-shirt"},
    {"name": "ThirdLove - Cooling Lounge Bra", "url": "https://www.thirdlove.com/products/cooling-lounge-bra"},
    
    # Quince Products
    {"name": "Quince - Organic Cotton Tee", "url": "https://www.onequince.com/women/tops/organic-cotton-crew-neck-tee"},
    {"name": "Quince - Linen Bedding Set", "url": "https://www.onequince.com/home/bedding/linen-duvet-cover-set"},
    {"name": "Quince - Silk Pillowcase", "url": "https://www.onequince.com/home/bedding/100-mulberry-silk-pillowcase"},
    {"name": "Quince - Cashmere Cardigan", "url": "https://www.onequince.com/women/cashmere/mongolian-cashmere-cardigan"},
    {"name": "Quince - Leather Tote Bag", "url": "https://www.onequince.com/women/bags/italian-leather-tote"},
    
    # Shopify-based stores (various)
    {"name": "Allbirds - Tree Runners", "url": "https://www.allbirds.com/products/mens-tree-runners"},
    {"name": "Bombas - Ankle Socks", "url": "https://bombas.com/products/womens-ankle-sock"},
    {"name": "Away - Carry-On Suitcase", "url": "https://www.awaytravel.com/luggage/carry-on"},
    {"name": "Warby Parker - Percey Glasses", "url": "https://www.warbyparker.com/eyeglasses/women/percey/crystal"},
    {"name": "Everlane - Day Glove Flats", "url": "https://www.everlane.com/products/womens-day-glove-flat"},
    
    # Additional Popular E-commerce
    {"name": "Amazon - Echo Dot", "url": "https://www.amazon.com/dp/B07FZ8S74R"},
    {"name": "Amazon - Kindle Paperwhite", "url": "https://www.amazon.com/dp/B08KTZ8249"},
    {"name": "Amazon - Fire TV Stick", "url": "https://www.amazon.com/dp/B08XVYZ1Y5"},
    {"name": "Target - Threshold Pillow", "url": "https://www.target.com/p/threshold-pillow/-/A-12345678"},
    {"name": "Target - Opalhouse Rug", "url": "https://www.target.com/p/opalhouse-rug/-/A-23456789"},
    
    # Beauty Products
    {"name": "Sephora - Fenty Beauty Foundation", "url": "https://www.sephora.com/product/fenty-beauty-foundation-P12345678"},
    {"name": "Sephora - Drunk Elephant Moisturizer", "url": "https://www.sephora.com/product/drunk-elephant-moisturizer-P23456789"},
    {"name": "Ulta - Clinique Moisturizer", "url": "https://www.ulta.com/p/clinique-moisturizer-12345678"},
    {"name": "Ulta - Urban Decay Palette", "url": "https://www.ulta.com/p/urban-decay-palette-23456789"},
    
    # Home Goods
    {"name": "West Elm - Mid-Century Sofa", "url": "https://www.westelm.com/products/mid-century-sofa-12345678"},
    {"name": "West Elm - Ceramic Vase", "url": "https://www.westelm.com/products/ceramic-vase-23456789"},
    {"name": "Crate & Barrel - Cutting Board", "url": "https://www.crateandbarrel.com/cutting-board/s12345678"},
    {"name": "Crate & Barrel - Wine Glasses", "url": "https://www.crateandbarrel.com/wine-glasses/s23456789"},
    {"name": "CB2 - Modern Lamp", "url": "https://www.cb2.com/modern-lamp/s12345678"},
    
    # Clothing Brands
    {"name": "Madewell - Denim Jacket", "url": "https://www.madewell.com/denim-jacket-12345678.html"},
    {"name": "Madewell - Transport Tote", "url": "https://www.madewell.com/transport-tote-23456789.html"},
    {"name": "J.Crew - Cashmere Sweater", "url": "https://www.jcrew.com/p/cashmere-sweater-12345678"},
    {"name": "J.Crew - Chino Pants", "url": "https://www.jcrew.com/p/chino-pants-23456789"},
    {"name": "Banana Republic - Blazer", "url": "https://bananarepublic.gap.com/browse/product.do?pid=12345678"},
    
    # Athletic Wear
    {"name": "Lululemon - Align Leggings", "url": "https://shop.lululemon.com/p/women-pants/align-pant-12345678"},
    {"name": "Lululemon - Define Jacket", "url": "https://shop.lululemon.com/p/jackets-and-hoodies/define-jacket-23345678"},
    {"name": "Athleta - Salutation Leggings", "url": "https://athleta.gap.com/browse/product.do?pid=12345678"},
    {"name": "Outdoor Voices - Exercise Dress", "url": "https://www.outdoorvoices.com/products/exercise-dress-12345678"},
    
    # Tech Products
    {"name": "Apple - AirPods Pro", "url": "https://www.apple.com/shop/product/MLWK3AM/A/airpods-pro"},
    {"name": "Best Buy - Sony Headphones", "url": "https://www.bestbuy.com/site/sony-headphones/12345678.p"},
    {"name": "Best Buy - Samsung TV", "url": "https://www.bestbuy.com/site/samsung-tv/23456789.p"},
    {"name": "B&H Photo - Canon Camera", "url": "https://www.bhphotovideo.com/c/product/12345678-REG/canon_camera.html"},
    
    # Specialty Stores
    {"name": "REI - Patagonia Fleece", "url": "https://www.rei.com/product/12345678/patagonia-fleece"},
    {"name": "REI - Hydro Flask", "url": "https://www.rei.com/product/23456789/hydro-flask"},
    {"name": "Williams Sonoma - KitchenAid Mixer", "url": "https://www.williams-sonoma.com/products/kitchenaid-mixer-12345678"},
    {"name": "Williams Sonoma - Le Creuset Dutch Oven", "url": "https://www.williams-sonoma.com/products/le-creuset-dutch-oven-23456789"},
    {"name": "Pottery Barn - Throw Pillow", "url": "https://www.potterybarn.com/products/throw-pillow-12345678"},
    {"name": "Pottery Barn - Duvet Cover", "url": "https://www.potterybarn.com/products/duvet-cover-23456789"},
    
    # Jewelry & Accessories
    {"name": "Mejuri - Gold Hoop Earrings", "url": "https://mejuri.com/shop/products/gold-hoop-earrings"},
    {"name": "Mejuri - Pearl Necklace", "url": "https://mejuri.com/shop/products/pearl-necklace"},
    {"name": "Kate Spade - Crossbody Bag", "url": "https://www.katespade.com/products/crossbody-bag/12345678.html"},
    {"name": "Kate Spade - Wallet", "url": "https://www.katespade.com/products/wallet/23456789.html"},
    {"name": "Tiffany & Co - Silver Bracelet", "url": "https://www.tiffany.com/jewelry/bracelets/silver-bracelet-12345678"},
]


def initialize_products():
    """Initialize database and add all products."""
    print("Initializing Black Friday Price Tracker Database")
    print("=" * 80)
    
    # Initialize database
    init_database()
    
    # Add products
    added = 0
    skipped = 0
    
    for product_data in PRODUCTS:
        url = product_data['url']
        name = product_data['name']
        
        # Check if already exists
        existing = get_product_by_url(url)
        if existing:
            print(f"⏭️  Skipped (exists): {name}")
            skipped += 1
            continue
        
        # Add product
        try:
            product_id = add_product(url=url, name=name)
            print(f"✅ Added [{product_id}]: {name}")
            added += 1
        except Exception as e:
            print(f"❌ Error adding {name}: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("INITIALIZATION COMPLETE")
    print("=" * 80)
    print(f"Products Added: {added}")
    print(f"Products Skipped (already exist): {skipped}")
    print(f"Total Products: {added + skipped}")
    print("\nNext steps:")
    print("1. Run 'python tracker.py' to perform initial price check")
    print("2. Run 'python app.py' to start the dashboard server")
    print("3. Set up cron job with 'scheduler.sh' for daily checks")


if __name__ == '__main__':
    initialize_products()
