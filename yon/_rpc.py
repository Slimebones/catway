"""
Remote procedure call support for yon.

Core messages - RpcReq and RpcEvt. Each of it has identification "key", in
format "<fn_code>::<token>". Token is UUID4 string to differentiate which
exact call should receive the result. Token is generated by client.

Rpc works only in network mode (client-server communication).
"""
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel
from ryz.res import Res

from yon._msg import Mbody


class EmptyRpcArgs(BaseModel):
    """
    When you need to use empty args for your rpc function.
    """

class SrpcSend(BaseModel):
    key: str
    body: dict
    """
    Any parseable kwargs passed to rpc fn.
    """

    @staticmethod
    def code() -> str:
        return "yon::srpc_send"

class SrpcRecv(BaseModel):
    """
    Only ``val`` field directly passed to serialization, so the msg's body
    contain this directly.
    """
    val: Any
    """
    Returned value can be anything serializable or an exception, which will
    be serialized to ErrDto.
    """

    @staticmethod
    def code() -> str:
        return "yon::srpc_recv"

class RpcFn(Protocol):
    """
    Function that can be used as RPC endpoint.

    Must accept data in form of validated pydantic model. Must return
    serializable object.
    """
    # it's not "data: BaseModel" since we haven't yet found how to allow it
    # to accept any instance of BaseModel
    #
    # ...and we don't want to use generics here, for now
    async def __call__(self, msg: Mbody) -> Res[Any]: ...
TRpcFn = TypeVar("TRpcFn", bound=RpcFn)
