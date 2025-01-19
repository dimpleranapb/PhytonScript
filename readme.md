# Data Collection Script for Top Crypto Token Traders

This script is designed to scrape wallet addresses of the top traders for the top 20 meme coins in the Solana ecosystem. The data is collected from DexScreener and saved into a CSV file. The script uses Selenium and the Chrome WebDriver to automate the process.

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.x
- pip (Python package manager)

### Dependencies

Install the required Python packages by running:

```bash
pip install selenium webdriver-manager
```

Additionally, ensure that you have a Chrome browser installed on your system.

## How to Use

### Start Chrome with Remote Debugging

You need to run Chrome with the `--remote-debugging-port=9222` flag. This allows the script to connect to the open Chrome instance.

To start Chrome with remote debugging:

1. Close all open Chrome windows.
2. Open a terminal/command prompt and run:

```bash
chrome --remote-debugging-port=9222
```

### Run the Script

Once Chrome is running with remote debugging enabled, execute the Python script:

```bash
python collect_wallet_addresses.py
```

### Output

The script will collect wallet addresses from the top 20 meme coins and save them into a CSV file named `top_traders_account_numbers.csv`. The CSV will contain a list of wallet addresses under the header "Account Number".

### Retries

The script will automatically retry up to 3 times if it encounters any issues with a coin's page or the wallet links.