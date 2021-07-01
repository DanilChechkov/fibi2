#!/bin/bash
sleep 5
DIRROOT=$(cd $(dirname $0) && pwd)
mv -f "${DIRROOT}/fibi.py" "${DIRROOT}/fibiO.py"
mv -f "${DIRROOT}/fibiu.py" "${DIRROOT}/fibi.py"
chmod 0777 "${DIRROOT}/fibi.py"
cd $DIRROOT
./fibi.py
