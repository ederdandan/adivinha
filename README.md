# ❓ Adivinha o que é

Jogo de dedução para família e amigos, jogado no navegador do celular. Cada jogador recebe um **item secreto** e tenta descobrir os itens dos outros com perguntas de Sim/Não, dicas e palpites.

- 👨‍👩‍👧‍👦 De 2 a 4 jogadores, cada um no próprio celular
- 🔗 Sala com código, link e QR code para compartilhar
- 🙅 Sem cadastro, sem servidor e sem custo
- 📸 Foto de perfil para cada jogador
- 🃏 1.000 itens em 25 categorias (filmes, desenhos, comidas, animais, super-heróis…), cada um com 4 dicas
- 🎚️ Níveis Fácil e Médio
- ❓ 800 perguntas prontas, com busca e sugestões que combinam com o item
- 📱 Funciona em celular, tablet e computador, com tema claro e escuro

---

## Como jogar

1. O **anfitrião** abre o site, escolhe uma foto (opcional), digita o nome e toca em **Criar sala**.
2. Ele compartilha o link (WhatsApp, cópia ou QR code).
3. Os outros abrem o link, digitam o nome e entram.
4. O anfitrião escolhe a categoria (ou "Tudo misturado") e a dificuldade, e toca em **Começar partida**.

### Regras

| | |
|---|---|
| **Item secreto** | Cada jogador recebe um item sorteado. A categoria do item é visível para todos. No modo "Tudo misturado", cada jogador recebe uma categoria diferente. |
| **Na sua vez** | Escolha **uma** ação: ❓ **Perguntar**, 💡 **Usar dica** ou 🎯 **Palpite**. |
| **Perguntar** | Busque uma das 800 perguntas prontas, toque numa sugestão ou escreva a sua. O dono do item responde **Sim**, **Não** ou **Não sei**. |
| **Usar dica** | Revela uma dica sobre o item de um oponente. Cada jogador pode usar **2 dicas** por partida. Cada item tem 4 dicas, da mais vaga para a mais reveladora. |
| **Palpite certo** | Você ganha **1 ponto**, e o item do oponente é revelado. |
| **Palpite errado** | **Dica Forçada**: uma dica sobre o *seu* item é revelada para todos. |
| **Espectador Ativo** | Quem teve o item descoberto continua jogando: pergunta, usa dicas e dá palpites. |
| **Fim de jogo** | Quando restam **2 itens** sem descobrir (com 2 jogadores, quando resta 1). Vence quem tiver mais pontos. |
| **Histórico** | Todas as perguntas, respostas, dicas e palpites ficam visíveis para todos. |

---

## Publicar de graça no GitHub Pages

1. Crie um repositório **público** no GitHub (ex.: `adivinha`).
2. Envie o `index.html`, o `perguntas.js` e a pasta **`itens`** inteira (**Add file → Upload files**, arrastando a pasta junto, e depois **Commit changes**). A pasta `tools/` é opcional.
3. Vá em **Settings → Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)`, e clique em **Save**.
4. Em 1 ou 2 minutos o site estará em `https://SEU-USUARIO.github.io/adivinha/`.

O passo a passo detalhado está em [`COMO_PUBLICAR.md`](COMO_PUBLICAR.md).

---

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `index.html` | O jogo: telas, regras e conexão entre os celulares. |
| `perguntas.js` | 800 perguntas prontas, separadas por tipo de item (geral, seres vivos, comidas, objetos, lugares, filmes, personagens…). |
| `itens/categorias.js` | Lista das 25 categorias. |
| `itens/<categoria>.json` | Os itens de cada categoria, com 4 dicas cada. |
| `tools/itens/*.txt` | **Onde você edita os itens e as dicas** (texto simples). |
| `tools/gerar_itens.py` | Confere os itens e gera a pasta `itens/`. |
| `tools/gerar_perguntas.py` | Gera o `perguntas.js`. |

## Adicionar ou mudar itens

Os itens ficam em `tools/itens/*.txt`, um por linha:

```
Nome | nível | dica 1 | dica 2 | dica 3 | dica 4 | apelidos;separados;por;ponto-e-vírgula
Cachorro | f | É um mamífero que vive com as pessoas. | Abana o rabo quando está feliz. | É chamado de melhor amigo do homem. | Late. | Cão;Cachorrinho
```

- **Nível:** `f` (fácil), `m` (médio) ou `d` (difícil).
- **Dicas:** da mais vaga para a mais reveladora. Todas precisam ser verdadeiras e nenhuma pode conter o nome do item.
- **Apelidos (opcional):** outros nomes aceitos no palpite. Por exemplo, "Mandioca" aceita "Aipim" e "Macaxeira".
- Para criar uma categoria nova, adicione uma linha de título: `# chave | Nome da categoria | 🙂 | grupo`. O grupo escolhe as perguntas sugeridas: `geral`, `vivo`, `comida`, `objeto`, `pessoa`, `lugar`, `obra` ou `personagem`.

Depois rode:
```bash
python3 tools/gerar_itens.py
```
O script avisa se alguma dica entrega o nome do item ou se há itens repetidos, e gera a pasta `itens/`. Envie a pasta atualizada para o GitHub.

### Categorias (40 itens cada)

Animais, Comidas, Doces e sobremesas, Bebidas, Frutas e legumes, Objetos da casa, Brinquedos e brincadeiras, Roupas e acessórios, Profissões, Lugares, Países e cidades, Meios de transporte, Esportes, Instrumentos musicais, Natureza e clima, Corpo humano, Tecnologia, Ciência e espaço, Escola, Festas e datas, Filmes, Desenhos animados, Séries e novelas, Contos, lendas e folclore, Super-heróis e vilões.

### Outras configurações (no `index.html`)

- **`MAX_HINTS`**: quantas dicas cada jogador pode usar por partida (padrão: 2).
- **`QUESTIONS`**: lista curta de perguntas, usada só se o `perguntas.js` não carregar.

---

## Como funciona por dentro

- HTML, CSS e JavaScript puros, sem etapa de build.
- **Leve:** o celular só baixa os itens das categorias sorteadas na partida (cerca de 8 KB cada). As perguntas ocupam 17 KB.
- Os aparelhos se conectam diretamente por **WebRTC**, usando a biblioteca [PeerJS](https://peerjs.com/) e o servidor de sinalização gratuito dela.
- O celular do **anfitrião** guarda o estado da partida e envia a cada jogador apenas o que ele pode ver. Os itens dos outros ficam ocultos até serem descobertos.
- O estado é salvo no navegador do anfitrião. Se ele recarregar a página, a partida é recuperada e os outros jogadores reconectam sozinhos.
- As fotos de perfil são reduzidas para 160×160 pixels no próprio celular e enviadas pela conexão da sala. Não há banco de dados: cada aparelho guarda a própria foto no navegador.
- O QR code é gerado com [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator).

## Limitações conhecidas

- Se o anfitrião **fechar** o site, a sala é encerrada.
- Abrir o `index.html` direto do computador (clicando duas vezes no arquivo) não funciona, porque o navegador bloqueia a leitura da pasta `itens`. Use o site publicado no GitHub Pages.
- É preciso internet para conectar, mesmo com todos no mesmo lugar.
- Algumas redes muito restritas (corporativas ou certas operadoras móveis) podem bloquear a conexão direta. Se alguém não conseguir entrar, coloquem todos no mesmo Wi‑Fi.
- Se alguém sair durante a partida, o anfitrião pode usar **Pular a vez**.

---

Feito para brincar em família. 🎲
