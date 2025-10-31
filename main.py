"""
RainGuard Protocol - Real-Time Simulation Dashboard
FastAPI Backend for AI-Powered Agricultural Insurance System
"""
import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

app = FastAPI(title="RainGuard Protocol Simulation")

# African regions from dataset
AFRICAN_REGIONS = [
    {"name": "Ethiopia South", "lat": 6.5, "lon": 38.5, "variability": 223.87},
    {"name": "Ghana Northern", "lat": 9.5, "lon": -1.0, "variability": 251.26},
    {"name": "Kenya Western", "lat": 0.5, "lon": 34.5, "variability": 192.83},
    {"name": "Malawi South", "lat": -15.5, "lon": 35.0, "variability": 281.38},
    {"name": "Nigeria North", "lat": 11.5, "lon": 8.5, "variability": 397.43},
    {"name": "Tanzania Central", "lat": -6.0, "lon": 35.0, "variability": 249.05},
    {"name": "Uganda Central", "lat": 1.0, "lon": 32.5, "variability": 203.23},
    {"name": "Zambia East", "lat": -13.5, "lon": 32.5, "variability": 283.07}
]

# Simulated farmer database (Solana addresses)
FARMERS_DB = {}

# Active connections
active_connections: List[WebSocket] = []


class WeatherData(BaseModel):
    region: str
    temperature: float
    rainfall: float
    drought_probability: float
    timestamp: str


class FarmerRegistration(BaseModel):
    farmer_id: str
    name: str
    region: str
    location: Dict[str, float]
    wallet_address: str
    sum_insured: float
    registered_at: str


async def broadcast(message: dict):
    """Broadcast message to all connected clients"""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            pass


def generate_solana_address():
    """Generate realistic Solana wallet address"""
    chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for _ in range(44))


def generate_tx_signature():
    """Generate Solana transaction signature"""
    chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for _ in range(88))


def initialize_farmers():
    """Initialize simulated farmer database"""
    african_names = [
        "Kofi Mensah", "Amara Okonkwo", "Jabari Nkosi", "Nia Kamau", "Kwame Asante",
        "Zuri Mwangi", "Sefu Banda", "Imani Tembo", "Desta Alemu", "Fatima Diallo",
        "Chidi Eze", "Ayana Getachew", "Tendai Moyo", "Naledi Khumalo", "Abasi Mutua",
        "Zara Kimani", "Babatunde Adeyemi", "Thandiwe Ngcobo", "Jelani Okello", "Mariam Keita"
    ]
    
    for i, name in enumerate(african_names):
        region = random.choice(AFRICAN_REGIONS)
        farmer_id = str(uuid.uuid4())
        FARMERS_DB[farmer_id] = {
            "farmer_id": farmer_id,
            "name": name,
            "region": region["name"],
            "location": {
                "lat": region["lat"] + random.uniform(-0.5, 0.5),
                "lon": region["lon"] + random.uniform(-0.5, 0.5)
            },
            "wallet_address": generate_solana_address(),
            "sum_insured": random.randint(200, 500),
            "registered_at": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            "email": f"{name.lower().replace(' ', '.')}@farmer.africa",
            "contract_address": generate_solana_address(),
            "status": "active"
        }


async def simulate_weather_monitoring():
    """Simulate continuous weather data monitoring"""
    while True:
        try:
            # Random region
            region = random.choice(AFRICAN_REGIONS)
            
            # Generate weather data
            temp = random.uniform(18, 34)
            rainfall = max(0, random.gauss(5.3, 22.2))  # From dataset statistics
            
            # Calculate drought probability (higher when rainfall is low)
            drought_prob = 0.0
            if rainfall < 0.27:  # Drought threshold from dataset
                drought_prob = random.uniform(0.65, 0.95)
            elif rainfall < 2.0:
                drought_prob = random.uniform(0.30, 0.70)
            else:
                drought_prob = random.uniform(0.05, 0.30)
            
            weather_data = {
                "type": "weather_update",
                "data": {
                    "region": region["name"],
                    "location": {"lat": region["lat"], "lon": region["lon"]},
                    "temperature": round(temp, 2),
                    "rainfall": round(rainfall, 2),
                    "drought_probability": round(drought_prob, 3),
                    "timestamp": datetime.now().isoformat(),
                    "status": "drought_detected" if drought_prob > 0.70 else "normal"
                }
            }
            
            await broadcast(weather_data)
            
            # If drought detected, trigger insurance flow
            if drought_prob > 0.70:
                await process_drought_detection(region, drought_prob)
            
            # Wait 2-4 seconds before next update (simulated 6-hour intervals)
            await asyncio.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Weather monitoring error: {e}")
            await asyncio.sleep(2)


async def process_drought_detection(region: dict, drought_prob: float):
    """Process drought detection and trigger insurance claims"""
    await asyncio.sleep(0.5)
    
    # Find farmers in affected region
    affected_farmers = [
        f for f in FARMERS_DB.values() 
        if f["region"] == region["name"]
    ]
    
    if not affected_farmers:
        await broadcast({
            "type": "no_farmers",
            "data": {
                "region": region["name"],
                "message": "No registered farmers in affected area",
                "timestamp": datetime.now().isoformat()
            }
        })
        return
    
    # Process each affected farmer
    for farmer in affected_farmers[:3]:  # Limit to 3 for demo
        await process_farmer_claim(farmer, drought_prob)
        await asyncio.sleep(1)


async def process_farmer_claim(farmer: dict, drought_prob: float):
    """Process individual farmer insurance claim"""
    
    # Step 1: Farmer Detection
    await broadcast({
        "type": "farmer_detected",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "name": farmer["name"],
            "region": farmer["region"],
            "location": farmer["location"],
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(0.8)
    
    # Step 2: Blockchain Verification
    await broadcast({
        "type": "blockchain_verification",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "wallet_address": farmer["wallet_address"],
            "contract_address": farmer["contract_address"],
            "status": "verifying",
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(1.2)
    
    # Verification success
    await broadcast({
        "type": "blockchain_verified",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "wallet_address": farmer["wallet_address"],
            "status": "verified",
            "transaction_signature": generate_tx_signature(),
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(0.5)
    
    # Step 3: Calculate Pre-emptive Payout (50% of coverage)
    preemptive_fraction = 0.5
    sum_insured = farmer["sum_insured"]
    
    # Formula from paper: S × κ × (P(Drought) - θ_pre) / (1 - θ_pre)
    theta_pre = 0.85
    if drought_prob > theta_pre:
        preemptive_payout = sum_insured * preemptive_fraction * ((drought_prob - theta_pre) / (1 - theta_pre))
    else:
        preemptive_payout = 0
    
    preemptive_payout = round(preemptive_payout, 2)
    
    await broadcast({
        "type": "payout_calculation",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "sum_insured": sum_insured,
            "drought_probability": drought_prob,
            "preemptive_payout": preemptive_payout,
            "remaining_coverage": round(sum_insured - preemptive_payout, 2),
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(1.0)
    
    # Step 4: Execute Pre-emptive Disbursement
    if preemptive_payout > 0:
        tx_sig = generate_tx_signature()
        await broadcast({
            "type": "preemptive_disbursement",
            "data": {
                "farmer_id": farmer["farmer_id"],
                "name": farmer["name"],
                "amount": preemptive_payout,
                "wallet_address": farmer["wallet_address"],
                "transaction_signature": tx_sig,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
        })
        await asyncio.sleep(0.8)
        
        # Step 5: Send Email Notification
        await broadcast({
            "type": "email_sent",
            "data": {
                "farmer_id": farmer["farmer_id"],
                "email": farmer["email"],
                "subject": "RainGuard: Pre-emptive Funds Disbursed - Action Required",
                "amount": preemptive_payout,
                "action_required": "Submit crop photos for final verification",
                "deadline": (datetime.now() + timedelta(days=14)).isoformat(),
                "timestamp": datetime.now().isoformat()
            }
        })
        await asyncio.sleep(1.5)
        
        # Step 6: Simulate Farmer Photo Submission (after delay)
        await simulate_photo_submission(farmer, sum_insured - preemptive_payout)


async def simulate_photo_submission(farmer: dict, remaining_amount: float):
    """Simulate farmer submitting crop photos"""
    await asyncio.sleep(random.uniform(2, 4))
    
    # Photo submission
    num_photos = random.randint(3, 6)
    await broadcast({
        "type": "photo_submission",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "name": farmer["name"],
            "num_photos": num_photos,
            "location": farmer["location"],
            "timestamp": datetime.now().isoformat(),
            "status": "received"
        }
    })
    await asyncio.sleep(1.0)
    
    # AI Analysis using PlantVillage model
    await broadcast({
        "type": "ai_analysis_started",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "model": "EfficientNetV2B0-PlantVillage",
            "status": "analyzing",
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(2.0)
    
    # AI Results
    health_classes = ["healthy", "minor", "moderate", "major", "severe"]
    detected_class = random.choice(health_classes[2:])  # Moderate to severe
    confidence = random.uniform(0.82, 0.94)
    yield_loss = random.uniform(25, 65)
    
    await broadcast({
        "type": "ai_analysis_completed",
        "data": {
            "farmer_id": farmer["farmer_id"],
            "health_classification": detected_class,
            "confidence": round(confidence, 3),
            "yield_loss_percent": round(yield_loss, 1),
            "damage_verified": True,
            "timestamp": datetime.now().isoformat()
        }
    })
    await asyncio.sleep(1.0)
    
    # Final Settlement
    if detected_class in ["moderate", "major", "severe"]:
        # Release remaining funds
        tx_sig = generate_tx_signature()
        await broadcast({
            "type": "final_settlement",
            "data": {
                "farmer_id": farmer["farmer_id"],
                "name": farmer["name"],
                "amount": round(remaining_amount, 2),
                "wallet_address": farmer["wallet_address"],
                "transaction_signature": tx_sig,
                "total_payout": round(farmer["sum_insured"], 2),
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
        })
        
        # Success notification
        await asyncio.sleep(0.5)
        await broadcast({
            "type": "claim_completed",
            "data": {
                "farmer_id": farmer["farmer_id"],
                "name": farmer["name"],
                "total_payout": round(farmer["sum_insured"], 2),
                "status": "success",
                "message": "Full insurance claim processed successfully",
                "timestamp": datetime.now().isoformat()
            }
        })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    # Send initial system status
    await websocket.send_json({
        "type": "system_ready",
        "data": {
            "message": "RainGuard Protocol Simulation Active",
            "regions": len(AFRICAN_REGIONS),
            "registered_farmers": len(FARMERS_DB),
            "timestamp": datetime.now().isoformat()
        }
    })
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    initialize_farmers()
    # Start weather monitoring in background
    asyncio.create_task(simulate_weather_monitoring())


@app.get("/api/farmers")
async def get_farmers():
    """Get registered farmers"""
    return {"farmers": list(FARMERS_DB.values())}


@app.get("/api/regions")
async def get_regions():
    """Get African regions"""
    return {"regions": AFRICAN_REGIONS}


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_farmers": len(FARMERS_DB),
        "total_regions": len(AFRICAN_REGIONS),
        "active_claims": 0,
        "total_disbursed": 0
    }


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    """Serve the dashboard"""
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

