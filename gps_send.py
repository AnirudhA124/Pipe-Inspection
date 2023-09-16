import time
import board
import busio
import pyrebase
import adafruit_gps
import serial
def gps_sent():
    firebaseConfig = {
      "apiKey": "AIzaSyC3HFnPh3-I0sQvrTPkHY0MlGrVi4TlxM4",
      "authDomain": "gps-tracker01.firebaseapp.com",
      "databaseURL": "https://gps-tracker01-default-rtdb.firebaseio.com",
      "projectId": "gps-tracker01",
      "storageBucket": "gps-tracker01.appspot.com",
      "messagingSenderId": "877588705727",
      "appId": "1:877588705727:web:e77ed1dd266b75c2c8710a",
      "measurementId": "G-JEWN6VW1QT"
    }

    firebase=pyrebase.initialize_app(firebaseConfig)
    db=firebase.database()

    uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3000)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    last_print = time.monotonic()
    f=0
    while True:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                print("Waiting for fix...")
                continue
            print("=" * 40)
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            lat=str(gps.latitude)
            lng=str(gps.longitude)
            Gps = "Latitude=" + lat + " and Longitude=" + lng
            print(Gps)
            data = {"LAT": lat, "LNG": lng}
            db.update(data)
            print("Data sent")
gps_sent()