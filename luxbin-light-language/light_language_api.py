#!/usr/bin/env python3
"""
LUXBIN Light Language API Server
FastAPI server for universal quantum communication via photonic encoding

Developed by Nicheai - Quantum Computing Infrastructure
Optimized for Diamond NV Center Quantum Computers

Usage:
    python light_language_api.py

    Or with uvicorn:
    uvicorn light_language_api:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
from luxbin_light_converter import LuxbinLightConverter
import time

# Initialize FastAPI app
app = FastAPI(
    title="LUXBIN Light Language API",
    description="Universal Quantum Communication Protocol - Optimized for Diamond NV Centers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication (simple implementation)
API_KEYS = os.getenv("LUXBIN_API_KEYS", "").split(",")
if not API_KEYS or API_KEYS == [""]:
    print("⚠️  WARNING: No API keys configured. Set LUXBIN_API_KEYS environment variable.")
    API_KEYS = ["demo_key_for_testing"]  # Demo key for testing

def verify_api_key(authorization: Optional[str] = Header(None)) -> str:
    """Verify API key from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format. Use: Bearer <api_key>")

    api_key = authorization.replace("Bearer ", "")

    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key

# Request/Response Models
class TranslateRequest(BaseModel):
    text: str = Field(..., description="Text to convert to photonic light sequence")
    category: Optional[str] = Field(None, description="Optional category for grammar analysis")
    enable_quantum: bool = Field(True, description="Enable quantum NV center optimization (default: True)")
    enable_satellite: bool = Field(False, description="Enable satellite laser communication")
    format: str = Field("full", description="Response format: 'full', 'summary', or 'compact'")

class QuantumEncodeRequest(BaseModel):
    text: str = Field(..., description="Text to encode for quantum NV centers")
    use_grammar: bool = Field(True, description="Use grammar-aware encoding")
    nv_center_type: str = Field("diamond", description="NV center type: 'diamond' or 'custom'")

class IonTrapControlRequest(BaseModel):
    command: str = Field(..., description="Quantum gate command (e.g., 'HADAMARD GATE', 'CNOT GATE')")
    ion_type: Optional[str] = Field(None, description="Specific ion type: 'calcium_40', 'strontium_88', 'ytterbium_171', 'rubidium_87'")

class BinaryEncodeRequest(BaseModel):
    binary_data: str = Field(..., description="Hex-encoded binary data")
    use_compression: bool = Field(True, description="Apply run-length compression")
    enable_quantum: bool = Field(True, description="Enable quantum mode")

class SatelliteLaserRequest(BaseModel):
    data: str = Field(..., description="Data to transmit via satellite laser")
    region: str = Field("global", description="Target region for transmission")

# API Routes

@app.get("/")
async def root():
    """API information and status"""
    return {
        "name": "LUXBIN Light Language API",
        "version": "1.0.0",
        "description": "Universal Quantum Communication Protocol",
        "quantum_optimized": True,
        "nv_center_ready": True,
        "endpoints": {
            "translate": "/v1/translate",
            "quantum_encode": "/v1/quantum/encode",
            "ion_trap": "/v1/quantum/ion-trap",
            "binary": "/v1/binary/encode",
            "satellite": "/v1/satellite/transmit"
        },
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "quantum_systems": "operational"
    }

@app.post("/v1/translate")
async def translate_to_light(
    request: TranslateRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Translate text to photonic light sequence

    Optimized for diamond NV center quantum computers by default.
    Falls back to classical mode if quantum is disabled.
    """
    try:
        # Create converter with quantum mode enabled by default
        converter = LuxbinLightConverter(
            enable_quantum=request.enable_quantum,
            enable_satellite=request.enable_satellite
        )

        # Use grammar-aware light show for text
        if request.category or request.text.split():
            light_show = converter.create_grammar_light_show(request.text)
        else:
            binary_data = request.text.encode('utf-8')
            light_show = converter.create_light_show(binary_data)

        # Format response based on request
        if request.format == "summary":
            return {
                "success": True,
                "text": request.text,
                "quantum_mode": request.enable_quantum,
                "total_characters": len(request.text),
                "total_duration": light_show['total_duration'],
                "wavelength_range": "400-700nm (visible spectrum)",
                "nv_center_optimized": request.enable_quantum,
                "light_sequence_length": len(light_show['light_sequence'])
            }
        elif request.format == "compact":
            return {
                "success": True,
                "light_sequence": light_show['light_sequence'][:10],  # First 10 only
                "total_length": len(light_show['light_sequence']),
                "quantum_data": light_show['quantum_data']
            }
        else:  # full
            return {
                "success": True,
                "text": request.text,
                "quantum_mode": request.enable_quantum,
                "satellite_mode": request.enable_satellite,
                "light_show": light_show,
                "api_version": "1.0.0",
                "timestamp": time.time()
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/v1/quantum/encode")
async def quantum_encode(
    request: QuantumEncodeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Quantum-optimized encoding specifically for diamond NV center systems

    This endpoint is optimized for:
    - Diamond nitrogen-vacancy (NV) centers
    - Zero-phonon line at ~637nm
    - Phonon sidebands (violet <635nm, red >640nm)
    - Quantum state initialization and readout
    """
    try:
        # Always enable quantum mode for this endpoint
        converter = LuxbinLightConverter(enable_quantum=True)

        if request.use_grammar:
            light_show = converter.create_grammar_light_show(request.text)
        else:
            binary_data = request.text.encode('utf-8')
            light_show = converter.create_light_show(binary_data)

        # Extract NV center specific data
        nv_data = light_show['quantum_data']

        # Categorize wavelengths for NV centers
        nv_transitions = {
            'zero_phonon': [],
            'violet_sideband': [],
            'red_sideband': []
        }

        for item in light_show['light_sequence']:
            wavelength = item['wavelength_nm']
            if 635 <= wavelength <= 640:
                nv_transitions['zero_phonon'].append(item)
            elif wavelength < 635:
                nv_transitions['violet_sideband'].append(item)
            else:
                nv_transitions['red_sideband'].append(item)

        return {
            "success": True,
            "text": request.text,
            "nv_center_type": request.nv_center_type,
            "quantum_data": nv_data,
            "nv_transitions": {
                "zero_phonon_count": len(nv_transitions['zero_phonon']),
                "violet_sideband_count": len(nv_transitions['violet_sideband']),
                "red_sideband_count": len(nv_transitions['red_sideband'])
            },
            "light_sequence": light_show['light_sequence'],
            "programming_instructions": {
                "primary_wavelength": "637nm (zero-phonon line)",
                "pulse_sequence": f"{nv_data['total_states']} pulses",
                "estimated_storage_time": f"{nv_data['estimated_storage_time']}μs",
                "coherence_time": "~100μs at room temperature"
            },
            "timestamp": time.time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quantum encoding failed: {str(e)}")

@app.post("/v1/quantum/ion-trap")
async def ion_trap_control(
    request: IonTrapControlRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Ion trap quantum computer control interface

    Maps LUXBIN light sequences to real atomic transitions:
    - 397nm: Calcium-40 single qubit gates
    - 422nm: Strontium-88 state preparation
    - 729nm: Ytterbium-171 two-qubit gates
    - 854nm: Rubidium-87 cooling cycles
    """
    try:
        converter = LuxbinLightConverter(enable_quantum=True)
        light_show = converter.create_grammar_light_show(request.command)

        # Extract ion trap specific operations
        ion_operations = []
        for item in light_show['light_sequence']:
            if 'quantum_operation' in item:
                ion_operations.append({
                    'character': item['character'],
                    'wavelength': item['wavelength_nm'],
                    'operation': item['quantum_operation']['operation'],
                    'ion_type': item['quantum_operation']['ion_type'],
                    'transition': item['quantum_operation']['transition'],
                    'duration': item['duration_s'],
                    'control_parameters': item['quantum_operation']['control_parameters']
                })

        return {
            "success": True,
            "command": request.command,
            "ion_operations": ion_operations,
            "total_operations": len(ion_operations),
            "execution_time": sum(op['duration'] for op in ion_operations),
            "hardware_ready": True,
            "timestamp": time.time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ion trap control failed: {str(e)}")

@app.post("/v1/binary/encode")
async def binary_encode(
    request: BinaryEncodeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Encode raw binary data to light sequence with optional compression

    Useful for non-text data: images, executables, encrypted data, etc.
    """
    try:
        # Convert hex string to binary
        binary_data = bytes.fromhex(request.binary_data)

        converter = LuxbinLightConverter(enable_quantum=request.enable_quantum)
        light_show = converter.create_binary_light_show(binary_data, use_compression=request.use_compression)

        return {
            "success": True,
            "original_size": light_show['original_size'],
            "compressed_size": light_show['compressed_size'],
            "compression_ratio": light_show['data_compression'],
            "quantum_mode": request.enable_quantum,
            "light_sequence": light_show['light_sequence'],
            "total_duration": light_show['total_duration'],
            "quantum_data": light_show['quantum_data'],
            "timestamp": time.time()
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid hex data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Binary encoding failed: {str(e)}")

@app.post("/v1/satellite/transmit")
async def satellite_transmit(
    request: SatelliteLaserRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Encode data for satellite laser communication

    Uses Starlink-style laser constellation networking with LUXBIN encoding.
    Supports global photonic internet infrastructure.
    """
    try:
        converter = LuxbinLightConverter(enable_satellite=True)
        light_show = converter.create_grammar_light_show(request.data)

        # Extract satellite operations
        satellite_ops = []
        for item in light_show['light_sequence']:
            if 'satellite_operation' in item:
                satellite_ops.append({
                    'character': item['character'],
                    'wavelength': item['wavelength_nm'],
                    'operation': item['satellite_operation']['operation'],
                    'protocol': item['satellite_operation']['protocol'],
                    'data_rate': item['satellite_operation']['data_rate'],
                    'duration': item['duration_s']
                })

        return {
            "success": True,
            "data": request.data,
            "region": request.region,
            "satellite_operations": satellite_ops,
            "total_operations": len(satellite_ops),
            "transmission_time": sum(op['duration'] for op in satellite_ops),
            "global_coverage": True,
            "timestamp": time.time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite transmission failed: {str(e)}")

# Run with: uvicorn light_language_api:app --reload
if __name__ == "__main__":
    import uvicorn
    print("🌈 Starting LUXBIN Light Language API Server")
    print("🔬 Quantum Mode: ENABLED (Diamond NV Centers)")
    print("📡 Universal Communication: READY")
    print("🔑 API Key: demo_key_for_testing (for testing only)")
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Interactive API: http://localhost:8000/redoc\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
