import pytest

from pinkiepie_trading.stock.repositories.stock_firm_reader import (
    StockFirmReader,
)


@pytest.mark.asyncio
async def test_get_list(session, firm_factory):
    # given
    total_length = 10
    expected_length = 5
    for i in range(total_length):
        await firm_factory(name=f"KB_{i}", trading_fee=0.1)

    reader = StockFirmReader(session)

    # when
    firms = await reader.get_list(limit=expected_length)

    # then
    assert len(firms) == expected_length
