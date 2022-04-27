import os
import gemini
import json
from decimal import Decimal
import util
import click
from generate_encrypted_api_keys import encrypt_keys, decrypt_keys
import cmd, sys
from version import __version__


class Trader():
    def __init__(self):
#         gemini_pub = os.environ.get('GEMINI_PUB')#.encode()
#         gemini_pri = os.environ.get('GEMINI_PRI')#.encode()
        gemini_pub, gemini_pri = decrypt_keys()

#         print(gemini_pub)
#         print(gemini_pri)
        self.client = gemini.PrivateClient(gemini_pub, gemini_pri)
        self._maker_fee = 0.001 # 0.100%

    def get_order_book(self, symbol):
        return self.client.get_current_order_book(symbol)

    def get_spread(self, symbol):
        order_book = self.get_order_book(symbol)
        bids = order_book["bids"]
        asks = order_book["asks"]

#         print("Bids: \n", json.dumps(bids, indent=4, sort_keys=True))
#         print("asks: \n", json.dumps(asks, indent=4, sort_keys=True))

        max_bid_item = max(bids, key=lambda x:x['price'])
        min_ask_item = min(asks, key=lambda x:x['price'])
#         print('max_bid: ', max_bid_item)
#         print('min_ask: ', min_ask_item)

        max_bid_price = float(max(bid['price'] for bid in bids))
        min_ask_price = float(min(ask['price'] for ask in asks))
        spread = min_ask_price-max_bid_price

        return max_bid_price, min_ask_price, spread

    def get_symbol_trade_info(self, symbol):
        symbol_info = {'symbol':symbol}
        symbol_info['max_bid'], symbol_info['min_ask'], symbol_info['spread'] = self.get_spread(symbol)
        return symbol_info

    def get_recommended_price(self, symbol, trade_type):
        if trade_type == "buy":
            symbol_info = self.get_symbol_trade_info(symbol)
            print(symbol_info)
            price = float(symbol_info['max_bid'])
        elif trade_type == "sell":
            symbol_info = self.get_symbol_trade_info(symbol)
            print(symbol_info)
            price = float(symbol_info['min_ask'])
        else:
            return -1

#         print("max_bid: ", symbol_info['max_bid'])
#         print("spread: ", symbol_info['spread'])
#         print("spread/2: ", float(symbol_info['spread'])/2)
#         print("price: ", price)
#         print("price-spread/2: ", float(price)-float(symbol_info['spread'])/2)
        return price


def propose_trade(trader, symbol, trade_type, investment_USD='', quantity=''):
    confirm = 'R'
    while confirm == 'R' or len(confirm) == 0:
        price = trader.get_recommended_price(symbol, trade_type)

        if investment_USD == '':
            investment_USD = quantity*price
        else:
            investment_USD = float(investment_USD)

        if quantity == '':
            quantity = investment_USD/price
        else:
            quantity = float(quantity)

        fee = trader._maker_fee*investment_USD
        investment_plus_fee_USD = investment_USD + fee

        print("price: \t\t\t${:,.2f}".format(price))
        print("quantity:\t\t", quantity)
        print("investment_USD: \t${:,.2f}".format(quantity*price))
        print("fee: \t\t\t${:,.2f}".format(fee))
        print("investment + fee: \t${:,.2f}".format(investment_plus_fee_USD))

        input_str = "" + trade_type +' '+ "{:,.8f}".format(quantity) +' '+ symbol[0:3].upper() +' '+ "@" +' '+ "${:,.2f}".format(price) +" for " + "${:,.2f} ".format(investment_plus_fee_USD) + "?" + " Y/N? "
        confirm = input(input_str)

    return confirm, price


def get_available_balance(trader, currency):
    balance = 0.0
    for entry in trader.client.get_balance():
        if entry['type'] == 'exchange':
#             print("{} {}".format(entry['currency'], currency))
            if entry['currency'].casefold()  == currency.casefold():
                balance = float(entry['available'])
                break
    return balance

def invest(trader, symbol='', investment_USD=''):
    # buy(): Purchase N Crypto at a recommended price

    currency  = symbol[3:6] # currency is 'USD' in the symbol 'ETHUSD'
    commodity = symbol[0:3] # commodity is 'ETH' in the symbol 'ETHUSD'
    if symbol.casefold() not in trader.client.symbols():
        print("Invalid symbol", symbol)
        return

    try:
        investment_USD = float(investment_USD)
    except ValueError:
        max_currency_qty = 0.0

        max_currency_qty = get_available_balance(trader, currency)

        investment_USD = input("Amount of {} invest (max = {:.10f} {}): ".format(currency.upper(), max_currency_qty, currency.upper()))
        if(investment_USD == 'max' or investment_USD == ''):
            investment_USD=max_currency_qty
        else:
            #TODO: Re-use code.
            try:
                investment_USD = float(investment_USD)
            except ValueError:
                print("Invalid quantity.")
                return

    confirm, price = propose_trade(trader, symbol, "buy", investment_USD)

    amount_SYM = investment_USD/price

    if confirm == 'Y':
        print("Placing Order {:.6f} for ${:.2f}...".format(amount_SYM, price))
        print(trader.client.new_order(symbol, "{:.6f}".format(amount_SYM),"{:.2f}".format(price), "buy", options=["maker-or-cancel"]))
        print("Order Placed")
        print("----------")
    else:
        print("Goodbye.")
        return

def buy(trader, symbol='', quantity=''):
    # buy(): Purchase N Crypto at a recommended price

    currency  = symbol[3:6] # currency is 'USD' in the symbol 'ETHUSD'
    commodity = symbol[0:3] # commodity is 'ETH' in the symbol 'ETHUSD'
    if symbol.casefold() not in trader.client.symbols():
        print("Invalid symbol", symbol)
        return

    try:
        quantity = float(quantity)
    except ValueError:
        max_currency_qty = 0.0
        # quantity of "commodity" that can be purchased is a function of the amount of "currency" held
        #   commodity_quantity = currency_balance/commodity_price

        # 1) Get amount of currency held
        max_currency_qty = get_available_balance(trader, currency)

        # 2) Get recommended price
        # TODO: The price snapshot is taken here, then again in 'propose_trade()'
        price = trader.get_recommended_price(symbol, "buy")

        # 3) Get approximate quantity of "commodity"
        #   commodity_quantity = currency_balance/commodity_price
        max_commodity_qty = max_currency_qty / price
        quantity = input("Quantity (max = ~{:.10f} {}): ".format(max_commodity_qty, commodity.upper()))
        if(quantity == 'max' or quantity == ''):
            quantity=max_commodity_qty
        else:
            #TODO: Re-use code.
            try:
                quantity = float(quantity)
            except ValueError:
                print("Invalid quantity.")
                return

    confirm, price = propose_trade(trader, symbol, "buy", quantity=quantity)
    #amount_SYM = investment_USD/p rice

    if confirm == 'Y':
        print("Placing Order {:.6f} for ${:.2f}...".format(quantity, price))
        print(trader.client.new_order(symbol, "{:.6f}".format(quantity),"{:.2f}".format(price), "buy", options=["maker-or-cancel"]))
        print("Order Placed")
        print("----------")
    else:
        print("Goodbye.")
        return

def sell(trader, symbol='', quantity=""):
    commodity = symbol[0:3] # Commodity is 'ETH' in the symbol 'ETHUSD'
    if symbol.casefold() not in trader.client.symbols():
        print("Invalid symbol", symbol)
        return
    try:
        quantity = float(quantity)
    except ValueError:
        max_commodity_qty = get_available_balance(trader, commodity)

        quantity = input("Quantity (max = {:.10f} {}): ".format(max_commodity_qty, commodity.upper()))
        if(quantity == 'max' or quantity == ''):
            quantity=max_commodity_qty
        else:
            #TODO: Re-use code.
            try:
                quantity = float(quantity)
            except ValueError:
                print("Invalid quantity.")
                return

#     maker_fee = 0.001 # 0.100%
    trade_type = "sell"

    confirm = 'R'
    # def new_order(self, symbol, amount, price, side, options=["immediate-or-cancel"]):
    while confirm == 'R' or len(confirm) == 0:
        price = trader.get_recommended_price(symbol, trade_type)
        trade_total_USD = quantity * price
        fee = trader._maker_fee*trade_total_USD
        amount_return_minus_fee_USD = (trade_total_USD-fee)

        print("price: \t\t\t${:,.2f}".format(price))
        print("trade_total_USD: \t${:,.2f}".format(trade_total_USD))
        print("quantity:\t\t", quantity)
        print("fee: \t\t\t${:,.2f}".format(fee))
        print("return (USD) after fees:$", amount_return_minus_fee_USD)

        input_str = "" + trade_type +' '+ "{:,.8f}".format(quantity) +' '+ commodity.upper() +' '+ "@" +' '+ "${:,.2f}".format(price) +" for " + "${:,.2f}".format(trade_total_USD) + "?" + " Y/N? "
        confirm = input(input_str)

    if confirm == 'Y':
        print("Order Placed")
        print(trader.client.new_order(symbol, "{:.8f}".format(quantity),"{:.2f}".format(price), trade_type, options=["maker-or-cancel"]))
        print("----------")
    else:
        print("Goodbye.")
        return
    return

def holdings(trader, symbol=''):
    print(json.dumps(trader.client.get_balance(), indent=4, sort_keys=True))
    return trader.client.get_balance()

def active(trader, symbol=''):
    print(trader.client.active_orders())
    return

def history(trader, symbol='', n=1):
    symbol = symbol.lower()
    if symbol not in trader.client.symbols():
        print("Invalid symbol", symbol)
        return

    hist = trader.client.get_past_trades(symbol)
    if hist:
        if int(n) > 0:
            for m in range(int(n)):
                print(json.dumps(hist[m], indent=4, sort_keys=True))
    return

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(str, arg.split()))

def quit():
    sys.exit()

class TradeShell(cmd.Cmd):
    intro = 'Welcome to the trading shell.   Type help or ? to list commands.\n'
    prompt = '$ '
    file = None

    def __init__(self):
        super(TradeShell, self).__init__()
        self.trader = Trader()

    def emptyline(self):
        return

    def do_quit(self, arg):
        'quit'
        quit()

    def do_history(self, arg):
        'history SYMBOL [num_entries=1]'
        history(self.trader, *parse(arg))

    def do_holdings(self, arg):
        'holdings'
        holdings(self.trader, arg)

    def do_active(self, arg):
        'active'
        active(self.trader, arg)

    def do_symbols(self, arg):
        'symbols'
#         print(json.dumps(self.trader.client.symbols(), indent=4, sort_keys=True))
        print(self.trader.client.symbols())

    def do_invest(self, arg):
        'invest SYMBOL [total_investment]'
        invest(self.trader, *parse(arg))

    def do_buy(self, arg):
        'buy SYMBOL [quantity]'
        buy(self.trader, *parse(arg))

    def do_sell(self, arg):
        'sell SYMBOL [quantity]'
        sell(self.trader, *parse(arg))


@click.version_option(__version__, '--version', '-v')
@click.group()
def cli():
     click.echo('CLI')

@cli.command()
def trade():
    TradeShell().cmdloop()
    click.echo('()NOT IMPLEMENTED) trade_loop')

if __name__== "__main__":
    cli()


# EOF
