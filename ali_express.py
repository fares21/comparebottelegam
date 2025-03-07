import os
import logging
import aiohttp
from typing import Dict, List

class AliExpressAPI:
    def __init__(self):
        self.api_key = os.getenv("ALIEXPRESS_API_KEY")
        self.affiliate_id = os.getenv("ALIEXPRESS_AFFILIATE_ID")
        self.base_url = "https://api.aliexpress.com/v2"
        
    async def get_reviews(self, product_name: str) -> str:
        """Get product reviews from AliExpress."""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'api_key': self.api_key,
                    'product_name': product_name,
                }
                async with session.get(f"{self.base_url}/reviews", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_reviews(data['reviews'])
                    else:
                        logging.error(f"Error fetching reviews: {response.status}")
                        return "عذراً، حدث خطأ في جلب المراجعات"
        except Exception as e:
            logging.error(f"Exception in get_reviews: {str(e)}")
            return "عذراً، حدث خطأ في الاتصال"

    async def get_affiliate_link(self, product_name: str) -> str:
        """Generate affiliate link for the product."""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'api_key': self.api_key,
                    'affiliate_id': self.affiliate_id,
                    'product_name': product_name,
                }
                async with session.get(f"{self.base_url}/affiliate/link", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['affiliate_link']
                    else:
                        logging.error(f"Error generating affiliate link: {response.status}")
                        return "عذراً، حدث خطأ في إنشاء رابط التسويق بالعمولة"
        except Exception as e:
            logging.error(f"Exception in get_affiliate_link: {str(e)}")
            return "عذراً، حدث خطأ في الاتصال"

    def _format_reviews(self, reviews: List[Dict]) -> str:
        """Format reviews for display."""
        formatted = ""
        for review in reviews[:5]:  # Show top 5 reviews
            formatted += f"⭐ {review['rating']}/5\n"
            formatted += f"👤 {review['reviewer']}\n"
            formatted += f"📝 {review['comment']}\n\n"
        return formatted
