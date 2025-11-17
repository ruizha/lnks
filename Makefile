run:
	python src/main.py

dockerrun:
	docker build -t lnks-app . && docker run -p 5000:5000 lnks-app