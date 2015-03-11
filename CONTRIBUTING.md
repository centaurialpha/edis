# Formas de Contribuir

Hay varias maneras de contribuir y ser parte del proyecto:

## Reportando bugs

Si encontraste un bug puedes detallarlo [acá](https://github.com/centaurialpha/edis/issues/new) y asegúrate de agregarle el *Label* **bug** desde la pestaña *Labels*.

## Solicitar feature o mejora

Puedes solicitar una nueva funcionalidad para incluir en las próximas versiones, o reportar una mejora de alguna funcionalidad que ya existe desde [acá](https://github.com/centaurialpha/edis/issues/new) (no olvides de agregar el *Label* correcto).

## Contribuyendo en el código fuente

Antes de comenzar:

### ¿ Qué es un Fork ?

Un fork o bifurcación es una copia del proyecto original, es decir, el proyecto copia puede avanzar sin modificar el original.

### ¿ Qué es un Pull Request ?

Un *Pull Request* es una solicitud, petición que el propietario del *Fork* de un repositorio hace al propietario del proyecto original para que agregue las modificaciones que se hicieron en el *Fork*.

Sabiendo esto puedes comenzar:

1. *Forkea* el proyecto, ésto creará una copia en tu cuenta.
2. *Clona* el repositorio usando la URL que se encuentra en el sidebar:

```bash
git clone https://github.com/tu_cuenta/edis.git
```

Con estos pasos ya tendrás el código fuente del proyecto en tu computadora. Ahora, dentro del directorio del proyecto, añade el *upstream* remoto para sincronizar con el repositorio original:

```bash
git remote add upstream https://github.com/centaurialpha/edis.git
```

Actualiza y combina:

```bash
git fetch upstream
git merge upstream/master
```

Ahora estas listo para contribuir en el código fuente.
Supongamos que encontraste un bug y sabes como arreglarlo, lo ideal sería crear una rama específica para solucionar el problema, por ejemplo:

```bash
git branch issue_12
git checkout issue_12
```

Solucionas el bug y haces el push a tu repositorio remoto:

```bash
git add .
git commit -am "Fixed issue #12"
git push origin issue_12
```

Vuelve a la rama master y combina con *issue_12*:

```bash
git checkout master
git merge isse_12
```

Por último, en tu repositorio remoto, deberás ver un mensaje *Compare & pull request*, esto te llevará a una página para crear el *Pull Request* y hacer comentarios sobre la solicitud.
