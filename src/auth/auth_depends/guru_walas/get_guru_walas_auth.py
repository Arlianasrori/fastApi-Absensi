from fastapi import Request

async def getWalasAuth(req : Request) :
    return req.guruWalas