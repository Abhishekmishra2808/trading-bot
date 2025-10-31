import os
import sys
from dotenv import load_dotenv
from basic_bot import BasicBot


def print_header():
    print("\n" + "=" * 80)
    print(" " * 20 + "BINANCE FUTURES TRADING BOT")
    print(" " * 25 + "(Testnet Mode)")
    print("=" * 80 + "\n")


def print_menu():
    print("\n" + "-" * 80)
    print("SELECT ORDER TYPE:")
    print("-" * 80)
    print("  [1] Market Order (Immediate execution)")
    print("  [2] Limit Order (Execute at specific price)")
    print("  [3] Stop-Limit Order (Trigger at stop price)")
    print("  [4] OCO Order (One-Cancels-the-Other)")
    print("  [5] TWAP Strategy (Time-Weighted Average Price)")
    print("  [6] View Account Balance")
    print("  [7] Check Order Status")
    print("  [0] Exit")
    print("-" * 80)


def get_input(prompt, input_type=str, default=None):
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            
            if not value and default is not None:
                return default
            
            if input_type == str:
                return value.upper() if value else ""
            elif input_type == float:
                return float(value)
            elif input_type == int:
                return int(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}")


def place_market_order(bot):
    print("\n" + "=" * 80)
    print("MARKET ORDER (Immediate Execution)")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    side = get_input("Enter side (BUY/SELL)", str)
    quantity = get_input("Enter quantity", float)
    
    confirm = input(f"\nConfirm MARKET {side} {quantity} {symbol}? (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            order = bot.place_market_order(symbol, side, quantity)
            print("\nORDER PLACED SUCCESSFULLY!")
            print(f"Order ID: {order.get('orderId')}")
            print(f"Status: {order.get('status')}")
            print(f"Executed Qty: {order.get('executedQty')}")
        except Exception as e:
            print(f"\nOrder failed: {e}")
    else:
        print("\nOrder cancelled by user")


def place_limit_order(bot):
    print("\n" + "=" * 80)
    print("LIMIT ORDER (Execute at Specific Price)")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    side = get_input("Enter side (BUY/SELL)", str)
    quantity = get_input("Enter quantity", float)
    price = get_input("Enter limit price", float)
    
    confirm = input(f"\nConfirm LIMIT {side} {quantity} {symbol} @ {price}? (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            order = bot.place_limit_order(symbol, side, quantity, price)
            print("\nORDER PLACED SUCCESSFULLY!")
            print(f"Order ID: {order.get('orderId')}")
            print(f"Status: {order.get('status')}")
            print(f"Price: {order.get('price')}")
        except Exception as e:
            print(f"\nOrder failed: {e}")
    else:
        print("\nOrder cancelled by user")


def place_stop_limit_order(bot):
    print("\n" + "=" * 80)
    print("STOP-LIMIT ORDER (Trigger at Stop Price)")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    side = get_input("Enter side (BUY/SELL)", str)
    quantity = get_input("Enter quantity", float)
    price = get_input("Enter limit price", float)
    stop_price = get_input("Enter stop price (trigger)", float)
    
    confirm = input(
        f"\nConfirm STOP-LIMIT {side} {quantity} {symbol} @ {price} (stop: {stop_price})? (yes/no): "
    )
    
    if confirm.lower() == 'yes':
        try:
            order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
            print("\nORDER PLACED SUCCESSFULLY!")
            print(f"Order ID: {order.get('orderId')}")
        except Exception as e:
            print(f"\nOrder failed: {e}")
    else:
        print("\nOrder cancelled by user")


def place_oco_order(bot):
    print("\n" + "=" * 80)
    print("OCO ORDER (One-Cancels-the-Other)")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    side = get_input("Enter side of initial position (BUY/SELL)", str)
    quantity = get_input("Enter quantity", float)
    tp_price = get_input("Enter take-profit price", float)
    sl_price = get_input("Enter stop-loss price", float)
    
    confirm = input(
        f"\nConfirm OCO for {quantity} {symbol} (TP: {tp_price}, SL: {sl_price})? (yes/no): "
    )
    
    if confirm.lower() == 'yes':
        try:
            result = bot.place_oco_order(symbol, side, quantity, tp_price, sl_price)
            print("\nOCO ORDERS PLACED SUCCESSFULLY!")
            print(f"Take-Profit Order ID: {result['take_profit_order'].get('orderId')}")
            print(f"Stop-Loss Order ID: {result['stop_loss_order'].get('orderId')}")
        except Exception as e:
            print(f"\nOCO order failed: {e}")
    else:
        print("\nOrder cancelled by user")


def execute_twap(bot):
    print("\n" + "=" * 80)
    print("TWAP STRATEGY (Time-Weighted Average Price)")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    side = get_input("Enter side (BUY/SELL)", str)
    total_quantity = get_input("Enter total quantity", float)
    duration = get_input("Enter duration in minutes", int)
    num_orders = get_input("Enter number of orders (default: 10)", int, default=10)
    
    confirm = input(
        f"\nConfirm TWAP {side} {total_quantity} {symbol} over {duration}min ({num_orders} orders)? (yes/no): "
    )
    
    if confirm.lower() == 'yes':
        try:
            print("\nExecuting TWAP strategy...")
            result = bot.execute_twap(symbol, side, total_quantity, duration, num_orders)
            print("\nTWAP STRATEGY COMPLETED!")
            print(f"Total Orders: {result['total_orders']}")
            print(f"Successful: {result['successful_orders']}")
        except Exception as e:
            print(f"\nTWAP failed: {e}")
    else:
        print("\nStrategy cancelled by user")


def view_balance(bot):
    print("\n" + "=" * 80)
    print("ACCOUNT BALANCE")
    print("=" * 80)
    
    try:
        balances = bot.get_account_balance()
        
        print("\n{:<15} {:<20} {:<20}".format("Asset", "Available", "Balance"))
        print("-" * 60)
        
        for balance in balances:
            if float(balance['balance']) > 0:
                print("{:<15} {:<20} {:<20}".format(
                    balance['asset'],
                    balance['availableBalance'],
                    balance['balance']
                ))
    except Exception as e:
        print(f"\nFailed to get balance: {e}")


def check_order_status(bot):
    print("\n" + "=" * 80)
    print("CHECK ORDER STATUS")
    print("=" * 80)
    
    symbol = get_input("Enter symbol (e.g., BTCUSDT)", str)
    order_id = get_input("Enter order ID", int)
    
    try:
        order = bot.get_order_status(symbol, order_id)
        print("\n" + "=" * 80)
        print(f"Order ID: {order.get('orderId')}")
        print(f"Symbol: {order.get('symbol')}")
        print(f"Type: {order.get('type')}")
        print(f"Side: {order.get('side')}")
        print(f"Status: {order.get('status')}")
        print(f"Quantity: {order.get('origQty')}")
        print(f"Executed: {order.get('executedQty')}")
        print(f"Price: {order.get('price')}")
        print("=" * 80)
    except Exception as e:
        print(f"\nFailed to get order status: {e}")


def main():
    load_dotenv()
    
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: API credentials not found in .env file")
        sys.exit(1)
    
    print_header()
    print("Initializing bot...")
    
    try:
        bot = BasicBot(api_key, api_secret, testnet=True)
        print("Bot initialized successfully!\n")
    except Exception as e:
        print(f"Failed to initialize bot: {e}")
        sys.exit(1)
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == '1':
            place_market_order(bot)
        elif choice == '2':
            place_limit_order(bot)
        elif choice == '3':
            place_stop_limit_order(bot)
        elif choice == '4':
            place_oco_order(bot)
        elif choice == '5':
            execute_twap(bot)
        elif choice == '6':
            view_balance(bot)
        elif choice == '7':
            check_order_status(bot)
        elif choice == '0':
            print("\n" + "=" * 80)
            print(" " * 25 + "Goodbye! Happy Trading!")
            print("=" * 80 + "\n")
            break
        else:
            print("\nInvalid choice. Please select 0-7.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
