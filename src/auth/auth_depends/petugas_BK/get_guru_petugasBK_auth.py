from fastapi import Request

async def getPetugasBKAuth(req : Request) :
    return req.petugasBK