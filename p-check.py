import socket
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore

# Initialize colorama
colorama.init()

def print_banner():
    banner = """
    ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    ██████╔╝    ██║     ███████║█████╗  ██║     █████╔╝ 
    ██╔═══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
    ██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚═╝          ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
    """
    print(Fore.MAGENTA + banner + Fore.RESET)
    print(Fore.CYAN + "Developed by: Alfaz Infosec @alfazinfosec" + Fore.RESET)

def validate_proxy(proxy):
    proxy = proxy.strip()
    if ':' not in proxy:
        return (proxy, False)

    try:
        host, port = proxy.split(':')
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((host, port))
        return (proxy, True)
    except Exception:
        return (proxy, False)

def main():
    # Print the banner and developer information
    print_banner()

    # Get the path for the proxy list
    proxy_list_path = input(Fore.CYAN + "Enter the path to the proxy list: " + Fore.RESET)

    # Get the output file name
    output_file_name = input(Fore.CYAN + "Enter the name of the output file: " + Fore.RESET)

    try:
        # Open the proxy list and read the lines
        with open(proxy_list_path, 'r') as proxy_list:
            proxies = [line.strip() for line in proxy_list if line.strip()]

        print(Fore.YELLOW + f"Total proxies loaded: {len(proxies)}" + Fore.RESET)

        # Validate proxies using parallel processing
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(validate_proxy, proxies)

        # Write valid proxies to the output file
        with open(output_file_name, 'w') as output_file:
            working_count = 0
            for proxy, is_working in results:
                if is_working:
                    output_file.write(f"{proxy}\n")
                    print(Fore.GREEN + f"{proxy} - Working" + Fore.RESET)
                    working_count += 1

        print(Fore.GREEN + f"The working proxies have been saved to {output_file_name}." + Fore.RESET)
        print(Fore.YELLOW + f"Total working proxies: {working_count}" + Fore.RESET)

    except FileNotFoundError:
        print(Fore.RED + "Error: The proxy list file was not found." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Fore.RESET)

if __name__ == "__main__":
    main()

