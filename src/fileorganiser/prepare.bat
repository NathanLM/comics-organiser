echo "toto" > "[Comics-FR]SpiderMan.zip"
echo "toto" > "[Comics-FR]Iron-Man l'H‚ritage.rar"
cd test
del *.* /Q
cd ..
cd FR\Marvel\Spiderman
del *.* /Q
cd C:\Users\Nathan\Desktop\truc
del *.* /S /Q
cd C:\Users\Nathan\workspace\fileorganiser\fileorganiser\src\fileorganiser
python fileorganiser.py C:\Users\Nathan\Desktop\truc --real
pause
