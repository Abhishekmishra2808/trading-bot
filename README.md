# 🤖 Binance Futures Trading Bot

A production-ready Binance Futures trading bot with web UI and CLI interface, supporting multiple order types and trading strategies.

## ✨ Features

- **Multiple Order Types**: Market, Limit, Stop-Limit, OCO (One-Cancels-Other)
- **Advanced Strategies**: TWAP (Time-Weighted Average Price)
- **Dual Interface**: Web UI and CLI
- **Comprehensive Logging**: Full API request/response logging
- **Error Handling**: Robust validation and exception handling
- **Testnet Support**: Safe testing environment
- **Cloud-Ready**: Deploy to Vercel, Railway, or any cloud platform

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/binance-futures-bot.git
   cd binance-futures-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Binance Testnet API keys
   # Get them from: https://testnet.binancefuture.com
   ```

4. **Run the bot**
   ```bash
   # Web UI
   python app.py
   # Then open http://localhost:5000
   
   # CLI
   python cli_interface.py
   ```

## 🌐 Deployment

### ⚠️ Important: Geo-Restriction Issue

If deploying to Vercel, you might encounter geo-restriction errors from Binance. See **[QUICKSTART.md](QUICKSTART.md)** for solutions.

### Deploy to Railway (Recommended)

Railway works reliably with Binance API:

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select this repository
4. Add environment variables:
   - `API_KEY`: Your Binance API key
   - `API_SECRET`: Your Binance API secret
5. Deploy!

**Cost**: $5 free credit/month (enough for testing)

**See [RAILWAY_GUIDE.md](RAILWAY_GUIDE.md) for detailed instructions.**

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repo to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy

**Note**: May have geo-restrictions with Binance. See [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md).

### Hybrid Deployment (Best for Production)

- **Frontend**: Vercel (free, fast CDN)
- **Backend**: Railway (reliable Binance access)

See [QUICKSTART.md](QUICKSTART.md) for setup instructions.

## 📋 Order Types

### 1. Market Order
Executes immediately at current market price.

```python
bot.place_market_order('BTCUSDT', 'BUY', 0.001)
```

### 2. Limit Order
Executes at specified price or better.

```python
bot.place_limit_order('BTCUSDT', 'BUY', 0.001, 50000.0)
```

### 3. Stop-Limit Order
Triggers a limit order when stop price is reached.

```python
bot.place_stop_limit_order('BTCUSDT', 'SELL', 0.001, 49000.0, 49500.0)
```

### 4. OCO (One-Cancels-Other)
Combines take-profit and stop-loss orders.

```python
bot.place_oco_order('BTCUSDT', 'SELL', 0.001, 55000.0, 45000.0)
```

### 5. TWAP Strategy
Splits large order into smaller chunks over time.

```python
bot.execute_twap('BTCUSDT', 'BUY', 0.01, duration_minutes=10, num_orders=5)
```

## 🎨 Web Interface

The web UI provides:
- Order placement with all types
- Account balance display
- Order status checking
- Recent activity log
- Testnet/Production toggle

Access at `http://localhost:5000` after starting the Flask app.

## 🖥️ CLI Interface

Interactive command-line interface with menu-driven navigation:

```bash
python cli_interface.py
```

Features:
- Place all order types
- Check balances
- View order status
- Execute TWAP strategy

## 📁 Project Structure

```
binance-futures-bot/
├── app.py                 # Flask web application
├── basic_bot.py          # Core trading bot logic
├── cli_interface.py      # Command-line interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
├── .env.example         # Template for environment variables
├── vercel.json          # Vercel deployment config
├── railway.toml         # Railway deployment config
├── static/
│   └── app.js           # Frontend JavaScript
├── templates/
│   └── index.html       # Web UI template
└── docs/
    ├── QUICKSTART.md           # Quick solutions guide
    ├── RAILWAY_GUIDE.md        # Railway deployment
    ├── VERCEL_DEPLOYMENT_GUIDE.md
    └── PROXY_SETUP.md          # Proxy configuration
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
```

**Get API keys from:**
- **Testnet**: https://testnet.binancefuture.com
- **Production**: https://www.binance.com/en/my/settings/api-management

### Security Best Practices

1. ✅ Use testnet for development
2. ✅ Enable IP whitelist on API keys
3. ✅ Restrict API permissions (Futures trading only)
4. ✅ Never commit `.env` file
5. ✅ Use read-only keys for monitoring
6. ✅ Enable 2FA on your Binance account

## 🐛 Troubleshooting

### Geo-Restriction Error

```
APIError(code=0): Service unavailable from a restricted location
```

**Solution**: Deploy to Railway instead of Vercel. See [QUICKSTART.md](QUICKSTART.md).

### Bot Not Initializing

1. Check environment variables are set correctly
2. Verify API keys are from testnet (if using testnet)
3. Check API key permissions
4. Review logs for specific errors

### Connection Timeout

1. Check your internet connection
2. Verify Binance API status: https://binance.com/en/support/announcement
3. Try using testnet
4. Check firewall settings

## 📊 Logging

All API requests and responses are logged to:
- Console (stdout)
- `bot.log` file (local only)
- `/tmp/bot.log` (on serverless platforms)

Log format:
```
2024-11-01 10:30:45 | INFO | BasicBot | place_market_order | PLACING MARKET ORDER: BUY 0.001 BTCUSDT
```

## 🧪 Testing

### Test Connection
```python
from basic_bot import BasicBot
import os
from dotenv import load_dotenv

load_dotenv()
bot = BasicBot(
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    testnet=True
)
```

### Test Balance
```bash
python -c "from basic_bot import BasicBot; import os; from dotenv import load_dotenv; load_dotenv(); bot = BasicBot(os.getenv('API_KEY'), os.getenv('API_SECRET'), testnet=True); print(bot.get_account_balance())"
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick solutions for common issues
- **[RAILWAY_GUIDE.md](RAILWAY_GUIDE.md)** - Deploy to Railway
- **[VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)** - Deploy to Vercel
- **[PROXY_SETUP.md](PROXY_SETUP.md)** - Configure proxy (advanced)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on testnet
5. Submit a pull request

## ⚠️ Disclaimer

**This bot is for educational purposes only.**

- Cryptocurrency trading carries substantial risk
- Past performance does not guarantee future results
- Test thoroughly on testnet before any production use
- The author is not responsible for any trading losses
- Use at your own risk

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by Abhishek Mishra

## 🔗 Resources

- [Binance Futures Testnet](https://testnet.binancefuture.com)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [python-binance Library](https://python-binance.readthedocs.io/)
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)

---

**⭐ If you found this helpful, please star the repository!**
