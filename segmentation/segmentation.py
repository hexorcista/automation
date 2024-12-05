import sys
import subprocess
import ipaddress
import os

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"{Colors.RED}Error running command: {command}\n{result.stderr.strip()}{Colors.RESET}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"{Colors.RED}Exception running command: {command}\n{e}{Colors.RESET}")
        return None

def get_ip_with_command(command):
    output = run_command(command)
    if not output:
        return None, None

    lines = output.splitlines()
    for line in lines:
        if command == "ip a" and "inet " in line and not "127.0.0.1" in line:
            parts = line.split()
            ip_with_netmask = parts[1]
            ip, prefix = ip_with_netmask.split("/")
            return ip, int(prefix)
        elif command == "ifconfig" and "inet " in line and not "127.0.0.1" in line:
            parts = line.split()
            ip = parts[1]
            mask = parts[3] if len(parts) > 3 else None
            if mask and mask.startswith("0x"):  # Convert hexadecimal mask to CIDR prefix
                mask = ".".join(str(int(mask[i:i+2], 16)) for i in range(2, len(mask), 2))
            if mask:
                cidr_prefix = sum(bin(int(octet)).count("1") for octet in mask.split("."))
                return ip, cidr_prefix
    return None, None

def ping_sweep(segment, mask):
    print(f"\n{Colors.BLUE}[+] Performing ping sweep on {segment}/{mask}{Colors.RESET}")
    command = f"nmap -sn {segment}/{mask} -oN ping_sweep_{segment.replace('/', '_')}_{mask}.out"
    response = run_command(command)
    if response:
        print(f"{Colors.GREEN}[+] Ping sweep completed. Results saved in ping_sweep_{segment.replace('/', '_')}_{mask}.out{Colors.RESET}")

def service_scan_single_port(network, mask, port, service_name):
    output_file = f"service-{service_name}-{network.replace('/', '_')}-{mask}.out"
    print(f"{Colors.BLUE}[+] Scanning for {service_name} (port {port}) on {network}/{mask}{Colors.RESET}")
    command = f"nmap -Pn -p {port} {network}/{mask} -oN {output_file}"
    response = run_command(command)

    if response and os.path.exists(output_file):
        with open(output_file, 'r') as file:
            lines = file.readlines()
        open_ports = [line for line in lines if "open" in line.lower()]
        if open_ports:
            print(f"\n{Colors.GREEN}[+] Open {service_name} ports found. Check the output file for more details.{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] No open {service_name} ports found.{Colors.RESET}")
    else:
        print(f"{Colors.RED}[-] Failed to scan for {service_name}. Check nmap output manually.{Colors.RESET}")

def scan_network(base_ip, mask, services):
    network = ipaddress.IPv4Network(f"{base_ip}/{mask}", strict=False)
    network_range = f"{network.network_address}/{mask}"
    ping_sweep(str(network.network_address), mask)
    for service_name, port in services.items():
        service_scan_single_port(str(network.network_address), mask, port, service_name)

def nxcCmd(base_ip, mask, protocol):
    print(f"{Colors.BLUE}[+] Executing: nxc {protocol} {base_ip}/{mask} {Colors.RESET}")
    output_file = f"nxc-{protocol}-{base_ip}-{mask}.out"
    command = f"nxc {protocol} {base_ip}/{mask} | tee {output_file}"
    response = run_command(command)
    if response:
        print(f"{Colors.GREEN}[+] Results saved in {output_file}{Colors.RESET}")

def main():
    print(f"{Colors.BLUE}[+] Choose the command to fetch the IP address:{Colors.RESET}")
    print("    1. ip a")
    print("    2. ifconfig")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        command = "ip a"
    elif choice == "2":
        command = "ifconfig"
    else:
        print(f"{Colors.RED}Invalid choice. Exiting.{Colors.RESET}")
        sys.exit(1)

    print(f"\n{Colors.BLUE}[+] Using '{command}' to extract IP information...{Colors.RESET}")
    ip, netmask = get_ip_with_command(command)
    if not ip:
        print(f"{Colors.RED}[-] Failed to extract IP address. Please check your network configuration.{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.GREEN}[+] Current IP: {ip}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Netmask: {netmask}{Colors.RESET}")

    # Calculate the network segment
    try:
        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        network_segment = str(network.network_address)
    except Exception as e:
        print(f"{Colors.RED}[-] Failed to calculate network segment: {e}{Colors.RESET}")
        sys.exit(1)

    services = {
        "http": 80,
        "https": 443,
        "ssh": 22,
        "ftp": 21,
        "smb": 445,
        "rdp": 3389,
        "mysql": 3306,
        "postgresql": 5432,
        "mssql": 1433,
        "ldap": 389,
        "ldaps": 636,
        "pop3": 110,
        "pop3s": 995,
        "imap": 143,
        "imaps": 993,
        "smtp": 25,
        "smtps": 465,
        "dns": 53,
        "ntp": 123,
        "snmp": 161,
        "telnet": 23,
        "winrm": 5985,
        "winrm-https": 5986,
        "wmi": 135,
        "vnc": 5900,
        "elastic": 9200,
        "mongodb": 27017,
        "redis": 6379,
        "oracle": 1521,
        "kafka": 9092,
        "docker": 2375,
        "jenkins": 8080,
    }

    services_nxc = ["smb", "ssh", "ldap", "ftp", "wmi", "winrm", "rdp", "vnc", "mssql", "nfs"]

    print(f"\n{Colors.BLUE}[+] Starting scans for /24 subnet...{Colors.RESET}")
    scan_network(network_segment, 24, services)

    choicenxc = input(f"\n{Colors.YELLOW}[?] Do you want to use nxc to test? (yes/no): {Colors.RESET}").strip().lower()
    if choicenxc == "yes":
        choicenxc2 = input(f"\n{Colors.YELLOW}[?] Do you want to test /24(24), /16(16), or both(both)? {Colors.RESET}").strip().lower()
        if choicenxc2 == "24":
            mask = 24
            for protocol in services_nxc:
                nxcCmd(network_segment, mask, protocol)
        elif choicenxc2 == "16":
            mask = 16
            for protocol in services_nxc:
                nxcCmd(network_segment, mask, protocol)
        elif choicenxc2 == "both":
            for mask in [24, 16]:
                for protocol in services_nxc:
                    nxcCmd(network_segment, mask, protocol)
        else:
            print(f"{Colors.RED}Invalid choice. Exiting.{Colors.RESET}")
            sys.exit(1)

    choice = input(f"\n{Colors.YELLOW}[?] Do you want to expand to /16 for deeper scans? (yes/no): {Colors.RESET}").strip().lower()
    if choice == "yes":
        print(f"\n{Colors.BLUE}[+] Starting scans for /16 subnet...{Colors.RESET}")
        scan_network(network_segment, 16, services)
    else:
        print(f"{Colors.YELLOW}[-] Skipping /16 scan.{Colors.RESET}")

if __name__ == "__main__":
    main()
