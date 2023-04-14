import requests
from bs4 import BeautifulSoup
import htmlmin

# Download webpage
url = 'https://remix.ethereum.org/'
response = requests.get(url)

# Parse webpage using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Inline all JS and CSS into HTML
for script in soup(['script', 'link']):
    if script.has_attr('src'):
        # Download and replace external JS and CSS with inline JS and CSS
        if script.name == 'script':
            content = requests.get(script['src']).text
            script.string = content
            script.attrs = {}
        elif script.name == 'link' and script['rel'] == ['stylesheet']:
            content = requests.get(script['href']).text
            style = soup.new_tag('style', type='text/css')
            style.string = content
            script.replace_with(style)

# Minify HTML
minified_html = htmlmin.minify(str(soup))

# Save minified HTML to a file
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(minified_html)
