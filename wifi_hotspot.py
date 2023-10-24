import os

# Nombre y contraseÃ±a de tu punto de acceso
ssid = "VideoGate"
password = "Conectores!!"

# Configura la interfaz inalÃ¡mbrica secundaria (asegÃºrate de que sea diferente de la interfaz principal)
interface = "wlan0"

# DetÃ©n el servicio de hostapd si se estaba ejecutando
os.system("sudo systemctl stop hostapd")

# Configura la interfaz inalÃ¡mbrica
os.system(f"sudo ifconfig {interface} 192.168.4.1 netmask 255.255.255.0")

# Inicia el servicio DHCP
os.system("sudo systemctl start isc-dhcp-server")

# Configura las reglas de IP masquerade
os.system("sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE")
os.system("sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'")

# Configura hostapd
hostapd_conf = f"""
interface={interface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""

with open("/etc/hostapd/hostapd.conf", "w") as file:
    file.write(hostapd_conf)

# Reinicia el servicio de hostapd
os.system("sudo systemctl start hostapd")

