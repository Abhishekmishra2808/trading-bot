from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from basic_bot import BasicBot
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = None
# Environment variables loaded from Vercel

def initialize_bot():
    global bot
    try:
        api_key = os.getenv('API_KEY') or os.environ.get('API_KEY')
        api_secret = os.getenv('API_SECRET') or os.environ.get('API_SECRET')
        
        if not api_key or not api_secret:
            logger.error(f"API credentials not found. API_KEY exists: {bool(api_key)}, API_SECRET exists: {bool(api_secret)}")
            return False
        
        logger.info(f"Initializing bot with API key: {api_key[:10]}...")
        bot = BasicBot(api_key, api_secret, testnet=True)
        logger.info("Bot initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def init_bot():
    if initialize_bot():
        return jsonify({'success': True, 'message': 'Bot initialized successfully'})
    return jsonify({'success': False, 'message': 'Failed to initialize bot'}), 500

@app.route('/api/market-order', methods=['POST'])
def market_order():
    global bot
    try:
        # Reinitialize bot if needed
        if bot is None:
            logger.info("Bot is None, reinitializing...")
            if not initialize_bot():
                return jsonify({'success': False, 'message': 'Bot not initialized. Failed to connect to API.'}), 400
        
        data = request.json
        order = bot.place_market_order(
            data['symbol'],
            data['side'],
            float(data['quantity'])
        )
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        logger.error(f"Market order error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/limit-order', methods=['POST'])
def limit_order():
    global bot
    try:
        # Reinitialize bot if needed
        if bot is None:
            logger.info("Bot is None, reinitializing...")
            if not initialize_bot():
                return jsonify({'success': False, 'message': 'Bot not initialized. Failed to connect to API.'}), 400
        
        data = request.json
        order = bot.place_limit_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['price'])
        )
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        logger.error(f"Limit order error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/stop-limit-order', methods=['POST'])
def stop_limit_order():
    try:
        data = request.json
        order = bot.place_stop_limit_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['price']),
            float(data['stopPrice'])
        )
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/oco-order', methods=['POST'])
def oco_order():
    try:
        data = request.json
        order = bot.place_oco_order(
            data['symbol'],
            data['side'],
            float(data['quantity']),
            float(data['takeProfitPrice']),
            float(data['stopLossPrice'])
        )
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/twap', methods=['POST'])
def twap_strategy():
    try:
        data = request.json
        result = bot.execute_twap(
            data['symbol'],
            data['side'],
            float(data['totalQuantity']),
            int(data['duration']),
            int(data.get('numOrders', 10))
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/balance', methods=['GET'])
def get_balance():
    global bot
    try:
        # Reinitialize bot if needed
        if bot is None:
            logger.info("Bot is None, reinitializing...")
            if not initialize_bot():
                return jsonify({'success': False, 'message': 'Bot not initialized. Failed to connect to API.'}), 400
        
        balance = bot.get_account_balance()
        return jsonify({'success': True, 'balance': balance})
    except Exception as e:
        logger.error(f"Balance error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/order-status', methods=['POST'])
def order_status():
    try:
        data = request.json
        order = bot.get_order_status(data['symbol'], int(data['orderId']))
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Initialize bot on module load for Vercel
initialize_bot()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
