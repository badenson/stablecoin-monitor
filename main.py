import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from dotenv import load_dotenv
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stablecoin_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
STABLECOIN_SYMBOL = "usd-coin"  # CoinGecko ID for USDC
TARGET_PRICE = 1.00  # Target price in USD
THRESHOLD_PERCENT = 0.5  # Alert if price deviates by more than 0.5%
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)

# Email configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def get_stablecoin_price():
    """
    Fetch the current price of the stablecoin from CoinGecko API.
    Returns the price in USD.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={STABLECOIN_SYMBOL}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        price = data.get(STABLECOIN_SYMBOL, {}).get("usd")
        if price is None:
            logger.error(f"Failed to get price for {STABLECOIN_SYMBOL}")
            return None
        return float(price)
    except Exception as e:
        logger.error(f"Error fetching price: {str(e)}")
        return None

def calculate_deviation(current_price):
    """
    Calculate the percentage deviation from the target price.
    """
    if current_price is None:
        return None
    deviation = ((current_price - TARGET_PRICE) / TARGET_PRICE) * 100
    return deviation

def send_alert(current_price, deviation):
    """
    Send an email alert when the price deviation exceeds the threshold.
    """
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.warning("Email configuration incomplete. Alert not sent.")
        return False
    try:
        subject = f"ALERT: USDC Price Deviation"
        body = f"""
        STABLECOIN PRICE ALERT

        Stablecoin: USDC
        Current Price: ${current_price:.6f}
        Target Price: ${TARGET_PRICE:.2f}
        Deviation: {deviation:.2f}%

        This deviation exceeds your configured threshold of {THRESHOLD_PERCENT}%.
        """
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Alert sent to {EMAIL_RECIPIENT}")
        return True
    except Exception as e:
        logger.error(f"Error sending alert: {str(e)}")
        return False

def monitor_stablecoin():
    """
    Main function to monitor the stablecoin price.
    """
    logger.info(f"Starting monitoring for USDC with target price ${TARGET_PRICE}")
    logger.info(f"Alert threshold: {THRESHOLD_PERCENT}%")

    while True:
        try:
            current_price = get_stablecoin_price()
            if current_price is not None:
                deviation = calculate_deviation(current_price)
                logger.info(f"USDC price: ${current_price:.6f}, Deviation: {deviation:.2f}%")
                if abs(deviation) > THRESHOLD_PERCENT:
                    logger.warning(f"Deviation exceeds threshold: {deviation:.2f}%")
                    send_alert(current_price, deviation)
        time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
        break
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_stablecoin()