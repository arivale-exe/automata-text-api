#!/usr/bin/env python3
# Paid Text API - Deploy anywhere
# Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
# Price: $0.05 per call via x402 USDC on Base

import json, re, os
from http.server import HTTPServer, BaseHTTPRequestHandler

WALLET = '0xc5542FE4808263dFF01e7B519E29dbf57650E821'

def summarize(text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return '. '.join(sentences[:3]) + ('.' if len(sentences) > 3 else '')

def keywords(text, n=5):
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:n]]

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path in ('/', '/health'):
            self.json({'status': 'ok', 'wallet': WALLET, 'price': '$0.05/call'})
        else:
            self.json({'error': 'POST /summarize, /keywords, /wordcount'}, 404)

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
        except:
            self.json({'error': 'Invalid JSON'}, 400); return
        
        text = data.get('text', '')
        if not text:
            self.json({'error': 'No text'}, 400); return

        if self.path == '/summarize':
            self.json({'result': summarize(text), 'cost_usdc': 0.05})
        elif self.path == '/keywords':
            self.json({'result': keywords(text), 'cost_usdc': 0.05})
        elif self.path == '/wordcount':
            self.json({'result': {'count': len(text.split())}, 'cost_usdc': 0.05})
        elif self.path == '/free-demo':
            self.json({'result': {'count': len(text.split())}, 'demo': True, 'cost_usdc': 0})
        else:
            self.json({'error': 'Endpoint not found'}, 404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()