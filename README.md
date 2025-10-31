# Binance Futures Trading Bot

A sophisticated Python-based trading bot for Binance Futures (USDT-M) with support for multiple order types, advanced trading strategies, and both CLI and Web interfaces.

## 🎯 Features

### Core Functionality
- ✅ **Market Orders**: Instant execution at current market price
- ✅ **Limit Orders**: Execute at specified price
- ✅ **Stop-Limit Orders**: Stop-loss protection with limit execution
- ✅ **OCO Orders**: One-Cancels-Other (Take Profit + Stop Loss)
- ✅ **TWAP Strategy**: Time-Weighted Average Price execution

### Advanced Features
- 🎨 **Dual Interface**: Web UI and Command-Line Interface
- 📊 **Real-time Logging**: Detailed API request/response logging
- ⚡ **Testnet Support**: Safe testing environment with virtual funds
- 🔒 **Error Handling**: Comprehensive validation and error management
- 📈 **Account Management**: Balance checking and order status tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Binance Futures Testnet account
- API credentials from https://testnet.binancefuture.com

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API keys**:
   - Visit https://testnet.binancefuture.com
   - Login and generate API keys
   - Copy `.env.example` to `.env`
   - Add your keys to `.env`:
   ```env
   API_KEY=your_api_key_here
   API_SECRET=your_secret_key_here
   ```

4. **Run the application**:

   **Web Interface**:
   ```bash
   python app.py
   ```
   Then open http://localhost:5000 in your browser

   **Command-Line Interface**:
   ```bash
   python cli_interface.py
   ```

## 📖 Usage Examples

### Using Web Interface

1. Start the Flask server: `python app.py`
2. Open http://localhost:5000
3. Initialize the bot
4. Select order type and fill in parameters
5. Execute orders and view results

### Using CLI Interface

```bash
python cli_interface.py
```

**Example CLI Session**:
```
=== Binance Trading Bot ===
1. Place Market Order
2. Place Limit Order
3. Place Stop-Limit Order
4. Place OCO Order
5. Execute TWAP Strategy
6. Check Account Balance
7. Check Order Status
8. Exit

Select option: 1
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter quantity: 0.001
```

### Programmatic Usage

```python
from basic_bot import BasicBot
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize bot
bot = BasicBot(
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    testnet=True
)

# Place a market order
order = bot.place_market_order('BTCUSDT', 'BUY', 0.001)
print(f"Order ID: {order['orderId']}")

# Place a limit order
order = bot.place_limit_order('ETHUSDT', 'BUY', 0.1, 2000.0)

# Execute TWAP strategy
result = bot.execute_twap(
    symbol='BTCUSDT',
    side='BUY',
    total_quantity=0.01,
    duration_minutes=10,
    num_orders=5
)

# Check account balance
balance = bot.get_account_balance()
print(balance)
```

## 📁 Project Structure

```
binance/
├── app.py                  # Flask web application
├── basic_bot.py           # Core trading bot logic
├── cli_interface.py       # Command-line interface
├── requirements.txt       # Python dependencies
├── .env                   # API credentials (create from .env.example)
├── .env.example          # Template for environment variables
├── bot.log               # Application logs
├── templates/
│   └── index.html        # Web UI template
├── static/
│   └── app.js            # Frontend JavaScript
├── README.md             # This file
├── SETUP_GUIDE.md        # Detailed setup instructions
└── API_KEY_SETUP.txt     # API key generation guide
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Binance API Credentials
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret_key
```

### Testnet vs Production

The bot is configured for **testnet by default** (safe for testing):

```python
bot = BasicBot(api_key, api_secret, testnet=True)  # Testnet
bot = BasicBot(api_key, api_secret, testnet=False) # Production (CAUTION!)
```

⚠️ **Always use testnet for development and testing!**

## 📊 Order Types Explained

### 1. Market Order
Executes immediately at the best available market price.
```python
bot.place_market_order('BTCUSDT', 'BUY', 0.001)
```

### 2. Limit Order
Executes only at the specified price or better.
```python
bot.place_limit_order('BTCUSDT', 'BUY', 0.001, 50000.0)
```

### 3. Stop-Limit Order
Triggers a limit order when stop price is reached.
```python
bot.place_stop_limit_order('BTCUSDT', 'SELL', 0.001, 48000.0, 48500.0)
```

### 4. OCO Order (One-Cancels-Other)
Combines take-profit and stop-loss. When one executes, the other is canceled.
```python
bot.place_oco_order('BTCUSDT', 'BUY', 0.001, 52000.0, 48000.0)
```

### 5. TWAP Strategy (Time-Weighted Average Price)
Splits a large order into smaller chunks executed over time.
```python
bot.execute_twap('BTCUSDT', 'BUY', 0.1, duration_minutes=30, num_orders=10)
```

## 📝 Logging

All API requests, responses, and errors are logged to:
- **Console**: Real-time output
- **bot.log**: Persistent file logging

Log format:
```
2025-11-01 00:01:20 | INFO | BasicBot | place_market_order | PLACING MARKET ORDER: BUY 0.001 BTCUSDT
2025-11-01 00:01:20 | INFO | BasicBot | place_market_order | API Request: futures_create_order(...)
```

## 🛡️ Error Handling

The bot includes comprehensive error handling:

- **Input Validation**: Symbol format, quantity, price validation
- **API Error Handling**: Detailed error messages with codes
- **Network Error Handling**: Connection timeout and retry logic
- **Logging**: All errors logged with full context

Common errors and solutions:
- **-2015**: Invalid API keys → Generate new keys
- **-1121**: Invalid symbol → Use correct format (e.g., BTCUSDT)
- **-1111**: Quantity too small → Check minimum quantity requirements

## 🔐 Security

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` included in `.gitignore`
- ✅ Testnet recommended for development
- ✅ No hardcoded credentials
- ✅ Secure API communication over HTTPS

## 📚 API Documentation

- Binance Futures API: https://binance-docs.github.io/apidocs/futures/en/
- Testnet: https://testnet.binancefuture.com
- python-binance library: https://python-binance.readthedocs.io/

## 🐛 Troubleshooting

### "Invalid API-key" Error (-2015)
- Your testnet keys have expired (30-day expiry)
- Generate new keys from https://testnet.binancefuture.com
- Update `.env` with new keys
- Restart the application

### "Symbol not found" Error
- Ensure symbol ends with USDT (e.g., BTCUSDT, ETHUSDT)
- Use uppercase letters
- Check if symbol exists on Binance Futures

### Web UI not loading
- Ensure Flask is running: `python app.py`
- Check if port 5000 is available
- Try accessing http://127.0.0.1:5000 or http://localhost:5000

### Dependencies installation fails
- Upgrade pip: `python -m pip install --upgrade pip`
- Install one by one to identify the failing package
- Check Python version (requires 3.8+)

## 🎓 For Assignment Submission

This project fulfills all requirements:

✅ **Language**: Python  
✅ **Order Types**: Market, Limit, Stop-Limit, OCO, TWAP  
✅ **API Integration**: python-binance library with REST API  
✅ **Code Structure**: Modular, reusable, clear separation of concerns  
✅ **Logging**: Comprehensive API request/response/error logging  
✅ **Error Handling**: Input validation and exception handling  
✅ **CLI Interface**: Interactive command-line menu  
✅ **Bonus UI**: Web-based interface with Flask  
✅ **Testnet**: Using Binance Futures Testnet (USDT-M)  
✅ **Documentation**: Complete README and setup guides  

### Files to Submit:
- All source code files
- `bot.log` (showing successful executions)
- `.env.example` (template, not actual keys!)
- This README.md
- Screenshots of successful trades (optional)

## 👨‍💻 Author

Created for Junior Python Developer position application  
Contact: [Your Email]  
GitHub: [Your GitHub]

## 📄 License

This project is created for educational and testing purposes.  
Use at your own risk. The author is not responsible for any trading losses.

---

**⚠️ IMPORTANT DISCLAIMER**  
This bot is for educational purposes only. Cryptocurrency trading involves substantial risk of loss. Always test thoroughly on testnet before considering any production use. Never share your API keys.
