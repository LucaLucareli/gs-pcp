import sys
from base_conhecimento import BaseConhecimento
from assistente import Assistente


def exibir_cabecalho(nome_assistente):
    print("=" * 65)
    print(f"       {nome_assistente} - Orientação ao Cidadão")
    print("  Informações Oficiais para Jovens, Primeiro Emprego e Cidadania")
    print("=" * 65)


def exibir_menu_principal():
    print("\nMENU PRINCIPAL:")
    print("1. Fazer uma pergunta (busca inteligente)")
    print("2. Navegar por categorias de serviços")
    print("3. Visualizar indicadores de atendimento")
    print("4. Exportar atendimentos para CSV")
    print("0. Sair do assistente")


def main():
    caminho_base = "data/base_conhecimento.json"
    base = BaseConhecimento(caminho_base)
    sucesso_carga = base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    exibir_cabecalho(assistente.nome)

    if not sucesso_carga or len(base.orientacoes) == 0:
        print("[Aviso] A base de conhecimento não possui orientações carregadas.")
        print(f"Verifique se o arquivo '{caminho_base}' existe e está preenchido corretamente.\n")

    while True:
        exibir_menu_principal()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            print("\nEncerrando sessão de atendimento...")
            assistente.avaliar_facilidade()
            assistente.exportar_csv()
            print("\nObrigado por utilizar o Citizen Assist AI. Até logo!\n")
            sys.exit(0)
        else:
            print("Opção inválida! Por favor, digite um número entre 0 e 4.")


if __name__ == "__main__":
    main()

