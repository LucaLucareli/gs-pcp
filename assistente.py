import csv
import json
import os
import time
from datetime import datetime


def contem_dados_pessoais(texto):
    digitos = sum(1 for c in texto if c.isdigit())
    if digitos >= 8 or "@" in texto:
        return True
    return False


def obter_resposta_sim_nao(mensagem="Essa orientação respondeu sua dúvida? (s/n): "):
    while True:
        resp = input(mensagem).strip().lower()
        if resp in ["s", "sim"]:
            return True
        elif resp in ["n", "nao", "não"]:
            return False
        else:
            print("Entrada inválida. Por favor, digite 's' para sim ou 'n' para não.")


class Assistente:
    def __init__(self, nome="Citizen Assist AI", base=None):
        self.nome = nome
        self.base = base
        self.historico_arquivo = "data/historico.json"
        self.csv_arquivo = "data/atendimentos.csv"
        self.avaliacoes_arquivo = "data/avaliacoes.json"
        self.historico = []
        self.avaliacoes = []
        self._carregar_historico()
        self._carregar_avaliacoes()

    def _carregar_historico(self):
        if os.path.exists(self.historico_arquivo):
            try:
                with open(self.historico_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        self.historico = dados
            except (json.JSONDecodeError, OSError) as erro:
                print(f"[Aviso] Histórico existente não pôde ser lido ({erro}). Iniciando novo histórico em memória.")
                self.historico = []

    def _salvar_historico(self):
        os.makedirs(os.path.dirname(self.historico_arquivo), exist_ok=True)
        try:
            with open(self.historico_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f"[Erro] Não foi possível gravar em {self.historico_arquivo}: {erro}")

    def _carregar_avaliacoes(self):
        if os.path.exists(self.avaliacoes_arquivo):
            try:
                with open(self.avaliacoes_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        self.avaliacoes = dados
            except (json.JSONDecodeError, OSError):
                self.avaliacoes = []

    def _salvar_avaliacoes(self):
        os.makedirs(os.path.dirname(self.avaliacoes_arquivo), exist_ok=True)
        try:
            with open(self.avaliacoes_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.avaliacoes, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo_segundos):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": str(origem),
            "pergunta": str(pergunta),
            "id_orientacao": id_orientacao,
            "encontrou": bool(encontrou),
            "ajudou": bool(ajudou),
            "tentativas": int(tentativas),
            "tempo_segundos": float(tempo_segundos)
        }
        self.historico.append(registro)
        self._salvar_historico()

    def perguntar(self):
        tentativas = 0
        inicio = time.time()

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                print("Retornando ao menu...")
                return

            if not pergunta:
                print("A dúvida não pode ser vazia. Por favor, digite sua pergunta.")
                continue

            if contem_dados_pessoais(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            melhor_pontos, melhor_orientacao = resultados[0] if resultados else (0, None)

            if melhor_pontos >= 6:
                confianca = "ALTA"
            elif melhor_pontos >= 3:
                confianca = "MÉDIA"
            else:
                confianca = "BAIXA"

            if confianca in ["ALTA", "MÉDIA"] and melhor_orientacao is not None:
                print(f"\nConfiança da resposta: {confianca} ({melhor_pontos} pontos)")
                melhor_orientacao.exibir()

                alternativas = [item for item in resultados[1:3] if item[0] >= 3]
                if alternativas:
                    print("\n--- Outras opções relacionadas ---")
                    for idx, (pts, alt) in enumerate(alternativas, start=1):
                        print(f" {idx}. {alt.titulo} ({pts} pontos) [{alt.categoria}]")

                ajudou = obter_resposta_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                tempo_total = round(time.time() - inicio, 1)

                self.registrar(
                    origem="pergunta",
                    pergunta=pergunta,
                    id_orientacao=melhor_orientacao.id,
                    encontrou=True,
                    ajudou=ajudou,
                    tentativas=tentativas,
                    tempo_segundos=tempo_total
                )

                if ajudou:
                    print("Excelente! Ficamos felizes em ajudar.")
                    break
                else:
                    print("Lamentamos que não tenha resolvido totalmente. Você pode tentar reformular a pergunta ou consultar as categorias.")
                    reiterar = obter_resposta_sim_nao("Deseja tentar outra pergunta agora? (s/n): ")
                    if not reiterar:
                        break
            else:
                print("\nNão encontrei uma resposta com pontuação suficiente para sua dúvida.")
                print("Sugestão: tente usar outras palavras-chave ou utilize a opção de Navegação por Categorias no menu.")
                
                tempo_total = round(time.time() - inicio, 1)
                self.registrar(
                    origem="pergunta",
                    pergunta=pergunta,
                    id_orientacao=None,
                    encontrou=False,
                    ajudou=False,
                    tentativas=tentativas,
                    tempo_segundos=tempo_total
                )

                continuar = obter_resposta_sim_nao("Deseja tentar fazer outra pergunta? (s/n): ")
                if not continuar:
                    break

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("\nNenhuma categoria disponível no momento.")
            return

        while True:
            print("\n=== Navegação por Categorias ===")
            for i, cat in enumerate(categorias, start=1):
                print(f"{i}. {cat}")
            print("0. Voltar ao menu principal")

            opcao = input("\nEscolha uma categoria (0 para voltar): ").strip()
            if opcao == "0":
                break

            if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(categorias):
                print("Opção inválida! Digite o número correspondente à categoria ou 0 para voltar.")
                continue

            categoria_escolhida = categorias[int(opcao) - 1]
            self._navegar_orientacoes(categoria_escolhida)

    def _navegar_orientacoes(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        if not orientacoes:
            print(f"\nNenhuma orientação cadastrada para a categoria '{categoria}'.")
            return

        while True:
            print(f"\n--- {categoria} ---")
            for i, ori in enumerate(orientacoes, start=1):
                print(f"{i}. {ori.titulo}")
            print("0. Voltar")

            escolha = input("\nEscolha uma orientação para visualizar (0 para voltar): ").strip()
            if escolha == "0":
                break

            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(orientacoes):
                print("Opção inválida! Escolha um número da lista ou 0 para voltar.")
                continue

            inicio = time.time()
            orientacao = orientacoes[int(escolha) - 1]
            orientacao.exibir()

            ajudou = obter_resposta_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo_total = round(time.time() - inicio, 1)

            self.registrar(
                origem="categoria",
                pergunta=f"Navegação: {categoria} -> {orientacao.titulo}",
                id_orientacao=orientacao.id,
                encontrou=True,
                ajudou=ajudou,
                tentativas=1,
                tempo_segundos=tempo_total
            )

            if ajudou:
                print("Ficamos felizes em ajudar!")
            else:
                print("Obrigado pelo feedback. Estamos sempre aprimorando nosso banco de dados.")

            input("\nPressione ENTER para continuar...")

    def indicadores(self):
        total = len(self.historico)
        print("\n================ INDICADORES DE ATENDIMENTO ================")
        if total == 0:
            print("Nenhum atendimento registrado até o momento.")
            print("Realize atendimentos por pergunta ou categoria para gerar métricas.")
            print("============================================================")
            return

        encontradas = sum(1 for a in self.historico if a.get("encontrou") is True)
        ajudaram = sum(1 for a in self.historico if a.get("ajudou") is True)

        pct_encontrada = (encontradas / total) * 100
        taxa_acerto = (ajudaram / total) * 100

        tempos_encontrados = [a.get("tempo_segundos", 0.0) for a in self.historico if a.get("encontrou") is True]
        tempo_medio = sum(tempos_encontrados) / len(tempos_encontrados) if tempos_encontrados else 0.0

        todas_tentativas = [a.get("tentativas", 1) for a in self.historico]
        tentativas_medias = sum(todas_tentativas) / total if todas_tentativas else 1.0

        if self.avaliacoes:
            media_facilidade = sum(self.avaliacoes) / len(self.avaliacoes)
            str_facilidade = f"{media_facilidade:.1f} / 5.0 (baseado em {len(self.avaliacoes)} avaliações)"
        else:
            str_facilidade = "Ainda não avaliada"

        duvidas_sem_solucao = [
            a.get("pergunta", "") for a in self.historico
            if a.get("origem") == "pergunta" and (not a.get("encontrou") or not a.get("ajudou"))
        ]

        print(f"Total de atendimentos registrados : {total}")
        print(f"Resposta encontrada (%)           : {pct_encontrada:.1f}% ({encontradas}/{total})")
        print(f"Taxa de acerto: ajudou (%)         : {taxa_acerto:.1f}% ({ajudaram}/{total})")
        print(f"Tempo médio para encontrar         : {tempo_medio:.1f} segundos")
        print(f"Tentativas por atendimento (média) : {tentativas_medias:.1f}")
        print(f"Facilidade de uso (1 a 5)          : {str_facilidade}")
        print("------------------------------------------------------------")
        print(f"Lista de dúvidas sem solução ({len(duvidas_sem_solucao)}):")
        if duvidas_sem_solucao:
            for idx, duvida in enumerate(duvidas_sem_solucao, start=1):
                print(f"  {idx}. {duvida}")
        else:
            print("  Nenhuma dúvida sem solução registrada! Excelente taxa de resolução.")
        print("============================================================\n")

    def exportar_csv(self):
        os.makedirs(os.path.dirname(self.csv_arquivo), exist_ok=True)
        campos = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos"
        ]

        try:
            with open(self.csv_arquivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
                escritor.writeheader()
                for registro in self.historico:
                    escritor.writerow(registro)
            print(f"Atendimentos exportados com sucesso para: {self.csv_arquivo} ({len(self.historico)} registros)")
            return True
        except OSError as erro:
            print(f"[Erro] Falha ao exportar atendimentos para CSV: {erro}")
            return False

    def avaliar_facilidade(self):
        while True:
            nota_str = input("\nDe 1 a 5, como você avalia a facilidade de uso do assistente? ").strip()
            if nota_str.isdigit():
                nota = int(nota_str)
                if 1 <= nota <= 5:
                    self.avaliacoes.append(nota)
                    self._salvar_avaliacoes()
                    print(f"Obrigado pelo seu feedback! Sua nota {nota} foi registrada com sucesso.")
                    break
            print("Nota inválida! Por favor, digite um número inteiro entre 1 e 5.")
