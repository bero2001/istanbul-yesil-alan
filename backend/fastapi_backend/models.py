from pydantic import BaseModel

class IlceVerisi(BaseModel):
    """
    Bir ilçeye ait yeşil alan verilerini temsil eden model.
    API yanıtlarında kullanılır.
    """
    ilce: str                  # İlçe adı
    yesil_alan_m2: float        # İlçedeki toplam yeşil alan (m²)
    nufus: int                  # İlçenin nüfusu
    kisi_basi_m2: float         # Kişi başına düşen yeşil alan (m²)
