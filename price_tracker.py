
import os
import re
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Securely grab affiliate IDs from GitHub environment variables or use fallbacks
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_TAG", "premiumhea0ac-21")
FLIPKART_AFFILIATE_ID = os.getenv("FLIPKART_ID", "akhtarmon")
EARNKARO_PRO_ID = os.getenv("EARNKARO_ID", "5391028")

def generate_affiliate_link(url, platform):
    """Dynamically converts raw product URLs into monetized affiliate tracking links."""
    if not url or url == "#":
        return "#"
        
    try:
        parsed_url = urlparse(url)
        
        if platform.lower() == "amazon":
            query_params = parse_qs(parsed_url.query)
            query_params['tag'] = [AMAZON_ASSOCIATE_TAG]
            new_query = urlencode(query_params, doseq=True)
            return urlunparse(parsed_url._replace(query=new_query))
            
        elif platform.lower() == "flipkart":
            query_params = parse_qs(parsed_url.query)
            query_params['affid'] = [FLIPKART_AFFILIATE_ID]
            new_query = urlencode(query_params, doseq=True)
            return urlunparse(parsed_url._replace(query=new_query))
            
        elif platform.lower() == "earnkaro":
            encoded_target = urlencode({"url": url})
            return f"https://earnkaro.com/stores/sharing-profit-link?dl={encoded_target}&r={EARNKARO_PRO_ID}"
            
    except Exception as e:
        print(f"Link optimization skipped for {url}. Error: {e}")
        
    return url

def update_deal_page():
    html_file = "index.html"
    
    # 1. Define your dynamic deal data (Just paste raw links here!)
    deals = [
        {
            "title": "Xiaomi Power Bank 4i 20000mAh 33W Super Fast Charging PD |Smart 12 Layer Protection|Type C Input & Output|Triple Output Ports|Supports Android,Apple, Tablets, Earbuds,Watch(MI Powerbank),Black",
            "price": "₹2299",
            "original_price": "₹3999",
            "tag": "Loot Deal",
            "platform": "amazon",
            "raw_url": "https://amzn.in/d/0gr0V5WH"
        },
        {
            "title": "Premium Digital Micro-Product Accelerator Kit",
            "price": "₹149",
            "original_price": "₹1,499",
            "tag": "Top Pick",
            "platform": "earnkaro",
            "raw_url": "https://www.ajio.com/s/example-product"
        }
    ]
    
    # 2. Build out the structured HTML layout cards dynamically
    cards_html = ""
    for deal in deals:
        affiliate_link = generate_affiliate_link(deal["raw_url"], deal["platform"])
        
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
                    <a href="{affiliate_link}" target="_blank" rel="noopener noreferrer" class="bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm">Buy Now</a>
                </div>
            </div>
        </div>
        """

    # 3. Inject the newly generated deals seamlessly into your index.html
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = r'(<div id="deals-container"[^>]*>)(.*?)(</div>)'
        
        if re.search(pattern, content, flags=re.DOTALL):
            updated_content = re.sub(pattern, f"\\1\n{cards_html}\n\\3", content, flags=re.DOTALL)
            
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Success: Live Deals Parsed with Custom Affiliate Parameters Automatically!")
        else:
            print("Error: Could not find target id='deals-container' pattern wrapper.")
            sys.exit(1)
    else:
        print(f"Error: {html_file} not found.")
        sys.exit(1)

if __name__ == "__main__":
    update_deal_page()
