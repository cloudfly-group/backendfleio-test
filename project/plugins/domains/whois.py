import requests
import socket

from typing import List


class Whois:
    @staticmethod
    def whois_tcp_query(query: str, server: str, strip_comments: bool = False) -> List[str]:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        client_socket.connect((server, 43))
        client_socket.send(bytes(query, 'utf-8') + b'\r\n')
        response = b''
        while True:
            received_data = client_socket.recv(4096)
            response += received_data
            if not received_data:
                break
        client_socket.close()
        response_str = response.decode('utf-8', 'replace')
        response_lines = [line for line in response_str.splitlines() if line]
        if strip_comments:
            return [response_line for response_line in response_lines if not response_line.startswith('%')]
        else:
            return response_lines

    @staticmethod
    def whois_http_query(query: str, server: str, strip_comments: bool = False) -> List[str]:
        url = server + query
        response = requests.request(
            method='GET',
            url=url,
            verify=False,
        )
        if response.status_code == 200:
            response_lines = response.content.splitlines()
            if strip_comments:
                return [response_line for response_line in response_lines if not response_line.startswith('%')]
            else:
                return response_lines
        else:
            return []

    def get_whois_server(self, tld_name: str) -> str:
        tld_name = tld_name.lower()
        response_lines = self.whois_tcp_query(tld_name, 'whois.iana.org')
        whois_server = None
        for line in response_lines:
            if line.startswith('whois:'):
                whois_server = line.replace('whois:', '').strip()

        return whois_server

    def domain_query(self, domain_name: str) -> List[str]:
        domain_parts = domain_name.split('.')
        whois_server = self.get_whois_server(domain_parts[1])
        return Whois.whois_tcp_query(
            query=domain_name, server=whois_server
        )

    @staticmethod
    def domain_available(domain_name: str, whois_server: str, available_search_str: str) -> bool:
        whois_server_parts = whois_server.split('://')
        protocol = whois_server_parts[0].lower()

        response_lines = []
        if protocol == 'socket':
            response_lines = Whois.whois_tcp_query(
                query=domain_name, server=whois_server_parts[1]
            )

        if protocol in ['http', 'https']:
            response_lines = Whois.whois_http_query(
                query=domain_name, server=whois_server
            )

        if not available_search_str:
            return len(response_lines) == 0
        else:
            for response_line in response_lines:
                if available_search_str in response_line:
                    return True

        return False
