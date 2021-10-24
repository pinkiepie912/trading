from datetime import datetime, timezone

import pytest
from trading_db.rdb.constants import Currency, StockType

from pinkiepie_trading.stock.repositories.stock_asset_reader import (
    StockAssetReader,
)


@pytest.mark.asyncio
async def test_get_count(
    session, firm_factory, ticker_factory, stock_asset_factory
):
    # given
    expected_cnt = 10

    firm = await firm_factory(id=1, name="KB증권", trading_fee=0.1)
    ticker = await ticker_factory(
        id=1,
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    for idx in range(expected_cnt):
        sell_price = 0
        sold_at = None
        if idx % 2 == 0:
            sell_price = 100
            sold_at = datetime.now(timezone.utc)

        await stock_asset_factory(
            ticker_id=ticker.id,
            description="",
            currency=Currency.USD,
            purchase_price=10,
            sell_price=sell_price,
            amount=10,
            purchased_at=datetime.now(timezone.utc),
            sold_at=sold_at,
            ticker=ticker,
        )

    reader = StockAssetReader(session)

    # when
    count = await reader.get_count()
    has_not_yet_sold_count = await reader.get_count(has_not_yet_sold_only=True)

    # then
    assert count == expected_cnt
    assert has_not_yet_sold_count == expected_cnt / 2


@pytest.mark.asyncio
async def test_get_assets(
    session, firm_factory, ticker_factory, stock_asset_factory
):
    # given
    expected_cnt = 10

    firm = await firm_factory(id=1, name="KB증권", trading_fee=0.1)
    ticker = await ticker_factory(
        id=1,
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    for idx in range(expected_cnt):
        sell_price = 0
        sold_at = None
        if idx % 2 == 0:
            sell_price = 100
            sold_at = datetime.now(timezone.utc)

        await stock_asset_factory(
            ticker_id=ticker.id,
            description="",
            currency=Currency.USD,
            purchase_price=10,
            sell_price=sell_price,
            amount=10,
            purchased_at=datetime.now(timezone.utc),
            sold_at=sold_at,
            ticker=ticker,
        )

    reader = StockAssetReader(session)

    # when
    assets = await reader.get_assets()
    not_yet_sold_assets = await reader.get_assets(has_not_yet_sold_only=True)

    # then
    assert len(assets) == expected_cnt
    assert all([asset.has_not_yet_sold for asset in not_yet_sold_assets])
