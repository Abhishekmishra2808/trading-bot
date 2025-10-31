from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
from typing import Optional, Dict, Any
import time


class BasicBot:
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        self._setup_logging()
        self.client = Client(api_key, api_secret, testnet=testnet)
        
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com/fapi'
            self.logger.info("Using Binance Futures TESTNET: https://testnet.binancefuture.com")
        else:
            self.logger.warning("Using Binance Futures PRODUCTION environment")
        
        self._test_connection()
    
    def _setup_logging(self):
        self.logger = logging.getLogger('BasicBot')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler('bot.log')
            file_handler.setLevel(logging.INFO)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        self.logger.info("=" * 80)
        self.logger.info("BasicBot initialized")
        self.logger.info(f"Testnet mode: {self.testnet}")
        self.logger.info("=" * 80)
    
    def _test_connection(self):
        try:
            self.client.ping()
            self.logger.info("Successfully connected to Binance Futures API")
        except Exception as e:
            self.logger.error(f"Failed to connect to Binance API: {e}")
            raise
    
    def _validate_symbol(self, symbol: str) -> str:
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        
        symbol = symbol.upper()
        
        if not symbol.endswith('USDT'):
            raise ValueError(f"Symbol must end with 'USDT' for USDT-M Futures. Got: {symbol}")
        
        return symbol
    
    def _validate_side(self, side: str) -> str:
        if not side:
            raise ValueError("Side cannot be empty")
        
        side = side.upper()
        
        if side not in ['BUY', 'SELL']:
            raise ValueError(f"Side must be 'BUY' or 'SELL'. Got: {side}")
        
        return side
    
    def _validate_quantity(self, quantity: float) -> float:
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid quantity: {quantity}. Must be a number")
        
        if qty <= 0:
            raise ValueError(f"Quantity must be positive. Got: {qty}")
        
        return qty
    
    def _validate_price(self, price: float) -> float:
        try:
            prc = float(price)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid price: {price}. Must be a number")
        
        if prc <= 0:
            raise ValueError(f"Price must be positive. Got: {prc}")
        
        return prc
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        symbol = self._validate_symbol(symbol)
        side = self._validate_side(side)
        quantity = self._validate_quantity(quantity)
        
        self.logger.info("=" * 80)
        self.logger.info(f"PLACING MARKET ORDER: {side} {quantity} {symbol}")
        self.logger.info("=" * 80)
        
        try:
            self.logger.info(f"API Request: futures_create_order(symbol={symbol}, side={side}, type=MARKET, quantity={quantity})")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            self.logger.info(f"API Response: {order}")
            self.logger.info("=" * 80)
            self.logger.info("MARKET ORDER PLACED SUCCESSFULLY")
            self.logger.info(f"Order ID: {order.get('orderId')}")
            self.logger.info(f"Status: {order.get('status')}")
            self.logger.info(f"Executed Qty: {order.get('executedQty')}")
            self.logger.info("=" * 80)
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error("=" * 80)
            self.logger.error("BINANCE API ERROR")
            self.logger.error(f"Error Code: {e.code}")
            self.logger.error(f"Error Message: {e.message}")
            self.logger.error("=" * 80)
            raise
        except Exception as e:
            self.logger.error("=" * 80)
            self.logger.error(f"UNEXPECTED ERROR: {e}")
            self.logger.error("=" * 80)
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float, 
                         time_in_force: str = 'GTC') -> Dict[str, Any]:
        symbol = self._validate_symbol(symbol)
        side = self._validate_side(side)
        quantity = self._validate_quantity(quantity)
        price = self._validate_price(price)
        
        self.logger.info("=" * 80)
        self.logger.info(f"PLACING LIMIT ORDER: {side} {quantity} {symbol} @ {price}")
        self.logger.info("=" * 80)
        
        try:
            self.logger.info(
                f"API Request: futures_create_order(symbol={symbol}, side={side}, "
                f"type=LIMIT, quantity={quantity}, price={price}, timeInForce={time_in_force})"
            )
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce=time_in_force,
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"API Response: {order}")
            self.logger.info("=" * 80)
            self.logger.info("LIMIT ORDER PLACED SUCCESSFULLY")
            self.logger.info(f"Order ID: {order.get('orderId')}")
            self.logger.info(f"Status: {order.get('status')}")
            self.logger.info(f"Price: {order.get('price')}")
            self.logger.info("=" * 80)
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error("=" * 80)
            self.logger.error("BINANCE API ERROR")
            self.logger.error(f"Error Code: {e.code}")
            self.logger.error(f"Error Message: {e.message}")
            self.logger.error("=" * 80)
            raise
        except Exception as e:
            self.logger.error("=" * 80)
            self.logger.error(f"UNEXPECTED ERROR: {e}")
            self.logger.error("=" * 80)
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float) -> Dict[str, Any]:
        symbol = self._validate_symbol(symbol)
        side = self._validate_side(side)
        quantity = self._validate_quantity(quantity)
        price = self._validate_price(price)
        stop_price = self._validate_price(stop_price)
        
        self.logger.info("=" * 80)
        self.logger.info(f"PLACING STOP-LIMIT ORDER: {side} {quantity} {symbol} @ {price} (stop: {stop_price})")
        self.logger.info("=" * 80)
        
        try:
            self.logger.info(
                f"API Request: futures_create_order(symbol={symbol}, side={side}, "
                f"type=STOP, quantity={quantity}, price={price}, stopPrice={stop_price})"
            )
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            
            self.logger.info(f"API Response: {order}")
            self.logger.info("STOP-LIMIT ORDER PLACED SUCCESSFULLY")
            self.logger.info(f"Order ID: {order.get('orderId')}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"API ERROR: {e.code} - {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"UNEXPECTED ERROR: {e}")
            raise
    
    def place_oco_order(self, symbol: str, side: str, quantity: float, 
                       price: float, stop_price: float, 
                       stop_limit_price: Optional[float] = None) -> Dict[str, Any]:
        symbol = self._validate_symbol(symbol)
        side = self._validate_side(side)
        quantity = self._validate_quantity(quantity)
        price = self._validate_price(price)
        stop_price = self._validate_price(stop_price)
        stop_limit_price = stop_limit_price if stop_limit_price else stop_price
        
        opposite_side = 'SELL' if side == 'BUY' else 'BUY'
        
        self.logger.info("=" * 80)
        self.logger.info(f"PLACING OCO ORDER: {opposite_side} {quantity} {symbol}")
        self.logger.info(f"Take-Profit: {price} | Stop-Loss: {stop_price}")
        self.logger.info("=" * 80)
        
        try:
            tp_order = self.place_limit_order(symbol, opposite_side, quantity, price)
            
            sl_order = self.place_stop_limit_order(
                symbol, opposite_side, quantity, stop_limit_price, stop_price
            )
            
            result = {
                'oco_type': 'OCO',
                'take_profit_order': tp_order,
                'stop_loss_order': sl_order
            }
            
            self.logger.info("OCO ORDERS PLACED SUCCESSFULLY")
            return result
            
        except Exception as e:
            self.logger.error(f"OCO ORDER FAILED: {e}")
            raise
    
    def execute_twap(self, symbol: str, side: str, total_quantity: float, 
                     duration_minutes: int, num_orders: int = 10) -> Dict[str, Any]:
        symbol = self._validate_symbol(symbol)
        side = self._validate_side(side)
        total_quantity = self._validate_quantity(total_quantity)
        
        if num_orders < 2:
            raise ValueError("Number of orders must be at least 2")
        
        quantity_per_order = total_quantity / num_orders
        interval_seconds = (duration_minutes * 60) / num_orders
        
        self.logger.info("=" * 80)
        self.logger.info(f"EXECUTING TWAP STRATEGY: {side} {total_quantity} {symbol}")
        self.logger.info(f"Orders: {num_orders} | Interval: {interval_seconds:.2f}s")
        self.logger.info("=" * 80)
        
        executed_orders = []
        
        try:
            for i in range(num_orders):
                self.logger.info(f"TWAP Order {i+1}/{num_orders}")
                
                order = self.place_market_order(symbol, side, quantity_per_order)
                executed_orders.append(order)
                
                if i < num_orders - 1:
                    time.sleep(interval_seconds)
            
            summary = {
                'strategy': 'TWAP',
                'total_orders': num_orders,
                'successful_orders': len(executed_orders),
                'orders': executed_orders
            }
            
            self.logger.info("TWAP STRATEGY COMPLETED")
            return summary
            
        except Exception as e:
            self.logger.error(f"TWAP FAILED: {e}")
            raise
    
    def get_account_balance(self) -> Dict[str, Any]:
        try:
            self.logger.info("Fetching account balance...")
            balance = self.client.futures_account_balance()
            self.logger.info(f"API Response: {balance}")
            return balance
        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        try:
            symbol = self._validate_symbol(symbol)
            self.logger.info(f"Fetching order status for Order ID: {order_id}")
            
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order Status: {order.get('status')}")
            
            return order
        except Exception as e:
            self.logger.error(f"Failed to get order status: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        try:
            symbol = self._validate_symbol(symbol)
            self.logger.info(f"Cancelling order: {order_id}")
            
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order cancelled: {order_id}")
            
            return result
        except Exception as e:
            self.logger.error(f"Failed to cancel order: {e}")
            raise


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    bot = BasicBot(
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET'),
        testnet=True
    )
