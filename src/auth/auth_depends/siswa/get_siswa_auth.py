from fastapi import Request

async def getSiswaAuth(req : Request) :
    return req.siswa