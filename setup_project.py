from pathlib import Path

# Utiliza o diretório atual como raiz
root_dir = Path(".")

# Lista de diretórios a serem criados
directories = [
    root_dir / "data" / "raw",
    root_dir / "data" / "processed",
    root_dir / "data" / "warehouse",
    root_dir / "src" / "ingestion",
    root_dir / "src" / "transformation",
    root_dir / "src" / "quality",
    root_dir / "src" / "database",
    root_dir / "src" / "config",
    root_dir / "tests",
]

# Lista de arquivos a serem criados
files = [
    root_dir / ".gitignore",
    root_dir / "README.md",
    root_dir / "requirements.txt",
]


def create_project_structure():
    # Criar diretórios
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Diretório verificado/criado: {directory}")

    # Criar arquivos vazios (sem sobrescrever se já existirem)
    for file in files:
        file.touch(exist_ok=True)
        print(f"Arquivo verificado/criado: {file}")

    print("\n✅ Estrutura criada com sucesso no diretório atual!")


if __name__ == "__main__":
    create_project_structure()