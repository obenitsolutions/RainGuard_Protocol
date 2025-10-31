# RainGuard Protocol - Live Simulation Dashboard

This is a professional real-time simulation dashboard for the RainGuard Protocol AI-Powered Deterministic Parametric Agricultural Insurance System.

## 📚 Research Paper & Resources

- **📄 Research Paper (DOI)**: [https://doi.org/10.5281/zenodo.17490459](https://doi.org/10.5281/zenodo.17490459)
- **🎥 Demo Video**: [Watch Simulation Demo](https://drive.google.com/file/d/1vDbZd8B8dn3xk1vlnsJvxWduxSS44ZGM/view?usp=sharing)
- **📦 Repository**: https://github.com/obenitsolutions/RainGuard_Protocol
- **🐛 Issues & Support**: https://github.com/obenitsolutions/RainGuard_Protocol/issues

## Overview

The simulation demonstrates the complete insurance workflow:
1. **Weather Oracle Monitoring** - Real-time satellite data monitoring across 8 African regions
2. **Drought Detection** - AI-powered drought probability calculation
3. **Farmer Detection** - Identifying registered farmers in affected areas
4. **Blockchain Verification** - Verifying farmer registration on Solana blockchain
5. **Pre-emptive Disbursement** - Calculating and disbursing 40-60% of coverage before event
6. **Email Notification** - Automated farmer notification system
7. **Photo Submission** - Farmers submit crop photos
8. **AI Crop Analysis** - PlantVillage model analyzes crop health
9. **Final Settlement** - Remaining funds disbursed based on verified damage

## Features

- **Real-time WebSocket updates** - Live data streaming
- **Professional Silicon Valley UI** - Clean, modern dashboard design
- **Multiple simultaneous activities** - 8 panels showing different system components
- **Animated updates** - Smooth transitions and visual feedback
- **Solana blockchain integration** - Realistic wallet addresses and transactions
- **African regions** - 8 regions from actual climate dataset
- **AI model simulation** - EfficientNetV2B0-PlantVillage model

## Technology Stack

- **Backend**: FastAPI + WebSockets
- **Frontend**: Vue.js 3 (CDN)
- **Styling**: Custom CSS (Silicon Valley inspired)
- **Real-time**: WebSocket for live updates

## Quick Start

### Simple Run (Single Command)

```bash
# Activate virtual environment
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate

# Navigate to simulation directory
cd /Users/macbookpro/Documents/projects/Research/RainGuard_Protocol/docs/simulation

# Run the simulation
python main.py
```

Then open your browser to: **http://localhost:8000**

### Alternative (Using uvicorn directly)

```bash
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate
cd /Users/macbookpro/Documents/projects/Research/RainGuard_Protocol/docs/simulation
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Dashboard Panels

1. **Weather Oracle Monitoring** - Live weather data from African regions
2. **Blockchain Verification** - Solana wallet and contract verification
3. **Active Claims Processing** - Real-time claim status tracking
4. **Fund Disbursement** - Pre-emptive and final payments
5. **Email Notifications** - Automated farmer communications
6. **AI Crop Analysis** - Computer vision-based damage assessment
7. **System Activity Log** - Complete event timeline
8. **Live Statistics** - Real-time system metrics

## Data Flow

```
Weather Data → Drought Detection → Farmer Lookup → Blockchain Verification
    ↓
Calculate Payout (50% pre-emptive) → Disburse Funds → Send Email
    ↓
Wait for Photos → AI Analysis (PlantVillage) → Verify Damage
    ↓
Final Settlement (remaining 50%) → Claim Complete
```

## Simulation Details

- **Weather Updates**: Every 2-4 seconds (simulating 6-hour intervals)
- **Drought Threshold**: 70% probability triggers claim
- **Pre-emptive Payout**: 40-60% of coverage (κ = 0.5)
- **Registered Farmers**: 20 simulated farmers across 8 regions
- **AI Confidence**: 82-94% (realistic model performance)
- **Transaction Signatures**: Realistic 88-character Solana signatures
- **Wallet Addresses**: Realistic 44-character Solana addresses

## System Requirements

- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Font Awesome icons)

## Project Structure

```
simulation/
├── main.py              # FastAPI backend with WebSocket
├── static/
│   ├── index.html       # Dashboard HTML
│   ├── styles/
│   │   └── dashboard.css    # Professional styling
│   └── script/
│       ├── app.js           # Vue.js application logic
│       ├── vue.global.prod.js
│       └── axios.min.js
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Endpoints

- `GET /` - Dashboard interface
- `GET /api/farmers` - List registered farmers
- `GET /api/regions` - List African regions
- `GET /api/stats` - System statistics
- `WS /ws` - WebSocket for real-time updates

## Development Notes

- All data is simulated for demonstration purposes
- No actual blockchain transactions are made
- Weather data based on real dataset statistics
- African regions from actual climate analysis
- Farmer names are culturally appropriate African names
- Email addresses follow realistic format

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**WebSocket connection failed:**
- Check that the server is running
- Ensure no firewall is blocking port 8000
- Try refreshing the browser

**Slow performance:**
- Close unused browser tabs
- Check CPU usage
- Reduce number of simultaneous simulations

## Credits

- **Research Paper**: [RainGuard Protocol (DOI: 10.5281/zenodo.17490459)](https://doi.org/10.5281/zenodo.17490459)
- **Demo Video**: [Watch the Simulation Demo](https://drive.google.com/file/d/1vDbZd8B8dn3xk1vlnsJvxWduxSS44ZGM/view?usp=sharing)
- **Climate Data**: CHIRPS satellite data (8 African regions)
- **AI Model**: EfficientNetV2B0 + PlantVillage dataset
- **Blockchain**: Solana network specifications
- **Design**: Professional dashboard inspired by leading tech companies

## License

This work is released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

Attribution is required if you use this code, derivative works, or figures produced by it. Please include ALL of the following in your README, paper, or product docs:

1) Text attribution
   "RainGuard Protocol Simulation (CC BY 4.0). Cite: Mbu, O.E.; Kehinde, O.P.; Ayuk, O.P. (2025). RainGuard Protocol: AI-Powered Deterministic Parametric Agricultural Insurance for African Smallholder Farmers Using Blockchain Coordination."

2) Link to the source repository: https://github.com/obenitsolutions/RainGuard_Protocol

3) Keep this license notice in redistributed or modified copies.

Full license text: see LICENSE file in this folder.

If you deploy or demonstrate this simulation publicly, please add a visible "Powered by RainGuard Protocol (CC BY 4.0)" note on your page.

## How to Cite

Recommended citation (plain text):

Mbu, O. E.; Kehinde, O. P.; Ayuk, O. P. (2025). RainGuard Protocol: AI-Powered Deterministic Parametric Agricultural Insurance for African Smallholder Farmers Using Blockchain Coordination. Software: Simulation Dashboard (v1.0). DOI: [10.5281/zenodo.17490459](https://doi.org/10.5281/zenodo.17490459). Available at: https://github.com/obenitsolutions/RainGuard_Protocol

BibTeX:

@techreport{oben2025rainguard,
  title        = {RainGuard Protocol: AI-Powered Deterministic Parametric Agricultural Insurance for African Smallholder Farmers Using Blockchain Coordination},
  author       = {Oben, Emmanuel Mbu and Kehinde, Olotu Paul and Oben, Peter Ayuk},
  year         = {2025},
  institution  = {OBEN IT Solutions},
  number       = {OBEN-TR-2025-002},
  doi          = {10.5281/zenodo.17490459},
  url          = {https://zenodo.org/records/17490459}
}

