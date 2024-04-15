from flask import Flask, request
from quotation.OrderBooks import OrderBooks
from usercenter.Deposit import Deposit

app = Flask(__name__)


@app.route('/quotation/orderBooks', methods=["post"])
def drape_order():
    """铺单"""
    data = request.json
    return OrderBooks.drape_order_book(**data)


@app.route("/usercenter/deposit", methods=["post"])
def admin_deposit():
    data = request.json
    return Deposit.admin_deposit(**data)


@app.route("/coinslist", methods=["get"])
def coins_list():
    return [
        {'coinName': 'BTC', 'coinId': '1'},
        {'coinName': 'ETH', 'coinId': '2'},
        {'coinName': 'USDT', 'coinId': '3'},
    ]


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
