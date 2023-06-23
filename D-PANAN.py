import psycopg2 
from tabulate import tabulate as tb
import os
from datetime import datetime
import time

os.system("cls")

# CONNECT
def connect():
    global con
    con = psycopg2.connect(
    database="lapangan",
    user="postgres",
    password="admin",
    host="localhost",
    port= '5432'
    )

# READ
def readHeaderLap():
    connect()
    gedung_obj = con.cursor()
    gedung_obj.execute('SELECT nama_gedung from gedung ORDER BY id_gedung')
    namaGedung = gedung_obj.fetchall()
    nomor = 1
    listGedung = []
    for i in namaGedung:
        i_list = list(i)
        listGedung.append(i_list[0])
    for x in listGedung:
        print(f"{nomor}. {x}")
        nomor += 1
    pilGedung = int(input("Pilih disini: "))
    cursor_obj = con.cursor()
    cursor_obj.execute(f'SELECT nomor_lapangan from detail_gedung where gedung_id = {pilGedung} ORDER BY id_detail')
    nomorLapangan = cursor_obj.fetchall()
    for i in nomorLapangan:
        i_list = list(i)
        header.append(i_list[0])
    return pilGedung

def readJam():
    connect()
    cursor_obj = con.cursor()
    cursor_obj.execute('SELECT jam_sewa from jam')
    jam = cursor_obj.fetchall()
    listJam = []
    for i in jam:
        i_list = list(i)
        for x in range(len(header)-1):
            i_list.append('')
        listJam.append(i_list)
    return listJam

def readJadwalAdmin():
    kodeGedung = readHeaderLap()
    nomorLap = header[1:]
    jadwalJam = readJam()
    cursor_obj = con.cursor()
    cursor_obj.execute(f'SELECT username_user, jam_sewa, nomor_lapangan, gedung_id, tanggal FROM pemesanan INNER JOIN detail_gedung ON id_detail = detail_id INNER JOIN "user" ON id_user = user_id INNER JOIN jam ON id_jam = jam_id INNER JOIN gedung ON id_gedung = gedung_id WHERE gedung_id = {kodeGedung}')
    dataPesanan = cursor_obj.fetchall()
    tglCek = input("Masukkan tanggal yang ingin dicek [dd/mm/yyyy, misal: 30/05/2023]: ")
    for i in dataPesanan:
        tgl = i[4]
        tglFmt = tgl.strftime('%d/%m/%Y')
        if tglFmt == tglCek:
            if kodeGedung == i[3]:
                kodeLap = i[2]
                kodeJam = i[1]
                kodeNama = i[0]
                counterLap = 0
                for x in nomorLap:
                    if kodeLap == x:
                        counterJam = 0
                        for y in jadwalJam:
                            if y[0] == kodeJam:
                                jadwalJam[counterJam][counterLap+1] = kodeNama
                            else:
                                counterJam += 1
                    else:
                        counterLap += 1
    print(tb(jadwalJam, headers=header, tablefmt="fancy_grid"))
    lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
    if lagi == 'y':
        os.system('cls')
        subReadAdmin()
    elif lagi == 'n':
        menuAdmin()

def readJadwalUser():
    kodeGedung = readHeaderLap()
    nomorLap = header[1:]
    jadwalJam = readJam()
    cursor_obj = con.cursor()
    cursor_obj.execute(f'SELECT username_user, jam_sewa, nomor_lapangan, gedung_id, tanggal FROM pemesanan INNER JOIN detail_gedung ON id_detail = detail_id INNER JOIN "user" ON id_user = user_id INNER JOIN jam ON id_jam = jam_id INNER JOIN gedung ON id_gedung = gedung_id WHERE gedung_id = {kodeGedung}')
    dataPesanan = cursor_obj.fetchall()
    tglCek = input("Masukkan tanggal yang ingin dicek [dd/mm/yyyy, misal: 30/05/2023]: ")
    for i in dataPesanan:
        tgl = i[4]
        tglFmt = tgl.strftime('%d/%m/%Y')
        if tglFmt == tglCek:
            if kodeGedung == i[3]:
                kodeLap = i[2]
                kodeJam = i[1]
                kodeNama = i[0]
                counterLap = 0
                for x in nomorLap:
                    if kodeLap == x:
                        counterJam = 0
                        for y in jadwalJam:
                            if y[0] == kodeJam:
                                jadwalJam[counterJam][counterLap+1] = kodeNama
                            else:
                                counterJam += 1
                    else:
                        counterLap += 1
    print(tb(jadwalJam, headers=header, tablefmt="fancy_grid"))
    lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
    if lagi == 'y':
        os.system('cls')
        subReadUser()
    elif lagi == 'n':
        menuUser()

# SUBREAD
def subReadAdmin():
    lagi = 'y'
    while lagi == 'y':
        print("1. Lihat jadwal pada gedung")
        print("2. Sorting Data")
        print("3. Searching Data")
        print("4. Kembali ke menu utama")
        pilih = int(input("Pilih disini: "))
        if pilih == 1:
            global header
            header = ["jam"]
            readJadwalAdmin()
        elif pilih == 2:
            print("\n1. Sorting berdasarkan nama pemesan")
            print("2. Sorting berdasarkan tanggal sewa")
            print("3. Sorting berdasarkan jam sewa")
            pilih2 = int(input("Pilih disini: "))
            listDataSorting = bahanSorting()
            headerSub = ["ID Pemesanan", "Nama", "Tanggal Sewa", "Jam Sewa", "Nama Gedung", "Nomor Lapangan"]
            if pilih2 == 1:
                print(tb(selectionSort(listDataSorting, 1), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()
            elif pilih2 == 2:
                print(tb(selectionSort(listDataSorting, 2), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()                
            elif pilih2 == 3:
                print(tb(selectionSort(listDataSorting, 3), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()
        elif pilih == 3:
            print("\n1. Searching nama pemesan")
            print("2. Searching berdasarkan gedung")
            print("3. Searching secara spesifik")
            pilih3 = int(input("Pilih disini: "))
            listDataSearching = bahanSearching()
            headerSub = ["Nama", "Tanggal Sewa", "Jam Sewa", "Nama Gedung", "Nomor Lapangan"]
            if pilih3 == 1:
                key = input("Masukkan Nama Pemesan yang ingin dicari: ").lower()
                print(tb(linearSearch(listDataSearching, key, 0), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()
            elif pilih3 == 2:
                key = input("Masukkan Nama Gedung: ")
                print(tb(linearSearch(listDataSearching, key, 3), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()
            elif pilih3 == 3:
                nama = input("Masukkan Nama Pemesan: ").lower()
                tgl = input("Masukkan tanggal pemesanan [30/05/2023]: ")
                tgl_format = datetime.strptime(f"{tgl}", "%d/%m/%Y")
                tgl_formatt = tgl_format.date()
                key = [nama, tgl_formatt]
                print(tb(linearSearchSpes(listDataSearching, key), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadAdmin()
                elif lagi == 'n':
                    menuAdmin()
        elif pilih == 4:
            menuAdmin()

def subReadUser():
    lagi = 'y'
    while lagi == 'y':
        print("1. Lihat jadwal pada gedung")
        print("2. Sorting Data")
        print("3. Searching Data")
        print("4. Kembali ke menu utama")
        pilih = int(input("Pilih disini: "))
        if pilih == 1:
            global header
            header = ["jam"]
            readJadwalUser()
        elif pilih == 2:
            print("\n1. Sorting berdasarkan nama pemesan")
            print("2. Sorting berdasarkan tanggal sewa")
            print("3. Sorting berdasarkan jam sewa")
            pilih2 = int(input("Pilih disini: "))
            listDataSorting = bahanSorting()
            headerSub = ["ID Pemesanan", "Nama", "Tanggal Sewa", "Jam Sewa", "Nama Gedung", "Nomor Lapangan"]
            if pilih2 == 1:
                print(tb(selectionSort(listDataSorting, 1), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()
            elif pilih2 == 2:
                print(tb(selectionSort(listDataSorting, 2), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()                
            elif pilih2 == 3:
                print(tb(selectionSort(listDataSorting, 3), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()
        elif pilih == 3:
            print("\n1. Searching nama pemesan")
            print("2. Searching berdasarkan gedung")
            print("3. Searching secara spesifik")
            pilih3 = int(input("Pilih disini: "))
            listDataSearching = bahanSearching()
            headerSub = ["Nama", "Tanggal Sewa", "Jam Sewa", "Nama Gedung", "Nomor Lapangan"]
            if pilih3 == 1:
                key = input("Masukkan Nama Pemesan yang ingin dicari: ").lower()
                print(tb(linearSearch(listDataSearching, key, 0), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()
            elif pilih3 == 2:
                key = input("Masukkan Nama Gedung: ")
                print(tb(linearSearch(listDataSearching, key, 3), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()
            elif pilih3 == 3:
                nama = input("Masukkan Nama Pemesan: ").lower()
                tgl = input("Masukkan tanggal pemesanan [30/05/2023]: ")
                tgl_format = datetime.strptime(f"{tgl}", "%d/%m/%Y")
                tgl_formatt = tgl_format.date()
                key = [nama, tgl_formatt]
                print(tb(linearSearchSpes(listDataSearching, key), headers=headerSub, tablefmt="fancy_grid"))
                lagi = input("Apakah ingin memilih menu Read lagi? [y/n]: ").lower()
                if lagi == 'y':
                    os.system('cls')
                    subReadUser()
                elif lagi == 'n':
                    menuUser()
        elif pilih == 4:
            menuUser()

# CREATE
def createJadwalAdmin():
    connect()
    headerDetail = ["Nomor", "Nomor Lapangan", "Nama Gedung"]
    detail_obj = con.cursor()
    detail_obj.execute('SELECT id_detail, nomor_lapangan, nama_gedung from detail_gedung inner join gedung on id_gedung = gedung_id order by id_detail')
    detail_gedung = detail_obj.fetchall()
    print(tb(detail_gedung, headers=headerDetail, tablefmt="fancy_grid"))
    pilDetail = int(input("Silahkan masukkan nomor lapangan yang ingin dipilih: "))
    print()
    
    headerJam = ["Nomor", "Jam"]
    jam_obj = con.cursor()
    jam_obj.execute('SELECT id_jam, jam_sewa from jam order by id_jam')
    jam = jam_obj.fetchall()
    print(tb(jam, headers = headerJam, tablefmt="fancy_grid"))
    pilJam = int(input("Silahkan masukkan nomor jadwal jam yang ingin dipilih: "))
    print()
    
    headerUser = ["Nomor", "Nama User"]
    user_obj = con.cursor()
    user_obj.execute('SELECT id_user, username_user from "user" order by id_user')
    user = user_obj.fetchall()
    print(tb(user, headers = headerUser, tablefmt="fancy_grid"))
    pilUser = int(input("Silahkan masukkan nomor user yang ingin memesan: "))
    print()

    tglPesan = input("Masukkan tanggal pemesanan [dd/mm/yyyy, misal: 30/05/2023]: ")
    tgl_format = datetime.strptime(f"{tglPesan}", "%d/%m/%Y")
    tgl_formatt = tgl_format.date()
    
    pesanan_obj = con.cursor()
    pesanan_obj.execute(f"SELECT detail_id, jam_id, tanggal, user_id from pemesanan where tanggal = '{tgl_formatt}' and detail_id = {pilDetail} and jam_id = {pilJam}")
    pesanan = pesanan_obj.fetchall()
    if pesanan == []:
        create_obj = con.cursor()
        queryCreate = f"INSERT INTO pemesanan (detail_id, jam_id, tanggal, user_id) VALUES ({pilDetail}, {pilJam}, '{tgl_formatt}', {pilUser});"
        create_obj.execute(queryCreate)
        con.commit()
        print("\nCreate Jadwal Berhasil!")
        lagi = input("Apakah ingin create jadwal lagi? [y/n]: ").lower()
        if lagi == 'y':
            createJadwalAdmin()
        elif lagi == 'n':
            menuAdmin()
        
    else:
        print("Maaf, sudah ada pesanan pada tanggal, lapangan, dan jam yang sama, silahkan pilih yang lain")
        for i in range(3):
            print(".")
            time.sleep(1)
        os.system("cls")
        createJadwalAdmin()

def createJadwalUser():
    connect()
    headerDetail = ["Nomor", "Nomor Lapangan", "Nama Gedung"]
    detail_obj = con.cursor()
    detail_obj.execute('SELECT id_detail, nomor_lapangan, nama_gedung from detail_gedung inner join gedung on id_gedung = gedung_id order by id_detail')
    detail_gedung = detail_obj.fetchall()
    print(tb(detail_gedung, headers=headerDetail, tablefmt="fancy_grid"))
    pilDetail = int(input("Silahkan masukkan nomor lapangan yang ingin dipilih: "))
    print()
    
    headerJam = ["Nomor", "Jam"]
    jam_obj = con.cursor()
    jam_obj.execute('SELECT id_jam, jam_sewa from jam order by id_jam')
    jam = jam_obj.fetchall()
    print(tb(jam, headers = headerJam, tablefmt="fancy_grid"))
    pilJam = int(input("Silahkan masukkan nomor jadwal jam yang ingin dipilih: "))
    print()
    
    headerUser = ["Nomor", "Nama User"]
    user_obj = con.cursor()
    user_obj.execute('SELECT id_user, username_user from "user" order by id_user')
    user = user_obj.fetchall()
    print(tb(user, headers = headerUser, tablefmt="fancy_grid"))
    pilUser = int(input("Silahkan masukkan nomor user yang ingin memesan: "))
    print()

    tglPesan = input("Masukkan tanggal pemesanan [dd/mm/yyyy, misal: 30/05/2023]: ")
    tgl_format = datetime.strptime(f"{tglPesan}", "%d/%m/%Y")
    tgl_formatt = tgl_format.date()
    
    pesanan_obj = con.cursor()
    pesanan_obj.execute(f"SELECT detail_id, jam_id, tanggal, user_id from pemesanan where tanggal = '{tgl_formatt}' and detail_id = {pilDetail} and jam_id = {pilJam}")
    pesanan = pesanan_obj.fetchall()
    if pesanan == []:
        create_obj = con.cursor()
        queryCreate = f"INSERT INTO pemesanan (detail_id, jam_id, tanggal, user_id) VALUES ({pilDetail}, {pilJam}, '{tgl_formatt}', {pilUser});"
        create_obj.execute(queryCreate)
        con.commit()
        print("\nCreate Jadwal Berhasil!")
        lagi = input("Apakah ingin create jadwal lagi? [y/n]: ").lower()
        if lagi == 'y':
            createJadwalUser()
        elif lagi == 'n':
            menuUser()
        
    else:
        print("Maaf, sudah ada pesanan pada tanggal, lapangan, dan jam yang sama, silahkan pilih yang lain")
        for i in range(3):
            print(".")
            time.sleep(1)
        os.system("cls")
        createJadwalUser()

# UPDATE
def updateJadwal():
    connect()
    headerPilih = ["Nomor", "Nama", "Gedung", "Nomor Lapangan", "Jam Sewa", "Tanggal"]
    pilih_obj = con.cursor()
    pilih_obj.execute(f'SELECT id_pemesanan, username_user, nama_gedung, nomor_lapangan, jam_sewa, tanggal from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
    pilih = pilih_obj.fetchall()
    print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
    pilihUpdate = int(input("Silahkan pilih nomor yang ingin di update: "))
    print()
    
    headerDetail = ["Nomor", "Nomor Lapangan", "Nama Gedung"]
    detail_obj = con.cursor()
    detail_obj.execute('SELECT id_detail, nomor_lapangan, nama_gedung from detail_gedung inner join gedung on id_gedung = gedung_id order by id_detail')
    detail_gedung = detail_obj.fetchall()
    print(tb(detail_gedung, headers=headerDetail, tablefmt="fancy_grid"))
    pilDetail = int(input("Silahkan masukkan nomor lapangan yang ingin dipilih: "))
    print()
    
    headerJam = ["Nomor", "Jam"]
    jam_obj = con.cursor()
    jam_obj.execute('SELECT id_jam, jam_sewa from jam order by id_jam')
    jam = jam_obj.fetchall()
    print(tb(jam, headers = headerJam, tablefmt="fancy_grid"))
    pilJam = int(input("Silahkan masukkan nomor jadwal jam yang ingin dipilih: "))
    print()
    
    headerUser = ["Nomor", "Nama User"]
    user_obj = con.cursor()
    user_obj.execute('SELECT id_user, username_user from "user" order by id_user')
    user = user_obj.fetchall()
    print(tb(user, headers = headerUser, tablefmt="fancy_grid"))
    pilUser = int(input("Silahkan masukkan nomor user yang ingin memesan: "))
    print()

    tglPesan = input("Masukkan tanggal pemesanan [dd/mm/yyyy, misal: 30/05/2023]: ")
    tgl_format = datetime.strptime(f"{tglPesan}", "%d/%m/%Y")
    tgl_formatt = tgl_format.date()
    
    pesanan_obj = con.cursor()
    pesanan_obj.execute(f"SELECT detail_id, jam_id, tanggal, user_id from pemesanan where tanggal = '{tgl_formatt}' and detail_id = {pilDetail} and jam_id = {pilJam} and user_id = {pilUser}")
    pesanan = pesanan_obj.fetchall()
    if pesanan == []:
        update_obj = con.cursor()
        queryUpdate = f"UPDATE pemesanan SET detail_id = {pilDetail}, jam_id = {pilJam}, tanggal = '{tgl_formatt}', user_id = {pilUser} WHERE id_pemesanan = {pilihUpdate}"
        update_obj.execute(queryUpdate)
        con.commit()
        print("\nUpdate Jadwal Berhasil!")
        pilih_obj.execute(f'SELECT id_pemesanan, username_user, nama_gedung, nomor_lapangan, jam_sewa, tanggal from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
        pilih = pilih_obj.fetchall()
        print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
        lagi = input("Apakah ingin update jadwal lagi? [y/n]: ").lower()
        if lagi == 'y':
            updateJadwal()
        elif lagi == 'n':
            menuAdmin()
    else:
        print("Maaf, sudah ada pesanan pada tanggal, lapangan, dan jam yang sama, silahkan pilih yang lain")
        for i in range(3):
            print(".")
            time.sleep(1)
        os.system("cls")
        updateJadwal()

# DELETE
def deleteJadwal():
    connect()
    headerPilih = ["Nomor", "Nama", "Gedung", "Nomor Lapangan", "Jam Sewa", "Tanggal"]
    pilih_obj = con.cursor()
    pilih_obj.execute(f'SELECT id_pemesanan, username_user, nama_gedung, nomor_lapangan, jam_sewa, tanggal from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
    pilih = pilih_obj.fetchall()
    print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
    pilihDelete = int(input("Silahkan pilih nomor yang ingin di delete: "))
    print()
    
    delete_obj = con.cursor()
    queryDelete = f"DELETE FROM pemesanan WHERE id_pemesanan = {pilihDelete};"
    delete_obj.execute(queryDelete)
    con.commit()
    print("\nDelete Jadwal Berhasil!")
    pilih_obj.execute(f'SELECT id_pemesanan, username_user, nama_gedung, nomor_lapangan, jam_sewa, tanggal from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
    pilih = pilih_obj.fetchall()
    print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
    lagi = input("Apakah ingin delete jadwal lagi? [y/n]: ").lower()
    if lagi == 'y':
        deleteJadwal()
    elif lagi == 'n':
        menuAdmin()

# REGISTER
def registerUser():
    connect()
    user_obj = con.cursor()
    user_obj.execute('SELECT username_user, password_user from "user"')
    user = user_obj.fetchall()
    listUser = []
    for i in user:
        i_list = list(i)
        listUser.append(i_list)
    print("--------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI REGISTER USER                       |")
    print("--------------------------------------------------------------------------")
    time.sleep(3)
    username = input("\nMasukkan Username anda: ")
    for i in listUser:
        if username == i[0]:
            print("\nUsername telah ada, silahkan pilih username lain\n")
            return registerUser()
    password = input("Masukkan Password Anda: ")
    create_obj = con.cursor()
    queryCreate = f"INSERT INTO \"user\" (username_user, password_user) VALUES ('{username}', '{password}');"
    create_obj.execute(queryCreate)
    con.commit()
    print("\nRegister Akun User Berhasil!\n")
    for i in range(3):
        print(".")
        time.sleep(1)
    print("Ingin lanjut login?")
    print("1. Ya, Login")
    print("2. Exit")
    pilih = int(input("Pilih disini: "))
    if pilih == 1:
        os.system('cls')
        loginUser()
    elif pilih == 2:
        os.system('cls')
        exit

# LOGIN
def loginAdmin():
    connect()
    admin_obj = con.cursor()
    admin_obj.execute('SELECT username_admin, password_admin from admin')
    admin = admin_obj.fetchall()
    listAdmin = []
    for i in admin:
        i_list = list(i)
        listAdmin.append(i_list)
    print("------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI LOGIN ADMIN                       |")
    print("------------------------------------------------------------------------")
    time.sleep(3)
    username = input("\nMasukkan Username anda: ")
    password = input("Masukkan Password Anda: ")
    def check():
        for i in listAdmin:
            if username != i[0]:
                continue
            elif username == i[0] and password != i[1]:
                print("\nPassword Salah!\n")
                loginAdmin()
                return 1
            elif username == i[0] and password == i[1]:
                kata = "Login Sukses"
                kata2 = "Loading..."
                for i in range(0,101):
                    print("\r{0}{1}%".format(kata2,i),end="")
                    time.sleep(0.005)
                print(kata)
                menuAdmin()
                return 1
    cek = check()
    if cek != 1:
        print("Login Gagal")
        for i in range(3):
            print(".")
            time.sleep(1)
        print("Apakah anda admin? Jika bukan, coba login user!")
        print("1. Coba login Admin lagi")
        print("2. Login User")
        pilih = int(input("Pilih disini: "))
        if pilih == 1:
            os.system('cls')
            loginAdmin()
        elif pilih == 2:
            os.system('cls')
            loginUser()
        
def loginUser():
    connect()
    user_obj = con.cursor()
    user_obj.execute('SELECT username_user, password_user from "user"')
    user = user_obj.fetchall()
    listUser = []
    for i in user:
        i_list = list(i)
        listUser.append(i_list)
    print("------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI LOGIN USER                        |")
    print("------------------------------------------------------------------------")
    time.sleep(3)
    username = input("\nMasukkan Username anda: ")
    password = input("Masukkan Password Anda: ")
    def check():
        for i in listUser:
            if username != i[0]:
                continue
            elif username == i[0] and password != i[1]:
                print("\nPassword Salah!\n")
                loginUser()
                return 1
            elif username == i[0] and password == i[1]:
                kata = "Login Sukses"
                kata2 = "Loading..."
                for i in range(0,101):
                    print("\r{0}{1}%".format(kata2,i),end="")
                    time.sleep(0.005)
                print(kata)
                menuUser()
                return 1
    cek = check()
    if cek != 1:
        print("Login Gagal")
        for i in range(3):
            print(".")
            time.sleep(1)
        print("Belum punya akun? Register terlebih dahulu!")
        print("1. Coba login lagi")
        print("2. Register")
        pilih = int(input("Pilih disini: "))
        if pilih == 1:
            os.system('cls')
            loginUser()
        elif pilih == 2:
            os.system('cls')
            registerUser()

# ALGORITHM
def selectionSort(data, n):
    for index in range(len(data)):
        minValue = index
        for check in range(index+1, len(data)):
            if data[check][n] < data[minValue][n]:
                minValue = check
        (data[index], data[minValue]) = (data[minValue], data[index])
    return data

def linearSearch(listData, key, n):
    hasilSearch = []
    for i in range(len(listData)): 
        if listData[i][n] == key:
            hasilSearch.append(listData[i])
    return hasilSearch
    
def linearSearchSpes(listData, key):
    hasilSearch = []
    for i in range(len(listData)): 
        if listData[i][0:2] == key:
            hasilSearch.append(listData[i])
    return hasilSearch

def bahanSorting():
    connect()
    listData = []
    data_obj = con.cursor()
    data_obj.execute(f'SELECT id_pemesanan, username_user, tanggal, jam_sewa, nama_gedung, nomor_lapangan from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
    data = data_obj.fetchall()
    for i in data:
        i_list = list(i)
        listData.append(i_list)
    return listData

def bahanSearching():
    connect()
    listData = []
    lowerName = []
    data_obj = con.cursor()
    data_obj.execute(f'SELECT username_user, tanggal, jam_sewa, nama_gedung, nomor_lapangan from pemesanan inner join "user" on id_user = user_id inner join detail_gedung on id_detail = detail_id inner join gedung on id_gedung = gedung_id inner join jam on id_jam = jam_id order by id_pemesanan')
    data = data_obj.fetchall()
    for i in data:
        i_list = list(i)
        listData.append(i_list)
    for y in listData:
        lowerName.append(y[0].lower())
    index = 0    
    for z in lowerName:
        listData[index][0] = z
        index += 1
        
    return listData

def jarakTerdekat(): 
    class Graph:
        def __init__(self, vertices):
            self.V = vertices
            self.graph = [[float('inf') for _ in range(vertices)] for _ in range(vertices)]
            self.gedung_names = ["Lokasi Anda", "Stadion Unej", "Futsalindo", "Zona Futsal", "Elpashindo", "lapangan 8"]


        def min_key(self, key, mst_set):
            min_dist = float('inf')
            min_index = -1
            for v in range(self.V):
                if key[v] < min_dist and mst_set[v] == False:
                    min_dist = key[v]
                    min_index = v
            return min_index

        def print_distances(self, dist):
            print("Gedung\t\t\tJarak dalam KM")
            for i in range(self.V):
                print(self.gedung_names[i], "\t\t", dist[i])

        def dijkstra(self, start_vertex):
            dist = [float('inf')] * self.V
            dist[start_vertex] = 0
            mst_set = [False] * self.V

            for _ in range(self.V):
                u = self.min_key(dist, mst_set)
                mst_set[u] = True
                for v in range(self.V):
                    if (
                        self.graph[u][v] > 0
                        and mst_set[v] == False
                        and dist[v] > dist[u] + self.graph[u][v]
                    ):
                        dist[v] = dist[u] + self.graph[u][v]

            self.print_distances(dist)

    g = Graph(6)
    g.graph =[
        [1, 2, 4, 6, 8, 10, 12],
        [2, 1, 0, 0, 0, 0, 0],
        [4, 0, 1, 0, 0, 0, 0],
        [6, 0, 0, 1, 0, 0, 0],
        [8, 0, 0, 0, 1, 0, 0],
        [10, 0, 0, 0, 0, 1, 0],
        [12, 0, 0, 0, 0, 0, 1]
    ]
    e = Graph(6)
    e.graph =[
        [1, 6, 10, 8, 14, 17, 21],
        [6, 1, 0, 0, 0, 0, 0],
        [10, 0, 1, 0, 0, 0, 0],
        [8, 0, 0, 1, 0, 0, 0],
        [14, 0, 0, 0, 1, 0, 0],
        [17, 0, 0, 0, 0, 1, 0],
        [21, 0, 0, 0, 0, 0, 1]
    ]
    f = Graph(6)
    f.graph =[
        [1, 14, 7, 11, 24, 20, 42],
        [14, 1, 0, 0, 0, 0, 0],
        [7, 0, 1, 0, 0, 0, 0],
        [11, 0, 0, 1, 0, 0, 0],
        [24, 0, 0, 0, 1, 0, 0],
        [20, 0, 0, 0, 0, 1, 0],
        [42, 0, 0, 0, 0, 0, 1]
    ]
    d = Graph(6)
    d.graph =[
        [1, 32, 52, 27, 19, 11, 32],
        [32, 1, 0, 0, 0, 0, 0],
        [52, 0, 1, 0, 0, 0, 0],
        [27, 0, 0, 1, 0, 0, 0],
        [19, 0, 0, 0, 1, 0, 0],
        [11, 0, 0, 0, 0, 1, 0],
        [32, 0, 0, 0, 0, 0, 1]
    ]
    c = Graph(6)
    c.graph =[
        [1, 13, 25, 5, 10, 12, 22],
        [13, 1, 0, 0, 0, 0, 0],
        [25, 0, 1, 0, 0, 0, 0],
        [5, 0, 0, 1, 0, 0, 0],
        [10, 0, 0, 0, 1, 0, 0],
        [12, 0, 0, 0, 0, 1, 0],
        [22, 0, 0, 0, 0, 0, 1]
    ]
    b = Graph(6)
    b.graph =[
        [1, 20, 12, 14, 9, 21, 14],
        [20, 1, 0, 0, 0, 0, 0],
        [12, 0, 1, 0, 0, 0, 0],
        [14, 0, 0, 1, 0, 0, 0],
        [9, 0, 0, 0, 1, 0, 0],
        [21, 0, 0, 0, 0, 1, 0],
        [14, 0, 0, 0, 0, 0, 1]
    ]
    a = Graph(6)
    a.graph =[
        [1, 12, 2, 6, 18, 21, 10],
        [12, 1, 0, 0, 0, 0, 0],
        [2, 0, 1, 0, 0, 0, 0],
        [6, 0, 0, 1, 0, 0, 0],
        [18, 0, 0, 0, 1, 0, 0],
        [21, 0, 0, 0, 0, 1, 0],
        [10, 0, 0, 0, 0, 0, 1]
    ]

    start_vertex = 0


    def pilihTitik():
        print("Anda berada di lokasi mana nichh? ")
        print("1. Alun-Alun")
        print("2. Mastrip")
        print("3. Kalimantan")
        print("4. Kaliwates")
        print("5. Patrang")
        print("6. Jawa")
        print("7. UNEJ")
        while True:
            baru = int(input("Pilih Disini: "))
            if baru == 1:
                print("Lokasi anda ke gedung memiliki jarak")
                g.gedung_names
                g.dijkstra(start_vertex)
                break
            elif baru == 2:
                print("Lokasi anda ke gedung memiliki jarak")
                f.gedung_names
                f.dijkstra(start_vertex)
                break
            elif baru == 3:
                print("Lokasi anda ke gedung memiliki jarak")
                e.gedung_names
                e.dijkstra(start_vertex)
                break
            elif baru == 4:
                print("Lokasi anda ke gedung memiliki jarak")
                d.gedung_names
                d.dijkstra(start_vertex)
                break
            elif baru == 5:
                print("Lokasi anda ke gedung memiliki jarak")
                c.gedung_names
                c.dijkstra(start_vertex)
                break
            elif baru == 6:
                print("Lokasi anda ke gedung memiliki jarak")
                b.gedung_names
                b.dijkstra(start_vertex)
                break
            elif baru == 7:
                print("Lokasi anda ke gedung memiliki jarak")
                a.gedung_names
                a.dijkstra(start_vertex)
                break
    pilihTitik()
    
    lagi = input("Apakah anda ingin mencari jarak terdekat lagi? [y/n] : ") 
    if lagi == "y":
        jarakTerdekat()
    else :
        menuUser()
# HOMEPAGE
def authorPage():
    print("--------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI D-PANAN                       |")
    print("|                   Data Pemesanan Lapangan                        |")
    print("--------------------------------------------------------------------")
    print("\nSilahkan pilih menu otorisasi!")
    print("1. Admin")
    print("2. User")
    pilih = int(input("Pilih disini: "))
    if pilih == 1:
        os.system("cls")    
        loginAdmin()
    elif pilih == 2:
        print("\n1. Login")
        print("2. Register")
        pilih2 = int(input("Pilih disini: "))
        if pilih2 == 1:
            os.system("cls")
            loginUser()
        elif pilih2 == 2:
            os.system("cls")
            registerUser()

# MENU UTAMA ADMIN
def menuAdmin():
    os.system("cls")
    print("------------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI MENU ADMIN D-PANAN                       |")
    print("|                         Data Pemesanan Lapangan                             |")
    print("-------------------------------------------------------------------------------")
    print("\n1. Create Jadwal")
    print("2. Read Jadwal")
    print("3. Update Jadwal")
    print("4. Delete Jadwal")
    print("5. Exit")
    pilih = int(input("Silahkan pilih menu: "))
    if pilih == 1:
        os.system("cls")
        createJadwalAdmin()
    elif pilih == 2:
        os.system("cls")
        subReadAdmin()
    elif pilih == 3:
        os.system("cls")
        updateJadwal()
    elif pilih == 4:
        os.system("cls")
        deleteJadwal()
    elif pilih == 5:
        exit()

# MENU UTAMA USER
def menuUser():
    os.system("cls")
    print("-------------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI MENU USER D-PANAN                        |")
    print("|                         Data Pemesanan Lapangan                             |")
    print("-------------------------------------------------------------------------------")
    print("\n1. Create Jadwal")
    print("2. Read Jadwal")
    print("3. Cek Lapangan Terdekat")
    print("4. Exit")
    pilih = int(input("Silahkan pilih menu: "))
    if pilih == 1:
        os.system("cls")
        createJadwalUser()
    elif pilih == 2:
        os.system("cls")
        subReadUser()
    elif pilih == 3:
        os.system("cls")
        jarakTerdekat()
    elif pilih == 4:
        exit()

authorPage()