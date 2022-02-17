import os
import gemini
import json
from decimal import Decimal
import util
import click
from generate_encrypted_api_keys import encrypt_keys, decrypt_keys
import cmd, sys

# 1) Generate encrypted API keys
# 2) Propose a trade

class Trader():
    def __init__(self):
#         gemini_pub = os.environ.get('GEMINI_PUB')#.encode()
#         gemini_pri = os.environ.get('GEMINI_PRI')#.encode()
        gemini_pub, gemini_pri = decrypt_keys()

#         print(gemini_pub)
#         print(gemini_pri)
        self.client = gemini.PrivateClient(gemini_pub, gemini_pri)

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

    def get_recommended_price(self, symbol):
        symbol_info = self.get_symbol_trade_info(symbol);
        print(symbol_info)
        price = float(symbol_info['max_bid'])

#         print("max_bid: ", symbol_info['max_bid'])
#         print("spread: ", symbol_info['spread'])
#         print("spread/2: ", float(symbol_info['spread'])/2)
#         print("price: ", price)
#         print("price-spread/2: ", float(price)-float(symbol_info['spread'])/2)
        return price


# def print_version(ctx, param, value):
#     if not value or ctx.resilient_parsing:
#         return
#     click.echo('Version 1.0')
#     ctx.exit()
#
# @click.command()
# @click.option('--version', is_flag=True, callback=print_version,
#               expose_value=False, is_eager=True)
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
        'Close the program.'
        quit()

    def do_buy(self, arg):
        'buy something'
        click.echo('do_buy')
        symbol = arg
        print(symbol)
        buy(self.trader)

@click.group()
def cli():
    click.echo('CLI')
#     trader = Trader()

@cli.command()
def trade():
    TradeShell().cmdloop()
    click.echo('()NOT IMPLEMENTED) trade_loop')

@cli.command()
def sell():
    click.echo('()NOT IMPLEMENTED) Sell')


def buy(trader):

#     trader = Trader()

    maker_fee = 0.001 # 0.100%

    symbol = 'BTCUSD'
    type = "buy"

    confirm = 'R'
    # def new_order(self, symbol, amount, price, side, options=["immediate-or-cancel"]):
    while confirm == 'R' or len(confirm) == 0:
        price = trader.get_recommended_price(symbol)
        investment_USD = 12500
        amount_SYM = investment_USD/price
        fee = maker_fee*investment_USD
        amount_SYM_minus_fee = (investment_USD-fee)/price

        print("price: \t\t\t${:,.2f}".format(price))
        print("investment_USD: \t${:,.2f}".format(amount_SYM*price))
        print("amount_SYM:\t\t", amount_SYM)
        print("fee: \t\t\t${:,.2f}".format(fee))
        print("amount_SYM after fees: ", amount_SYM_minus_fee)

        input_str = "" + type +' '+ "{:,.8f}".format(amount_SYM) +' '+ symbol +' '+ "@" +' '+ "${:,.2f}".format(price) +" for " + "${:,.2f} ".format(investment_USD) + "?" + " Y/N? "
        confirm = input(input_str)


    #confirm = input()
    if confirm == 'Y':
        print("Order Placed")
        #print(trader.client.new_order(symbol, "{:.8f}".format(amount_SYM),"{:.2f}".format(price), type, options=["maker-or-cancel"]))
        print("----------")
    else:
        print("Goodbye.")
        return

    print(json.dumps(trader.client.get_balance(), indent=4, sort_keys=True))
    print(json.dumps(trader.client.get_past_trades(symbol)[0], indent=4, sort_keys=True))
    print(trader.client.active_orders())

# cli.add_command(encrypt_api_keys)
# cli.add_command(trade)
# trade_options.add_command(buy)
# trade_options.add_command(sell)

if __name__== "__main__":
    cli()



# EOF
