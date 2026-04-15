# T1_ProcessComunication — TCP & UDP (Sistemas Distribuídos)

Trabalho 1 da cadeira de **Sistemas Distribuídos** focado em **comunicação por sockets** e **troca de fluxos de bytes** entre **cliente e servidor**, com implementação em **Java (servidor)** e **Python (cliente)**.

O projeto implementa um “serviço remoto” comu um **Mural de PixelArt Colaborativo**: o cliente desenha pixels e envia atualizações ao servidor, enquanto o servidor mantém o estado do **Board** e faz **broadcast** das alterações para todos os clientes conectados via **TCP** e também suporta **UDP**.

---

## 1) Serviço remoto escolhido e modelagem

### Serviço remoto (sugestão aplicada)
Um serviço de “quadro de pixels” (board) que permite:
- representar um **Pixel** (posição e cor),
- representar um **Board** (matriz de cores),

### POJOs (representações de dados)

#### `Pixel`
- **Java:** `src/main/java/br/com/sd/entitys/Pixel.java`
- **Python:** `pyapp/entitys/pixel.py`

Atributos (mínimo exigido: 3 atributos):
- `x` (int)
- `y` (int)
- `color` (int)

#### `Board`
- **Java:** `src/main/java/br/com/sd/entitys/Board.java`
- **Python:** `pyapp/entitys/board.py`

Representa o estado completo do quadro:
- `width`, `height`
- `grid` (matriz de inteiros com cores)

### Classes de modelo (implementam serviços)

- **`BoardService`**: `src/main/java/br/com/sd/services/BoardService.java`  
  (criação/carregamento de Board e atualização de Pixel validando limites)

No lado Python, existe:
- **`BoardService`**: `pyapp/services/boardService.py` (serviço equivalente)

Essas classes cumprem o papel de **camada de modelo/serviço**, separando:
- regras (validação, atualização),
- de estruturas puras de dados (POJOs).

---

## 2) `PojoEscolhidoOutputStream`: OutputStream para transmitir POJOs (TCP/arquivo/console)

### Implementação: `PixelOutputStream`
O POJO escolhido foi o **Pixel**, e ele foi “transformado” em um stream de saída:

- **Java:** `src/main/java/br/com/sd/streams/PixelOutputStream.java` (extends `OutputStream`)
- **Python (equivalente):** `pyapp/streams/pixelOutputStream.py`

#### Regras
O construtor recebe:
1. **array/lista de objetos** (`Pixel[]` / `list[Pixel]`)
2. **número de objetos** (`quantidade`)
3. envio de dados de **pelo menos 3 atributos** (no caso: `x`, `y`, `color`)
4. **OutputStream de destino** (`OutputStream out` / arquivo/socket/stdout)

#### Formato (serialização manual em bytes)
A serialização foi feita “na mão”, em **big-endian**, usando 4 bytes por inteiro:

- Primeiro envia: `quantidade` (int, 4 bytes)
- Para cada Pixel:
  - `x` (int, 4 bytes)
  - `y` (int, 4 bytes)
  - `color` (int, 4 bytes)

Isso atende a ideia do trabalho: **empacotar** dados em bytes antes de enviar por stream (TCP/arquivo/etc).

#### Como testar (exemplos)
- **Saída padrão:** passar `System.out` no Java
- **Arquivo:** usar `FileOutputStream`
- **Servidor remoto TCP:** usar `Socket.getOutputStream()`

No projeto, o envio para servidor TCP aparece no fluxo real do cliente/servidor (ver seção TCP abaixo).

---

## 3) `PojoEscolhidoInputStream`: InputStream para ler os bytes gerados

### Implementação: `PixelInputStream`
- **Java:** `src/main/java/br/com/sd/streams/PixelInputStream.java` (extends `InputStream`)
- **Python (equivalente):** `pyapp/streams/pixelInputStream.py`

#### Regras do enunciado
- Construtor recebe um `InputStream` de origem
- Lê os bytes na mesma ordem do `PixelOutputStream`:
  - lê `quantidade`
  - reconstrói `Pixel[]`/lista lendo `x`, `y`, `color` como inteiros (4 bytes)

#### Como testar
- **Entrada padrão:** `System.in`
- **Arquivo:** `FileInputStream`
- **Servidor remoto TCP:** `Socket.getInputStream()`

---

## 4) Serviço remoto via cliente-servidor com sockets TCP (fluxos de bytes)

### Visão geral do TCP (unicast)
A comunicação principal implementada é **TCP**, trocando **fluxos de bytes**:

- **Servidor Java (TCP):** `src/main/java/br/com/sd/tests/ServerTCP.java`
- **Cliente Python (TCP):** `pyapp/streams/pixelHubSocketTCP.py` + `pyapp/main.py`

### Visão geral do UDP (multicast)
A comunicação principal implementada é **UDP**, trocando **fluxos de bytes**:

- **Servidor Java (TCP):** `src/main/java/br/com/sd/tests/ServerTCP.java`
- **Cliente Python (TCP):** `pyapp/streams/pixelHubSocketUDP.py` + `pyapp/main.py`

#### O que o servidor faz (Java)
1. Cria um `ServerSocket` na porta `5000`
2. Aceita múltiplos clientes, cria uma thread por cliente e uma thread para atualizar o board(**multi-threaded**)
3. Ao conectar:
   - envia o **Board completo** para o cliente (via `BoardOutputStream`)
   - entra em loop lendo **pixels** do cliente (via `PixelInputStream`)
4. Mantém um buffer concorrente (`tickBuffer`) e faz “tick”:
   - aplica pixels no `BoardService`
   - faz **broadcast** das mudanças para todos clientes com `PixelOutputStream`

Ou seja:
- o cliente envia pixels (request),
- o servidor atualiza o estado,
- o servidor envia pixels para todos (reply/broadcast em TCP).

#### O que o cliente faz (Python)
1. Abre socket TCP e conecta no servidor (`socket.SOCK_STREAM`)
2. Cria streams (`makefile('wb')` e `makefile('rb')`)
3. Lê o **Board inicial** (via `BoardInputStream`)
4. Em threads:
   - recebe pixels do servidor (via `PixelInputStream`)
   - envia pixels desenhados (via `PixelOutputStream`)

Isso demonstra o requisito:
- cliente empacota request (bytes) e envia,
- servidor desempacota request,
- servidor empacota reply e envia,
- cliente desempacota reply.

---

## Como executar (exemplo)

### 1) Subir servidor TCP (Java)
- Executar a classe:
  - `br.com.sd.tests.ServerTCP`
- Porta usada: `5000`

### 2) Subir servidor MultiCast TCP/UDP (Java)
- Executar a classe:
- `br.com.sd.tests.ServerMultiCast`
- Porta usada: `5003`

- _substituição do TCP caso seja usado em redes estáveis_

### 3) Rodar cliente (Python)
- Executar:
  - `pyapp/main.py`
- `python pyapp/main.py --ip 192.168.0.10 --port 5000 --udp --udp-group 224.1.1.1 --udp-port 5003`
    --ip: Endereço IP da máquina servidor (Padrão: 127.0.0.1)
    --port: Porta de conexão TCP do servidor (Padrão: 5000)
    --udp: Flag para ativar o modo UDP Multicast para o `recv` dos pixels
    --udp-group: Endereço do grupo Multicast (Padrão: 224.1.1.1)
    --udp-port: Porta para o tráfego UDP (Padrão: 5003)

---

## Protocolo (resumo do empacotamento)

O envio é serializado em bytes de inteiros no cliente e servidor. `br.com.sd.streams.PixelOutpuStream`

### Pixels (PixelOutputStream/PixelInputStream)
```
[int n]
repetir n vezes:
  [int x]
  [int y]
  [int color]
```

### Board (BoardOutputStream/BoardInputStream)
```
[int largura]
[int altura]
repetir y em 0..altura-1:
  repetir x em 0..largura-1:
    [int color]
```