RPM_DIRS = --define "_sourcedir `pwd`" \
		   --define "_rpmdir `pwd`" \
		   --define "_specdir `pwd`" \
		   --define "_builddir `pwd`/rpmbuilddir" \
		   --define "_srcrpmdir `pwd`"

download:
	wget https://github.com/mozeq/fros/archive/`git rev-parse HEAD`/fros-1.0-`git rev-parse HEAD | cut -c -7`.tar.gz

sdist:
	python setup.py sdist

rpm: sdist
	rpmbuild $(RPM_DIRS) -ba fros.spec

srpm: sdist
	rpmbuild $(RPM_DIRS) -bs fros.spec
