from fastapi import FastAPI

app = FastAPI()

contagem = 0

@app.get("/pulso")
async def on_pulse():
    global contagem
    contagem += 1
    return f"Contagem de pulsos: {contagem}"
