# Schedule Optimizer Web Service

A cloud-ready web service for optimizing weekly employee schedule assignments using constraint programming.

## Features

- Upload Excel files with employee schedules, costs, and preferences
- Optimize assignments using Google OR-Tools CP-SAT solver
- Download optimized schedules with complete sanity checks
- Considers availability, preferences, days off, and weekly hour limits
- Web interface for easy file upload/download

## Quick Start

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web service
python app.py
```

Visit http://localhost:8080 in your browser.

### Deploy to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

Quick deploy:
1. Push this repo to GitHub
2. Connect to Render
3. Deploy as Docker service
4. Access your URL and upload Excel files

## Files

- `optimize_schedules_with_sanity.py` - Core optimization engine
- `app.py` - Flask web service
- `Dockerfile` - Container configuration
- `render.yaml` - Render deployment config
- `requirements.txt` - Python dependencies
- `DEPLOYMENT.md` - Detailed deployment guide

## Usage

1. Prepare Excel file with schedule data (see script comments for format)
2. Upload via web interface
3. Wait for optimization (up to 60 seconds)
4. Download optimized results with assignments

## Excel Format Requirements

Your Excel file must include:
- Day sheets (Mon-Sun) with COST, PREF, HOURS data
- Weekly sheet with λ, Max Shifts, Max Hours parameters
- See inline documentation for exact cell ranges

## License

Open source - use freely for your scheduling needs!