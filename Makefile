
build: 
	docker compose build

run: 
	docker compose up

# cahnge 
build-local:
	uvicorn app.main:app --reload


# frontennd local

frontend_local:
		npx serve . -l 3000