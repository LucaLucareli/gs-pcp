# 🎬 Roteiro Completo do Vídeo Técnico - Citizen Assist AI
**FIAP - Global Solution 2026.2 | Disciplina: Pensamento Computacional e Automação com Python**

> [!IMPORTANT]
> **Regras Oficiais do Vídeo:**
> * **Duração obrigatória:** Entre **5 e 8 minutos** (vídeos com mais de 8 minutos são desconsiderados pela banca).
> * **Publicação:** YouTube como **Não Listado** (*Unlisted*).
> * **Formato:** Gravação de tela com código fonte nítido/legível e terminal rodando. Câmera é opcional.
> * **Vozes:** Todos os integrantes devem falar, explicando partes técnicas. É **proibida** narração por IA ou voz sintética.
> * **Foco:** Não é um pitch comercial! Trata-se de uma **explicação técnica e demonstração prática do código**.

---

## ⏱️ Distribuição do Tempo Sugerida (Meta: ~6m30s a 7m00s)

| Bloco | Item Obrigatório do Edital | Responsável Sugerido | Duração Estimada |
|---|---|---|---|
| **Bloco 1** | 1. Equipe, público e problema escolhido | Integrante 1 | 00:00 - 00:30 (30s) |
| **Bloco 2** | 2. Estrutura JSON, dicionários e tuplas | Integrante 2 | 00:30 - 01:20 (50s) |
| **Bloco 3** | 3. Classes: atributos, métodos, `self` e composição | Integrante 3 | 01:20 - 02:20 (60s) |
| **Bloco 4** | 4. Busca: `normalizar()` e `pontuar()` com cálculo real | Integrante 1 | 02:20 - 03:20 (60s) |
| **Bloco 5** | 5. Execução ao vivo: Casos de teste e navegação | Integrante 2 | 03:20 - 04:35 (75s) |
| **Bloco 6** | 6. Alteração ao vivo no JSON: Antes e depois | Integrante 3 | 04:35 - 05:30 (55s) |
| **Bloco 7** | 7. `historico.json`, CSV exportado e indicadores | Integrante 1 | 05:30 - 06:15 (45s) |
| **Bloco 8** | 8. Decisão técnica e limitação do assistente | Integrante 2 e 3 | 06:15 - 06:50 (35s) |

---

## 📝 Passo a Passo Detalhado para Gravação

---

### Bloco 1: Apresentação da Equipe, Público e Problema (Até 30 segundos)
* **Na tela:** VS Code aberto mostrando a estrutura de pastas do projeto (`citizen-assist-ai/`) e o arquivo `README.md`.
* **Falas sugeridas:**
  > *"Olá, professor e avaliadores da FIAP! Somos o grupo [Nome do Grupo], composto por [Nome 1 - RM], [Nome 2 - RM] e [Nome 3 - RM].*
  > *Para esta Global Solution, escolhemos o público de **Jovens no Primeiro Emprego e Cidadania Digital**.*
  > *O problema que atacamos é a grande desinformação e fragmentação de dados oficiais sobre documentação obrigatória como Carteira de Trabalho Digital, Título de Eleitor, Alistamento Militar e vagas de Jovem Aprendiz. Desenvolvemos o **Citizen Assist AI** para responder dúvidas de forma transparente, com fontes oficiais e sem coletar nenhum dado pessoal."*

---

### Bloco 2: JSON, Dicionários e Tuplas (Aprox. 50 segundos)
* **Na tela:** Abra o arquivo `data/base_conhecimento.json`. Destaque um registro específico (exemplo: ID 1 ou ID 11).
* **Falas sugeridas:**
  > *"Aqui no arquivo `data/base_conhecimento.json`, temos a nossa base de conhecimento estruturada como uma lista de dicionários Python.*
  > *Cada dicionário representa uma orientação e contém rigorosamente todos os campos obrigatórios: `id`, `categoria`, `titulo`, `palavras_chave` (com no mínimo 3 palavras ou variações), `resposta` em linguagem simples, `documentos`, `onde` o cidadão deve ir, a `fonte` oficial verificada do governo e a data `verificado_em`.*
  > *Na manipulação interna dos dados no código, utilizamos **tuplas** no formato `(pontos, orientacao)`. A tupla é ideal aqui por ser imutável e leve, permitindo ordenar os resultados da busca por relevância decrescente de pontuação de forma muito eficiente."*

---

### Bloco 3: Classes, Atributos, Métodos, `self` e Composição (Aprox. 60 segundos)
* **Na tela:** Mostre `orientacao.py`, `base_conhecimento.py` e `assistente.py`.
* **Falas sugeridas:**
  > *"O sistema foi dividido em três classes bem definidas, aplicando Orientação a Objetos e o conceito de composição visto na disciplina:*
  > *1. Na classe `Orientacao` (em `orientacao.py`), guardamos os atributos de um registro e o método `exibir()`, que imprime a resposta formatada com os documentos necessários, o local, a fonte oficial e o aviso legal de que não somos canal oficial.*
  > *2. Na classe `BaseConhecimento` (em `base_conhecimento.py`), temos a lista `self.orientacoes`, que armazena objetos `Orientacao`. Ela contém os métodos `carregar()`, que lê o JSON com tratamento de erros para não travar a aplicação, `categorias()`, `por_categoria()` e o algoritmo de busca.*
  > *3. Na classe `Assistente` (em `assistente.py`), temos o atributo `self.base`, que recebe o objeto `BaseConhecimento` por **composição**. O `self` é utilizado em todos os métodos para referenciar a própria instância, seus atributos de estado e seu histórico de atendimentos."*

---

### Bloco 4: Busca Inteligente: `normalizar()` e `pontuar()` (Aprox. 60 segundos)
* **Na tela:** Mostre o código de `base_conhecimento.py` nas funções `normalizar()` e no método `pontuar()`.
* **Falas sugeridas:**
  > *"A nossa busca inteligente é baseada em regras determinísticas:*
  > *A função `normalizar()` converte todo o texto para minúsculas, remove acentos usando um dicionário de substituição, retira pontuações e adiciona espaços nas bordas.*
  > *No método `pontuar()`, aplicamos as duas regras do edital:*
  > *Primeiro: se uma palavra-chave da orientação aparece na pergunta normalizada, somamos **+3 pontos**.*
  > *Segundo: para cada palavra da pergunta com 4 letras ou mais presente no título da orientação, somamos **+1 ponto**.*
  > *Por exemplo, quando o usuário digita: 'Como faço o cartão do SUS?':*
  > *A orientação do Cartão SUS recebe +3 pela palavra-chave 'cartao do sus', +3 por 'sus', e +1 porque a palavra 'cartao' tem 6 letras e está no título. Totalizando **7 pontos**, o que classifica a resposta com **Confiança ALTA** (pois atingiu 6 ou mais pontos)."*

---

### Bloco 5: Execução do Programa no Terminal (Aprox. 75 segundos)
* **Na tela:** Terminal rodando `python main.py`.
* **Ações práticas no terminal:**
  1. **Pergunta Encontrada:**
     * Escolha opção `1` (Fazer uma pergunta).
     * Digite: `Como faco o cartao do sus?`
     * Aponte na tela: Confiança ALTA (7 pontos), os dados oficiais, a fonte e o aviso.
     * Responda: `s` para indicar que ajudou.
  2. **Bloqueio de Dados Pessoais (LGPD):**
     * Na pergunta seguinte, digite: `meu cpf é 123.456.789-00`
     * Mostre a mensagem de bloqueio imediato: *"Atenção: não digite CPF, telefone ou e-mail. Reescreva."*
     * Digite um e-mail: `contato@teste.com` e mostre que também é bloqueado e **não é registrado** no histórico.
  3. **Pergunta Não Encontrada:**
     * Digite uma dúvida fora do tema: `como viajar para o planeta marte`
     * Mostre a mensagem de "Não encontrei" e a sugestão de consultar categorias.
     * Responda `n` para voltar ao menu.
  4. **Entrada Inválida:**
     * No menu, digite letras (ex: `abc`), enter vazio ou número fora da faixa (ex: `9`).
     * Mostre que o programa trata graciosamente e **nunca encerra ou quebra**.
  5. **Navegação por Categorias:**
     * Escolha opção `2` (Navegar por categorias).
     * Escolha `1` (Documentação Básica).
     * Mostre as orientações listadas numeradas com opção `0 para voltar`.
     * Selecione `1` (Carteira de Trabalho Digital) e mostre a exibição.
     * Use `0` para voltar em todas as telas até o menu principal.

---

### Bloco 6: Alteração ao Vivo no JSON (Obrigatório do Edital) (Aprox. 55 segundos)
* **Na tela:** Terminal + arquivo `data/base_conhecimento.json` lado a lado.
* **Passo a passo da demonstração ao vivo:**
  1. No terminal, vá na opção `1` (Fazer uma pergunta) e digite uma frase que contenha uma palavra não mapeada ainda, por exemplo:
     * Dúvida: `como acessar o passe livre de estudante`
     * Resultado: Mostra que **Não encontrou** (confiança baixa / 0 pontos).
  2. Sem fechar o programa (ou reiniciando após salvar):
     * Abra o arquivo `data/base_conhecimento.json`.
     * Vá na orientação ID 10 (*Emitir a Identidade Jovem - ID Jovem*).
     * Adicione nas `palavras_chave`: `"passe livre"`.
     * Salve o arquivo (`Ctrl + S`).
  3. No terminal:
     * Digite a mesma pergunta: `como acessar o passe livre de estudante`
     * Resultado imediato: **Encontrou com sucesso!** A orientação da ID Jovem é exibida na tela.
* **Falas sugeridas:**
  > *"Como exigido no edital, demonstramos agora a alteração ao vivo: a dúvida sobre 'passe livre' anteriormente não recebia pontuação suficiente. Adicionamos a palavra-chave correspondente no JSON e, imediatamente, o algoritmo passa a reconhecer e orientar o cidadão com sucesso!"*

---

### Bloco 7: Histórico, CSV Exportado e Indicadores (Aprox. 45 segundos)
* **Na tela:** Volte ao menu principal do terminal e depois abra os arquivos no VS Code.
* **Ações:**
  1. No terminal, selecione a opção `3` (Visualizar indicadores de atendimento).
     * Explique na tela os indicadores calculados em tempo real:
       * **Resposta encontrada (%):** ~83%
       * **Taxa de acerto: ajudou (%):** ~83%
       * **Tempo médio para encontrar:** ~4.5 segundos (medido via `time.time()`)
       * **Tentativas por atendimento:** ~1.2
       * **Facilidade de uso:** ~4.7 / 5.0
       * **Lista de dúvidas sem solução:** listadas de forma clara para melhoria contínua da equipe.
  2. No terminal, selecione a opção `4` (Exportar atendimentos para CSV).
  3. Mostre o arquivo `data/historico.json` e o `data/atendimentos.csv` aberto no VS Code, destacando o uso do `csv.DictWriter` conforme ensinado na Aula 09.

---

### Bloco 8: Decisão Técnica e Limitação do Assistente (Aprox. 35 segundos)
* **Na tela:** Todos os integrantes ou o integrante responsável concluindo a apresentação.
* **Falas sugeridas:**
  > *"Para encerrar, compartilhamos uma decisão técnica relevante e uma limitação:*
  > * Como **decisão técnica**, optamos por envelopar o texto normalizado com espaços (`' ' + texto + ' '`) e usar busca por palavras inteiras. Isso eliminou completamente falsos positivos de substrings (como a palavra 'sus' casar indevidamente dentro de 'sustentável' ou 'suspensão').*
  > * Como **limitação**, o assistente opera por regras estritas e palavras-chave. Portanto, caso o usuário utilize termos com erros ortográficos muito graves ou gírias não mapeadas, o sistema não adivinha a intenção por aproximação semântica profunda, dependendo de o usuário navegar pelas categorias.*
  > *Ao selecionar a opção 0 para sair, o sistema nos solicita a nota de avaliação de 1 a 5 e encerra com segurança.*
  > *Muito obrigado a todos!"*

---

##  Checklist Final Pré-Gravação
- [ ] Testar `python main.py` antes de gravar para garantir que não há erros de digitação.
- [ ] Deixar a fonte do editor e do terminal com tamanho legível (Zoom: `Ctrl + +`).
- [ ] Certificar-se de que o microfone de todos os integrantes esteja limpo e audível.
- [ ] Cronometrar para ficar entre **5 minutos e 8 minutos** (sugestão: 6 a 7 minutos).
- [ ] Subir o vídeo no YouTube com visibilidade **Não Listado** (*Unlisted*).
- [ ] Copiar o link do YouTube para o `README.md` e para o `entrega_fiap.txt`.

