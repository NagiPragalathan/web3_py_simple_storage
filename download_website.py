import os
import requests

# Function to download HTML and CSS files from a given URL


def download_html_css(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Raise an exception if the response status code is not 200 OK
    response.raise_for_status()

    # Get the HTML content from the response
    html = response.text

    # Find all CSS links in the HTML content
    css_links = []
    for line in html.split('\n'):
        if 'rel="stylesheet"' in line and 'href="' in line:
            start = line.index('href="') + len('href="')
            end = line.index('"', start)
            css_links.append(line[start:end])

    # Download the CSS files and replace the links in the HTML content with the local file paths
    for css_link in css_links:
        css_response = requests.get(css_link)
        # Raise an exception if the response status code is not 200 OK
        css_response.raise_for_status()

        # Get the CSS content from the response
        css = css_response.text

        # Get the filename from the URL
        filename = os.path.basename(css_link)

        # Save the CSS content to a local file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(css)

        # Replace the CSS link in the HTML content with the local file path
        html = html.replace(css_link, filename)

    # Save the HTML content to a local file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('Download complete.')


# Example usage
url = 'https://github.com/NagiPragalathan'
download_html_css(url)
