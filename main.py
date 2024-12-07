from fastapi import FastAPI, HTTPException
import requests
from typing import List, Dict
from pyngrok import ngrok 

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
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5MDgiLCJqdGkiOiI5YzgzMWRkNmQyNTVmOTJmYTYyMmM0OGQyNTJiZTdiYjNkZGRkNDA0MjJlNTUxMTAwOWFmY2E5OGNiYTZkYjNhY2ZkODcxNDVjYmMwNzliOCIsImlhdCI6MTczMzA2NjAwOS4xMzM4MywibmJmIjoxNzMzMDY2MDA5LjEzMzgzNCwiZXhwIjoxNzY0NjAyMDA5LjAyMDAyNSwic3ViIjoiIiwic2NvcGVzIjpbXX0.QtWALi-tafeWtSrPPrm4AY8OE82jPcK5SyZAmDdp7T0xqA2PHZaK7-Y4cUnoIjXSH7CUz5gkHMfSWeKPbbewnzFSxgDv5HDmTTb3Z4weNM5WD0a6xzhdwogzIqDo_Rx7Zl2NnV_zF9FaSBF5gm6484locDV2PuszIADP52o1-k3VQLQeF65uV8CAvA4DZ2El-zRs2K_O3S-WpVLdxzo6m1AGX0CQNcy2KZCQs47FgobkYJxbiCxCjKV0xYjLXojbTgiiZ_QaRnYIebIRMq3ACZWcwAZBLu-UyyBgauzBqzIpAhjQS-YRFBAAaUrsteS82RTuP2mcSccDYYgrYKTR7GjskdAgDFRfMQqNavd2DJrEr2CbAEMurHChtyN_C5VREHtmASuZ1KklcPsrzFvjFTa1d81bTvqulj16DXfZTzMMl-INjtZhfmepM_gDcSKWcUm0NSjBKOnDkPu8Tp0xP8-y1m4x5ac6vTnhFvjs6KmEquH9cnoWWpyfvIZJj3loQuUXsZaTExaISITfPLmSPGI-9K6cjM-cYYnFqbB2n-ilM6huFmMeKilvIqS08wueGtrYGkzah_vUdQn0EYzfSYcwrhaapU-mSRsyRuA593jq-eH2eyioF710LRZQ727g1Z6CzHy70lB7ky_EvSggDliQPJgJjaJ4CKS-6UAXaSM"  # Замените на ваш токен


@app.get("/api/regions", summary="Список регионов", tags=["Регионы"])
async def get_regions() -> List[Dict[str, str]]:
    """
    Возвращает список доступных регионов для вызова API.
    
    - **Описание**: Этот маршрут возвращает список регионов с их идентификаторами и названиями.
    - **Ответ**:
        ```json
        [
            {
                "id": "eu",
                "name": "Europe"
            },
            {
                "id": "us",
                "name": "United States"
            }
        ]
        ```
    """
    try:
        headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
        response = requests.get(f"{BASE_URL}/regions", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/{region}/emission",
    summary="Статус выбросов в регионе",
    tags=["Регионы"]
)
async def get_emission_status(region: str) -> Dict[str, str]:
    """
    Возвращает информацию о текущем выбросе (если есть) и данные о предыдущем выбросе.
    
    - **Параметры**:
        - `region`: ID региона, например, `eu` или `us`.
    - **Описание**: Этот маршрут возвращает временные метки для текущего и предыдущего выбросов.
    - **Ответ**:
        ```json
        {
            "currentStart": "2024-12-01T14:15:22Z",
            "previousStart": "2024-11-30T10:00:00Z",
            "previousEnd": "2024-11-30T12:00:00Z"
        }
        ```
    """
    try:
        headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
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
    
    - **Параметры**:
        - `region`: ID региона, например, `eu` или `us`.
        - `character`: Имя персонажа, для которого нужно получить список друзей.
    - **Описание**: Этот маршрут возвращает список имён персонажей, которые являются друзьями указанного персонажа.
    - **Ответ**:
        ```json
        [
            "Friend-1",
            "Friend-2",
            "Friend-3"
        ]
        ```
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
        url = f"{BASE_URL}/{region}/friends/{character}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/{region}/auction/{item}/history",
    summary="История цен на предмет с аукциона",
    tags=["Аукцион"]
)
async def get_item_price_history(region: str, item: str, additional: str = "false", limit: int = 20, offset: int = 0) -> Dict[str, List[Dict[str, str]]]:
    """
    Возвращает историю цен на предмет с аукциона.
    
    - **Параметры**:
        - `region`: ID региона, например, `eu` или `us`.
        - `item`: Название предмета, для которого нужно получить историю цен.
        - `additional`: Включить дополнительную информацию о лотах (по умолчанию `false`).
        - `limit`: Количество цен для возврата (по умолчанию 20, максимум 200).
        - `offset`: Количество цен, которые нужно пропустить (по умолчанию 0).
    - **Ответ**:
        ```json
        {
            "total": 100,
            "prices": [
                {
                    "amount": 10,
                    "price": 500,
                    "time": "2024-12-01T12:00:00Z",
                    "additional": {}
                },
                {
                    "amount": 5,
                    "price": 450,
                    "time": "2024-12-01T11:30:00Z",
                    "additional": {}
                }
            ]
        }
        ```
    """
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
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
    # Run the app with a public URL using pyngrok
    ngrok.set_auth_token("2pcxlBV2BVL7uINxiwwKqpW2lne_E4MAvDB7i5bySG4qK4uG")  # Optionally, authenticate ngrok (if you have a token)
    public_url = ngrok.connect(8000)  # Specify the port where your FastAPI app runs
    print(f"FastAPI is accessible at {public_url}")
    # Run the app with Uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)