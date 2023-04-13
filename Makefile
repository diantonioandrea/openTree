unix: # Linux and macOS
	pyinstaller --onefile --console src/main.py
	mv dist/main openTree

windows: # Windows
	pyinstaller --onefile --console .\src\main.py
	move .\dist\main.exe .\openTree.exe

clean: # Linux and macOS only
	rm -rf dist build reports data src/__pycache__ .vscode
	rm -rf *.spec openTree