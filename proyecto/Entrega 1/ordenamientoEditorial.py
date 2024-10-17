import os
import pandas as pd
import time
import re
import matplotlib.pyplot as plt

# Función para limpiar las cadenas y dejar solo letras, números, - y _
def limpiar_cadena(cadena):
    return re.sub(r'[^a-zA-Z0-9-_]', '', cadena)

# Implementación de TimSort (nativo en Python)
def tim_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    return sorted(arr, key=lambda x: ord(x[0]))

# Implementación de Comb Sort
def getNextGap(gap):
    gap = (gap * 10) // 13
    if gap < 1:
        return 1
    return gap

def comb_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    n = len(arr)
    gap = n
    swapped = True
    while gap != 1 or swapped:
        gap = getNextGap(gap)
        swapped = False
        for i in range(0, n - gap):
            if ord(arr[i][0]) > ord(arr[i + gap][0]):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    return arr

# Implementación de Selection Sort
def selection_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if ord(arr[j][0]) < ord(arr[min_idx][0]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Implementación iterativa de Tree Sort para evitar desbordamiento
class TreeNode:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

def insert_iter(root, key):
    new_node = TreeNode(key)
    if root is None:
        return new_node
    current = root
    while True:
        if ord(key[0]) < ord(current.val[0]):
            if current.left is None:
                current.left = new_node
                break
            else:
                current = current.left
        elif ord(key[0]) > ord(current.val[0]):
            if current.right is None:
                current.right = new_node
                break
            else:
                current = current.right
        else:
            # Compara más allá del primer carácter si son iguales
            if key < current.val:
                if current.left is None:
                    current.left = new_node
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                else:
                    current = current.right
    return root

def inorder_traversal(root, res):
    stack = []
    current = root
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        res.append(current.val)
        current = current.right

def tree_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    if not arr:
        return arr
    root = None
    for key in arr:
        root = insert_iter(root, key)
    sorted_arr = []
    inorder_traversal(root, sorted_arr)
    return sorted_arr

# Implementación de Bucket Sort por primer carácter ASCII
def insertion_sort_bucket(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and ord(bucket[j][0]) > ord(key[0]):
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket

def bucket_sort_ascii(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    num_buckets = 256  # Basado en los caracteres ASCII
    buckets = [[] for _ in range(num_buckets)]

    for cadena in arr:
        ascii_val = ord(cadena[0])
        buckets[ascii_val].append(cadena)

    for i in range(num_buckets):
        buckets[i] = insertion_sort_bucket(buckets[i])

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr

# Implementación de QuickSort
def quick_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if ord(x[0]) < ord(pivot[0])]
    middle = [x for x in arr if ord(x[0]) == ord(pivot[0])]
    right = [x for x in arr if ord(x[0]) > ord(pivot[0])]
    return quick_sort(left) + middle + quick_sort(right)

# Implementación de Pigeonhole Sort
def pigeonhole_sort(arr):
    # Limpiar las cadenas antes de ordenar
    arr = [limpiar_cadena(cadena) for cadena in arr]
    
    # Encuentra el mínimo y el máximo valor en el primer carácter ASCII de las cadenas
    my_min = min(ord(cadena[0]) for cadena in arr)
    my_max = max(ord(cadena[0]) for cadena in arr)
    
    # Calcula el rango de valores
    size = my_max - my_min + 1
    
    # Lista de "pigeonholes" o huecos
    holes = [[] for _ in range(size)]
    
    # Distribuir las cadenas en sus respectivos huecos
    for cadena in arr:
        index = ord(cadena[0]) - my_min
        holes[index].append(cadena)
    
    # Recoger las cadenas ordenadas
    sorted_arr = []
    for hole in holes:
        sorted_arr.extend(hole)
    
    return sorted_arr


# Implementación de HeapSort
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and ord(arr[l][0]) > ord(arr[largest][0]):
        largest = l

    if r < n and ord(arr[r][0]) > ord(arr[largest][0]):
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

# Implementación de Gnome Sort
def gnome_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    index = 0
    while index < len(arr):
        if index == 0 or ord(arr[index][0]) >= ord(arr[index - 1][0]):
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

# Implementación de Binary Insertion Sort
def binary_search(arr, val, start, end):
    if start == end:
        if ord(arr[start][0]) > ord(val[0]):
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if ord(arr[mid][0]) < ord(val[0]):
        return binary_search(arr, val, mid + 1, end)
    elif ord(arr[mid][0]) > ord(val[0]):
        return binary_search(arr, val, start, mid - 1)
    else:
        return mid

def binary_insertion_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]
    return arr

# Implementación de Bitonic Sort
def compAndSwap(arr, i, j, dire):
    if (dire == 1 and ord(arr[i][0]) > ord(arr[j][0])) or (dire == 0 and ord(arr[i][0]) < ord(arr[j][0])):
        arr[i], arr[j] = arr[j], arr[i]

def bitonicMerge(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compAndSwap(arr, i, i + k, dire)
        bitonicMerge(arr, low, k, dire)
        bitonicMerge(arr, low + k, k, dire)

def bitonicSort(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        bitonicSort(arr, low, k, 1)
        bitonicSort(arr, low + k, k, 0)
        bitonicMerge(arr, low, cnt, dire)

def sort_bitonic(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    n = len(arr)
    bitonicSort(arr, 0, n, 1)
    return arr

# Implementación de Radix Sort adaptado para cadenas
def radix_sort(arr):
    arr = [limpiar_cadena(cadena) for cadena in arr]
    arr_tamanios = [len(cadena) for cadena in arr]
    max1 = max(arr_tamanios)
    exp = 1
    while max1 // exp > 0:
        counting_sort_tamanio(arr, arr_tamanios, exp)
        exp *= 10
    return arr

# Función auxiliar de Counting Sort para Radix Sort adaptado
def counting_sort_tamanio(arr, arr_tamanios, exp):
    n = len(arr)
    output_strings = [""] * n
    count = [0] * 10

    for i in range(n):
        index = arr_tamanios[i] // exp
        count[(index % 10)] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr_tamanios[i] // exp
        output_strings[count[(index % 10)] - 1] = arr[i]
        count[(index % 10)] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output_strings[i]

# Función auxiliar para medir el tiempo de los algoritmos
def medir_tiempo(algoritmo, data):
    start_time = time.time()
    sorted_data = algoritmo(data)
    end_time = time.time()
    return sorted_data, end_time - start_time

def seguimiento_ordenamiento(archivo_csv):
    df = pd.read_csv(archivo_csv)
    data = df["Editorial"].dropna().tolist()  # Se utiliza la columna "Editorial"

    # Diccionario de algoritmos
    algoritmos = {
        "TimSort": tim_sort,
        "CombSort": comb_sort,
        "SelectionSort": selection_sort,
        "TreeSort": tree_sort,
        "BucketSort ASCII": bucket_sort_ascii,
        "QuickSort": quick_sort,
        "HeapSort": heap_sort,
        "GnomeSort": gnome_sort,
        "BinaryInsertionSort": binary_insertion_sort,
        "RadixSort": radix_sort,
        "BitonicSort": sort_bitonic,
        "PigeonholeSort": pigeonhole_sort
    }

    # Aplicar cada algoritmo y medir el tiempo
    resultados = {}
    tiempos = []
    for nombre, algoritmo in algoritmos.items():
        sorted_data, tiempo = medir_tiempo(algoritmo, data.copy())
        resultados[nombre] = {"Tiempo": tiempo, "Datos Ordenados": sorted_data}
        tiempos.append((nombre, tiempo))
        print(f"{nombre}: {tiempo} segundos")
        
        # Guardar resultados en la carpeta 'resultados'
        if not os.path.exists('resultados'):
            os.makedirs('resultados')
        df_ordenado = pd.DataFrame(sorted_data, columns=["Editorial"])
        df_ordenado.to_csv(f"resultados/{nombre}_ordenado.csv", index=False)
        print(f"Archivo {nombre}_ordenado.csv guardado.")
    
    # Generar el diagrama de tiempos
    generar_diagrama(tiempos)
    return resultados

def generar_diagrama(tiempos):
    nombres = [t[0] for t in tiempos]
    valores = [t[1] for t in tiempos]

    plt.figure(figsize=(10, 5))
    plt.bar(nombres, valores, color='skyblue')
    plt.xlabel('Algoritmos de Ordenamiento')
    plt.ylabel('Tiempo de Ejecución (segundos)')
    plt.title('Comparación de Algoritmos de Ordenamiento')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('comparacion_algoritmos_ordenamiento.png')
    plt.show()
    print("Diagrama de tiempos guardado como 'comparacion_algoritmos_ordenamiento.png'.")

if __name__ == "__main__":
    archivo_csv = "unified_articles.csv"  
    resultados = seguimiento_ordenamiento(archivo_csv)

