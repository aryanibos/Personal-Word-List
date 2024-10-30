import requests

api_key = '4e3d0a0c-f901-416e-ad42-e11b625b4320'
word = 'voluminous'
root_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json'
final_url = f'{root_url}/{word}?key={api_key}'

# Lakukan request
r = requests.get(final_url)

# Periksa status kode dan tampilkan respons jika gagal
if r.status_code == 200:
    try:
        result = r.json()  # Ubah ke JSON
        print(result)
    except requests.exceptions.JSONDecodeError:
        print("Error: Respons tidak dapat diuraikan sebagai JSON.")
        print("Isi respons:", r.text)
else:
    print(f"Error: Respons gagal dengan status kode {r.status_code}")
    print("Isi respons:", r.text)
