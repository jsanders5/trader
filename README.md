# Trader

## Getting Started

1. Extract zip to a known location
2. Open a command prompt in that folder (Open a file browser, navigate to the directory, then click in the address bar, type `cmd`, press enter)
3. Run `generate_encrypted_api_keys.exe`
4. Follow the prompts to encrypt your API keys. You'll need to enter a password, then copy and paste your key, then copy and paste your secret.

Now you're ready to run the trader command line application.

### Executing Trader Application

In the same prompt as above, run 'trader', you will see the help menu

```
>trader

Usage: trader [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  trade
```

Run `trader.exe trade`, you will be prompted for a password that you set as part of step (4)

```
>trader trade
CLI
Decrypting API keys...
Enter Password:
```

Enter password, then you'll be prompted with a trading shell

```
Enter Password: *
Welcome to the trading shell.   Type help or ? to list commands.

$
```

Type `?` to list the available commands

```
$ ?

Documented commands (type help <topic>):
========================================
active  buy  help  history  holdings  invest  quit  sell  symbols
```

You can type `help <command>` to see usage for each command

```
$ help buy
buy SYMBOL [quantity]
```

**Note: Arguments in `[square braces]` are optional.**

**Be careful moving forward. When using buy/sell/invest commands, once prompted to make the trade, if you select "Y" by mistake, the trade is going LIVE and there is no way to stop it unless you can cancel before the order is filled.**

## Command Examples

---

### *symbols*

Display all supported symbols

### `symbols`

```
$ symbols
['btcusd', 'btcgusd', 'btcdai', 'btcgbp', 'btceur', 'btcsgd', 'ethbtc', 'ethusd', 'ethgusd', 'ethgbp', 'etheur', 'ethsgd', 'ethdai', 'bchusd', 'bchbtc', 'bcheth', 'ltcusd', 'ltcbtc', 'ltceth', 'ltcbch', 'zecusd', 'zecbtc', 'zeceth', 'z
ecbch', 'zecltc', 'batusd', 'batbtc', 'bateth', 'linkusd', 'linkbtc', 'linketh', 'daiusd', 'oxtusd', 'oxtbtc', 'oxteth', 'filusd', 'ampusd', 'paxgusd', 'compusd', 'mkrusd', 'zrxusd', 'kncusd', 'storjusd', 'manausd', 'aaveusd', 'snxusd'
, 'yfiusd', 'umausd', 'balusd', 'crvusd', 'renusd', 'uniusd', 'enjusd', 'bntusd', '1inchusd', 'sklusd', 'grtusd', 'lrcusd', 'sandusd', 'cubeusd', 'lptusd', 'bondusd', 'maticusd', 'injusd', 'sushiusd', 'dogeusd', 'api3usd', 'mirusd', 'c
txusd', 'alcxusd', 'ankrusd', 'ftmusd', 'xtzusd', 'axsusd', 'usdcusd', 'slpusd', 'lunausd', 'ustusd', 'mco2usd', 'dogebtc', 'dogeeth', 'cvcusd', 'spellusd', 'mimusd', 'galausd', 'mcusd', 'ensusd', 'elonusd', 'ashusd', 'wcfgusd', 'rareu
sd', 'radusd', 'qntusd', 'maskusd', 'fetusd', 'audiousd', 'nmrusd', 'rlyusd', 'rndrusd', 'shibusd', 'ldousd', 'kp3rusd', 'tokeusd', 'efilfil', 'gusdusd']
```

---

### *holdings*

Display user's current holdings

### `holdings`

```
$ holdings
[
{
"amount": "0.37477794",
"available": "0.37477794",
"availableForWithdrawal": "0.37477794",
"currency": "BTC",
"type": "exchange"
},
{
"amount": "3.992933",
"available": "3.992933",
"availableForWithdrawal": "3.992933",
"currency": "ETH",
"type": "exchange"
},
{
"amount": "50958.3450725145415",
"available": "50958.34",
"availableForWithdrawal": "958.34",
"currency": "USD",
"type": "exchange"
}
]
```

---

### *history*

Display user's order history for a given symbol

### `history SYMBOL [num_entries=1]`

```
$ history ETHUSD 1
{
"aggressor": false,
"amount": "0.001",
"exchange": "gemini",
"fee_amount": "0.00289",
"fee_currency": "USD",
"is_auction_fill": false,
"is_clearing_fill": false,
"order_id": "89832119161",
"price": "2893.66",
"symbol": "ETHUSD",
"tid": 89832145235,
"timestamp": 1645140475,
"timestampms": 1645140475118,
"type": "Sell"
}
```

---

### *active*

### `active`

This command will list the users active trades on the order book

---

### *buy*

### `buy SYMBOL [quantity]`

**Note: For the 'buy' command, if quantity is omitted, you will be prompted for a quantity later.**

The command `buy ethusd`, will prompt the user to enter a  quantity:

```
$ buy ethusd
{'symbol': 'ethusd', 'max_bid': 2813.52, 'min_ask': 2814.59, 'spread': 1.0700000000001637}
Quantity (max = ~18.1119522875 ETH):
```

Pressing enter here will use the max quantity, otherwise enter a quantity.

```
Quantity (max = ~18.3597269010 ETH): 0.001
{'symbol': 'ethusd', 'max_bid': 2777.92, 'min_ask': 2778.01, 'spread': 0.09000000000014552}
price:                  $2,777.92
quantity:                0.001
investment_USD:         $2.78
fee:                    $0.00
investment + fee:       $2.78
buy 0.00100000 ETH @ $2,777.92 for $2.78 ? Y/N?
```

**Caution:** typing `Y` here and pressing enter with submit the order on the order book.

*Hint: typing `R` here will generate a new suggested price based on the current highest bid on the
order book*

```
buy 0.00100000 ETH @ $2,777.92 for $2.78 ? Y/N? N
Goodbye.
```

---

### *invest*

Use the invest command to "invest" N number of currency (ex. USD) on a commodity (ex. ETH)

### `invest SYMBOL [total_investment]`

**Note: For the 'invest' command, if `total_investment` is omitted, you will be prompted for a quantity later.**

The command `invest ethusd`, will prompt the user to enter a  quantity:

```
$ invest ETHUSD
Quantity (max = 50958.3400000000 USD):
```

Pressing enter here will use the max quantity, otherwise enter a quantity.

```
Quantity (max = ~18.3597269010 ETH): 0.001
{'symbol': 'ethusd', 'max_bid': 2777.92, 'min_ask': 2778.01, 'spread': 0.09000000000014552}
price:                  $2,777.92
quantity:                0.001
investment_USD:         $2.78
fee:                    $0.00
investment + fee:       $2.78
buy 0.00100000 ETH @ $2,777.92 for $2.78 ? Y/N?
```

**Caution:** typing `Y` here and pressing enter with submit the order on the order book.

*Hint: typing `R` here will generate a new suggested price based on the current highest bid on the
order book*

```
buy 0.00100000 ETH @ $2,777.92 for $2.78 ? Y/N? N
Goodbye.
```

---

### *sell*

### `sell SYMBOL [quantity]`

**Note: For the 'sell' command, if quantity is omitted, you will be prompted for a quantity later.**

The command `sell ethusd`, will prompt the user to enter a  quantity:

```
$ sell ethusd
Quantity (max = 3.9929330000 ETH):
```

Pressing enter here will use the max quantity, otherwise enter a quantity.

```
Quantity (max = 3.9929330000 ETH): 0.001
{'symbol': 'ethusd', 'max_bid': 2777.89, 'min_ask': 2778.6, 'spread': 0.7100000000000364}
price:                  $2,778.60
trade_total_USD:        $2.78
quantity:                0.001
fee:                    $0.00
return (USD) after fees:$ 2.7758214
sell 0.00100000 ETH @ $2,778.60 for $2.78? Y/N?
```

**Caution:** typing `Y` here and pressing enter with submit the order on the order book.

*Hint: typing `R` here will generate a new suggested price based on the current lowest ask on the
order book*

```
sell 0.00100000 ETH @ $2,778.60 for $2.78? Y/N? N
Goodbye.
$
```
---

