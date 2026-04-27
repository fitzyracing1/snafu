#!/usr/bin/env python3
"""
#newdragon - Web-based search engine
Linear type search: extracts last word and searches the internet
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
from urllib.error import URLError
import re


class NewDragonSearchEngine:
    """Core search engine logic"""
    
    def extract_last_word(self, text):
        """Extract the last meaningful word from text"""
        cleaned = re.sub(r'[^\w\s]', '', text.strip())
        words = cleaned.split()
        return words[-1].lower() if words else None
    
    def search_internet(self, keyword):
        """Search the internet using DuckDuckGo API"""
        try:
            params = urllib.parse.urlencode({
                'q': keyword,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            })
            
            url = f"https://api.duckduckgo.com/?{params}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'NewDragonSearch/1.0'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            results = []
            
            # Abstract
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', keyword),
                    'snippet': data.get('Abstract'),
                    'url': data.get('AbstractURL', ''),
                    'source': data.get('AbstractSource', 'Web')
                })
            
            # Related topics
            for topic in data.get('RelatedTopics', [])[:10]:
                if isinstance(topic, dict) and 'Text' in topic:
                    text = topic.get('Text', '')
                    title = text.split(' - ')[0] if ' - ' in text else text[:80]
                    results.append({
                        'title': title,
                        'snippet': text,
                        'url': topic.get('FirstURL', ''),
                        'source': 'Related'
                    })
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]


class SearchHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the search engine"""
    
    search_engine = NewDragonSearchEngine()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for search"""
        if self.path == '/search':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            query = data.get('query', '')
            keyword = self.search_engine.extract_last_word(query)
            
            if not keyword:
                response = {
                    'error': 'No valid word found',
                    'keyword': None,
                    'results': []
                }
            else:
                results = self.search_engine.search_internet(keyword)
                response = {
                    'query': query,
                    'keyword': keyword,
                    'results': results
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_html(self):
        """Return the HTML for the search engine"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#NewDragon Search Engine</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding-top: 60px;
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .search-box {
            background: white;
            border-radius: 50px;
            padding: 8px 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .search-box input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 1.2em;
            padding: 15px;
        }
        
        .search-box button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .search-box button:hover {
            transform: scale(1.05);
        }
        
        .keyword-display {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        
        .keyword-display.show {
            display: block;
        }
        
        .results {
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .result-item {
            background: white;
            padding: 20px 25px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .result-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .result-item h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .result-item p {
            color: #555;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .result-item a {
            color: #764ba2;
            text-decoration: none;
            font-size: 0.9em;
        }
        
        .result-item a:hover {
            text-decoration: underline;
        }
        
        .result-source {
            display: inline-block;
            background: #f0f0f0;
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            color: #666;
            margin-left: 10px;
        }
        
        .loading {
            text-align: center;
            color: white;
            font-size: 1.2em;
            display: none;
            margin: 20px 0;
        }
        
        .loading.show {
            display: block;
        }
        
        .error {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 #NewDragon</h1>
            <p>Linear Type Search Engine</p>
            <p style="font-size: 0.9em; opacity: 0.8;">Enter any text - the last word becomes your search</p>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Type your conclusion here..." />
            <button onclick="search()">Search</button>
        </div>
        
        <div class="keyword-display" id="keywordDisplay"></div>
        <div class="loading" id="loading">🔍 Searching the internet...</div>
        <div class="error" id="error"></div>
        
        <div class="results" id="results"></div>
    </div>
    
    <script>
        const searchInput = document.getElementById('searchInput');
        const keywordDisplay = document.getElementById('keywordDisplay');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const results = document.getElementById('results');
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                search();
            }
        });
        
        async function search() {
            const query = searchInput.value.trim();
            
            if (!query) {
                showError('Please enter some text');
                return;
            }
            
            // Reset displays
            keywordDisplay.classList.remove('show');
            results.classList.remove('show');
            error.classList.remove('show');
            loading.classList.add('show');
            results.innerHTML = '';
            
            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                loading.classList.remove('show');
                
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                // Show extracted keyword
                keywordDisplay.innerHTML = `
                    <strong>Extracted Keyword:</strong> "${data.keyword}"
                `;
                keywordDisplay.classList.add('show');
                
                // Display results
                if (data.results && data.results.length > 0) {
                    displayResults(data.results);
                } else {
                    showError('No results found for: ' + data.keyword);
                }
                
            } catch (err) {
                loading.classList.remove('show');
                showError('Search failed: ' + err.message);
            }
        }
        
        function displayResults(resultData) {
            results.innerHTML = '';
            
            resultData.forEach((result, index) => {
                if (result.error) {
                    showError('Search error: ' + result.error);
                    return;
                }
                
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                
                const title = document.createElement('h3');
                title.textContent = (index + 1) + '. ' + (result.title || 'No title');
                
                const snippet = document.createElement('p');
                snippet.textContent = result.snippet || 'No description available';
                
                const linkContainer = document.createElement('div');
                
                if (result.url) {
                    const link = document.createElement('a');
                    link.href = result.url;
                    link.target = '_blank';
                    link.textContent = result.url;
                    linkContainer.appendChild(link);
                }
                
                if (result.source) {
                    const source = document.createElement('span');
                    source.className = 'result-source';
                    source.textContent = result.source;
                    linkContainer.appendChild(source);
                }
                
                resultItem.appendChild(title);
                resultItem.appendChild(snippet);
                resultItem.appendChild(linkContainer);
                
                results.appendChild(resultItem);
            });
            
            results.classList.add('show');
        }
        
        function showError(message) {
            error.textContent = message;
            error.classList.add('show');
            setTimeout(() => {
                error.classList.remove('show');
            }, 5000);
        }
    </script>
</body>
</html>
"""
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def main():
    """Start the search engine server"""
    port = 8080
    server = HTTPServer(('localhost', port), SearchHandler)
    
    print("=" * 60)
    print("🐉 #NEWDRAGON SEARCH ENGINE")
    print("=" * 60)
    print(f"\n✅ Search engine running at: http://localhost:{port}")
    print("\n📝 How it works:")
    print("   1. Type any text or conclusion")
    print("   2. Last word is extracted automatically")
    print("   3. Internet search is performed using that keyword")
    print("\n🔥 Example: 'The best fruit is apple' → searches for 'apple'")
    print("\n⌨️  Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down search engine...")
        server.shutdown()


if __name__ == "__main__":
    main()
