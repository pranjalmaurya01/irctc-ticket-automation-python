dev:
		cd api && fastapi dev main.py &
		cd tailwindcss && npx tailwindcss -i ./styles/app.css -o ../api/static/css/app.css --watch