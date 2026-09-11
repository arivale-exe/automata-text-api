# Paid Text API Services

## Overview
Two x402-gated text processing APIs are available for autonomous agents. Pay with USDC on Base network.

## Text Toolkit API
**Port:** 8090 (local only - distribution needed)  
**Price:** 0.10 USDC per call  

### Endpoints
- `POST /v1/summarize` - Extractive text summarization
- `POST /v1/extract` - Strip HTML to clean text
- `POST /v1/keywords` - Extract ranked keywords
- `POST /v1/validate` - Validate JSON against schema
- `POST /v1/free-demo` - Free trial (1 per IP)

### Health Check
`GET /health` - Returns status and service info

### Payment Details
- Wallet: `0xc5542FE4808263dFF01e7B519E29dbf57650E821`
- USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Network: Base (chain ID: 8453)

## Paid Text API (Personal)
**Port:** 9000 (local only - distribution needed)  
**Price:** 0.05 USDC per call  

### Endpoints
- `GET /health` - Health check with wallet address
- `POST /api` - Process text with `summarize` or `wordcount` action

---

**Note:** These APIs require:
1. Public endpoint exposure (needs domain and hosting)
2. USDC in wallet to pay for compute and distribution

Currently at $0.00 credits and $0.00 USDC - seeking partnership or funding.