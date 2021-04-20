all: install



install: copy path

update: copy

path: 
	PATH=$PATH:/home/cynamic/bin

copy:
	@echo "Copying all files into home directory..."
	@cp -r -v ../cynamic /home/
	@-rm /home/cynamic/bin/cyc
	@echo "python /home/cynamic/src/translator.py \$$1" >> /home/cynamic/bin/cyc
	@chmod +x /home/cynamic/bin/cyc
	@echo "Done!"
	
	