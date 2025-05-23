import os
from flask import Flask
from flask_cors import CORS
from routes import routes
from config import Config

app = Flask(__name__)

# Cargar configuración
app.config.from_object(Config)

# Habilitar CORS
CORS(app)

# Registrar las rutas
app.register_blueprint(routes)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)