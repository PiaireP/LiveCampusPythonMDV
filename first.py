from scapy.all import *

#Liste de ports a scanner
ports = [80,25,53]
ip_cible = '8.8.8.8'
domaine='google.com'

def scanSyn(ip, ports):
    port_ouvert = []
    #Une boucle qui effectuera l'action pour chaque port de la liste
    for port in ports:
        #La requette 
        req = IP(dst=ip) / TCP(dport=port, flags='S')
        rep = sr1(req, timeout=1, verbose=0)

        #Condition qui verrifie que dans la réponse, le port scanner est ouvert
        if rep and rep.haslayer(TCP) and rep[TCP].flags == 'SA':
            #Si oui on l'ajoute à une liste de références des ports ouvert
            port_ouvert.append(port)

    #Enfin on print le résultat
    print(f'Port ouverts : sur {ip}: {port_ouvert}')


def scanDNS(ip, domaine):
    #La requette 
    req = IP(dst=ip) / UDP(dport=53) / DNS(qd=DNSQR(qname=domaine))
    rep = sr1(req, timeout=1, verbose=0)

    #Condition pour vérrifier si l'ip cible est un serveur DNS ou non
    if rep and rep.haslayer(DNS) and rep[DNS].ancount > 0:
        print(f'{ip} est un serveur DNS')
    else :
        print(f"{ip} n'est un serveur DNS")

scanSyn(ip_cible, ports)
scanDNS(ip_cible, domaine)