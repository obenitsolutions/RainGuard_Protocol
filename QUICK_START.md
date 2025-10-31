# RainGuard Protocol Simulation - Quick Start Guide

## Fastest Way to Run (3 Steps)

### Option 1: Using the run script

```bash
cd /Users/macbookpro/Documents/projects/Research/RainGuard_Protocol/docs/simulation
./run.sh
```

### Option 2: Manual start

```bash
# Step 1: Activate virtual environment
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate

# Step 2: Navigate to simulation directory
cd /Users/macbookpro/Documents/projects/Research/RainGuard_Protocol/docs/simulation

# Step 3: Run the server
python main.py
```

### Option 3: Using uvicorn

```bash
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate
cd /Users/macbookpro/Documents/projects/Research/RainGuard_Protocol/docs/simulation
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Access the Dashboard

Open your browser and go to:
**http://localhost:8000**

## What You'll See

The dashboard displays 8 panels showing real-time simulation:

1. **Weather Oracle Monitoring** (Top Left)
   - Live weather data from 8 African regions
   - Temperature, rainfall, drought probability
   - Automatic drought detection (>70% probability)

2. **Blockchain Verification** (Top Right)
   - Solana wallet address verification
   - Contract address validation
   - Transaction signatures

3. **Active Claims Processing** (Middle Left)
   - Real-time claim status
   - 5-step progress tracking
   - Payout amounts

4. **Fund Disbursement** (Middle Right)
   - Pre-emptive payouts (40-60%)
   - Final settlements
   - Transaction details

5. **Email Notifications** (Bottom Left)
   - Automated farmer notifications
   - Action required reminders
   - Deadline tracking

6. **AI Crop Analysis** (Bottom Right)
   - Photo submissions
   - PlantVillage model analysis
   - Health classification & yield loss

7. **System Activity Log** (Full Left Column)
   - Complete event timeline
   - Status updates
   - Error tracking

8. **Live Statistics** (Bottom Right)
   - Weather update count
   - Total claims processed
   - Total funds disbursed
   - Completed claims

## Simulation Flow

Watch as the system automatically:
1. Monitors weather data every few seconds
2. Detects drought conditions (>70% probability)
3. Identifies farmers in affected regions
4. Verifies their blockchain registration
5. Calculates pre-emptive payout (50% of coverage)
6. Disburses funds to Solana wallets
7. Sends email notifications
8. Waits for photo submissions
9. Runs AI analysis on crop photos
10. Verifies damage and releases remaining funds

## Features

- **Real-time Updates**: WebSocket for instant updates
- **Professional UI**: Silicon Valley-style dashboard
- **Realistic Data**: Based on actual research paper
- **Multiple Activities**: 8 panels updating simultaneously
- **African Regions**: Ethiopia, Ghana, Kenya, Malawi, Nigeria, Tanzania, Uganda, Zambia
- **Smart Contracts**: Solana blockchain integration
- **AI Model**: EfficientNetV2B0-PlantVillage

## Stopping the Simulation

Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

**Problem**: Port 8000 already in use
**Solution**:
```bash
lsof -ti:8000 | xargs kill -9
```

**Problem**: Dependencies missing
**Solution**:
```bash
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate
pip install -r requirements.txt
```

**Problem**: WebSocket not connecting
**Solution**: 
- Refresh the browser
- Check that the server is running
- Ensure no firewall is blocking port 8000

## Performance Tips

- Use Chrome or Firefox for best performance
- Close unused browser tabs
- The simulation runs continuously - stop and restart if needed
- Each refresh starts fresh data streams

## Technical Details

- **Backend**: FastAPI with WebSocket support
- **Frontend**: Vue.js 3 (CDN version)
- **Real-time**: WebSocket for bidirectional communication
- **Data**: Simulated based on real climate dataset
- **Blockchain**: Solana wallet/contract address format
- **AI**: PlantVillage model simulation

## Research Integration

The simulation demonstrates concepts from the research paper:
- Pre-emptive disbursement (40-60% coverage)
- Dual-oracle architecture (weather + yield)
- Basis risk reduction (70% drought threshold)
- Sub-12-hour settlement timing
- Solana blockchain deterministic execution
- AI-powered crop damage assessment

## Next Steps

1. Run the simulation and observe the flow
2. Notice how drought detection triggers the entire workflow
3. Watch multiple farmers being processed simultaneously
4. See the real-time statistics update
5. Monitor the activity log for complete event timeline

---

**Dashboard URL**: http://localhost:8000
**Default Port**: 8000
**WebSocket**: ws://localhost:8000/ws

