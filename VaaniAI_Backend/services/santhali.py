import requests

SANTHALI_SERVICE_URL = "http://127.0.0.1:8001/translate"


def translate_hindi_to_santhali(text: str) -> str:
    """
    Send Hindi text to the WSL IndicTrans2 service
    and return the Santhali translation.
    """

    if not text or not text.strip():
        return ""

    try:
        response = requests.post(
            SANTHALI_SERVICE_URL,
            json={
                "text": text
            },
            timeout=120
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Santhali service error "
                f"{response.status_code}: {response.text}"
            )

        data = response.json()

        translation = data.get("translation", "")

        if not translation:
            raise RuntimeError(
                "Santhali service returned an empty translation."
            )

        return translation

    except requests.RequestException as e:
        raise RuntimeError(
            f"Could not connect to IndicTrans2 service: {e}"
        )