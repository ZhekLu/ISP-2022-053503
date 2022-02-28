build:
	docker build -t lab1 .
run:
	docker run --rm -it --name lab1 lab1:latest
stop:
	docker stop lab1