from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-url', methods=['POST'])
def check_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Get the domain from the URL
        domain = urlparse(url).netloc
        
        # Make request to the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for script tag in head
        script_found = False
        head_tag = soup.find('head')
        if head_tag:
            for script in head_tag.find_all('script'):
                src = script.get('src', '')
                if domain in src and 'track.js' in src:
                    script_found = True
                    break
        
        # Check for CTA link
        cta_found = False
        track_url = f"https://track.{domain}/click"
        
        # Check in all links
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if track_url in href:
                cta_found = True
                break
                
        # Check in all buttons
        for button in soup.find_all('button'):
            onclick = button.get('onclick', '')
            if track_url in onclick:
                cta_found = True
                break
        
        return jsonify({
            'script_found': script_found,
            'cta_found': cta_found,
            'domain': domain
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
