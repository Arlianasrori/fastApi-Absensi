from fastapi import Request

async def getMapelAuth(req : Request) :
    return req.guruMapel