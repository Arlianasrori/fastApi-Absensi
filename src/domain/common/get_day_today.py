from datetime import datetime
from ...types.hari_list import dayCodeSet
async def get_day() -> dict:
    # Mendapatkan hari ini (1-7, di mana 1 adalah Senin)
    day_code = (datetime.now().isoweekday()) - 1
    return {
        "day_code" : day_code,
        "day_name" : dayCodeSet[day_code]
    }
