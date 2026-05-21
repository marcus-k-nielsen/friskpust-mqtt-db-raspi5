import network
import time

SSID = "Asus2"
PASSWORD = "NowakogNielsen2528"


wlan = network.WLAN(network.STA_IF)

wlan.active(True)

print("Scanning networks...")
print(wlan.scan())

print("Connecting...")

wlan.connect(SSID, PASSWORD)


# Wait up to 10 seconds
for i in range(10):

    print(
        "Connected:",
        wlan.isconnected()
    )

    if wlan.isconnected():

        print("SUCCESS")
        print(wlan.ifconfig())

        break

    time.sleep(1)


if wlan.isconnected() == False:

    print("FAILED")
    print(wlan.status())