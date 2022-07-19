# Proyecto pipeline_procesamiento_cultura

_Este proyecto toma datos de 3 fuentes distintas de la web cultura.gov.ar, los procesa y convierte en tablas con informacion cultural sobre bibliotecas, museos y cines. Luego son enviados a una base de datos SQL donde se registra la fecha y hora de la última actualizacion de las tablas._

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local. (No testeado en windows)_

### Instalación 🔧

###### Primer paso

_Para MAC con procesador M1 instalar el entorno con el siguiente comando:_

```
conda env create -f environment.yml
conda activate pipeline
```

_Para arquitecturas X86 instalar el entorno de la siguente forma:_

```
conda create -n pipeline python=3.9
conda activate pipeline
pip install -r requirements.txt
```

###### Segundo paso

_Copiar el archivo **.env** enviado via email en el directorio raiz_

###### Tercer paso

_Ejecutar el container (se debe tener instalado docker)_

```
docker run --name postgres-alkemy -e POSTGRES_PASSWORD=[insertar_password] -e POSTGRES_USER=[insertar_usuario] -e POSTGRES_DB=culturagov -p 5432:5432 -d postgres
```

### Ejecucion ⌨️

_Correr el archivo python para crear las tablas con el siguiente comando, una unica vez_

```
python crear_tablas.py
```

_Correr el archivo python main para bajar, procesar y agregar los datos a las tablas SQL_

```
python main.py
```
