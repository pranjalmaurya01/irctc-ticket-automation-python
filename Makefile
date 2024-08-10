dev:
		cd tailwindcss && npx tailwindcss -i ./styles/app.css -o ../api/static/css/app.css --watch &
		cd api && fastapi dev main.py
