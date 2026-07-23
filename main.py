from fastapi import FastAPI

app=FastAPI()
@app.get("/")
def Hello():
    return {"message": "Hello World"}