5import os
import re
import sys

# Securely grab affiliate IDs from GitHub environment variables
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_TAG", "premiumhea0ac-21")
FLIPKART_AFFILIATE_ID = os.getenv("FLIPKART_ID", "akhtarmon")
EARNKARO_PRO_ID = os.getenv("EARNKARO_ID", "5391028")

def update_deal_page():
    html_file = "index.html"
    
    deals = [
        {
            "title": "Exclusive Tech Deal - High Speed Automation Workflow Setup",
            "price": "₹99",
            "original_price": "₹999",
            "tag": "Loot Deal",
            "link": "#"
        },
        {
            "title": "Premium Digital Micro-Product Accelerator Kit",
            "price": "₹149",
            "original_price": "₹1,499",
            "tag": "Top Pick",
            "link": "#"
        }
    ]
    
    cards_html = ""
    for deal in deals:
        cards_html += f"""
        <div class="bg-white rounded-2xl p-4 shadow-xs border border-gray-100 flex gap-4">
            <div class="w-24 h-24 bg-gray-50 rounded-xl flex items-center justify-center font-bold text-gray-400 shrink-0">🛍️</div>
            <div class="flex flex-col justify-between w-full">
                <div>
                    <span class="text-xs font-bold text-orange-500 bg-orange-50 px-2 py-0.5 rounded-md">{deal['tag']}</span>
                    <h3 class="font-semibold text-sm line-clamp-2 mt-1">{deal['title']}</h3>
                </div>
                <div class="flex items-center justify-between mt-2">
                    <div>
                        <span class="text-base font-bold text-gray-900">{deal['price']}</span>
                        <span class="text-xs text-gray-400 line-through ml-1">{deal['original_price']}</span>
                    </div>
                    <a href="{deal['link']}" class="bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm">Buy Now</a>
                </div>
            </div>
        </div>
        """

    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = r'(<div id="deals-container"[^>]*>)(.*?)(</div>)'
        
        if re.search(pattern, content, flags=re.DOTALL):
            updated_content = re.sub(pattern, f"\\1\n{cards_html}\n\\3", content, flags=re.DOTALL)
            
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Success: Live Deal Container Updated Atomically!")
        else:
            print("Error: Could not find target id='deals-container' pattern wrapper.")
            sys.exit(1)
    else:
        print(f"Error: {html_file} not found.")
        sys.exit(1)

if __name__ == "__main__":
    update_deal_page()
