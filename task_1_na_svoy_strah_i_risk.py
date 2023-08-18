# Создать декоратор для использования кэша. 
# Т.е. сохранять аргументы и результаты в словарь, 
# если вызывается функция с агрументами, которые уже записаны в кэше - вернуть результат из кэша, 
# если нет - выполнить функцию. Кэш лучше хранить в json.
from typing import Callable
import json
import os
os.system('cls')


def cache_json_log(func: Callable):
    try:
        with open('cache_log.json', 'r') as file:
            result_list = json.load(file)
    except FileNotFoundError:
        result_list = []                # замыкание result_list внутри json_logging
                              
    def wrapper(*args):        
        key_str = args_to_str(*args)        
        
        if len(result_list) == 0:           
            _cache_dict = {}
            _cache_dict[key_str] = func(*args)            
            res_dict = {}
            res_dict[f'{func.__name__}'] = _cache_dict
            result_list.append(res_dict)
               
        else:            
            res_dict = result_list[0]   
            if f'{func.__name__}' in res_dict:
                _cache_dict = res_dict[f'{func.__name__}']
                if key_str not in _cache_dict:
                    _cache_dict[key_str] = func(*args)
                                               

            else:                    
                _cache_dict = {}
                res_dict[f'{func.__name__}'] = _cache_dict
                if key_str not in _cache_dict:
                    _cache_dict[key_str] = func(*args)
                res_dict[f'{func.__name__}'] = _cache_dict
                 
        with open('cache_log.json', 'w') as file:
            json.dump(result_list, file, indent=4)
        return _cache_dict[key_str]
    return wrapper

def args_to_str(*args) -> str:
    """ Преобразует картеж аргументов в строку с разделением через запятую """
    m_str = ''
    for _ in range(len(args) - 1):
        current = args[_]
        m_str += str(current) + ','
    m_str += str(args[-1])
    return m_str


@cache_json_log
def exponentiation(n: int, m: int) -> int:
    print(f'Вычисляю значение числа {n} в степени {m}')
    res = 1
    for _ in range(m):
        res *= n
    return res

@cache_json_log
def sum_of_num(*args, **kwargs) -> int | float:
    print(f'Вычисляю сумму чисел {args}')
    return sum(args)

print(exponentiation(3, 3))
print(exponentiation(3, 3))
print(exponentiation(3, 4))
print(exponentiation(3, 3))
print(exponentiation(3, 4))
print(exponentiation(4, 3))
print(exponentiation(5, 5))

# print(sum_of_num(1, 2))
# print(sum_of_num(3, 2, 3))
# print(sum_of_num(1, 2))
# print(sum_of_num(4, 2, 3, 5))
# print(sum_of_num(4, 2, 3, 5))

