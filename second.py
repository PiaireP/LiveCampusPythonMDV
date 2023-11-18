import dns.resolver 
import socket

def ReverseDNS(ip):
    try : 
        #Requette
        hote = dns.reversename.from_address(ip)
        result = dns.resolver.resolve(hote, 'PTR')

        #Parcours le résultat
        for rep in result:
            print(f'Enregistrement PTR: {rep.target}')

    #Gestion d'erreur
    except socket.herror as e:
        print(f'Erreur : {e}')
    
    except dns.resolver.NXDOMAIN:
        print(f'Pas d enregistrement PTR')


def ReverseDNSSocket(ip):
    try:
        #Requette
        hote, _, _ = socket.gethostbyaddr(ip)
        print(f"nom hôte: {hote} pour {ip}")

    #Gestion d'erreur
    except socket.herror as e:
        print(f"Erreur : {e}")


def DNSRequest(domain):
    try:
        #Requette
        ipv4 = dns.resolver.resolve(domain, "A")

        #Réponse
        print(f"Enregistrements A pour le domaine {domain}:")
        for answer_ipv4 in ipv4:
            print(f"IPv4: {answer_ipv4}")

        #Requete mais ici pour IPV6
        result_ipv6 = dns.resolver.resolve(domain, "AAAA")

        #Réponse
        print(f"\nEnregistrements AAAA pour le domaine {domain}:")
        for answer_ipv6 in result_ipv6:
            print(f"IPv6: {answer_ipv6}")

    #Gestion d'erreur
    except dns.resolver.NXDOMAIN:
        print(f"Aucun enregistrement trouvé pour le domaine {domain}")


def DNSRequestSocket(domain):
    print('SOCKET')
    try:
        #Requette
        results = socket.getaddrinfo(domain, None)

        #Affichage Réponse
        print(f"Enregistrements pour le domaine {domain}:")
        for result in results:
            family, _, _, _, sockaddr = result
            #ipv4
            if family == socket.AF_INET: 
                print(f"ipv4: {sockaddr[0]}")
            #ipv6
            elif family == socket.AF_INET6: 
                print(f"ipv6: {sockaddr[0]}")

    #Gestion d'erreur
    except socket.gaierror as e:
        print(f"Erreur l: {e}")


def SubdomainSearch(domain, dictionary, nums):
    #Liste des sous domaines trouver
    subdomains = []

    #Parcours du dictionnaire de sous domaine
    for sub in dictionary:
        #Test valeur de base
        subdomain = f"{sub}.{domain}"
        try:
            result_ipv4 = dns.resolver.resolve(subdomain, "A")
            subdomains.append(subdomain)

        except dns.resolver.NXDOMAIN:
            pass

        except dns.resolver.NoAnswer:
                # Gestion d'une erreur si le sous-domaine n'a pas d'enregistrement de type A (IPv4)
                pass
        
        #Test avec un champs de nombres :
        for num in nums:
            subdomainN = f"{sub}{num}.{domain}"
            try:
                result_ipv4 = dns.resolver.resolve(subdomainN, "A")
                subdomains.append(subdomainN)

            except dns.resolver.NXDOMAIN:
                pass

            except dns.resolver.NoAnswer:
                pass

    return subdomains

def SubdomainSearchSocket(domain, dictionary, nums):
    subdomains = []

    try:
        socket.gethostbyname(domain)

        for sub in dictionary:
            subdomain = f"{sub}.{domain}"

            try:
                ip_address = socket.gethostbyname(subdomain)

                subdomains.append(subdomain)

            except socket.gaierror:
                pass
            
            for num in nums:
                subdomain = f"{sub}{num}.{domain}"

                try:
                    ip_address = socket.gethostbyname(subdomain)

                    subdomains.append(subdomain)

                except socket.gaierror:
                    pass

    except socket.gaierror:
        print(f"Le domaine de base {domain} n'existe pas.")

    return subdomains

addr = '8.8.8.8'
domaine = 'dns.google.'
subdomains_test = ["www", "blog", "test"]
domaine_test='netflix.com'
numbers_test = range(1, 10)
print('Reverse DNS avec dns.resolve :')
ReverseDNS(addr)
print('Reverse DNS avec socket :')
ReverseDNSSocket(addr)
print('Requete DNS avec dns.resolve :')
DNSRequest(domaine)
print('Requete DNS avec socket :')
DNSRequestSocket(domaine)
print('Recherche sous domaine avec dns.resolve :')
result = SubdomainSearch(domaine_test, subdomains_test, numbers_test)
for sub in result:
    print(sub)
print('Recherche sous domaine avec socket :')
resultSocket = SubdomainSearchSocket(domaine_test, subdomains_test, numbers_test)
for sub in resultSocket:
    print(sub)