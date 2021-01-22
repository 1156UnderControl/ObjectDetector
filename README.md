# ObjectDetector
Algoritmo de detecção de objetos para encontrar a configuração de bolas no autônomo utilizando uma Raspberry Pi


## Funcionalidade
Este software utiliza uma Raspberry Pi (Testado com [modelo 3 B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)) juntamente com uma câmera ([Picamera V2](https://www.raspberrypi.org/products/camera-module-v2/)) para detectar a configuração de objetos de jogo nos desafios at home (2021) e possibilitar ao robô a escolha do autônomo correto.

### Conceito de Funcionamento
Para detectar o layout de bolas, o algoritmo pressupõe que o robô sempre inicie na mesma posição para cada circuito. Desta forma, uma câmera posicionada no robô deve esperar encontrar as bolas aproximadamente no mesmo lugar sempre que iniciar um desafio. Utilizando este conhecimento, o software é configurado para, ao início de uma execução do circuito, tirar uma foto com a câmera da Raspberry Pi e cortar a imagem apenas a uma região onde a presença de uma bola é esperada apenas se o circuito estiver na configuração A ou apenas se o circuito estiver na configuração B. A partir deste recorte, o software utiliza filtros de cor para estabelecer se um percentual significativo da imagem é preenchido pela cor da bola, se sim, o valor verdadeiro é retornado indicando que a posição das bolas é a A (Caso a bola observada esteja presente apenas na configuração A). O retorno desta variável ao roboRIO é feito por meio de networktables, isto são variáveis que são compartilhadas por meio da rede que é utilizada pelo robô. Esta forma de compartilhamento de dados é a mesma utilizada pela dashboard do robô, apenas utilizando um nome de tabela diferente e nomes de variáveis diferentes, assim, estes dados podem ser vistos da mesma forma que dados provenientes da dashboard. Com este resultado de verdadeiro ou falso, o roboRIO está capacitado para escolher o percurso correto para adquirir as bolas da maneira mais eficiente possível. De uma maneira resumida, o fluxo é o seguinte:

**Tirar Foto > Cortar Área Relevante > Detectar Cor da Bola Usando HSV > Calcular Percentual de Preenchimento > Comparar com Valor Mínimo**


## Setup
Os scripts utilizados foram testados em uma Raspberry Pi recentemente formatada, de maneira a evitar qualquer interferência por configurações feitas previamente na placa, mas nada impede que este seja executado em uma Pi com outros softwares já instalados. Para formatar a Raspberry Pi, utilizar a [ferramenta de formatação de SD](https://www.raspberrypi.org/software/) da marca.

### Configurações da Raspberry Pi
Em uma placa recentemente formatada, é sugerido a instalação do VNC (Virtual Network Computing), que possibilita o acesso ao desktop da Raspberry Pi remotamente via rede local e um [software](https://www.realvnc.com/en/connect/download/viewer/) de visualização. Para fazer este setup é necessário estar conectado na internet com a raspberry pi e rodar o seguinte comando no terminal:
```
sudo apt -y install realvnc-vnc-viewer realvnc-vnc-server
```
Além disso é necessário habilitar as interfaces de vnc e câmera para que estes estejam disponíveis. Para se deve entrar em **Menu > Preferences > Raspberry Pi Configuration > Interfaces** e habilitar as linhas de câmera e vnc.

*Obs: Neste menu de configuração também é possível alterar a resolução da Raspberry Pi*

Após concluir estas modificações é necessário reiniciar a placa por meio dos menus ou do comando `sudo reboot`. Para conectar na placa por VNC é necessário abrir a janela do VNC na Raspberry Pi (Localizada no canto direito superior), expandir a aba de "Other ways to connect" e copiar o IP encontrado.

*Obs: Caso o IP da Raspberry Pi mude por algum motivo como mudança de rede utilizada, mudança de configurações do rádio, ou outras, a conexão de VNC não funcionará mais e este IP deve ser novamente consultado na Raspberry Pi por meio de um monitor.*

### Configurações do Software de Detecção
Tendo completado as configurações da Raspberry Pi, a configuração do software de deteção é simples. Basta enviar o arquivo `Object Detector.tar` para a Raspberry Pi (Um pendrive pode ser utilizado ou a ferramenta de transferência de arquivos do VNC) e extrair este **no Desktop**. Tendo extraído estes arquivos, pode se utilizar o Setup.sh (que necessita de conexão à internet) para instalar todas as outras dependências necessárias e fazer configurações. Para isto basta abrir um novo terminal e digitar os comandos:
```
cd Desktop
sudo sh Setup.sh
```
Como o script de setup deve baixar e instalar várias dependências, este processo pode levar algum tempo. Ao fim a Raspberry Pi será automaticamente reinicializada e o detector de objetos deverá rodar automaticamente sempre que esta for ligada. Inicialmente é esperado que este falhe mencionando a falta do arquivo `configuration.xml`. Isto acontece pois o detector utiliza arquivos de configuração para determinar onde buscar a bola para determinar o layout e que cores buscar. Como a pasta object-detection é criada pelo script de setup, esta está vazia. Quando os arquivos de configuração estiverem colocados lá, este erro deve parar.

*Obs: Se o erro estiver mencionando que não é possível acessar a câmera pois a interface está desabilitada, isto significa que ou a câmera não está conectada corretamente ou o passo anterior onde a interface de câmera é habilitada não foi completo.*

*Obs 2: A câmera utilizada deve ser uma câmera de barramento, conectada por um cabo flat diretamente na placa de circuitos. Webcams USB não irão funcionar no script de execução. Caso o uso destas seja necessário, o script deve ser modificado.*

## Uso
### Configuração de Detecção
Para configurar a detecção dos objetos de jogo, o robô deve estar posicionado da mesma maneira que ficará no início de uma tentativa do desafio e a Raspberry Pi deve ser acessada, ou via VNC ou por meio de monitor/mouse/teclado. Para rodar o software de configuração é necessário antes fechar o Runtime (Software de execução) que é aberto ao inicializar a Raspberry Pi. O software de configuração pode ser acessado via **ConfigurationTool**, um icone que já deve estar presente no desktop, ou via linha de comando com:
```
python3 /home/pi/Desktop/scripts/ObjectDetectorConfigurationTool.py
```
Isto irá abrir uma linha de comando utilizada para definir a detecção. Esta linha de comando possui sua própria documentação acessada pelo comando:
```
help
```
De maneira concisa, os parâmetros que devem ser calibrados nesta ferramenta são:
- Resolução (O padrão é 1920x1080)
- Área de busca: esta é a área da foto onde o software irá buscar a cor da bola para detectar se esta está presente ou não (É recomendado evitar buscar bolas em áreas onde exista uma possibilidade de uma bola indesejada aparecer se o robô não estiver posicionado perfeitamente. Bolas isoladas são as mais recomendáveis)
- Cor: A cor considerada como a da bola é definida por HSV (Hue, Saturation, Value) ao invés de RGB. Para cada uma das 3 variáveis é definido um valor mínimo e um máximo, que podem ser configurados por seleção na foto ou manualmente
- Fullness: Este seria o preenchimento esperado da área onde o objeto está sendo procurado. Um valor de 5 significaria que o detector apenas considerará a presença de uma bola se 5% ou mais da área observada estiver dentro da cor selecionada.

### Configuração de Execução
Na pasta scripts, existe um arquivo utilizado para configurar dois parâmetros:
- ip: Este é o IP utilizado para conectar no servidor do networktables. Este deve ser o mesmo IP que o utilizado pela dashboard
- configurationXML: Este é o nome do arquivo XML de configuração, gerado pelo passo anteror, que deve ser utilizado em execução (o arquivo deve estar na pasta object-detection)

O arquivo contendo estas configurações é chamado de `runtime.xml` e pode ser modificado com um editor de texto comum. Na Raspberry Pi isto pode ser feito com o Geany (Disponível ao clicar com o botão direito do mouse neste arquivo)

### Leitura pelo roboRIO
Para que o resultado da detecção seja lido no roborio, é necessário que a Raspberry Pi esteja na mesma rede que este. Os dados serão disponibilizados da mesma forma que dados da dashboard, por meio de networktables. A diferença é o nome de tabela e de variáveis, que são os seguintes:
```
tabela: "CameraVision"
```
Variáveis:
- `isDisabled`(boolean): Esta variável inicia como false e pode ser ativada pelo roborio para fazer com que o software pare de atualizar a detecção de objeto. Esta variável só é setada para false automaticamente quando a Raspberry Pi é reiniciada ou o código de execução é manualmente reiniciado.
- `isDetected`(boolean): Esta variável representa se o objeto buscado está presente na área desejada. Ela é atualizada pelo software a cada 200ms e não requer que o robô esteja habilitado para estar atualizada.


## Contato
Para dúvidas em relação ao funcionamento do detector entrar em contato com [@HenriqueSchmitz](https://github.com/orgs/1156UnderControl/people/HenriqueSchmitz) ou [@Silvxo](https://github.com/orgs/1156UnderControl/people/Silvxo)
