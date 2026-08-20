#!/usr/bin/env bash
# SELLAR (Ingeniero VUC) — guarda TODO en UN commit sobre la rama canonica.
# Copiado del estilo de `sellar.sh` de DMM (Julio, 2026-07-23) y con sus mismos candados:
#   1) solo la rama canonica          2) solo carpetas declaradas
#   3) NO se sella con una vigia roja 4) NO se sella si el verificador encuentra algo ROTO
#
# Uso:  bash sellar.sh "lo que cambio"
set -u
cd "/c/Ingeniero_VUC" || { echo "no existe la carpeta canonica C:\\Ingeniero_VUC"; exit 1; }

RAMA_OK="integration/ingeniero-vuc"
PERMITIDAS=$'arnes\ncerebro\ncuerpo\nmapa\nmemoria\nskills\nvigias'

# 1) Candado de rama: una sola via.
rama="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
if [ "$rama" != "$RAMA_OK" ]; then
  echo "BLOQUEADO: la via canonica es '$RAMA_OK', estas en '$rama'."
  echo "   git switch $RAMA_OK"
  exit 1
fi

# 2) Candado de carpetas: ninguna carpeta sin declarar (Julio: no crear carpetas a lo pendejo).
extra="$(find . -mindepth 1 -maxdepth 1 -type d ! -name '.git' ! -name '.claude' -printf '%f\n' \
        | grep -vxF "$PERMITIDAS" | while read -r d; do git check-ignore -q "$d" || echo "$d"; done)"
if [ -n "$extra" ]; then
  echo "BLOQUEADO por la regla de carpetas: hay carpeta(s) NO declarada(s):"
  echo "$extra" | sed 's/^/   /'
  echo "Declaralas en sellar.sh y en el contrato, o borralas."
  exit 1
fi

# 3) Candado de no-regresion: no se sella nada que rompa una vigia.
echo "Corriendo las vigias..."
if ! python -m pytest -q vigias/ >/tmp/sellar_ing.log 2>&1; then
  echo "BLOQUEADO: hay vigias ROJAS. No se sella para no romper otra cosa. Ultimas lineas:"
  tail -5 /tmp/sellar_ing.log
  exit 1
fi
echo "Vigias VERDES."

# 4) Candado anti-asumir: el verificador no puede encontrar nada ROTO.
echo "Verificando las ordenes de Julio contra el disco..."
if python verificar.py 2>&1 | grep -q "ROTO: [1-9]"; then
  echo "BLOQUEADO: el verificador encontro algo ROTO. Corre: python verificar.py"
  exit 1
fi

# 5) Sellar: un commit con todo.
msg="${1:-cambios del Ingeniero VUC}"
git add -A
if git diff --cached --quiet; then
  echo "Nada nuevo que sellar."
  exit 0
fi
git -c user.name="joules8315-stack" -c user.email="joules8315@gmail.com" commit -q -m "$msg

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
echo "SELLADO en $RAMA_OK: $(git log -1 --oneline)"
