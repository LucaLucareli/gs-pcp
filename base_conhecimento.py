import json
import os
from orientacao import Orientacao

# Tabela de substituição para normalização de texto sem acentos
ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e", "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u", "ç": "c"
}


def normalizar(texto):
    if not isinstance(texto, str):
        return " "
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()\"'[]{}-_":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho="data/base_conhecimento.json"):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        if not os.path.exists(self.caminho):
            print(f"[Aviso] Arquivo da base de conhecimento não encontrado: {self.caminho}")
            self.orientacoes = []
            return False

        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)

            if not isinstance(dados, list):
                print(f"[Aviso] Formato inesperado na base JSON ({self.caminho}). Esperava-se uma lista.")
                self.orientacoes = []
                return False

            self.orientacoes = []
            for item in dados:
                orientacao = Orientacao(
                    id=item.get("id", 0),
                    categoria=item.get("categoria", "Geral"),
                    titulo=item.get("titulo", "Sem título"),
                    palavras_chave=item.get("palavras_chave", []),
                    resposta=item.get("resposta", ""),
                    documentos=item.get("documentos", []),
                    onde=item.get("onde", ""),
                    fonte=item.get("fonte", ""),
                    verificado_em=item.get("verificado_em", "")
                )
                self.orientacoes.append(orientacao)
            return True

        except (json.JSONDecodeError, OSError) as erro:
            print(f"[Aviso] Falha ao ler/interpretar o arquivo JSON ({self.caminho}): {erro}")
            self.orientacoes = []
            return False

    def categorias(self):
        cats = sorted(list({o.categoria for o in self.orientacoes if o.categoria}))
        return cats

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria.strip().lower() == categoria.strip().lower()]

    def pontuar(self, pergunta, orientacao):
        pontos = 0
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)

        for pc in orientacao.palavras_chave:
            pc_norm = normalizar(pc).strip()
            if pc_norm and (f" {pc_norm} " in pergunta_norm):
                pontos += 3

        palavras_pergunta = set(pergunta_norm.split())
        for palavra in palavras_pergunta:
            if len(palavra) >= 4:
                termo_palavra = f" {palavra} "
                if termo_palavra in titulo_norm:
                    pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: (-item[0], item[1].id))
        return resultados
