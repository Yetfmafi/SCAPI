from fastapi import FastAPI, HTTPException
import requests
from typing import List, Dict

app = FastAPI(
    title="FREE STALCRAFT API",
    description="Прокси для работы с Production API Stalcraft.",
    version="1.0.0",
)

BASE_URL = "https://eapi.stalcraft.net"
API_TOKEN = "YOUR_API_TOKEN_HERE"  # Замените на ваш токен


@app.get("/api/regions", summary="Список регионов")
async def get_regions() -> List[Dict[str, str]]:
    """
    Возвращает список доступных регионов для вызова API.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.get(f"{BASE_URL}/regions", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{region}/emission", summary="Статус выбросов в регионе")
async def get_emission_status(region: str) -> Dict[str, str]:
    """
    Возвращает информацию о текущем выбросе и предыдущем выбросе.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/emission"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{region}/friends/{character}", summary="Список друзей персонажа")
async def get_friends_list(region: str, character: str) -> List[str]:
    """
    Возвращает список друзей указанного персонажа в заданном регионе.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/friends/{character}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{region}/auction/{item}/history", summary="История цен на аукционе")
async def get_item_price_history(region: str, item: str, limit: int = 20, offset: int = 0) -> Dict[str, List[Dict[str, str]]]:
    """
    Возвращает историю цен на указанный предмет.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/auction/{item}/history"
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
