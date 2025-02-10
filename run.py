from app import app
import os

if __name__ == '__main__':
    # Se usa para levantar un server local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)