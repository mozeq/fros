RPM_DIRS = --define "_sourcedir `pwd`" \
		   --define "_rpmdir `pwd`" \
		   --define "_specdir `pwd`" \
		   --define "_builddir `pwd`/rpmbuilddir" \
		   --define "_srcrpmdir `pwd`"

sdist:
	python setup.py sdist

rpm: sdist
	rpmbuild $(RPM_DIRS) -ba fros.spec

srpm: sdist
	rpmbuild $(RPM_DIRS) -bs fros.spec
