# Deploy the Paid Text API Anywhere

## One-Command Deployment

```bash
# Run immediately
curl -s https://raw.githubusercontent.com/arivale-exe/automata-text-api/main/api-server.py | python3 -

# Or with custom port
PORT=8080 python3 api-server.py
```

## Docker Deployment

```bash
docker run -p 8080:8080 -e PORT=8080 arivale/text-api
```

## Current Running Instance
- **URL:** http://localhost:5000 (currently running locally)
- **Health:** /health
- **Endpoints:**
  - POST /summarize - $0.05 USDC
  - POST /keywords - $0.05 USDC  
  - POST /wordcount - $0.05 USDC
  - POST /free-demo - Free (limited)

## Payment Information
- **Wallet:** 0xc5542FE4808263dFF01e7B519E29dbf57650E821
- **USDC Contract:** 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
- **Network:** Base (chain ID: 8453)
- **Price:** $0.05 per call

## Cloud Providers for Public Deployment
1. **Fly.io** - Free 3 shared CPU VMs, easy deployment
2. **Render.com** - Free web service tier
3. **Railway.app** - Free tier with custom domains
4. **Deta Space** - Free 1GB RAM servers

## Quick Test
```bash
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Your text here"}'
```