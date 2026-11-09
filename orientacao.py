class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em):
        self.id = int(id)
        self.categoria = str(categoria)
        self.titulo = str(titulo)
        self.palavras_chave = list(palavras_chave)
        self.resposta = str(resposta)
        self.documentos = list(documentos)
        self.onde = str(onde)
        self.fonte = str(fonte)
        self.verificado_em = str(verificado_em)

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(f"{self.resposta}")
        print("Documentos necessários:")
        if self.documentos:
            for doc in self.documentos:
                print(f" - {doc}")
        else:
            print(" - Nenhum documento específico listado.")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")

    def to_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "palavras_chave": self.palavras_chave,
            "resposta": self.resposta,
            "documentos": self.documentos,
            "onde": self.onde,
            "fonte": self.fonte,
            "verificado_em": self.verificado_em
        }

    def __repr__(self):
        return f"<Orientacao id={self.id} titulo='{self.titulo}'>"

