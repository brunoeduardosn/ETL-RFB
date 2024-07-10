REM Verificar versao instalado do python (este projeto foi feito em Python 3.11)
python --version

REM Crie um ambiente virtual em Python 3.11
python3.11 -m venv __my_env

REM Ativar o ambiente virtual
source __my_env/bin/activate

REM Atualizar PIP para última versão
python.exe -m pip install --upgrade pip

REM Instalar pacotes necessários usando o arquivo requerimentos.txt
python -m pip install -r requirements.txt

REM Listar pacotes instalados
pip list

python ./src/A_Main.py 