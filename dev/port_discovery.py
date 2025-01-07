import serial.tools.list_ports
import time

def list_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        port_list.append({
            "device": port.device,
            "description": port.description,
            "hwid": port.hwid
        })
    return port_list

def display_ports(port_list):
    print("Currently connected ports:")
    for port in port_list:
        print(f"Device: {port['device']}, Description: {port['description']}, HWID: {port['hwid']}")

def find_new_ports(old_ports, new_ports):
    old_devices = {port['device'] for port in old_ports}
    new_devices = {port['device'] for port in new_ports}
    added_ports = new_devices - old_devices

    return [port for port in new_ports if port['device'] in added_ports]

def main():
    print("Starting port discovery utility...")
    current_ports = list_ports()
    display_ports(current_ports)

    while True:
        try:
            print("\nRefreshing port list...")
            new_ports = list_ports()
            added_ports = find_new_ports(current_ports, new_ports)

            if added_ports:
                print("\nNewly connected ports:")
                display_ports(added_ports)
            else:
                print("\nNo new devices detected.")

            current_ports = new_ports
            time.sleep(5)  # Refresh every 5 seconds
        except KeyboardInterrupt:
            print("\nExiting port discovery utility.")
            break

if __name__ == "__main__":
    main()
