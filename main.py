from fastapi import FastAPI, HTTPException
import requests
from typing import List, Dict

app = FastAPI(
    title="FREE STALCRAFT API",
    description="Прокси для работы с Production API Stalcraft.",
    version="1.0.0",
    contact={
        "name": "W3nnaCry",
        "discord": "luh7092",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

BASE_URL = "https://eapi.stalcraft.net"
API_TOKEN = "YOUR_API_TOKEN_HERE"  # Замените на ваш токен


@app.get("/api/regions", summary="Список регионов", tags=["Регионы"])
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


@app.get("/api/{region}/emission", summary="Статус выбросов в регионе", tags=["Регионы"])
async def get_emission_status(region: str) -> Dict[str, str]:
    """
    Возвращает информацию о текущем выбросе (если есть) и данные о предыдущем выбросе.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/emission"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{region}/friends/{character}", summary="Список друзей персонажа", tags=["Друзья"])
async def get_friends_list(region: str, character: str) -> List[str]:
    """
    Возвращает список друзей для указанного персонажа в выбранном регионе.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/friends/{character}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{region}/auction/{item}/history", summary="История цен на предмет с аукциона", tags=["Аукцион"])
async def get_item_price_history(region: str, item: str, additional: str = "false", limit: int = 20, offset: int = 0) -> Dict[str, List[Dict[str, str]]]:
    """
    Возвращает историю цен на предмет с аукциона.
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        url = f"{BASE_URL}/{region}/auction/{item}/history"
        params = {
            "additional": additional,
            "limit": str(limit),
            "offset": str(offset)
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
