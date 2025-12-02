import pyshark
import argparse
import time
import socket
import ipaddress
from collections import defaultdict

def resolve_hostname(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            return "Private Network"
        if ip_obj.is_loopback:
            return "Localhost"
        if ip_obj.is_multicast:
            return "Multicast"
        if ip_obj.is_reserved:
            return "Reserved"
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except:
        return "No-DNS"

def monitor_basic(interface):
    capture = pyshark.LiveCapture(interface=interface)
    traffic_stats = {}
    start_time = time.time()

    print(f"Monitoring traffic on interface: {interface}")
    print("Press CTRL+C to stop.\n")

    for packet in capture.sniff_continuously():
        current_time = time.time()
        if current_time - start_time >= 1:
            print("\n--- Traffic Breakdown (last 1s) ---")
            if not traffic_stats:
                print("No traffic detected.")
            else:
                for key, total_bytes in traffic_stats.items():
                    src, dst, proto = key
                    kbps = (total_bytes * 8) / 1024
                    src_label = resolve_hostname(src)
                    dst_label = resolve_hostname(dst)
                    print(f"{src} ({src_label}) → {dst} ({dst_label}) ({proto}): {kbps:.2f} Kbps")
            traffic_stats = {}
            start_time = current_time

        try:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
        except:
            continue

        try:
            protocol = packet.transport_layer
        except:
            protocol = "None"

        pkt_len = int(packet.length)
        key = (src_ip, dst_ip, protocol)
        traffic_stats[key] = traffic_stats.get(key, 0) + pkt_len

def monitor_detailed(interface, window):
    print(f"Starting detailed bandwidth monitor on {interface}")
    print("Press Ctrl-C to stop.\n")
    capture = pyshark.LiveCapture(interface=interface)
    packets = []
    start_time = time.time()

    for packet in capture.sniff_continuously():
        now = time.time()
        try:
            length = int(packet.length)
        except:
            continue

        src = packet.ip.src if "IP" in packet else "Unknown"
        dst = packet.ip.dst if "IP" in packet else "Unknown"
        proto = packet.transport_layer if hasattr(packet, "transport_layer") else "N/A"

        packets.append((now, src, dst, proto, length))
        packets = [p for p in packets if p[0] >= now - window]

        traffic = defaultdict(int)
        for (_, src, dst, proto, length) in packets:
            key = f"{src} → {dst} ({proto})"
            traffic[key] += length

        if now - start_time >= 1.0:
            print("\n--- Traffic Breakdown (last 1s) ---")
            for key, total_bytes in traffic.items():
                rate_kbps = (total_bytes * 8) / 1000
                print(f"{key}: {rate_kbps:.2f} Kbps")
            start_time = now

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("--detailed", action="store_true", help="Enable sliding-window detailed mode")
    parser.add_argument("-w", "--window", type=float, default=1.0, help="Time window (seconds)")
    args = parser.parse_args()

    if args.detailed:
        monitor_detailed(args.interface, args.window)
    else:
        monitor_basic(args.interface)

if __name__ == "__main__":
    main()
