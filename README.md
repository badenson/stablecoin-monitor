```markdown
# Stablecoin Price Monitor

A simple Python application that monitors the price of a stablecoin (USDC) and sends alerts when the price deviates significantly from its peg.

## Features

- Fetches real-time stablecoin prices from CoinGecko API
- Monitors price deviations from the target price (e.g., $1.00)
- Sends email alerts when deviations exceed a configurable threshold
- Logs all activities for monitoring and debugging

## Prerequisites

- Python 3.7 or higher
- Internet connection to access the CoinGecko API
- Email account for sending alerts (Gmail recommended)

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/stablecoin-monitor.git
   cd stablecoin-monitor
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment variables:**
   - Copy the `.env.example` file to `.env`
   - Edit the `.env` file with your email credentials

## Configuration

You can customize the following parameters in `main.py`:

- `STABLECOIN_SYMBOL`: The CoinGecko ID of the stablecoin to monitor (default: "usd-coin" for USDC)
- `TARGET_PRICE`: The target price of the stablecoin (default: 1.00 USD)
- `THRESHOLD_PERCENT`: The percentage deviation that triggers an alert (default: 0.5%)
- `CHECK_INTERVAL`: How often to check the price in seconds (default: 300 seconds / 5 minutes)

## Usage

Run the application:

```bash
python main.py
```

The application will start monitoring the stablecoin price and log information to the console and a log file. If the price deviates by more than the specified threshold, an email alert will be sent.

## Notes for Gmail Users

If you're using Gmail to send alerts, you'll need to:
1. Enable 2-Step Verification for your Google account
2. Generate an App Password for this application
3. Use the App Password in the `.env` file instead of your regular password

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```