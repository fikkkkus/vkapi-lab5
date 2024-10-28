# Запуск для Windows:

**1)Клонируем репо:**   
git clone https://github.com/fikkkkus/vkapi-lab3

**2)Переходим к папке:**  
cd vkapi-lab3

**3)Устанавливаем зависимости:**   
pip install -r requirements.txt

**4)Запускаем скрипт, вам предложат ввести id и token:**   
python main.py

**5)Файл с результатами сохраниться в папке куда клонировали репо, чтобы просмотреть содержимое можно прописать:**  
type result.json

---

# Запуск Linux:

**1)Устанавливаем git если его нет и репо:**

sudo apt update

sudo apt install git

git clone https://github.com/fikkkkus/vkapi-lab3

**2)Переходим к папке:** 
cd vkapi-lab3

**3)Устанавливаем pip если нет и зависимости:** 

sudo apt update

sudo apt install python3 python3-pip

pip install -r requirements.txt

**4)Запускаем скрипт, вам предложат ввести id:**  
python3 main.py

**5)Файл с результатами сохраниться в папке куда клонировали репо, чтобы просмотреть содержимое можно прописать:**   
cat result.json
