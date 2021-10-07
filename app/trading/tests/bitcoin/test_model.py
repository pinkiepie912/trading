# import datetime
#
# from trading_db.rdb.bitcoin import Bitcoin as SABitcoin
#
# from pinkiepie_trading.coin.models.bitcoin import BitCoin
#
#
# def test_of():
#     # given
#     sa_obj = SABitcoin(
#         price=50643.1,
#         open=48,
#         high=899,
#         low=51,
#         volume=111,
#         change=48,
#         date=datetime.datetime.now().date,
#     )
#
#     # when
#     bitcoin = BitCoin.of(sa_obj)
#
#     # then
#     assert bitcoin.price == sa_obj.price
#     assert bitcoin.open == sa_obj.open
#     assert bitcoin.high == sa_obj.high
#     assert bitcoin.volume == sa_obj.volume
#     assert bitcoin.change == sa_obj.change
#     assert bitcoin.date == sa_obj.date
