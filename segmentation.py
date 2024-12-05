import sys
import subprocess
import ipaddress

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running command: {command}\n{e}")
        return None

def get_ip_with_command(command):
    """Extracts the IP address and netmask using the specified command."""
    output = run_command(command)
    lines = output.splitlines()

    for line in lines:
        if command == "ip a" and "inet " in line and not "127.0.0.1" in line:  # Ignore localhost
            parts = line.split()
            ip_with_netmask = parts[1]  # Format: 192.168.1.100/24
            ip, prefix = ip_with_netmask.split("/")
            return ip, str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)
        elif command == "ifconfig" and "inet " in line and not "127.0.0.1" in line:  # Ignore localhost
            parts = line.split()
            ip = parts[1]  # Extract the IP (e.g., inet 192.168.1.100)
            mask = parts[3] if len(parts) > 3 else None  # Extract the netmask if present
            return ip, mask
    return None, None

def ping_sweep(segment, mask):
    """Perform a ping sweep."""
    print(f"\n[+] Performing ping sweep on {segment}/{mask}")
    command = f"nmap -sn {segment}/{mask}"
    response = run_command(command)
    print(response)

def expand_mask_and_scan(base_ip):
    """Gradually expand the subnet mask and scan."""
    print("\n[+] Expanding subnet mask and scanning")
    base_network = ipaddress.IPv4Network(f"{base_ip}/24", strict=False)
    for mask in [24, 16]:
        network = ipaddress.IPv4Network(f"{base_network.network_address}/{mask}", strict=False)
        print(f"    Scanning: {network}")
        ping_sweep(str(network.network_address), mask)

def service_scan(ip, services):
    """Scan specific services on the target IP."""
    print(f"\n[+] Scanning services on {ip}")
    for service, port in services.items():
        print(f"[+] Scanning {service} on port {port}...")
        command = f"nmap -Pn -p {port} {ip}"
        response = run_command(command)
        print(response)

def main():
    print("[+] Choose the command to fetch the IP address:")
    print("    1. ip a")
    print("    2. ifconfig")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        command = "ip a"
    elif choice == "2":
        command = "ifconfig"
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    print(f"\n[+] Using '{command}' to extract IP information...")
    ip, netmask = get_ip_with_command(command)
    if not ip:
        print("[-] Failed to extract IP address. Please check your network configuration.")
        sys.exit(1)

    print(f"[+] Current IP: {ip}")
    print(f"[+] Netmask: {netmask}")

    # Extract the base network segment
    network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
    base_segment = str(network.network_address)

    # Perform ping sweep on the current segment
    ping_sweep(base_segment, 24)

    # Expand mask and scan
    expand_mask_and_scan(ip)

    # Perform specific service scans
    services = {
        "ldap": 389,
        "mssql": 1433,
        "smb": 445,
        "wmi": 135,
        "ssh": 22,
        "vnc": 5900,
        "ftp": 21,
        "winrm": 5985,
        "rdp": 3389,
    }
    service_scan(ip, services)

if __name__ == "__main__":
    main()

