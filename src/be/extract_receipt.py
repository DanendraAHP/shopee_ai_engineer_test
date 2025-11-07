import base64
from typing_extensions import List
from pydantic import BaseModel

from src.be.setup import llm

class Receipt(BaseModel):
    description : str
    quantity : int
    price : float
    date : str
    vendor : str

class Receipts(BaseModel):
    receipts : List[Receipt]
EXTRACT_LLM = llm.with_structured_output(Receipts)

async def image_to_base64(image_path: str) -> str:
    """
    Convert an image file (PNG/JPG/etc.) to a Base64-encoded string.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        str: Base64-encoded string representation of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read())
            encoded_str = encoded_bytes.decode("utf-8")
        return encoded_str
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise RuntimeError(f"Error converting image to base64: {e}")

async def extract_receipt(image_path:str):
    try:
        print('convert image to base64')
        image_base64 = await image_to_base64(image_path)
        print('converting image done')
        instruction = """Kamu adalah pengekstrak receipt yang handal,
        anda perlu mengekstrak setiap item dari sebuah receipt yang ada. Masing-masing item perlu diekstrak
        - deskripsi : deskripsi dari barangnya
        - quantity : jumlah barang yang dibeli, anggap 1 jika tidak ada di gambar
        - price : total harga dari barang tersebut, tidak perlu menghitung harga per-barangnya jika quantity>1. Cukup ambil saja harga yang tertera di gambar receipt secara langsung
        - date : tanggal pembelian barang, buat dalam format year-month-date
        - vendor : dimana item ini dibeli, biasanya yang dimaksud adalah merchant/toko
        karena ada banyak barang jadi anda perlu membuat list dari masing2 ekstraksi. Sehingga outputnya menjadi
        [{"deskripsi":"deskripsi 1", "quantity":1, "price":1000, "date":"2025-11-04"}]
        """
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {
                        "type": "image",
                        "base64": image_base64,
                        "mime_type": "image/jpeg",
                    },
                ]
            }
        ]
        print('ocr using gpt')
        response = EXTRACT_LLM.invoke(message)
        receipts = response.receipts
        print('ocr done')
        print(receipts)
        if receipts:
            receipts = [receipt.model_dump() for receipt in receipts]
        return receipts
    except Exception as e:
        print(e)