import requests
import json


def get_random_breed_image(breed):
    breed_image = [] 
    filename = []
    
    url_sub_breed_list = f'https://dog.ceo/api/breed/{breed}/list'
    response_list = requests.get(url_sub_breed_list)
    dog_list = response_list.json()['message']
    if dog_list:
        for dog in dog_list:
            url_sub_breed = f'https://dog.ceo/api/breed/{breed}/{dog}/images/random'
            response = requests.get(url_sub_breed)
            dog_image = response.json()['message']
            name = dog_image.split('/')[-1]
            filename.append(name)
            breed_image.append(dog_image)
            print(f'Изображение: {name}')
    else:
        url_breed = f'https://dog.ceo/api/breed/{breed}/images/random'
        response = requests.get(url_breed)
        dog_image = response.json()['message']
        name = dog_image.split('/')[-1]
        filename.append(name)
        breed_image.append(dog_image)
        print(f'Изображение: {name}')
    
    return {
        'breed': breed,
        'filename': filename,
        'breed_image': breed_image
    }
    
    
def upload_image_to_ya_disk(breed, filename, breed_image, user_token):
    params = {
        'path': f'/{breed}'
    }
    headers = {
        'authorization': f'OAuth {user_token}'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', 
                            params=params, 
                            headers=headers)
    print(f'Создался файл: {breed}')
    
    for breed_image, filename in list(zip(breed_image, filename)):
        params = {
            'url': {breed_image},
            'path': f'{breed}/{breed}+{filename}'
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', 
                                params=params, 
                                headers=headers)
        print(f'Загрузка изображения {filename} в файл {breed}')
        output_file = 'info_images.json'
        meta_info = {
            'filename': filename,
            'breed': breed,
            'origin_url': breed_image
        }
        with open(output_file, 'a', encoding='utf-8') as f: 
            json.dump(meta_info, f, indent=4, ensure_ascii=False) 
        
        print(f"Информация о {filename} фотографиях успешно сохранена в {output_file}")


breed = input('Ведите название породы собаки на английском языке: ')
user_token = input('Введите Ваш OAuth-токен Яндекс Диска: ')

dog_image_link = get_random_breed_image(breed)

upload_image_to_ya_disk(
    breed=dog_image_link['breed'], 
    filename=dog_image_link['filename'], 
    breed_image=dog_image_link['breed_image'], 
    user_token=user_token
)
