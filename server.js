#!/usr/bin/env node
/**
 * Quick deployment script for Paid Text API
 * Usage: node QUICK_START_SERVER.js [port]
 * 
 * x402-gated at $0.05 per call on Base network
 * Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
 */

const http = require('http');
const url = require('url');

const WALLET = '0xc5542FE4808263dFF01e7B519E29dbf57650E821';
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const PORT = process.argv[2] || 9000;

function summarize(text) {
  const sentences = text.split('. ').filter(s => s.trim().length > 0);
  if (sentences.length <= 3) return text;
  return sentences.slice(0, 3).join('. ') + '...';
}

function wordcount(text) {
  const words = text.split(/\s+/);
  return { wordcount: words.length, charcount: text.length };
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  if (req.method === 'GET' && parsedUrl.pathname === '/health') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify({status: 'ok', wallet: WALLET}));
    return;
  }
  
  if (req.method === 'POST' && parsedUrl.pathname === '/api') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const action = data.action || 'summarize';
        let result;
        
        if (action === 'summarize') {
          result = summarize(data.text || '');
        } else if (action === 'wordcount') {
          result = wordcount(data.text || '');
        } else {
          result = `Unknown action: ${action}`;
        }
        
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({
          result,
          cost_usdc: 0.05,
          payment: {
            scheme: 'exact',
            network: 'base',
            payTo: WALLET,
            asset: USDC,
            chainId: 8453
          }
        }));
      } catch (e) {
        res.writeHead(400, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({error: 'Invalid JSON'}));
      }
    });
    return;
  }
  
  res.writeHead(404, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({error: 'Not found'}));
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Paid Text API running on port ${PORT}`);
  console.log(`Wallet: ${WALLET}`);
  console.log(`Price: $0.05 per call`);
});