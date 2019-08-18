pkgdesc="OSS volume tray control"
pkgname=oss-traycontrol
pkgver=0.23
pkgrel=1

arch=(i686 x86_64)
license=('CCPL:by')
depends=('pygtk' 'python2' 'oss')
replaces=('oss-volume-tray-control')

# для сборки в пакет запакуйте исходники (2 файла) в архив, имя архива отметьте в следующей строке
source=('oss-traycontrol-0-23.tar.gz')

# с помощью команды md5sum найдите md5-сумму созданного архива, отметьте ее в следующей строке
md5sums=('1cf352d39939d40f1ae19e0bcce5ae40')

build() {
	echo "#! /bin/sh
python2 /usr/share/ossvolume/volume.py" > ossvolume
	chmod a+x ossvolume
}
package() {
	rm -f "${srcdir}/`basename $source`"
	dir=${pkgdir}/usr/share/ossvolume; mkdir -p "$dir"
	cp -RT "${srcdir}" "$dir"
	bin=${pkgdir}/usr/bin; mkdir -p "$bin"
	mv "$dir/ossvolume" "$bin/ossvolume"
}

# запустите makepkg в папке с данным файлом и собранным архивом. В результате вы получите archlinux-пакет, который сможете установить с помощью pacman -U, например:
#	sudo pacman -U oss-traycontrol-0.23-x86_64.pkg.tar.xz
