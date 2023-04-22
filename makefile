name=tap

install: package
	mv out/cal.py ~/Scripts/cal.py
	chmod u+x ~/Scripts/cal.py
	mkdir -p .local/share/tap/database

dirs:
	mkdir -p out

package: dirs
	cd src && zip ../out/${name}.zip *.py 
	echo '#!/usr/bin/env python3' | cat - out/${name}.zip > out/${name}.py

