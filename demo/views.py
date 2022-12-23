from django.shortcuts import render
import mysql.connector
from mysql.connector import Error

def base(request):
    connection = connect()

    cursor = connection.cursor(dictionary = True)
    cursor.execute('select * from employee')
    employee = cursor.fetchall()
    # print(type(employee))

    cursor.execute('select * from absen')
    absensi = cursor.fetchall()

    cursor.execute('select distinct employee.nik, employee.name, absen.tglAbsen from employee join absen on employee.nik = absen.nikEmployee group by absen.tglAbsen order by employee.nik')
    merge = cursor.fetchall()

    cursor.execute('SELECT DISTINCT tglAbsen FROM absen order by tglAbsen')
    absen = cursor.fetchall()

    context = {
        'employee' : employee,
        'absensi' : absensi,
        'merge' : merge,
        'absen' : absen,
    }
    

    if request.method == "POST":
        tglAbsen = ''
        niknama = request.POST.get('niknama')
        tglAbsen = request.POST.get('tglAbsen')
        
        if tglAbsen != '' :
            cursor.execute(f'insert into absen values ("{niknama}", "{tglAbsen}")')
            connection.commit() # buat save perubahan pada database
    

    return render(request, 'base.html', context)

def connect():
  try:
      connection = mysql.connector.connect(
          host= "127.0.0.1",
          port= '3306',
          user= "root",
          password= "PkmOba_2022",
          database= "kawanlama",
          auth_plugin='mysql_native_password')
      if connection.is_connected():
        return connection

  except Error as e:
      print("Error while connecting to MySQL", e)