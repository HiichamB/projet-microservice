import httpx
import pybreaker
from tenacity import retry, stop_after_attempt, wait_exponential

USER_URL = "http://user:8000" # nom DNS interne du Compose

client = httpx.AsyncClient(base_url=USER_URL, timeout=httpx.Timeout(1.0))


# Retries avec backoff (tenacity, déjà dans les dépendances)
@retry(stop=stop_after_attempt(2),
       wait=wait_exponential(multiplier=0.2, max=1),
       reraise=True)
async def _appel(client, url):
    reponse = await client.get(url)
    if reponse.status_code != 404: # une personne inconnue
        reponse.raise_for_status() # n'est PAS une panne !
    return reponse
# Budget pire cas = 2 tentatives x 1 s + 0,2 s = 2,2 s (< 3 s exigées)

# Disjoncteur : après 5 échecs consécutifs, on n'appelle plus user pendant 30 s
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)


async def get_personne(personne_id: int) -> dict | None:
    # calling() et non call_async (réservé à Tornado)
    with breaker.calling():
        reponse = await _appel(client, f"/personnes/{personne_id}")
    if reponse.status_code == 404:
        return None
    return reponse.json()
