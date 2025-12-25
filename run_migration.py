"""
Script para executar a migração de dados para Supabase
Teste para ver se conecta e migra os dados
"""

import os
import sys
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("""
╔════════════════════════════════════════════════════╗
║      MIGRAÇÃO: VPS PostgreSQL → Supabase          ║
║           755 Tickets para o Supabase             ║
╚════════════════════════════════════════════════════╝
""")

print("\n⚠️  INSTRUÇÕES IMPORTANTES:")
print("="*50)
print("""
1. Este script vai exportar dados do VPS via SSH
2. Criar tabelas no Supabase
3. Importar os 755 tickets
4. Validar a migração

⏱️  Tempo estimado: 5-10 minutos

Se tiver erro de chave SSH, certifique-se que:
   - vps_key.pem está em backend/
   - Tem as permissões corretas (chmod 600 vps_key.pem)
""")

input("\n👉 Pressione ENTER para continuar...")

from backend.migrate_to_supabase import main

success = main()

if success:
    print("\n" + "="*50)
    print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print("\nO que fazer agora:")
    print("1. Verificar dados no Supabase:")
    print("   - Vá para https://app.supabase.com")
    print("   - Table Editor → tickets")
    print("\n2. Adicionar secrets no Streamlit Cloud (se usar cloud):")
    print("   - SUPABASE_HOST: db.nmsarhysujzhpjbpnqtl.supabase.co")
    print("   - SUPABASE_USER: postgres")
    print("   - SUPABASE_PASSWORD: Dx220304@280110")
    print("   - SUPABASE_DB: postgres")
    print("\n3. Fazer git push dos arquivos novos")
    print("\n4. Deploy no Streamlit Cloud!")
else:
    print("\n" + "="*50)
    print("❌ ERRO NA MIGRAÇÃO")
    print("="*50)
    print("\nVerifique:")
    print("- SSH conecta ao VPS? (try: ssh -i backend/vps_key.pem root@91.108.124.150)")
    print("- Supabase credentials estão corretas?")
    print("- Docker está rodando no VPS?")
    
sys.exit(0 if success else 1)
