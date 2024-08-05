dev:
		fastapi dev main.py &
		cd tailwindcss && npx tailwindcss -i ./styles/app.css -o ../static/css/app.css --watch