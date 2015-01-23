# Maintainer: Gabriel Acosta <acostadariogabriel@gmail.com>

pkgname=edis
pkgver=1.0
pkgrel=1
pkgdesc="a simple cross-platform IDE for C"
arch=('any')
url="http://centaurialpha.github.io/edis"
license=('GPLv3')
depends=('python' 'python-pyqt4' 'python-qscintilla')
optdepends=('ctags: soporte para generar árbol de símbolos'
            'cppcheck: análisis estático de errores')
install=$pkgname.install
source=(https://github.com/centaurialpha/edis/zipball/master)
md5sums=()

package() {
    cd $startdir

    python setup.py install --root="$pkgdir" --optimize=1
}


md5sums=('cb05101e36914028cbce847d1cf1863f')
