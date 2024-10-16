import os
import pandas as pd
import time
import matplotlib.pyplot as plt

# Implementación de TimSort (nativo en Python)
def tim_sort(arr):
    return sorted(arr)

# Implementación de Comb Sort
def getNextGap(gap):
    gap = (gap * 10) // 13
    if gap < 1:
        return 1
    return gap

def comb_sort(arr):
    n = len(arr)
    gap = n
    swapped = True
    while gap != 1 or swapped:
        gap = getNextGap(gap)
        swapped = False
        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    return arr

# Implementación de Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Implementación de Tree Sort
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root

def inorder_traversal(root, res):
    if root:
        inorder_traversal(root.left, res)
        res.append(root.val)
        inorder_traversal(root.right, res)

def tree_sort(arr):
    if not arr:
        return arr
    root = None
    for key in arr:
        root = insert(root, key)
    sorted_arr = []
    inorder_traversal(root, sorted_arr)
    return sorted_arr

# Implementación de Pigeonhole Sort basado en el tamaño de las cadenas
def pigeonhole_sort_tamanio(arr):
    # Usar el tamaño de las cadenas como clave
    arr_tamanios = [len(cadena) for cadena in arr]
    
    my_min = min(arr_tamanios)
    my_max = max(arr_tamanios)
    size = my_max - my_min + 1
    holes = [0] * size

    # Contar ocurrencias
    for tamanio in arr_tamanios:
        holes[tamanio - my_min] += 1

    # Reconstruir el arreglo ordenado
    sorted_arr = []
    for i in range(size):
        while holes[i] > 0:
            # Encontrar la cadena correspondiente al tamaño ordenado
            for cadena in arr:
                if len(cadena) == i + my_min:
                    sorted_arr.append(cadena)
                    holes[i] -= 1
                    break
    return sorted_arr

# Implementación de Bucket Sort
def insertion_sort_bucket(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and key < bucket[j]:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket

def bucket_sort_tamanio(arr):
    # Usamos el tamaño de las cadenas como criterio
    arr_tamanios = [len(cadena) for cadena in arr]
    max_val = max(arr_tamanios)
    min_val = min(arr_tamanios)
    range_val = max_val - min_val + 1
    
    # Crear cubos
    num_buckets = len(arr)  # El número de cubos es igual al número de elementos
    buckets = [[] for _ in range(num_buckets)]
    
    # Asignar las cadenas a los cubos
    for cadena in arr:
        index = (len(cadena) - min_val) * num_buckets // range_val
        buckets[index].append(cadena)
    
    # Ordenar los cubos individualmente
    for bucket in buckets:
        bucket.sort()
    
    # Concatenar los cubos ordenados
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    
    return sorted_arr


# Implementación de QuickSort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Implementación de HeapSort
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

# Implementación de Gnome Sort
def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

# Implementación de Binary Insertion Sort
def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if arr[mid] < val:
        return binary_search(arr, val, mid + 1, end)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid - 1)
    else:
        return mid

def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]
    return arr

# Implementación de Radix Sort
def radix_sort(arr):
    # Convertir cada cadena a su tamaño (longitud)
    arr_tamanios = [len(cadena) for cadena in arr]
    max1 = max(arr_tamanios)
    exp = 1
    while max1 // exp > 0:
        counting_sort_tamanio(arr, arr_tamanios, exp)
        exp *= 10
    return arr
# Implementación de Bitonic Sort
def compAndSwap(arr, i, j, dire):
    if (dire == 1 and arr[i] > arr[j]) or (dire == 0 and arr[i] < arr[j]):
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
        bitonicSort(arr, low, k, 1)  # Ordenar en orden ascendente
        bitonicSort(arr, low + k, k, 0)  # Ordenar en orden descendente
        bitonicMerge(arr, low, cnt, dire)

def sort_bitonic(arr):
    n = len(arr)
    bitonicSort(arr, 0, n, 1)
    return arr

# Función auxiliar de Counting Sort para Radix Sort adaptado
def counting_sort_tamanio(arr, arr_tamanios, exp):
    n = len(arr)
    output = [0] * n
    output_strings = [""] * n
    count = [0] * 10

    # Contar las ocurrencias basadas en el dígito correspondiente
    for i in range(n):
        index = arr_tamanios[i] // exp
        count[(index % 10)] += 1

    # Modificar count para que contenga la posición de salida
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir el arreglo de salida
    i = n - 1
    while i >= 0:
        index = arr_tamanios[i] // exp
        output[count[(index % 10)] - 1] = arr_tamanios[i]
        output_strings[count[(index % 10)] - 1] = arr[i]
        count[(index % 10)] -= 1
        i -= 1

    # Copiar el contenido de output_strings a arr
    for i in range(n):
        arr[i] = output_strings[i]

# Función auxiliar para medir el tiempo de los algoritmos
def medir_tiempo(algoritmo, data):
    start_time = time.time()
    sorted_data = algoritmo(data)
    end_time = time.time()
    return sorted_data, end_time - start_time

# Función principal para el seguimiento
def seguimiento_ordenamiento(archivo_csv):
    df = pd.read_csv(archivo_csv)
    data = df["Titulo"].dropna().tolist()  # Cambiamos a la columna "Titulo"

    # Diccionario de algoritmos
    algoritmos = {
        "TimSort": tim_sort,
        "CombSort": comb_sort,
        "SelectionSort": selection_sort,
        "TreeSort": tree_sort,
        "PigeonholeSort (Adaptado por tamaño)": pigeonhole_sort_tamanio,  # Pigeonhole Sort adaptado por tamaño
        "BucketSort (Adaptado por tamaño)": bucket_sort_tamanio,  # Bucket Sort adaptado por tamaño
        "QuickSort": quick_sort,
        "HeapSort": heap_sort,
        "GnomeSort": gnome_sort,
        "BinaryInsertionSort": binary_insertion_sort,
        "RadixSort": radix_sort,
        "BitonicSort": sort_bitonic
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
        df_ordenado = pd.DataFrame(sorted_data, columns=["Titulo"])
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
    archivo_csv = "unified_articles.csv"  # Reemplazar con la ruta de tu archivo CSV
    resultados = seguimiento_ordenamiento(archivo_csv)

