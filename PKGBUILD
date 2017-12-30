# Maintainer: Martin Sträng <martin@tilljorden.com>
pkgname=python-nibe2influx
pkgver=0.1
pkgrel=1
pkgdesc="Reads values from Nibe Uplink and store in InfluxDB"
arch=(any)
url=""
license=('')
groups=()
depends=('python' 'python-oauthlib' 'influxdb')
makedepends=('python-setuptools')
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=()
md5sums=()

package() {
  cd $srcdir
  python setup.py install --root="$pkgdir/" --optimize=1
}
