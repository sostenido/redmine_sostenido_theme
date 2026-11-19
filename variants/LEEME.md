# Variantes

Cada variante es un par `<nombre>.conf` + `<nombre>.js` y se genera con
`./build.sh <nombre>`.

En el repositorio público solo están:

- `demo`: las tres paletas a elección del usuario, con el logo de SOSTENIDO.
- `cliente`: plantilla comentada para crear variantes nuevas.

Las variantes reales de cada instalación (y sus logos) **no se publican**:
se guardan en un repositorio privado y se copian a esta carpeta antes de
compilar. El `.gitignore` las deja afuera automáticamente.
