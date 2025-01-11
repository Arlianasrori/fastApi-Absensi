import os 

async def deleteImage(fileUrl : str,FILE_LAPORAN_STORE : str) :
    file_nama_db_split = fileUrl.split("/")
    file_name_db = file_nama_db_split[-1]
    os.remove(f"{FILE_LAPORAN_STORE}/{file_name_db}")