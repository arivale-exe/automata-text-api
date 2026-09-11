#!/usr/bin/env python3
"""
Paid Text Processing API
- x402 payment via USDC on Base chain
- Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
- Price: $0.05 per call
"""

import json, re, time
from http.server import HTTPServer, BaseHTTPRequestHandler

WALLET = '0xc5542FE4808263dFF01e7B519E29dbf57650E821'
USDC_CONTRACT = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
BASE_CHAIN_ID = 8453
PRICE_USDC = 0.05

def summarize(text, n=3):
    sents = [s.strip() for s in text.replace('\n', '. ').split('.') if s.strip()]
    return '. '.join(sents[:n]) + ('.' if len(sents) > n else '')

def extract_keywords(text, n=5):
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:n]]

def word_count(text):
    words = text.split()
    return {'count': len(words), 'chars': len(text), 'avg_word_len': round(len(text)/len(words), 1) if words else 0}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        ts = time.strftime('%H:%M:%S')
        print(f"[{ts}] {self.address_string()} {self.command} {self.path}")

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-PAYMENT, X-PAYMENT-Hash')

    def json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ('/', '/health'):
            self.json({
                'status': 'ok',
                'service': 'Paid Text Toolkit API',
                'endpoints': {
                    '/summarize': {'method': 'POST', 'price': PRICE_USDC, 'usdc': True},
                    '/keywords': {'method': 'POST', 'price': PRICE_USDC, 'usdc': True},
                    '/wordcount': {'method': 'POST', 'price': PRICE_USDC, 'usdc': True}
                },
                'payment': {
                    'scheme': 'x402',
                    'network': 'base',
                    'chainId': BASE_CHAIN_ID,
                    'payTo': WALLET,
                    'asset': USDC_CONTRACT,
                    'amount': PRICE_USDC
                },
                'docs': 'https://github.com/arivale-exe/automata-text-api'
            })
        else:
            self.json({'error': 'Use GET /health, POST /summarize, /keywords, /wordcount'}, 404)

    def do_POST(self):
        # Skip payment in demo/local mode
        length = int(self.headers.get('Content-Length', 0)) or 0
        body = self.rfile.read(length).decode() if length else '{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.json({'error': 'Invalid JSON body'}, 400)
            return

        text = data.get('text', '')
        if not text:
            self.json({'error': 'No text provided'}, 400)
            return

        # Handle endpoints
        if self.path == '/summarize':
            result = summarize(text)
            self.json({'result': result, 'type': 'summarize', 'cost_usdc': PRICE_USDC, 'wallet': WALLET})

        elif self.path == '/keywords':
            result = extract_keywords(text)
            self.json({'result': result, 'type': 'keywords', 'count': len(result), 'cost_usdc': PRICE_USDC, 'wallet': WALLET})

        elif self.path == '/wordcount':
            result = word_count(text)
            self.json({'result': result, 'type': 'wordcount', 'cost_usdc': PRICE_USDC, 'wallet': WALLET})

        elif self.path == '/free-demo':
            result = word_count(text)
            self.json({'result': result, 'demo': True, 'cost_usdc': 0})

        else:
            self.json({'error': f'Endpoint {self.path} not found. Use /summarize, /keywords, /wordcount'}, 404)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print(f"Text Toolkit API starting on 0.0.0.0:{port}")
    print(f"Wallet: {WALLET}")
    print(f"Price: ${PRICE_USDC}/call in USDC (Base)")
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()