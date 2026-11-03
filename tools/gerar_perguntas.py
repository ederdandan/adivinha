#!/usr/bin/env python3
"""Gera perguntas.js (banco enxuto de perguntas Sim/Não, separado por grupos).
Uso: python3 tools/gerar_perguntas.py  -> escreve perguntas.js na pasta do jogo.
Para adicionar perguntas, acrescente itens às listas abaixo e rode de novo."""
import json, os, unicodedata

def L(s):  # lista separada por "|"
    return [x.strip() for x in s.split('|') if x.strip()]

def cap(s): return s[0].upper() + s[1:]

# ---------------------------------------------------------------- GERAL
GERAL_BASE = L("""É um ser vivo?|É um animal?|É uma comida?|É um objeto?|É uma profissão?|É um lugar?|
Existe de verdade?|Dá para tocar?|Dá para comer?|Dá para beber?|Dá para segurar com uma mão?|Cabe na palma da mão?|
Cabe numa mochila?|Cabe dentro de uma casa?|É maior que uma pessoa?|É menor que um carro?|É pesado?|É leve?|
É barulhento?|Faz algum som?|Tem cheiro?|Tem cheiro bom?|Tem cheiro forte?|É macio?|É duro?|É gelado?|É quente?|
É molhado?|É colorido?|Tem uma cor só?|Brilha?|É redondo?|É comprido?|É quadrado?|Tem rodas?|Tem pernas ou patas?|
Tem olhos?|Tem pelos?|Se mexe sozinho?|Usa eletricidade?|Usa bateria?|Precisa de combustível?|Precisa de água?|
Vive ou fica na água?|Fica ao ar livre?|Fica dentro de casa?|Tem dentro da sua casa?|Você já viu de perto?|
Você usa todo dia?|Crianças gostam?|Idosos gostam?|É perigoso?|Pode machucar?|É caro?|É barato?|Dá para comprar?|
Dá para dar de presente?|Existe no Brasil?|Existe no mundo todo?|É comum?|É raro?|É moderno?|Existe há muito tempo?|
Existia na época dos dinossauros?|Existia na época dos seus avós?|Aparece em desenhos animados?|Aparece em filmes?|
Tem a ver com saúde?|Tem a ver com festa?|Tem a ver com escola?|Tem a ver com esporte?|Tem a ver com música?|
Tem a ver com natureza?|Tem a ver com tecnologia?|Tem a ver com comida?|Tem a ver com viagem?|Tem a ver com trabalho?|
Tem a ver com diversão?|Tem a ver com religião?|Tem a ver com dinheiro?|Tem a ver com segurança?|Tem a ver com limpeza?|
Tem a ver com o mar?|Tem a ver com o céu?|Tem a ver com o espaço?|Tem a ver com a noite?|Tem a ver com o calor?|
Tem a ver com o frio?|É feito pelo ser humano?|Vem da natureza?|Dá para reciclar?|Estraga com o tempo?|
Dura muitos anos?|Tem mais de um tipo?|Tem marcas famosas?|Tem um nome com mais de uma palavra?|
O nome começa com vogal?|O nome tem mais de 6 letras?|O nome tem acento?|É masculino (o/um)?|É feminino (a/uma)?|
Dá para desenhar facilmente?|Dá para imitar com mímica?|Dá para ver no céu?|Dá para ver da janela?|
É mais comum na cidade?|É mais comum no campo?|Está ligado ao Brasil?|É típico de outro país?|Tem a ver com o verão?|
Tem a ver com o inverno?|Tem a ver com o Natal?|Tem a ver com a Páscoa?|Tem a ver com aniversário?|
Tem a ver com férias?|Tem a ver com o fim de semana?|Tem a ver com a manhã?|Tem a ver com a hora de dormir?|
Usa-se em casa?|Usa-se na rua?|Você teria em casa?|Você gostaria de ter?|Você tem medo disso?|
Faz parte da rotina de muita gente?|Tem algo escrito?|Tem números?|Tem botões?|Tem tela?|Tem porta?|
Tem janela?|Tem tampa?|Abre e fecha?|Dá para dobrar?|Quebra fácil?|Molha?|Suja?|Precisa de cuidado?|
Precisa de manutenção?|Pode ser compartilhado?|É usado por uma pessoa só?|É coletivo?|Precisa de outra pessoa?|
É relacionado a algum esporte?|É relacionado a algum instrumento?|Aparece em histórias infantis?|
Aparece em músicas?|Tem algum personagem famoso?|É símbolo de alguma coisa?|Tem uma data comemorativa?|
Tem mais de um metro?|Tem mais de dez metros?|Pesa mais de um quilo?|Pesa mais de cem quilos?|Pesa mais de uma tonelada?""")

CORES = L("branco|preto|vermelho|azul|verde|amarelo|laranja|rosa|roxo|marrom|cinza|dourado|prateado|bege|colorido|"
          "transparente|listrado|estampado|azul-claro|verde-escuro|vinho|creme|lilás|bronze|furta-cor")
CORES_T = ["Pode ser {}?", "Costuma ser {}?", "Tem alguma parte {}?"]

REFS = L("""uma formiga|uma moeda|um grão de arroz|um botão|um dado|uma borracha|um lápis|uma colher|um ovo|uma maçã|
uma laranja|uma banana|um celular|um controle remoto|uma xícara|um livro|um caderno|um sapato|uma garrafa|um tijolo|
uma bola de tênis|uma bola de futebol|uma melancia|um gato|um cachorro pequeno|um cachorro grande|um travesseiro|
uma mochila|uma cadeira|uma mesa|um violão|uma criança|uma pessoa adulta|uma bicicleta|uma porta|uma televisão|
uma geladeira|um sofá|uma cama|um fogão|uma moto|um cavalo|um carro|uma vaca|um elefante|uma árvore|uma casa|
um ônibus|um caminhão|uma piscina|uma baleia|um avião|um prédio|um navio|uma igreja|um estádio|uma montanha|uma cidade|
um mosquito|um pássaro|um rato|uma galinha|um coelho|um computador|um notebook|uma caixa de sapato|uma caixa de leite|
um saco de arroz de 5 quilos|uma mala de viagem|um balde|uma panela|um micro-ondas|uma máquina de lavar|um armário|
um guarda-roupa|um poste|um ponto de ônibus|uma barraca de praia|um trator|um trem|uma canoa|um barco|uma girafa|
um dinossauro|um tubarão|um golfinho|um urso|um leão|uma cobra|uma tartaruga|uma abelha|uma borboleta|um tablet|um relógio""")
REFS_T = ["É maior que {}?", "É menor que {}?", "É mais pesado que {}?", "É mais leve que {}?",
          "É mais caro que {}?", "É mais barato que {}?",
          "É mais comprido que {}?", "É mais fácil de encontrar que {}?"]

TEMAS = L("""futebol|vôlei|basquete|natação|corrida|ciclismo|Olimpíadas|Copa do Mundo|ginástica|tênis|skate|surfe|
xadrez|jogos de tabuleiro|videogame|cinema|teatro|televisão|novela|desenho animado|super-heróis|princesas|piratas|
dinossauros|robôs|astronautas|fantasmas|bruxas|magia|contos de fadas|circo|palhaços|música|samba|forró|sertanejo|
rock|carnaval|festa junina|Natal|Páscoa|Ano-Novo|Dia das Mães|Dia dos Pais|Dia das Crianças|aniversário|casamento|
batizado|formatura|férias|praia|campo|montanha|floresta|deserto|neve|chuva|sol|vento|tempestade|arco-íris|lua|
estrelas|planetas|foguetes|aviões|trens|navios|carros|motos|bicicletas|ônibus|estradas|cidade grande|interior|
fazenda|zoológico|aquário|museu|biblioteca|escola|universidade|hospital|farmácia|supermercado|feira|shopping|
restaurante|padaria|lanchonete|cozinha|churrasco|café da manhã|almoço de domingo|jantar|sobremesa|doces|salgados|
frutas|verduras|legumes|carne|peixe|leite|queijo|pão|bolo|chocolate|sorvete|pipoca|refrigerante|suco|café|chá|
água|fogo|terra|ar|gelo|metal|madeira|plástico|vidro|papel|tecido|pedra|areia|barro|ouro|dinheiro|banco|compras|
trabalho|escritório|computador|internet|celular|fotografia|redes sociais|tecnologia|ciência|laboratório|
medicina|dentes|olhos|ouvidos|nariz|mãos|pés|cabelo|pele|coração|sono|sonhos|banho|limpeza|roupas|sapatos|
chapéus|óculos|joias|maquiagem|perfume|moda|cores|desenho|pintura|escultura|artesanato|costura|jardinagem|
flores|árvores|plantas|sementes|animais de estimação|animais selvagens|aves|peixes|insetos|répteis|mamíferos|
oceano|rios|lagos|cachoeiras|ilhas|praias|vulcões|cavernas|polo norte|Amazônia|Pantanal|África|Ásia|Europa|
Estados Unidos|Japão|Itália|França|Portugal|Argentina|México|China|Índia|Egito|história|reis e rainhas|castelos|
cavaleiros|índios|vikings|samurais|pirâmides|guerra|paz|polícia|bombeiros|exército|leis|política|eleições|
religião|igreja|oração|anjos|bebês|crianças|adolescentes|idosos|família|amigos|vizinhos|professores|médicos|
segurança|perigo|medo|alegria|tristeza|amor|saudade|surpresa|preguiça|força|velocidade|silêncio|barulho|luz|
escuridão|calor|frio|cheiro|gosto|tato|visão|audição|matemática|números|letras|livros|poesia|jornal|notícias|
rádio|telefone|cartas|correio|presentes|brinquedos|bonecas|bolas|balões|pipas|fantasias|máscaras|festas|dança|
canto|instrumentos musicais|piano|violão|bateria|flauta|tambor|ferramentas|construção|pintura de paredes|
eletricidade|energia|lâmpadas|água encanada|esgoto|lixo|reciclagem|meio ambiente|poluição|sustentabilidade|
camping|pesca|caça|navegação|mergulho|escalada|viagem de avião|viagem de carro|hotel|turismo|mapas|bússola|
relógios|calendário|tempo|passado|futuro|invenções|ficção científica|mistério|detetives|aventura|esportes radicais|
academia|saúde|remédios|vacinas|primeiros socorros|ambulância|nutrição|dieta|cozinhar|receitas|temperos|
casa|quarto|banheiro|sala|quintal|garagem|jardim|varanda|telhado|móveis|decoração|eletrodomésticos|
café colonial|festa de criança|piquenique|parque|praça|feriado|domingo|segunda-feira|madrugada|pôr do sol|
nascer do sol|primavera|verão|outono|inverno""")
TEMAS_T = ["Tem relação com {}?", "Você associa com {}?", "Lembra {}?", "Aparece em histórias sobre {}?"]

MOMENTOS = L("""de manhã|à tarde|à noite|de madrugada|no verão|no inverno|na primavera|no outono|no Natal|na Páscoa|
no Carnaval|na festa junina|no Ano-Novo|nas férias|no fim de semana|em dias de chuva|em dias de sol|em aniversários|
em casamentos|na hora do almoço|na hora do jantar|antes de dormir|ao acordar|na escola|no trabalho|em viagens|
em feriados|em festas|em emergências|em dias de calor|em dias de frio|na hora do recreio|no domingo""")
MOMENTOS_T = ["É mais comum {}?", "Aparece mais {}?"]

PESSOAS = L("""crianças|bebês|adolescentes|idosos|mães|pais|avós|professores|médicos|cozinheiros|atletas|músicos|artistas|
estudantes|turistas|agricultores|motoristas|policiais|bombeiros|cientistas|astronautas|pescadores|marinheiros|
mecânicos|engenheiros|dentistas|veterinários|cabeleireiros|vendedores|jardineiros|pedreiros|enfermeiros|
pilotos|jogadores de futebol|bailarinos|palhaços|mágicos|escritores|fotógrafos|youtubers|padeiros|carteiros""")
PESSOAS_T = ["Faz parte do dia a dia de {}?", "{} costumam usar ou ver isso?"]

PRECOS = ["1","5","10","20","50","100","200","500","1.000","2.000","5.000","10.000","50.000","100.000","1 milhão"]
ANOS = ["10","50","100","200","500","1.000","2.000","10.000","1 milhão"]

# ---------------------------------------------------------------- ANIMAIS
A_PARTES = L("""penas|pelos|escamas|bico|casco|chifres|tromba|garras|juba|listras|manchas|asas|nadadeiras|bigodes|presas|
crina|carapaça|antenas|rabo comprido|rabo curto|rabo peludo|orelhas grandes|orelhas pequenas|olhos grandes|
pescoço comprido|pernas compridas|patas com cascos|dentes afiados|língua comprida|pelagem grossa|pele lisa|
couro duro|espinhos|ferrão|tentáculos|focinho comprido|bolsa na barriga|quatro patas|duas patas|seis patas|
oito patas|mais de oito patas|crista|papo|guelras|corcova|chocalho no rabo|cauda que segura galhos|pelo branco|
pelo preto|penas coloridas|cascos fendidos|unhas retráteis""")
A_HAB = L("""na floresta|no mar|em rios|em lagos|na savana|no deserto|no gelo|na fazenda|dentro de casa|em árvores|
debaixo da terra|nas montanhas|no Brasil|na África|na Ásia|na Europa|na Austrália|na Amazônia|no Pantanal|
na Antártida|no Ártico|em cavernas|em pântanos|na cidade|em zoológicos|em aquários|em ninhos|em tocas|em grupos|
sozinho|perto das pessoas|em colmeias|em formigueiros|em recifes de coral|no fundo do oceano|em praias|no cerrado|
na caatinga|em lugares frios|em lugares quentes""")
A_HAB_T = ["Vive {}?", "Pode ser encontrado {}?"]
A_COME = L("""capim|carne|peixe|insetos|frutas|folhas|sementes|ração|néctar|minhocas|ovos|grãos|plantas aquáticas|
outros animais|restos de comida|sangue|bambu|cenoura|banana|ratos|plâncton|algas|mel|raízes|cascas de árvore|
milho|feno|carniça|pássaros|cobras""")
A_HAB2 = L("""nadar|voar|correr muito rápido|pular alto|subir em árvores|cavar buracos|enxergar no escuro|imitar sons|
mudar de cor|ficar muito tempo sem beber água|respirar debaixo d'água|andar sobre duas patas|carregar peso|
ser treinado|fazer truques|botar ovos|hibernar|enrolar o corpo|soltar veneno|rugir|latir|cantar|planar|
ficar de cabeça para baixo|se camuflar|viver mais de 50 anos|dormir em pé|correr mais que um carro|
mergulhar fundo|soltar tinta|regenerar partes do corpo|fazer teia|produzir mel|produzir leite que bebemos|
dar lã|puxar carroça|ser montado|morder com força|picar|uivar|rastejar|saltar entre galhos|segurar coisas com as mãos""")
A_TRACOS = L("""um mamífero|uma ave|um réptil|um peixe|um inseto|um anfíbio|um aracnídeo|um crustáceo|um molusco|
herbívoro|carnívoro|onívoro|doméstico|selvagem|perigoso|venenoso|peludo|colorido|noturno|rápido|lento|barulhento|
silencioso|ameaçado de extinção|fofo|pequeno|gigante|comum no Brasil|um animal de estimação|
criado para dar alimento|usado para trabalho|um bicho de fazenda|um animal marinho|um animal de água doce|
um felino|um primata|um roedor|um canino|uma ave de rapina|um animal da savana|um animal da floresta|
um animal do frio|um animal do deserto|um animal que voa|um bicho que dá medo|um animal que vive em bando|
um animal de circo antigo|um animal de desenho animado famoso|o símbolo de algum time|mais ativo de dia""")
A_REFS = L("""uma formiga|uma abelha|um rato|um coelho|um gato|um cachorro|uma raposa|um lobo|um porco|uma ovelha|uma cabra|
uma vaca|um cavalo|um camelo|um urso|um leão|um tigre|uma girafa|um elefante|uma baleia|um golfinho|um tubarão|
uma tartaruga|um jacaré|uma cobra|um sapo|um pato|uma galinha|um papagaio|uma águia|uma coruja|um pinguim|
um avestruz|um macaco|um gorila|uma zebra|um hipopótamo|um rinoceronte|um canguru|um coala|um panda|uma onça|
uma capivara|um tamanduá|uma preguiça|um tatu|um peixinho dourado|uma lula|um polvo|um caranguejo|uma lagosta|
uma estrela-do-mar|um cavalo-marinho|uma minhoca|um caracol|uma borboleta|uma joaninha|um gafanhoto|um besouro|
uma aranha|um escorpião|uma barata|um mosquito|uma mosca|um morcego|um esquilo|um hamster|um porquinho-da-índia|
um ouriço|um castor|uma lontra|uma foca|uma morsa|um urso-polar|um pavão|um flamingo|uma arara|um tucano|
um beija-flor|um pombo|um pardal|um urubu|um gavião|uma gaivota|um peru|um ganso|um cisne|uma cegonha|um lagarto|
uma iguana|um camaleão|um crocodilo|um búfalo|um alce|um cervo|uma lhama|um burro|um javali|uma hiena|um guepardo|
uma pantera|um chimpanzé|um orangotango|um cupim|uma vespa|uma piranha|um salmão|uma enguia|uma água-viva|
um bicho-preguiça|um lobo-guará|um mico-leão-dourado|uma ema|um quati|uma anta|um tamanduá-bandeira|um boto""")
A_REFS_T = ["É maior que {}?", "É menor que {}?", "É mais rápido que {}?", "É mais pesado que {}?",
            "Vive mais tempo que {}?", "É parente de {}?", "É parecido com {}?", "É mais perigoso que {}?",
            "Come o mesmo que {}?", "Vive no mesmo lugar que {}?",
            "É mais barulhento que {}?", "É mais fofo que {}?"]

# ---------------------------------------------------------------- COMIDAS
C_TRACOS = L("""doce|salgado|azedo|amargo|apimentado|gelado|quente|crocante|cremoso|mole|duro|líquido|frito|assado|cozido|
cru|integral|industrializado|caseiro|saudável|calórico|barato|caro|vegetariano|vegano|típico do Brasil|estrangeiro|
uma fruta|um legume|uma verdura|um doce|um salgado|uma bebida|um prato principal|uma sobremesa|um lanche|
um petisco|um tempero|um grão|um tipo de pão|um tipo de carne|um laticínio|um tipo de massa|de origem animal|
de origem vegetal|vendido em feira|vendido em padaria|vendido em lanchonete|servido em festas|comido com as mãos|
comido com talheres|comido de colher|servido em prato|servido em copo|servido em tigela|redondo|comprido|pequeno|
grande|colorido|marrom|amarelo|vermelho|verde|branco|recheado|feito no forno|feito na panela|feito na frigideira|
feito na churrasqueira|vendido congelado|vendido em lata|vendido em caixinha|comido em fatias|comido em pedaços|
servido com molho|um prato típico de alguma região|um alimento de festa infantil|algo que crianças adoram""")
C_ING = L("""açúcar|sal|farinha de trigo|leite|ovo|queijo|manteiga|chocolate|carne|frango|peixe|tomate|cebola|alho|batata|
milho|arroz|feijão|mandioca|polvilho|fermento|creme de leite|leite condensado|coco|banana|limão|laranja|morango|
abacaxi|maçã|uva|canela|cravo|pimenta|orégano|azeite|óleo|vinagre|mel|castanhas|amendoim|presunto|bacon|
linguiça|camarão|alface|cenoura|beterraba|abóbora|couve|repolho|pepino|ervilha|grão-de-bico|aveia|café|
chá|gelo|iogurte|requeijão|maionese|ketchup|mostarda|molho de tomate|calabresa|carne moída|atum|sardinha|
palmito|azeitona|goiabada|doce de leite|granulado|coco ralado|gengibre|salsinha|cebolinha|manjericão|
fubá|tapioca|amido de milho|baunilha|frutas vermelhas|carne de porco|carne seca|leite de coco|dendê""")
C_ING_T = ["Leva {}?", "Combina com {}?"]
C_MOM = L("""no café da manhã|no almoço|no jantar|no lanche da tarde|em festas de aniversário|no Natal|na Páscoa|
na festa junina|no Carnaval|no Ano-Novo|em churrascos|na praia|no cinema|no estádio|na escola|em casamentos|
em piqueniques|em restaurantes|em lanchonetes|em padarias|na rua|no inverno|no verão|em dias de chuva|
quando alguém está doente|de madrugada|na sobremesa|como entrada|como acompanhamento|em viagens|no domingo|
em rodízios|em feiras|em quermesses""")
C_MOM_T = ["É comum comer ou beber {}?", "Aparece {}?"]
C_REFS = L("""um pão francês|uma maçã|uma uva|um morango|uma melancia|um abacaxi|uma laranja|um limão|um ovo|um bife|
um hambúrguer|um cachorro-quente|uma pizza|uma lasanha|um prato de macarrão|uma salada|uma sopa|um bolo|um pudim|
um brigadeiro|um sorvete|um chocolate|uma bala|um chiclete|uma pipoca|uma coxinha|uma empada|um pastel|uma esfiha|
um pão de queijo|uma tapioca|um cuscuz|um acarajé|uma feijoada|um churrasco|um sushi|um croissant|uma panqueca|
uma torrada|um biscoito|uma bolacha recheada|um pirulito|uma paçoca|uma pamonha|um curau|um quindim|uma cocada|
um beijinho|um pé de moleque|uma rapadura|uma batata frita|um purê de batata|um arroz-doce|uma canjica|um mingau|
um iogurte|um queijo|um presunto|uma salsicha|uma linguiça|um frango assado|um peixe frito|um camarão|
uma azeitona|um pepino|uma cenoura|um tomate|uma alface|um brócolis|uma couve-flor|uma abóbora|um milho|
uma batata-doce|uma mandioca|um feijão|uma lentilha|uma castanha|um amendoim|um coco|uma manga|um mamão|
uma goiaba|um maracujá|uma pera|um kiwi|uma cereja|uma jabuticaba|um açaí|um caju|um suco de laranja|um café|
um chá|um refrigerante|um copo de leite|um milk-shake|uma vitamina|um caldo de cana|uma água de coco|
um chocolate quente|uma gelatina|uma mousse|uma torta de limão|um pavê|um churros|um sonho de padaria|
uma rosquinha|um bolo de cenoura|um pão de mel|uma broa de milho|um misto-quente|um sanduíche natural|
um arroz com feijão|um ovo frito|uma omelete|um nhoque|um risoto|um estrogonofe|uma moqueca|um vatapá|
um baião de dois|um tutu de feijão|uma farofa|um pão com manteiga""")
C_REFS_T = ["É mais doce que {}?", "É mais salgado que {}?", "É maior que {}?", "É mais caro que {}?",
            "É mais calórico que {}?", "É mais saudável que {}?", "É parecido com {}?", "Combina com {}?",
            "É mais fácil de fazer que {}?", "É mais popular que {}?",
            "É servido junto com {}?", "Tem a mesma cor que {}?"]

# ---------------------------------------------------------------- OBJETOS
O_MAT = L("""metal|plástico|madeira|vidro|papel|tecido|borracha|couro|cerâmica|pedra|algodão|lã|espuma|ferro|alumínio|
ouro|prata|aço|cera|barro|porcelana|isopor|papelão|silicone|acrílico|bambu|palha|cortiça|concreto|nylon""")
O_MAT_T = ["É feito de {}?", "Tem alguma parte de {}?"]
O_LOC = L("""na cozinha|no banheiro|no quarto|na sala|na lavanderia|no quintal|na garagem|no escritório|na escola|
no hospital|na praia|no carro|na mochila|na bolsa|no bolso|na gaveta|no armário|na geladeira|em cima da mesa|
na parede|no teto|no chão|na rua|no parque|na fazenda|numa loja de ferramentas|numa papelaria|numa farmácia|
num supermercado|numa loja de eletrônicos|num escritório|numa sala de aula|numa oficina|num salão de beleza|
numa loja de brinquedos|num restaurante""")
O_LOC_T = ["Fica {}?", "Dá para encontrar {}?"]
O_USO = L("""cortar|escrever|limpar|cozinhar|guardar coisas|iluminar|aquecer|esfriar|medir|pesar|proteger|
se comunicar|se divertir|estudar|trabalhar|se vestir|dormir|sentar|carregar coisas|abrir algo|fechar algo|
consertar coisas|enfeitar|brincar|tocar música|ouvir música|assistir a vídeos|fotografar|se locomover|
se exercitar|lavar|secar|passar roupa|pentear o cabelo|cuidar dos dentes|se maquiar|beber|comer|servir comida|
misturar|furar|pendurar coisas|amarrar|colar|apagar|desenhar|pintar|contar o tempo|enxergar melhor|
se proteger da chuva|se proteger do sol|descansar|jogar|organizar|segurar coisas|cobrir|abanar|tirar sujeira""")
O_PROPS = L("""Usa eletricidade?|Precisa ficar na tomada?|Usa pilha ou bateria?|Tem tela?|Tem botões?|Tem fio?|
Tem lâmina?|Tem ponta?|Tem cabo?|Tem alça?|Tem tampa?|Tem porta?|Tem gaveta?|Tem rodinhas?|Tem pernas?|
Tem motor?|Faz barulho quando funciona?|Esquenta quando usa?|Tem luz?|Tem espelho?|Tem lente?|Tem ponteiros?|
Tem teclas?|Tem cordas?|Tem cerdas?|Tem zíper?|Dá para usar no corpo?|Dá para vestir?|Dá para levar no bolso?|
Dá para carregar com uma mão?|Precisa de duas pessoas para carregar?|É um eletrodoméstico?|É um móvel?|
É uma ferramenta?|É um brinquedo?|É um utensílio de cozinha?|É uma roupa ou acessório?|É um aparelho eletrônico?|
É material escolar?|É um meio de transporte?|É um item de higiene?|É um instrumento musical?|É decorativo?|
É descartável?|Dura muitos anos?|Tem em quase toda casa?|Crianças podem usar sozinhas?|Precisa de cuidado para usar?|
Pode quebrar se cair?|Pode molhar?|Dá para lavar?|Dobra?|Abre e fecha?|Tem vários tamanhos?|Tem várias cores?|
Pode ser antigo de família?|Dá para fazer em casa?|Precisa de manual?|Fica pendurado?|Fica no chão?""")
O_REFS = L("""uma caneta|um lápis|uma borracha|um caderno|um livro|uma tesoura|uma colher|um garfo|uma faca|um prato|
um copo|uma panela|uma frigideira|uma chaleira|uma geladeira|um fogão|um micro-ondas|um liquidificador|
uma batedeira|uma torradeira|um ventilador|um ar-condicionado|uma televisão|um controle remoto|um celular|
um computador|um notebook|um tablet|um fone de ouvido|uma caixa de som|uma câmera|um relógio|um despertador|
uma lâmpada|uma lanterna|uma vela|um espelho|uma escova de cabelo|um pente|uma escova de dentes|uma toalha|
um sabonete|um travesseiro|um cobertor|uma cama|um sofá|uma cadeira|uma mesa|um armário|uma estante|um tapete|
uma cortina|um quadro|um vaso de flores|uma mochila|uma bolsa|uma carteira|uma chave|um cadeado|um guarda-chuva|
um chapéu|um boné|um par de óculos|um sapato|um chinelo|uma meia|uma camiseta|uma jaqueta|um cachecol|uma luva|
uma bola|uma boneca|um carrinho de brinquedo|um videogame|um quebra-cabeça|um dado|um baralho|um balão|uma pipa|
uma bicicleta|um skate|um patinete|um carro|uma moto|um martelo|uma chave de fenda|um alicate|uma furadeira|
uma serra|uma escada|um balde|uma vassoura|um rodo|um pano de chão|um aspirador de pó|uma máquina de lavar|
um ferro de passar|um varal|um prendedor de roupa|uma agulha|um botão|um zíper|uma fita adesiva|uma cola|
um grampeador|um clipe|uma régua|um calendário|uma moeda|uma nota de dinheiro|um cartão de crédito|uma garrafa|
uma caixa de papelão|um saco plástico|um cesto de lixo|um extintor|uma mangueira|um regador|uma tomada|
um carregador de celular|um pendrive|um violão|um piano|um microfone|uma mala""")
O_REFS_T = ["É maior que {}?", "É menor que {}?", "É mais pesado que {}?", "É mais caro que {}?",
            "É mais antigo que {}?", "É usado junto com {}?", "É parecido com {}?", "Fica perto de {} em casa?",
            "Dura mais que {}?", "É mais usado que {}?",
            "É feito do mesmo material que {}?", "Faz mais barulho que {}?"]

# ---------------------------------------------------------------- PROFISSÕES
P_BASE = L("""Usa uniforme?|Usa jaleco?|Usa capacete?|Usa luvas?|Usa máscara?|Precisa de faculdade?|Estuda muitos anos?|
Trabalha sentado?|Trabalha em pé?|Anda muito no trabalho?|Trabalha sozinho?|Trabalha em equipe?|
Atende pessoas?|Trabalha com o público?|Ganha bem?|É uma profissão perigosa?|Salva vidas?|Ajuda pessoas doentes?|
Ensina coisas?|Cria coisas?|Conserta coisas?|Constrói coisas?|Vende coisas?|Cuida de alguém?|Protege as pessoas?|
Aparece na televisão?|Fica famoso às vezes?|Viaja a trabalho?|Trabalha de madrugada?|Faz plantão?|
Trabalha em feriados?|Usa as mãos o tempo todo?|Precisa de força física?|Precisa ser criativo?|
Precisa saber matemática?|Precisa falar bem?|Precisa de coragem?|Precisa de paciência?|Precisa de carteira de motorista?|
Existe há séculos?|É uma profissão nova?|Crianças sonham com ela?|Tem em toda cidade?|Trabalha para o governo?|
Pode ter o próprio negócio?|Usa computador o dia todo?|Usa ferramentas?|Usa veículo no trabalho?|Trabalha com as mãos sujas?|
Trabalha com barulho?|Trabalha em silêncio?|Usa avental?|Usa apito?|Usa microfone?|Escreve muito?|Lê muito?|
Fala outro idioma?|Faz exercício no trabalho?|Mexe com comida?|Mexe com dinheiro?|Mexe com remédios?|
Mexe com animais?|Mexe com plantas?|Mexe com fogo?|Mexe com eletricidade?|Mexe com água?|Usa tinta?|
Tem um dia comemorativo?|Aparece em desenhos infantis?|Tem um chefe?|Dá ordens?|Faz provas ou testes nos outros?""")
P_LOCAIS = L("""num hospital|numa escola|num escritório|na rua|ao ar livre|numa fábrica|numa loja|num restaurante|
numa fazenda|num laboratório|num aeroporto|num navio|no mar|numa obra|num estúdio|num teatro|num estádio|
num tribunal|numa delegacia|num quartel|numa clínica|numa farmácia|num banco|num salão de beleza|numa oficina|
num supermercado|numa biblioteca|num museu|numa igreja|num hotel|num zoológico|numa floresta|numa mina|
numa usina|numa emissora de TV|numa rádio|num jornal|numa padaria|numa academia|numa creche|numa universidade|
em casa|em vários lugares diferentes|dentro de um veículo|nas alturas|debaixo da terra|à noite|
nos fins de semana|em feriados|no espaço|num circo|numa piscina|num consultório|num canteiro de obras|num cartório""")
P_FERR = L("""computador|caneta|tesoura|martelo|pincel|faca|panela|estetoscópio|seringa|microfone|câmera|volante|
mangueira|escada|capacete|luvas|máscara|jaleco|avental|apito|bola|livro|lousa|calculadora|telefone|rádio|
algemas|balança|régua|fita métrica|agulha|linha|tinta|pá|enxada|trator|avião|barco|caminhão|ônibus|bicicleta|
moto|carro|instrumento musical|prancheta|lupa|microscópio|telescópio|mapa|bússola|chave|tesoura de poda|
secador de cabelo|pente|espelho|furadeira|serrote|chave inglesa|vassoura|uniforme camuflado|crachá|carimbo""")
P_FERR_T = ["Usa {} no trabalho?"]
P_COM = L("""crianças|idosos|bebês|animais|plantas|dinheiro|comida|roupas|números|palavras|música|esporte|arte|
computadores|máquinas|carros|doentes|criminosos|turistas|alunos|clientes|pacientes|documentos|leis|construções|
eletricidade|água|fogo|madeira|metal|tecidos|cabelos|dentes|olhos|pés|notícias|imagens|vídeos|livros|cartas|
encomendas|remédios|vacinas|sementes|gado|peixes|foguetes|aviões|navios|trens|estradas|prédios|casas|
jardins|festas|casamentos|viagens|segurança|limpeza|saúde|beleza|moda|jogos|ciência|história|planetas""")
P_COM_T = ["Trabalha com {}?"]
P_REFS = L("""um médico|um enfermeiro|um dentista|um veterinário|um farmacêutico|um professor|um diretor de escola|
um bombeiro|um policial|um soldado|um advogado|um juiz|um engenheiro|um arquiteto|um pedreiro|um eletricista|
um encanador|um carpinteiro|um pintor de paredes|um mecânico|um motorista de ônibus|um taxista|um caminhoneiro|
um piloto de avião|um comissário de bordo|um marinheiro|um pescador|um agricultor|um jardineiro|um cozinheiro|
um garçom|um padeiro|um confeiteiro|um açougueiro|um feirante|um vendedor|um caixa de supermercado|
um gerente de banco|um contador|um jornalista|um fotógrafo|um ator|um cantor|um músico|um dançarino|um palhaço|
um mágico|um escritor|um desenhista|um programador|um cientista|um astronauta|um biólogo|um químico|
um matemático|um arqueólogo|um bibliotecário|um carteiro|um entregador|um faxineiro|um porteiro|um segurança|
um cabeleireiro|um barbeiro|uma manicure|um costureiro|um estilista|um modelo|um jogador de futebol|
um técnico de futebol|um árbitro|um professor de educação física|um nadador|um personal trainer|um psicólogo|
um fisioterapeuta|um nutricionista|um padre|um prefeito|um guia turístico|um recepcionista|um tradutor|
um detetive|um salva-vidas|uma babá|um maquinista de trem|um apresentador de TV|um youtuber|um professor universitário|
um sapateiro|um chaveiro|um vidraceiro|um soldador|um operário de fábrica|um motoboy|um frentista|um tratorista""")
P_REFS_T = ["Ganha mais que {}?", "Estuda mais que {}?", "Trabalha mais horas que {}?",
            "Tem um trabalho mais perigoso que {}?", "É uma profissão mais antiga que {}?", "Trabalha junto com {}?",
            "É parecido com o trabalho de {}?", "É mais conhecido que {}?", "Usa uniforme parecido com o de {}?",
            "Trabalha no mesmo lugar que {}?",
            "Ajuda o trabalho de {}?", "Precisa de mais coragem que {}?"]

# ---------------------------------------------------------------- LUGARES
L_BASE = L("""É ao ar livre?|É um lugar fechado?|É público?|É particular?|Precisa pagar para entrar?|Precisa de ingresso?|
Abre todos os dias?|Abre à noite?|Funciona 24 horas?|Fica cheio nos fins de semana?|É silencioso?|É barulhento?|
É grande?|É pequeno?|Tem em toda cidade?|Só existe em cidades grandes?|Fica na natureza?|Foi construído pelo ser humano?|
Tem água por perto?|Tem árvores?|Tem animais?|Tem funcionários?|Tem uniforme para quem trabalha lá?|É bom para crianças?|
Idosos frequentam?|É perigoso?|É divertido?|É romântico?|É turístico?|Vai gente de outros países?|É histórico?|
É moderno?|Tem comida para comprar?|Tem banheiro?|Tem estacionamento?|Tem fila?|Tem segurança na porta?|
Precisa de roupa especial?|Vai de chinelo?|Vai a pé normalmente?|Precisa de carro para chegar?|É longe da cidade?|
Fica no centro?|Você vai toda semana?|Você foi esta semana?|Você vai nas férias?|Dá para passar o dia todo?|
Dá para dormir lá?|Dá para morar lá?|Pode levar animais?|Tem música?|Tem luz forte?|É escuro?|É quente?|É frio?|
É molhado?|Tem areia?|Tem grama?|Tem cadeiras?|Tem palco?|Tem tela?|Tem prateleiras?|Vende coisas?|Ensina coisas?|
Cuida de pessoas?|Tem horário marcado?|Faz parte da rotina das crianças?|Aparece em filmes?|Tem cheiro característico?""")
L_ATV = L("""nadar|comer|dormir|estudar|comprar coisas|assistir a algo|dançar|rezar|correr|brincar|trabalhar|tomar sol|
pescar|andar de bicicleta|fazer piquenique|ver animais|ler|fazer exercícios|ouvir música|tirar fotos|
andar de barco|acampar|escalar|se tratar|pegar um avião|pegar um ônibus|pegar um trem|abastecer o carro|
cortar o cabelo|tomar banho|cozinhar|lavar roupa|votar|casar|aprender|jogar bola|andar a cavalo|
fazer compras de mercado|tomar café|beber água de coco|ver um show|ver um jogo|ver um filme|visitar exposições|
plantar|colher frutas|encontrar amigos|ficar em silêncio|gritar|usar biquíni|usar casaco|ver neve|
ver estrelas|ver o pôr do sol|andar descalço|entrar de graça|ir sozinho|levar o cachorro|comemorar aniversário""")
L_ATV_T = ["Dá para {} lá?"]
L_TEM = L("""areia|água|árvores|cadeiras|mesas|camas|luzes coloridas|música|animais|livros|computadores|carros|
prateleiras|caixas registradoras|filas|portões|escadas rolantes|elevadores|banheiros|janelas grandes|teto alto|
palco|tela grande|pista|grama|flores|bancos|barracas|guarda-sóis|lixeiras|seguranças|médicos|professores|
vendedores|turistas|crianças|idosos|bebês|uniformes|placas|mapas|catracas|ingressos|cardápio|balcão|vitrines|
estacionamento|piscina|quadra|jardim|sino|altar|esteira|carrinhos|macas|lousa|fogão|forno|ondas|pedras|
brinquedos|jaulas|torres|bandeiras""")
L_TEM_T = ["Tem {} lá?"]
L_FICA = L("""na cidade|no campo|perto do mar|nas montanhas|perto de rios|dentro de shoppings|no centro da cidade|
em bairros residenciais|em cidades pequenas|no Brasil todo|em outros países|debaixo da terra|no alto|
perto de estradas|perto de escolas|perto de hospitais|em ilhas|em florestas|no litoral|no interior|
em lugares frios|em lugares quentes|dentro de um prédio|em ruas movimentadas|em lugares calmos|em parques|
perto de aeroportos|perto de igrejas|em condomínios|em avenidas""")
L_FICA_T = ["Fica {}?"]
L_REFS = L("""uma casa|um apartamento|uma escola|uma universidade|um hospital|uma farmácia|um posto de saúde|
um supermercado|uma padaria|um açougue|uma feira|um shopping|uma loja de roupas|uma livraria|uma papelaria|
um banco|uma agência dos Correios|uma delegacia|um quartel de bombeiros|uma prefeitura|um tribunal|uma igreja|
um cemitério|um museu|um teatro|um cinema|uma biblioteca|um estádio|um ginásio|uma academia|uma piscina|
um clube|um parque|uma praça|um jardim botânico|um zoológico|um aquário|um parque de diversões|um circo|
uma praia|uma ilha|uma montanha|uma floresta|um rio|uma cachoeira|um lago|um deserto|uma caverna|um vulcão|
uma fazenda|um sítio|um acampamento|um hotel|uma pousada|um restaurante|uma lanchonete|uma sorveteria|
uma pizzaria|uma cafeteria|um aeroporto|uma rodoviária|uma estação de trem|uma estação de metrô|um porto|
um posto de gasolina|um estacionamento|uma oficina mecânica|uma fábrica|um escritório|um laboratório|
uma usina|uma mina|um navio|um castelo|um palácio|uma prisão|um farol|uma torre|uma ponte|um túnel|
um salão de beleza|uma barbearia|uma lavanderia|um pet shop|uma clínica veterinária|um consultório de dentista|
uma creche|uma loja de brinquedos|uma loja de ferramentas|uma floricultura|um mercado municipal|um condomínio|
uma quadra de esportes|um parquinho|uma sala de aula|uma cozinha|um quintal""")
L_REFS_T = ["É maior que {}?", "É mais barulhento que {}?", "É mais visitado que {}?", "É parecido com {}?",
            "É mais antigo que {}?", "É mais caro de frequentar que {}?", "Costuma ficar perto de {}?",
            "É mais cheio que {}?", "Tem mais gente trabalhando que {}?", "É mais divertido que {}?",
            "É mais silencioso que {}?", "Fica aberto mais tempo que {}?"]

# ---------------------------------------------------------------- OBRAS E PERSONAGENS
OBRA = L("""É um filme?|É um desenho animado?|É uma série?|É uma novela?|É brasileiro?|É americano?|É japonês?|
É da Disney?|É da Pixar?|É para crianças pequenas?|É para adultos?|É de comédia?|É de terror ou suspense?|
É de aventura?|É de romance?|É de ficção científica?|É musical?|Tem músicas famosas?|Foi lançado antes do ano 2000?|
Foi lançado depois de 2010?|Tem continuação?|Virou desenho e filme?|Começou nos quadrinhos ou gibis?|Começou num livro?|
Começou num videogame?|O protagonista é humano?|O protagonista é um animal?|O protagonista é um brinquedo ou robô?|
O protagonista é criança?|O protagonista é adolescente?|A protagonista é mulher?|Tem princesa?|Tem super-heróis?|
Tem magia?|Tem monstros?|Tem animais falantes?|Tem um vilão famoso?|Se passa no espaço?|Se passa no mar?|
Se passa numa escola?|Se passa numa cidade grande?|Se passa no passado?|Se passa no futuro?|Tem muita luta?|
Tem família como tema?|Tem amizade como tema?|É em preto e branco ou muito antigo?|Passou na TV aberta no Brasil?|
Passou no SBT?|Passou na Globo?|Está em streaming?|Ganhou muitos prêmios?|É engraçado?|Faz chorar?|
A família toda pode assistir?|Os personagens são amarelos ou coloridos?|Tem dinossauros?|Tem carros?|Tem comida como tema?""")
PERSONAGEM = L("""É humano?|É homem?|É mulher?|É criança?|É velho?|É um animal?|É um monstro ou criatura?|É do bem?|É vilão?|
Tem superpoderes?|Voa?|Usa capa?|Usa máscara?|Usa coroa?|Usa chapéu?|É rico?|É da realeza?|É uma princesa?|
É uma bruxa ou feiticeiro?|É do folclore brasileiro?|É de um conto de fadas?|É da Marvel?|É da DC?|É da Disney?|
Aparece em filmes?|Aparece em desenhos?|Aparece em livros?|Faz parte de uma equipe?|Tem um parceiro famoso?|
Tem um inimigo famoso?|Mora num castelo?|Mora na floresta?|Mora na cidade?|Mora no mar ou nos rios?|
Veio de outro planeta?|É muito forte?|É muito rápido?|É inteligente?|É engraçado?|Dá medo?|Assusta crianças?|
Ajuda as pessoas?|Usa uma arma ou objeto especial?|Tem cor verde?|Tem cor vermelha?|Tem cor azul?|Aparece à noite?|
Tem ligação com o Natal ou a Páscoa?|Tem um animal de estimação?|Tem uma história de amor?""")
VIVO_EXTRA = L("""Vive na água?|Voa?|Tem pelos?|Tem penas?|Tem escamas?|Tem quatro patas?|Bota ovos?|É doméstico?|É selvagem?|
Come carne?|Come plantas?|É maior que um cachorro?|É menor que um gato?|Vive no Brasil?|Vive na África?|Dá para ter em casa?|
Vive na fazenda?|É perigoso?|É venenoso?|Faz barulho?|É noturno?|Vive em grupo?|É colorido?|É lento?|É rápido?""")

# ---------------------------------------------------------------- montagem (banco enxuto)
seen = set()
def uniq(lst):
    out = []
    for q in lst:
        k = q.lower()
        if k in seen: continue
        seen.add(k); out.append(q)
    return out

data = {
  'geral': uniq(GERAL_BASE + [f"Pode ser {c}?" for c in CORES[:12]] + [f"Custa mais que R$ {v}?" for v in ["10","100","1.000"]]),
  'vivo': uniq(VIVO_EXTRA + [f"É {t}?" for t in A_TRACOS] + [f"Tem {p}?" for p in A_PARTES[:30]] + [f"Vive {h}?" for h in A_HAB[:20]]),
  'comida': uniq([f"É {t}?" for t in C_TRACOS] + [f"Leva {i}?" for i in C_ING[:30]] + [f"É comum {m}?" for m in C_MOM[:15]]),
  'objeto': uniq(O_PROPS + [f"É feito de {m}?" for m in O_MAT[:15]] + [f"Fica {l}?" for l in O_LOC[:20]] + [f"Serve para {u}?" for u in O_USO[:30]]),
  'pessoa': uniq(P_BASE + [f"Trabalha {l}?" for l in P_LOCAIS[:25]]),
  'lugar': uniq(L_BASE + [f"Dá para {a} lá?" for a in L_ATV[:25]] + [f"Fica {x}?" for x in L_FICA[:15]]),
  'obra': uniq(OBRA),
  'personagem': uniq(PERSONAGEM),
}
total = sum(len(v) for v in data.values())
for k, v in data.items(): print(f"{k:11s} {len(v):5d}")
print(f"{'TOTAL':11s} {total:5d}")

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(here, 'perguntas.js'), 'w', encoding='utf-8') as f:
    f.write("/* Banco de perguntas prontas (%d). Gerado por tools/gerar_perguntas.py.\n" % total)
    f.write("   'geral' vale para qualquer item; os outros grupos aparecem conforme a categoria do item. */\n")
    f.write("window.PERGUNTAS = ")
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";\n")
