$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Wi-Fi).IPAddress
$display = "${ip}:0.0"
docker run -e DISPLAY=$display misty_ui