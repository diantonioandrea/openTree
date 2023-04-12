darwin: # macOS release
	pyinstaller --onefile --console src/main.py
	mv dist/main openTree
	mkdir -p release
	zip -r "release/openTree-darwin.zip" openTree resources/

linux: # Linux release
	pyinstaller --onefile --console src/main.py
	mv dist/main openTree
	mkdir -p release
	zip -r "release/openTree-linux.zip" openTree resources/

windows: # Windows release
	pyinstaller --onefile --console .\src\main.py
	move .\dist\main.exe .\openTree.exe
	if exist .\release rd /s /q .\release
	mkdir release
	zip -r "release/openTree-windows.zip" .\openTree.exe .\resources\

clean: # Linux and macOS only
	rm -rf dist build reports release data src/__pycache__ .vscode
	rm -rf *.spec openTree