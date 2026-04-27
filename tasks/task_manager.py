
# Input: [70, 80, 90]
# Output: 80 
from collections import Counter
import math


def calculate_mean(scores: list) -> float:
    """Öğrencilerin notlarının ortalamasını hesapla."""
    return sum(scores) / len(scores)

#Input: [70, 80, 90, 100] 
# Output: 85.0 
def calculate_median(scores: list) -> float:
    """Öğrencilerin notlarının medyanını hesapla."""
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_scores[mid - 1] + sorted_scores[mid]) / 2
    return sorted_scores[mid]

#Input: [70, 70, 80, 90] 
# Output: 70
def calculate_mode(scores: list) -> int:
    """En sık görülen notu hesapla (mode)."""
    counts = Counter(scores)
    max_freq = max(counts.values())

    for num in scores:
        if counts[num] == max_freq:
            return num

#Input: [10, 20, 30]
#Output: 8.16
def calculate_std(scores: list) -> float:
    """Standart sapmayı hesapla."""
    mean = calculate_mean(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    return round(math.sqrt(variance), 2)

#Input: [10, 10, 10, 80] ise output median olmalı
#Input: [1,1,1,1] ise output mode
#Input: [10,15,20,25] ise output mean olmalı.
#Hardcoded bir şey olmamalı. Data içeriğine bakarak bu 3 hesaplamadan hangisini yapabileceğine bir kural ile kara vermelisin.
def determine_best_statistic(data: list) -> str:
    """Veri kümesine göre en uygun merkezi eğilim ölçüsünü seç ('mean', 'median' ya da 'mode')."""
    if len(set(data)) == 1:
        return "mode"
    
    mean = calculate_mean(data)
    median = calculate_median(data)
    std = calculate_std(data)

    outliers = find_outliers(data)
    if outliers:
        return "median"

    counts = Counter(data)
    if max(counts.values()) > 1:
        return "mode"

    return "mean"

#Input: ([10, 20, 30, 40, 50], 50) 
#Output: 30
def calculate_percentile(scores: list, percentile: float) -> float:
    """Belirli bir persentil değerini hesapla (örn. 90. persentil)."""
    sorted_scores = sorted(scores)
    k = (len(sorted_scores) - 1) * (percentile / 100)
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_scores[int(k)]

    d0 = sorted_scores[f] * (c - k)
    d1 = sorted_scores[c] * (k - f)
    return d0 + d1

#Input: ([10, 20, 30, 40, 50])
#Output: (20.0, 30.0, 40.0)
def calculate_quartiles(scores: list) -> tuple:
    """Q1, Q2, Q3 çeyrek değerlerini hesapla."""
    q1 = calculate_percentile(scores, 25)
    q2 = calculate_percentile(scores, 50)
    q3 = calculate_percentile(scores, 75)
    return (q1, q2, q3)

#Input: [10, 12, 14, 100]
#Output: [100]
# Bu işlemi yapmak için iqr dediğimiz bir hesaplama kullanmalısın. 
# iqr = q3-q1(q: quartile)
# Daha sonrasonda lower ve upper adında iki tane değişken tanımlamalısın. 
# lower = q1 - 1.5 * iqr, upper = q3 + 1.5 * iqr
# eğer dizideki elemanlar bu lower ve higher değerleri arasındaysa outlier değildirler.
def find_outliers(scores: list) -> list:
    """IQR kullanarak aykırı değerleri tespit et."""
    q1, _, q3 = calculate_quartiles(scores)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return [x for x in scores if x < lower or x > upper]


#Input: 
    # data = {
    #         'Gryffindor': [80, 85, 90],
    #         'Slytherin': [60, 65, 70]
    # }
#Output: 
    # {
    #   'Gryffindor': 85.0,
    #   'Slytherin': 65.0
    # }
def house_score_summary(house_scores: dict) -> dict:
    """Her bir grup (Gryffindor, Slytherin vb.) için ortalama ve medyan notları döndür."""
    return {
        house: {
            "mean": calculate_mean(scores),
            "median": calculate_median(scores)
        }
        for house, scores in house_scores.items()
    }


#Input:
#  data = {
#         'Gryffindor': [80, 85, 90],
#         'Slytherin': [60, 65, 70]
# }
#Output: 'Gryffindor'
def find_top_house(house_scores: dict) -> str:
    """En yüksek ortalamaya sahip grubu döndür."""
    return max(
        house_scores,
        key=lambda house: calculate_mean(house_scores[house])
    )