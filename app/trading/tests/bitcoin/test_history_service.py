# import datetime
#
# from pinkiepie_trading.coin.models.bitcoin import BitCoin
# from pinkiepie_trading.coin.repositories.history_reader import (
#     BitcoinHistoryReaderRepository,
# )
# from pinkiepie_trading.coin.services.history_service import (
#     BitcoinHistoryService,
# )
#
#
# def test_get_by(session, bitcoin_factory):
#     # given
#     target_date = datetime.datetime.now().date()
#     bitcoin_factory(
#         price=50643.1,
#         open=48,
#         high=899,
#         low=51,
#         volume=111,
#         change=48,
#         date=target_date,
#     )
#
#     repository = BitcoinHistoryReaderRepository(session=session)
#     service = BitcoinHistoryService(repository)
#
#     # when
#     bitcoin = service.get_by(target_date)
#
#     # then
#     assert isinstance(bitcoin, BitCoin)
#     assert bitcoin.date == target_date
#
#
# def test_get_list_by(session, bitcoin_factory):
#     # given
#     history_count = 10
#
#     end_date = datetime.datetime.now().date()
#     start_date = end_date - datetime.timedelta(days=history_count)
#
#     for day in range(history_count):
#         bitcoin_factory(
#             price=50643.1,
#             open=48,
#             high=899,
#             low=51,
#             volume=111,
#             change=48,
#             date=start_date + datetime.timedelta(days=day),
#         )
#
#     repository = BitcoinHistoryReaderRepository(session=session)
#     service = BitcoinHistoryService(repository)
#
#     # when
#     history = service.get_list_by(start_date, end_date)
#
#     # then
#     assert len(history) == history_count
