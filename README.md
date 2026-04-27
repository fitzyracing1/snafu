# 🐉 NewDragon Search Engine

**Linear Type Search System** - Extracts the last word from any text and searches the internet

## What is SNAFU?

SNAFU contains the NewDragon search engine prototype that implements a unique search algorithm:
1. You input any text or conclusion
2. The system extracts the **last word** 
3. That word becomes the search keyword
4. Real internet search results are fetched and displayed

## Files

- `newdragon_server.py` - Web-based search engine with UI (recommended)
- `newdragon_search.py` - Command-line version

## Usage

### Web Interface (Recommended)

```bash
cd snafu
python3 newdragon_server.py
```

Then open your browser to: `http://localhost:8080`

### Command Line Interface

```bash
cd snafu
python3 newdragon_search.py
```

## Examples

- Input: "The best programming language is Python"
  - Extracts: "Python"
  - Searches internet for: Python

- Input: "I really love pizza"
  - Extracts: "pizza"
  - Searches internet for: pizza

- Input: "The capital of France is Paris"
  - Extracts: "Paris"
  - Searches internet for: Paris

## Features

✅ Real-time internet search via DuckDuckGo API  
✅ Beautiful web interface  
✅ Automatic last-word extraction  
✅ Display of search results with titles, snippets, and URLs  
✅ Command-line alternative available

## Requirements

- Python 3.x
- No external dependencies (uses standard library only)

## How It Works

The linear type search algorithm:
1. Parses input text and removes punctuation
2. Splits text into words
3. Selects the last word as the search term
4. Queries DuckDuckGo API
5. Returns structured results with abstracts and related topics

---

**#NewDragon** - Where your conclusions become searches
