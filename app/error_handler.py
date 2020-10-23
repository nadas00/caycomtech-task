from app import app

@app.errorhandler(404) 
def not_found(e): 
    return {"Error":"404 Not found!"}, 404

