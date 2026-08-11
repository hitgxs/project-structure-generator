import io
import os
import sys

IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'dist', 'build', 
    'bin', 'obj', 'venv', 'env', '.venv', 'target', '.idea', '.vscode'
}

def print_tree(directory, prefix="", ignore_dirs=IGNORE_DIRS):
    try:
        items = sorted(os.listdir(directory))
    except (PermissionError, FileNotFoundError):
        return

    filtered_items = [
        item for item in items 
        if item not in ignore_dirs and not item.startswith('.')
    ]

    for i, item in enumerate(filtered_items):
        path = os.path.join(directory, item)
        is_last = (i == len(filtered_items) - 1)
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(path):
            print(f"{prefix}{connector}📁 {item}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, new_prefix, ignore_dirs)
        else:
            print(f"{prefix}{connector}📄 {item}")

def obter_caminho():
    print("=" * 60)
    print("🔍 GERADOR DE ESTRUTURA DE PROJETOS")
    print("=" * 60)
    
    while True:
        caminho = input("\n📂 Digite o caminho da pasta raiz do projeto: ").strip()
        
        if not caminho:
            caminho = os.getcwd()
            print(f"ℹ️  Usando diretório atual: {caminho}")
        
        caminho = os.path.expanduser(caminho)
        
        if os.path.exists(caminho) and os.path.isdir(caminho):
            return caminho
        
        print(f"❌ Erro: '{caminho}' não é uma pasta válida!")
        print("💡 Dica: Use caminhos absolutos ou relativos (ex: /home/user/projeto ou ./projeto)")

def salvar_em_arquivo(estrutura, nome_arquivo="estrutura_projeto.txt"):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(estrutura)
        print(f"\n✅ Estrutura salva em: {nome_arquivo}")
    except Exception as e:
        print(f"⚠️  Não foi possível salvar o arquivo: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    root_path = obter_caminho()
    nome_pasta = os.path.basename(os.path.abspath(root_path))
    
    print("\n" + "=" * 60)
    print(f"📁 Projeto: {nome_pasta}")
    print(f"📍 Caminho: {os.path.abspath(root_path)}")
    print("=" * 60 + "\n")
    print("📋 ESTRUTURA DO PROJETO:\n")
    
    output = io.StringIO()
    sys.stdout = output
    
    print(f"📁 {nome_pasta}/")
    print_tree(root_path)
    
    sys.stdout = sys.__stdout__
    estrutura = output.getvalue()
    
    print(estrutura)
    
    salvar = input("\n💾 Deseja salvar esta estrutura em um arquivo? (s/N): ").strip().lower()
    if salvar in ['s', 'sim', 'y', 'yes']:
        nome_arquivo = input("📝 Nome do arquivo (padrão: estrutura_projeto.txt): ").strip()
        if not nome_arquivo:
            nome_arquivo = "estrutura_projeto.txt"
        if not nome_arquivo.endswith('.txt'):
            nome_arquivo += '.txt'
        salvar_em_arquivo(estrutura, nome_arquivo)
    
    print("\n✨ Finalizado!")