import random

# Categorias expandidas com várias palavras diferentes
categorias = {
    "lugares": ["praia", "parque", "shopping", "cinema", "museu", "igreja", "praça", "hotel", "aeroporto", 
                "montanha", "deserto", "floresta", "cachoeira", "pista", "praia", "porto", "ponte", "vila",
                "bairro", "cidade antiga", "zona rural", "zona urbana", "torre", "castelo", "muralha", "farol",
                "biblioteca", "estádio", "ginásio", "metrô", "rodoviária", "avenida", "praça de alimentação",
                "parque de diversões", "jardim botânico", "museu de arte"],
    "atores e atrizes": ["Tom Cruise", "Meryl Streep", "Brad Pitt", "Angelina Jolie", "Scarlett Johansson",
                         "Robert De Niro", "Al Pacino", "Leonardo DiCaprio", "Natalie Portman", "Denzel Washington",
                         "Emma Stone", "Chris Hemsworth", "Johnny Depp", "Cate Blanchett", "Anne Hathaway", 
                         "Charlize Theron", "Joaquin Phoenix", "Keanu Reeves", "Ryan Gosling", "Tom Hardy"],
    "regiões": ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul", "Ásia", "Europa", "América do Norte",
                "América do Sul", "Oceania", "África", "Oriente Médio", "Leste Europeu", "Sul da Ásia", "Ártico",
                "Antártica"],
    "países": ["Brasil", "Estados Unidos", "França", "Itália", "China", "Japão", "Alemanha", "Rússia", "Índia",
               "Canadá", "México", "Argentina", "Chile", "Colômbia", "Peru", "Espanha", "Portugal", "Reino Unido",
               "Austrália", "Nova Zelândia"],
    "estados e municípios": ["São Paulo", "Rio de Janeiro", "Buenos Aires", "Nova York", "Paris", "Londres", 
                             "Tóquio", "Sydney", "Berlim", "Amsterdã", "Bruxelas", "Madri", "Lisboa", "Cidade do México",
                             "Santiago", "Bogotá", "Seul", "Pequim", "Mumbai", "Los Angeles", "Chicago", "Vancouver"],
    "animais": ["cachorro", "gato", "elefante", "tigre", "leão", "tartaruga", "pinguim", "tubarão", "baleia", "urso",
                "lobo", "raposa", "jaguar", "gorila", "macaco", "cobra", "águia", "papagaio", "pavão", "leopardo"],
    "física": ["energia", "força", "aceleração", "gravidade", "pressão", "massa", "trabalho", "potência", "inércia",
               "calor", "fricção", "impulso", "momento", "eletricidade", "campo magnético", "resistência", "capacitância",
               "indutância", "velocidade", "movimento"],
    "química": ["átomo", "molécula", "elemento", "composto", "reação", "ácido", "base", "sal", "pH", "oxidação", 
                "redução", "íon", "cátion", "ânion", "ligação covalente", "ligação iônica", "metal", "não-metal", 
                "polímero", "gás"],
    "geografia": ["continente", "oceano", "montanha", "rio", "deserto", "ilha", "floresta", "planície", "planalto",
                  "bacia hidrográfica", "costa", "península", "estreito", "golfo", "baía", "arquipélago", "delta",
                  "cordilheira", "vulcão", "fóssil"],
    "matemática": ["triângulo", "equação", "número primo", "cosseno", "logaritmo", "derivada", "integral", "fração",
                   "número irracional", "número imaginário", "raiz quadrada", "progressão aritmética", "progressão geométrica",
                   "vetor", "matriz", "determinante", "função", "parábola", "hipérbole", "seno"],
    "português": ["substantivo", "verbo", "adjetivo", "advérbio", "sujeito", "predicado", "frase", "oração", "sintaxe",
                  "morfologia", "antônimo", "sinônimo", "parágrafo", "pontuação", "gramática", "conjunção", "interjeição",
                  "pronomes", "concordância", "tempo verbal"],
    "monumentos": ["Torre Eiffel", "Cristo Redentor", "Estátua da Liberdade", "Muralha da China", "Coliseu", "Taj Mahal",
                   "Big Ben", "Sagrada Família", "Ponte Golden Gate", "Pirâmides de Gizé", "Templo de Luxor", 
                   "Stonehenge", "Machu Picchu", "Palácio de Versalhes", "Torre de Pisa", "Ópera de Sydney", 
                   "Templo de Kyoto", "Castelo de Neuschwanstein", "Alhambra", "Castelo de Windsor"],
    "objetos": ["cadeira", "mesa", "computador", "telefone", "televisão", "bicicleta", "geladeira", "fogão", "livro",
                "caneta", "lápis", "papel", "relógio", "óculos", "carteira", "mochila", "copo", "garrafa", "sapato",
                "chave"],
    "roupas": ["camiseta", "calça", "sapato", "vestido", "casaco", "boné", "blusa", "saia", "meia", "jaqueta", 
               "camisa", "bermuda", "terno", "gravata", "cinto", "luva", "chapéu", "cachecol", "uniforme", "calção"],
    "comida": ["pizza", "hambúrguer", "sushi", "feijoada", "macarrão", "lasanha", "batata frita", "bife", "salada",
               "frango", "arroz", "feijão", "torta", "pão", "bolo", "chocolate", "sorvete", "suco", "refrigerante",
               "café"],
    "cores": ["vermelho", "azul", "verde", "amarelo", "preto", "branco", "roxo", "rosa", "laranja", "marrom", 
              "cinza", "bege", "turquesa", "dourado", "prata", "violeta", "lavanda", "azul marinho", "verde claro",
              "vermelho escuro"],
    "prédios": ["arranha-céu", "escritório", "hospital", "escola", "igreja", "universidade", "biblioteca", "cinema", 
                "shopping", "restaurante", "farmácia", "supermercado", "aeroporto", "estação de trem", "estação de metrô",
                "hotel", "motel", "teatro", "museu", "delegacia"]
}

# Função para gerar 3000 palavras
def gerar_palavras(categorias, total_palavras=3000):
    palavras = []
    for categoria, lista_palavras in categorias.items():
        palavras.extend(lista_palavras)  # Adiciona todas as palavras da categoria

    # Se houver menos de 3000 palavras, duplicar aleatoriamente até atingir o total
    while len(palavras) < total_palavras:
        categoria = random.choice(list(categorias.keys()))
        palavra = random.choice(categorias[categoria])
        palavras.append(palavra)

    return palavras[:total_palavras]  # Garante que tenha exatamente 3000 palavras

# Gerando as palavras
palavras = gerar_palavras(categorias)

# Criando o arquivo txt com as palavras
with open("palavras.txt", "w") as file:
    for palavra in palavras:
        file.write(palavra + "\n")

print("Arquivo 'palavras.txt' criado com sucesso!")
