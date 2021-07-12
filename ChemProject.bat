set PATH=%PATH%;C:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin
rmdir /S /Q Release
pyrcc5 icons.qrc -o icons_rc.py
pyuic5 form.ui -o ui_form.py
pyinstaller --clean -F --onefile --noconsole ChemProject.py
mkdir Release
copy dist\ChemProject.exe Release\ChemProject.exe
rmdir /S /Q build
rmdir /S /Q dist
del /f ChemProject.spec
Release\ChemProject.exe