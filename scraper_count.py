import requests
from bs4 import BeautifulSoup

# Initialize counts
words_to_count = [
    "rails",
    "django",
    "laravel",
    "flask",
    "phoenix",
    "express",
    "node.js",
    "next.js",
    "python",
    "ruby",
    "javascript",
    "typescript",
    "elixir",
    "php",
    "java",
    "C#",
    ".net",
    "dotnet",
]
counts = {word: 0 for word in words_to_count}

# Define base URL and number of pages to scrape
base_url = "https://news.ycombinator.com/item?id=34530052&p="
num_pages = 5  # Modify this as needed

# Loop over each page
for i in range(1, num_pages + 1):
    url = base_url + str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the text content of the page
    content = soup.get_text()

    # Update counts
    for word in words_to_count:
        counts[word] += content.lower().count(word)

# Sort the counts and print them
for word, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
    print(f"{word}: {count}")
