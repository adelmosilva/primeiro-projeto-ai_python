"""
SOLUÇÃO DEFINITIVA: Monkey-patch socket.getaddrinfo para FORÇAR APENAS IPv4
Isso intercepta TODA tentativa de resolução DNS na aplicação
"""

import socket
import os

# Cache de resoluções para evitar múltiplas lookups
_dns_cache = {}
_original_getaddrinfo = None  # Será definida ao importar

def _force_ipv4_getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
    """
    Monkey-patch de socket.getaddrinfo que FORÇA APENAS IPv4
    Retorna APENAS endereços AF_INET (IPv4), nunca IPv6
    """
    global _original_getaddrinfo
    
    cache_key = (host, port)
    
    # Verificar cache
    if cache_key in _dns_cache:
        return _dns_cache[cache_key]
    
    try:
        # FORÇA AF_INET (APENAS IPv4)
        # Usar a função original armazenada
        results = _original_getaddrinfo(host, port, socket.AF_INET, socktype, proto, flags)
        
        # Dupla-segurança: filtrar qualquer IPv6 que tenha passado
        ipv4_only = [r for r in results if r[0] == socket.AF_INET]
        
        if not ipv4_only:
            # Se nenhum IPv4 encontrado, tentar direto
            ipv4_only = _original_getaddrinfo(host, port, socket.AF_INET, socktype, proto, flags)
        
        # Cachear resultado
        _dns_cache[cache_key] = ipv4_only
        
        print(f"🔍 DNS: {host} → IPv4 ✅")
        return ipv4_only
        
    except Exception as e:
        print(f"⚠️ IPv4 lookup failed for {host}: {e}")
        raise


def enable_ipv4_only():
    """
    ATIVA o monkey-patch para forçar APENAS IPv4 em toda a aplicação
    DEVE ser chamado ANTES de qualquer conexão
    """
    global _original_getaddrinfo
    
    # Guardar função original ANTES de fazer qualquer coisa
    if _original_getaddrinfo is None:
        _original_getaddrinfo = socket.getaddrinfo
    
    # Substituir por nossa versão
    socket.getaddrinfo = _force_ipv4_getaddrinfo
    
    # Variáveis de ambiente
    os.environ['PSYCOPG2_DISABLE_IPV6'] = '1'
    
    print("✅ IPv4-only mode ATIVADO globalmente!")


# AUTO-ATIVAR quando este módulo for importado
enable_ipv4_only()
