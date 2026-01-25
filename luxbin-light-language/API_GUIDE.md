# 🌈 LUXBIN Light Language API Guide

**Universal Quantum Communication Protocol**
Optimized for Diamond NV Center Quantum Computers

---

## 🚀 Quick Start

You have **TWO** APIs available for universal computer communication:

### 1️⃣ **Python FastAPI Server** (Quantum-Optimized)
**Best for:** Quantum computers, high-performance systems, direct protocol access

```bash
cd ~/luxbin-light-language
python3 light_language_api.py
```

Server runs on: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### 2️⃣ **luxbin-app Next.js API** (Web-Friendly)
**Best for:** Web applications, browsers, easy integration

```bash
cd ~/luxbin-app
npm run dev
```

Server runs on: `http://localhost:3000`
API Endpoints: `http://localhost:3000/api/v1/light-language/*`

---

## 🔑 Authentication

Both APIs use the same API key system.

### Get an API Key

1. Start luxbin-app: `cd ~/luxbin-app && npm run dev`
2. Visit: `http://localhost:3000/developers`
3. Click "API Keys" tab
4. Create a new key

### Using Your API Key

```bash
curl -X POST http://localhost:8000/v1/translate \
  -H "Authorization: Bearer YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello Quantum World",
    "enable_quantum": true
  }'
```

---

## 📡 API Endpoints

### Python FastAPI Server (Port 8000)

#### 1. Translate Text to Light
```bash
POST /v1/translate

{
  "text": "Hello World",
  "category": "quantum",
  "enable_quantum": true,
  "enable_satellite": false,
  "format": "full"
}
```

**Quantum Mode Enabled**: Optimizes for diamond NV centers (637nm zero-phonon line)

#### 2. Quantum NV Center Encoding
```bash
POST /v1/quantum/encode

{
  "text": "QUANTUM DATA",
  "use_grammar": true,
  "nv_center_type": "diamond"
}
```

**Returns:** NV center programming instructions, pulse sequences, coherence times

#### 3. Ion Trap Quantum Control
```bash
POST /v1/quantum/ion-trap

{
  "command": "HADAMARD GATE",
  "ion_type": "calcium_40"
}
```

**Wavelength Mappings:**
- 397nm: Calcium-40 single qubit gates
- 422nm: Strontium-88 state preparation
- 729nm: Ytterbium-171 two-qubit gates
- 854nm: Rubidium-87 cooling cycles

#### 4. Binary Data Encoding
```bash
POST /v1/binary/encode

{
  "binary_data": "48656c6c6f",
  "use_compression": true,
  "enable_quantum": true
}
```

#### 5. Satellite Laser Communication
```bash
POST /v1/satellite/transmit

{
  "data": "GLOBAL MESSAGE",
  "region": "north_america"
}
```

---

### Next.js API (Port 3000)

#### Light Language Translation
```bash
POST /api/v1/light-language/translate
Authorization: Bearer YOUR_API_KEY

{
  "text": "Hello World",
  "category": "technology",
  "format": "full",
  "enable_quantum": true
}
```

#### Colors API
```bash
GET /api/v1/light-language/colors?text=Hello
Authorization: Bearer YOUR_API_KEY
```

#### Binary Encoding
```bash
POST /api/v1/light-language/binary
Authorization: Bearer YOUR_API_KEY

{
  "data": "48656c6c6f"
}
```

---

## 🔬 Quantum Optimization

### Diamond NV Centers

The API is optimized for **nitrogen-vacancy centers in diamond** - the leading quantum memory technology.

**Key Parameters:**
- **Zero-phonon line**: 637nm (primary storage wavelength)
- **Violet sideband**: <635nm (initialization)
- **Red sideband**: >640nm (readout)
- **Coherence time**: ~100μs at room temperature
- **Storage time**: Seconds (with spin echo)

### Example Response (Quantum Mode)

```json
{
  "success": true,
  "text": "QUANTUM",
  "quantum_data": {
    "nv_center_states": [...],
    "total_states": 7,
    "estimated_storage_time": 700000
  },
  "nv_transitions": {
    "zero_phonon_count": 3,
    "violet_sideband_count": 2,
    "red_sideband_count": 2
  },
  "programming_instructions": {
    "primary_wavelength": "637nm (zero-phonon line)",
    "pulse_sequence": "7 pulses",
    "estimated_storage_time": "700000μs",
    "coherence_time": "~100μs at room temperature"
  }
}
```

---

## 🌐 Universal Communication Architecture

```
┌─────────────────────────────────────────────┐
│  Any Computer (Classical or Quantum)        │
│  - Web Browser                              │
│  - Server                                   │
│  - IoT Device                               │
│  - Quantum Computer                         │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
      ┌───────────────────────┐
      │   LUXBIN Light API    │
      │   (Choose One)        │
      ├───────────────────────┤
      │ Python FastAPI        │ ← Quantum-optimized
      │ :8000                 │
      │                       │
      │ Next.js API           │ ← Web-friendly
      │ :3000                 │
      └───────────┬───────────┘
                  │
                  ↓
      ┌───────────────────────┐
      │ Light Language Core   │
      │ (Python Library)      │
      └───────────┬───────────┘
                  │
                  ↓
    ┌─────────────────────────────┐
    │   Photonic Encoding          │
    │   - 400-700nm wavelengths    │
    │   - Diamond NV centers       │
    │   - Ion trap control         │
    │   - Satellite lasers         │
    └─────────────────────────────┘
```

---

## 💻 Code Examples

### Python Client

```python
import requests

API_KEY = "luxb_your_api_key_here"
BASE_URL = "http://localhost:8000"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Quantum encoding for NV centers
response = requests.post(
    f"{BASE_URL}/v1/quantum/encode",
    headers=headers,
    json={
        "text": "QUANTUM MESSAGE",
        "use_grammar": True,
        "nv_center_type": "diamond"
    }
)

quantum_data = response.json()
print(f"NV Center States: {quantum_data['quantum_data']['total_states']}")
print(f"Storage Time: {quantum_data['programming_instructions']['estimated_storage_time']}")
```

### JavaScript/TypeScript Client

```typescript
const API_KEY = "luxb_your_api_key_here";
const BASE_URL = "http://localhost:3000";

const response = await fetch(`${BASE_URL}/api/v1/light-language/translate`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    text: "Hello Quantum World",
    enable_quantum: true
  })
});

const data = await response.json();
console.log("Photonic Sequence:", data.photonicSequence);
```

### cURL Example

```bash
# Quantum-optimized translation
curl -X POST http://localhost:8000/v1/translate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "QUANTUM COMPUTING",
    "enable_quantum": true,
    "format": "full"
  }' | python3 -m json.tool
```

---

## 🛠️ Development

### Start Python API Server

```bash
cd ~/luxbin-light-language

# Install dependencies
pip3 install -r requirements.txt

# Start server
python3 light_language_api.py

# Or with custom port
uvicorn light_language_api:app --host 0.0.0.0 --port 8000 --reload
```

### Start Next.js API Server

```bash
cd ~/luxbin-app

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
npm start
```

---

## 🔒 API Key Environment Variables

### Python FastAPI

```bash
export LUXBIN_API_KEYS="key1,key2,key3"
python3 light_language_api.py
```

### Next.js App

API keys are stored in `.luxbin-data/api-keys.json` (file-based storage)

---

## 📊 Rate Limits

Default limits per API key:
- **60 requests per minute**
- **10,000 requests per day**

Configure in API key dashboard or modify in code.

---

## 🌟 Features

| Feature | Python API | Next.js API |
|---------|------------|-------------|
| Quantum NV Center Optimization | ✅ | ✅ |
| Ion Trap Control | ✅ | ❌ |
| Satellite Communication | ✅ | ❌ |
| Grammar-Aware Encoding | ✅ | ✅ |
| Binary Compression | ✅ | ✅ |
| API Key Auth | ✅ | ✅ |
| Rate Limiting | ✅ | ✅ |
| Interactive Docs | ✅ (Swagger) | ❌ |
| Web Dashboard | ❌ | ✅ |

---

## 🤝 Support

- **Documentation**: http://localhost:8000/docs (FastAPI)
- **Developer Portal**: http://localhost:3000/developers (Next.js)
- **GitHub**: https://github.com/mermaidnicheboutique-code/luxbin-light-language

---

## 🌈 Mission

**LUXBIN Light Language enables universal computer communication through photonic encoding.**

Optimized for quantum computers using diamond NV centers, but accessible to all computers through simple HTTP APIs.

**Developed by Nicheai - Pioneering Sustainable Quantum Computing**

---

*Ready to connect all computers through light!* ✨
