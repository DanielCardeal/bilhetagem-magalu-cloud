# /bin/env bash

# Configura um ambiente local de desenvolvimento para um dos projetos no
# repositório.

set -e

exit_fail () {
    if [ $# -eq 1 ]; then
        echo -e "$1"
    fi
    exit 1
}

if [ $# -ne 1 ]; then
    exit_fail "USO: ./setup-dev.sh <nome-do-projeto>"
fi

PROJ_NAME="$1"
REPO_ROOT=$(git rev-parse --show-toplevel)
PROJ_ROOT="${REPO_ROOT}/${PROJ_NAME}"

if [ ! -d "${PROJ_ROOT}" ]; then
    exit_fail "Nome inválido de projeto: ${PROJ_NAME}"
fi
echo "PROJETO: ${PROJ_NAME}"
cd "${PROJ_ROOT}"

# Cria o ambiente isolado para desenvolvimento da aplicação
if [ ! -d .venv/ ]; then
    python3 -m venv .venv/
fi
. $(pwd)/.venv/bin/activate
echo "Criação .venv/: OK"

# Instala primeiro a versão correta do pip antes de prosseguir com a instalação
# das dependências
echo "Instalação de dependências:"
if ! pip install -q -r "${REPO_ROOT}/pip-requirements.txt"; then
    exit_fail "\t- PIP: FALHA"
fi
echo "\t- PIP: OK"

if ! pip install -q -r "${REPO_ROOT}/dev-requirements.txt"; then
    exit_fail "\t- DEV: FALHA"
fi
echo "\t- DEV: OK"

if ! pip install -q -r requirements.txt; then
    exit_fail "\t- ${PROJ_NAME}: FALHA"
fi
echo "\t- ${PROJ_NAME}: OK"
