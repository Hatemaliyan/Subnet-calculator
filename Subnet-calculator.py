import re

class SubnetCalculator:
    def __init__(self, ip_address, cidr):
        self.ip_address = ip_address
        self.cidr = cidr
        self.mask_cidr = '/' + str(cidr)
        self.total_hosts = 2 ** (32 - cidr) - 2
        self.total_subnets = 2 ** cidr
        self.network_address = self.calculate_network_address()
        self.broadcast_address = self.calculate_broadcast_address()

    def calculate_network_address(self):
        ip_octets = [int(octet) for octet in self.ip_address.split('.')]
        subnet_mask = self.calculate_subnet_mask()
        network_octets = [ip_octets[i] & subnet_mask[i] for i in range(4)]
        return '.'.join([str(octet) for octet in network_octets])

    def calculate_broadcast_address(self):
        ip_octets = [int(octet) for octet in self.ip_address.split('.')]
        subnet_mask = self.calculate_subnet_mask()
        broadcast_octets = [ip_octets[i] | (255 - subnet_mask[i]) for i in range(4)]
        return '.'.join([str(octet) for octet in broadcast_octets])

    def calculate_subnet_mask(self):
        subnet_mask = [0, 0, 0, 0]
        for i in range(self.cidr):
            subnet_mask[i // 8] += 1 << (7 - i % 8)
        return subnet_mask

def get_ip_address() -> str:
    """
    Prompts the user to enter an IP address and returns it as a string.

    Returns:
        A string representing the user's input.
    """
    while True:
        ip_str = input("Enter IP address: ")
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_str):
            return ip_str
        print("Invalid IP address. Please try again.")


def get_subnet_mask() -> int:
    """
    Prompts the user to enter a subnet mask in CIDR notation and returns it as an integer.

    Returns:
        An integer representing the subnet mask in CIDR notation.
    """
    while True:
        subnet_mask_str = input("Enter subnet mask in CIDR notation (optional): ")
        if subnet_mask_str == '':
            return None
        elif re.match(r'^\d{1,2}$', subnet_mask_str):
            return int(subnet_mask_str)
        print("Invalid subnet mask. Please try again.")


def get_partitioning_type() -> str:
    """
    Prompts the user to choose whether to partition by number of hosts or number of subnets.

    Returns:
        A string representing the user's choice.
    """
    while True:
        partitioning_type = input("Will the partitioning be according to number of hosts or number of subnets? ")
        if partitioning_type.lower() == 'hosts' or partitioning_type.lower() == 'subnets':
            return partitioning_type.lower()
        print("Invalid partitioning type. Please try again.")


def get_num() -> int:
    """
    Prompts the user to enter a number of hosts or subnets.

    Returns:
        An integer representing the user's input.
    """
    while True:
        num_str = input("Enter number of hosts/subnets: ")
        if re.match(r'^\d+$', num_str):
            return int(num_str)
        print("Invalid number. Please try again.")


def calculate_subnet():
    """
    Calculates and prints information about a subnet based on user input.
    """
    ip_address = get_ip_address()
    subnet_mask = get_subnet_mask()
    if subnet_mask is None:
        subnet_mask = 24
    partitioning_type = get_partitioning_type()
    num = get_num()

    subnet_calc = SubnetCalculator(ip_address, subnet_mask)

    subnet_mask_decimal = '.'.join([str(subnet_calc.calculate_subnet_mask()[i]) for i in range(4)])
    cidr = str(subnet_calc.cidr)
    num_hosts = subnet_calc.total_hosts
    num_subnets = 2 ** (32 - subnet_calc.cidr)

    ip_octets = [int(octet) for octet in subnet_calc.ip_address.split('.')]
    network_address = subnet_calc.network_address
    broadcast_address = subnet_calc.broadcast_address

    print("1. Subnet mask (in mask decimal format):", subnet_mask_decimal)
    print("2. Subnet in CIDR:", cidr)
    print("3. Number of hosts:", num_hosts)
    print("4. Number of subnets:", num_subnets)
    print("5. Network address:", network_address)
    print("   Broadcast address:", broadcast_address)

if __name__ == '__main__':
    calculate_subnet()