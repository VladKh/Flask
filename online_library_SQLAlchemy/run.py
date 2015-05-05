from app import app
from config import *

app.run(
    host=HOST,
    port=PORT,
    debug=DEBUG
)
