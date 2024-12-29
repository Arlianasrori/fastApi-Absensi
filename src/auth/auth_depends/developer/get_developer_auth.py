from fastapi import Request

async def getDeveloperAuth(req : Request) :
    return req.developer