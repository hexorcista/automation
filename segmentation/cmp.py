import sys

def cmp(infile, ipfile):    
    try:
        with open(ipfile, 'r') as file2:
            ip2check = set(line.strip() for line in file2 if line.strip())
            with open(infile, 'r') as file1:
                print("\nMatching lines...")
                for ln, line in enumerate(file1, start=1):
                    for ip in ip2check:
                        if ip in line:
                            print(f"Line {ln}: {line.strip()}")
                            break
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == '__main__':
    try:
        infile = sys.argv[1]
        ipfile = sys.argv[2]
        cmp(infile, ipfile)
    except IndexError:
        print(f"Usage: {sys.argv[0]} <toolOutFile> <ipsFile2Match>")
        sys.exit(1)
