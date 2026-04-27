#!/usr/bin/env python3
"""
#newdragon prototype - Linear type search system
Extracts the last word from input text and uses it as a search key
"""

import re
import urllib.parse
import webbrowser
import json
from typing import Optional, List, Dict
from urllib.request import urlopen, Request
from urllib.error import URLError


class NewDragonSearch:
    """Search system that uses the last word as the search key"""
    
    def __init__(self):
        self.search_engine = "https://www.google.com/search?q="
        self.api_endpoint = "https://api.duckduckgo.com/"
    
    def extract_last_word(self, text: str) -> Optional[str]:
        """
        Extract the last meaningful word from text
        Ignores punctuation and whitespace
        """
        # Remove punctuation and extra whitespace
        cleaned = re.sub(r'[^\w\s]', '', text.strip())
        
        # Split into words and get the last one
        words = cleaned.split()
        if words:
            return words[-1].lower()
        return None
    
    def build_search_url(self, keyword: str) -> str:
        """Build search URL with the keyword"""
        encoded_keyword = urllib.parse.quote(keyword)
        return f"{self.search_engine}{encoded_keyword}"
    
    def search_internet(self, keyword: str) -> List[Dict]:
        """
        Perform actual internet search using DuckDuckGo API
        
        Args:
            keyword: Search term
            
        Returns:
            List of search results
        """
        try:
            # DuckDuckGo Instant Answer API
            params = urllib.parse.urlencode({
                'q': keyword,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            })
            
            url = f"{self.api_endpoint}?{params}"
            
            req = Request(url, headers={
                'User-Agent': 'NewDragonSearch/1.0'
            })
            
            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            results = []
            
            # Extract abstract/definition
            if data.get('Abstract'):
                results.append({
                    'type': 'abstract',
                    'title': data.get('Heading', keyword),
                    'content': data.get('Abstract'),
                    'url': data.get('AbstractURL', '')
                })
            
            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:5]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'type': 'related',
                        'title': topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else keyword,
                        'content': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            return results
            
        except URLError as e:
            return [{'error': f'Network error: {str(e)}'}]
        except Exception as e:
            return [{'error': f'Search error: {str(e)}'}]
    
    def process(self, text: str, auto_open: bool = False, fetch_results: bool = True) -> dict:
        """
        Process the input text and generate search
        
        Args:
            text: Input text/conclusion
            auto_open: If True, opens the search in browser
            fetch_results: If True, fetches actual search results
            
        Returns:
            Dictionary with keyword, search URL, and results
        """
        keyword = self.extract_last_word(text)
        
        if not keyword:
            return {
                "error": "No valid word found in input",
                "keyword": None,
                "url": None,
                "results": []
            }
        
        search_url = self.build_search_url(keyword)
        
        result = {
            "input": text,
            "keyword": keyword,
            "url": search_url,
            "results": [],
            "error": None
        }
        
        if fetch_results:
            print(f"🔍 Searching internet for: {keyword}")
            result['results'] = self.search_internet(keyword)
        
        if auto_open:
            print(f"Opening search for: {keyword}")
            webbrowser.open(search_url)
        
        return result


def main():
    """Demo of the NewDragon search system"""
    dragon = NewDragonSearch()
    
    # Example conclusions
    examples = [
        "The best programming language for beginners is Python",
        "I really enjoy eating pizza",
        "The capital of France is Paris",
        "Machine learning is powered by data"
    ]
    
    print("=" * 60)
    print("#NEWDRAGON PROTOTYPE - Linear Type Search System")
    print("=" * 60)
    print()
    
    for example in examples:
        result = dragon.process(example, fetch_results=True)
        print(f"Input: {result['input']}")
        print(f"Extracted Keyword: {result['keyword']}")
        print(f"Search URL: {result['url']}")
        
        if result['results']:
            print(f"\n📊 Search Results ({len(result['results'])} found):")
            for i, res in enumerate(result['results'][:3], 1):
                if 'error' in res:
                    print(f"  ⚠️  {res['error']}")
                else:
                    print(f"\n  {i}. {res.get('title', 'No title')}")
                    content = res.get('content', '')
                    if content:
                        print(f"     {content[:150]}{'...' if len(content) > 150 else ''}")
                    if res.get('url'):
                        print(f"     🔗 {res['url']}")
        else:
            print("  No results found")
        
        print("-" * 60)
    
    # Interactive mode
    print("\nInteractive Mode (type 'quit' to exit)")
    print("-" * 60)
    
    while True:
        user_input = input("\nEnter your conclusion: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = dragon.process(user_input, fetch_results=True)
        
        if result['error']:
            print(f"Error: {result['error']}")
        else:
            print(f"\n→ Extracted keyword: '{result['keyword']}'")
            print(f"→ Search URL: {result['url']}")
            
            if result['results']:
                print(f"\n📊 Internet Search Results:")
                print("=" * 60)
                for i, res in enumerate(result['results'], 1):
                    if 'error' in res:
                        print(f"⚠️  {res['error']}")
                    else:
                        print(f"\n{i}. {res.get('title', 'No title')}")
                        content = res.get('content', '')
                        if content:
                            print(f"   {content[:200]}{'...' if len(content) > 200 else ''}")
                        if res.get('url'):
                            print(f"   🔗 {res['url']}")
                print("=" * 60)
            else:
                print("\n⚠️  No results found")
            
            open_search = input("\nOpen in browser? (y/n): ").strip().lower()
            if open_search == 'y':
                webbrowser.open(result['url'])
                print("Search opened in browser!")


if __name__ == "__main__":
    main()
