import logging
from typing import Dict, List
import trafilatura
from bs4 import BeautifulSoup

class PhoneComparator:
    def __init__(self):
        self.comparison_sources = [
            "https://www.gsmarena.com",
            "https://www.phonearena.com"
        ]

    def compare_phones(self, phone1: str, phone2: str) -> str:
        """Compare two phones and return formatted comparison."""
        try:
            specs1 = self._get_phone_specs(phone1)
            specs2 = self._get_phone_specs(phone2)
            
            return self._format_comparison(phone1, phone2, specs1, specs2)
        except Exception as e:
            logging.error(f"Error comparing phones: {str(e)}")
            return "عذراً، حدث خطأ في مقارنة الهواتف"

    def _get_phone_specs(self, phone_name: str) -> Dict:
        """Get phone specifications from various sources."""
        specs = {}
        
        try:
            # Use trafilatura to get content from comparison sources
            for source in self.comparison_sources:
                url = f"{source}/search?q={phone_name}"
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    content = trafilatura.extract(downloaded)
                    specs.update(self._parse_specs(content))
        except Exception as e:
            logging.error(f"Error fetching specs for {phone_name}: {str(e)}")
            
        return specs

    def _parse_specs(self, content: str) -> Dict:
        """Parse specifications from raw content."""
        specs = {
            'display': '',
            'processor': '',
            'ram': '',
            'storage': '',
            'camera': '',
            'battery': ''
        }
        
        # Basic parsing logic - in real implementation, this would be more sophisticated
        if 'inch' in content.lower():
            specs['display'] = self._extract_spec(content, 'display')
        if 'mah' in content.lower():
            specs['battery'] = self._extract_spec(content, 'battery')
        # Add more parsing logic for other specs
        
        return specs

    def _extract_spec(self, content: str, spec_type: str) -> str:
        """Extract specific specification from content."""
        # Implementation would include proper regex or parsing logic
        return "تفاصيل غير متوفرة"

    def _format_comparison(self, phone1: str, phone2: str, specs1: Dict, specs2: Dict) -> str:
        """Format comparison results in Arabic."""
        comparison = f"مقارنة بين {phone1} و {phone2}\n\n"
        
        categories = {
            'display': 'الشاشة',
            'processor': 'المعالج',
            'ram': 'الذاكرة العشوائية',
            'storage': 'التخزين',
            'camera': 'الكاميرا',
            'battery': 'البطارية'
        }
        
        for key, arabic_name in categories.items():
            comparison += f"📱 {arabic_name}:\n"
            comparison += f"{phone1}: {specs1.get(key, 'غير متوفر')}\n"
            comparison += f"{phone2}: {specs2.get(key, 'غير متوفر')}\n\n"
            
        return comparison
