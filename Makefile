PKGNAME=argo-probe-eudat-pyhandle
SPECFILE=${PKGNAME}.spec
FILES=${SPECFILE} pyhandle/*

PKGVERSION=$(shell grep -s '^Version:' $(SPECFILE) | sed -e 's/Version:\s*//')

rpm: dist
	rpmbuild -ta ${PKGNAME}-${PKGVERSION}.tar.gz

dist:
	rm -rf dist
	mkdir -p dist/${PKGNAME}-${PKGVERSION}
	cp -pR ${FILES} dist/${PKGNAME}-${PKGVERSION}/
	tar zcf dist/${PKGNAME}-${PKGVERSION}.tar.gz -C dist ${PKGNAME}-${PKGVERSION}
	mv dist/${PKGNAME}-${PKGVERSION}.tar.gz .
	rm -rf dist

sources: dist

clean:
	rm -rf ${PKGNAME}-${PKGVERSION}.tar.gz
	rm -rf dist
