# Use Jetson Nano as Access Point

## Getting started

Jetson hack demonstrate method on how to set Jetson Nano as an access point. Please
refer to this great [Article](https://jetsonhacks.com/2021/10/05/wi-fi-hotspot-setup-nvidia-jetson-developer-kits/) from him
along side to get started

## Follow below step
1. Go to `wifi` -->  `edit connections`
2. Click `+` --> `choose wifi`
3. Set details as follow
```
Connection Name : "Hotspot"
SSID : "techmon"
Mode : "Hotspot"
Band : "Automatic"
Channel : "default"
Device select "wlan04 **"

IPV4 & IPV6 tab set to : "Shared to other Computers"
General : "Automatically Connect to this network"
Wifi Security : (WPA & WPA2 Personal) --> Set your password here

Save
```

4. Go to `wifi` --> `create new wifi network `
5. Connection `hotspot`
6. Connection Established !
