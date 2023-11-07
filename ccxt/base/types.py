import sys
import types
from typing import Union, List, Optional
from decimal import Decimal

if sys.version_info.minor > 7:
    from typing import TypedDict, Literal, Dict
else:
    from typing import Dict
    from typing_extensions import Literal
    TypedDict = Dict


OrderSide = Literal['buy', 'sell']
OrderType = Literal['limit', 'market']
PositionSide = Literal['long', 'short']


class Entry:
    def __init__(self, path, api, method, config):
        self.name = None
        self.path = path
        self.api = api
        self.method = method
        self.config = config

        def unbound_method(_self, params={}):
            return _self.request(self.path, self.api, self.method, params, config=self.config)

        self.unbound_method = unbound_method

    def __get__(self, instance, owner):
        if instance is None:
            return self.unbound_method
        else:
            return types.MethodType(self.unbound_method, instance)

    def __set_name__(self, owner, name):
        self.name = name


IndexType = Union[str, int]
Numeric = Union[None, str, float, int, Decimal]


class Balance(TypedDict):
    free: Numeric
    used: Numeric
    total: Numeric

class Fee(TypedDict):
    type: Optional[str]
    currency: Optional[str]
    rate: Optional[Numeric]
    cost: Numeric

class Trade(TypedDict):
    amount: Numeric
    datetime: str
    id: str
    info: None
    order: str
    price: Numeric
    timestamp: int
    type: str
    side: str
    symbol: str
    takerOrMaker: str
    cost: Numeric
    fee: Fee


class Position(TypedDict):
    symbol: str
    id: str
    timestamp: int
    datetime: str
    contracts: Numeric
    contractSize: Numeric
    side: str
    notional: Numeric
    leverage: Numeric
    unrealizedPnl: Numeric
    realizedPnl: Numeric
    collateral: Numeric
    entryPrice: Numeric
    markPrice: Numeric
    liquidationPrice: Numeric
    hedged: bool
    maintenanceMargin: Numeric
    initialMargin: Numeric
    initialMarginPercentage: Numeric
    marginMode: str
    marginRatio: Numeric
    lastUpdateTimestamp: int
    lastPrice: Numeric
    percentage: Numeric
    stopLossPrice: Numeric
    takeProfitPrice: Numeric
    info: Dict[str, any]


class OrderRequest(TypedDict):
    symbol: str
    type: str
    side: str
    amount: Union[None, float]
    price: Union[None, float]
    params: Dict[str, any]


class Order(TypedDict):
    id: str
    clientOrderId: str
    datetime: str
    timestamp: int
    lastTradeTimestamp: int
    lastUpdateTimestamp: Optional[int]
    status: str
    symbol: str
    type: str
    timeInForce: str
    side: OrderSide
    price: Numeric
    average: Optional[Numeric]
    amount: Numeric
    filled: Numeric
    remaining: Numeric
    stopPrice: Optional[Numeric]
    takeProfitPrice: Optional[Numeric]
    stopLossPrice: Optional[Numeric]
    cost: Numeric
    trades: List[Trade]
    fee: Fee
    info: Dict[str, any]


class FundingHistory(TypedDict):
    info: Dict[str, any]
    symbol: str
    code: str
    timestamp: Optional[int]
    datetime: Optional[str]
    id: str
    amount: Numeric



class Balances(Dict[str, Balance]):
    datetime: Optional[str]
    timestamp: Optional[int]

