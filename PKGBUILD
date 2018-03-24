# Maintainer: Martin Sträng <martin@tilljorden.com>
pkgname=python-nibe2influx
pkgver=0.1
pkgrel=5
pkgdesc="Reads values from Nibe Uplink and store in InfluxDB"
arch=(any)
url=""
license=('')
groups=()
depends=('python' 'python-requests-oauthlib')
makedepends=('python-setuptools')
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=('nibe2influx.service')
md5sums=('SKIP')

package() {
  cd $srcdir
  python setup.py install --root="$pkgdir/" --optimize=1
  install -Dm644 "${srcdir}/nibe2influx.service" "${pkgdir}/usr/lib/systemd/system/nibe2influx.service"
}
