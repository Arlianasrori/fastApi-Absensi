import os 

async def deleteImageList(fileList : list[dict],FILE_LAPORAN_STORE : str) :
    for fileLaporanItem in fileList :
        file_nama_db_split = fileLaporanItem.file.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{FILE_LAPORAN_STORE}/{file_name_db}")