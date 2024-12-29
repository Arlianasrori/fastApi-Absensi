from enum import Enum

class UserType(Enum) :
    SISWA = "siswa"
    GURU_WALAS = "guru_walas"
    GURU_MAPEL = "guru_mapel"
    PETUGAS_BK = "petugas_bk"
    DEVELOPER = "developer"
    ADMIN = "admin"

class GenderType(Enum) :
    laki = "laki"
    perempuan = "perempuan"

class EnvSecretTokenType(Enum) :
    SISWA = "SISWA"
    GURU_WALAS = "GURU_WALAS"
    GURU_MAPEL = "GURU_MAPEL"
    PETUGAS_BK = "PETUGAS_BK"
    DEVELOPER = "DEVELOPER"
    ADMIN = "ADMIN"