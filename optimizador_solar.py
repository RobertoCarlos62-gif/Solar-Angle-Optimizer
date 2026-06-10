import math
import os
from datetime import datetime

def calcular_declinacion_solar(dia_ano):
    """Calcula la declinación solar para un día del año específico (n)."""
    # Fórmula de Cooper (1969)
    return 23.45 * math.sin(math.radians((360 / 365) * (284 + dia_ano)))

def optimizar_angulos(latitud):
    """Calcula la inclinación óptima mensual para una latitud dada."""
    # Días promedio recomendados para cada mes (representativos)
    dias_medios_mes = {
        "Enero": 17, "Febrero": 47, "Marzo": 75, "Abril": 105,
        "Mayo": 135, "Junio": 162, "Julio": 198, "Agosto": 228,
        "Septiembre": 258, "Octubre": 288, "Noviembre": 318, "Diciembre": 344
    }
    
    resultados = {}
    es_hemisferio_norte = latitud >= 0
    lat_absoluta = abs(latitud)

    for mes, dia in dias_medios_mes.items():
        declinacion = calcular_declinacion_solar(dia)
        
        # Inclinación teórica ideal para el mediodía solar
        if es_hemisferio_norte:
            angulo_ideal = lat_absoluta - declinacion
        else:
            angulo_ideal = lat_absoluta + declinacion
            
        # Restricciones físicas: el ángulo no puede ser negativo ni mayor a 90°
        angulo_ideal = max(0, min(90, angulo_ideal))
        resultados[mes] = round(angulo_ideal, 2)
        
    return resultados

def generar_reporte(latitud, resultados):
    """Genera un archivo de texto con el reporte de ingeniería."""
    nombre_archivo = f"Reporte_Solar_Latitud_{latitud}.txt"
    orientacion = "Sur" if latitud >= 0 else "Norte"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("    REPORTE DE OPTIMIZACIÓN DE ENERGÍA SOLAR      \n")
        f.write("==================================================\n")
        f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Latitud analizada: {latitud}°\n")
        f.write(f"Orientación recomendada de los paneles: Hacia el {orientacion}\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Mes':<15} | {'Ángulo de Inclinación Óptimo':<30}\n")
        f.write("--------------------------------------------------\n")
        
        for mes, angulo in resultados.items():
            f.write(f"{mes:<15} | {angulo:<30}°\n")
            
        f.write("==================================================\n")
        f.write("Nota: Ajustar los paneles al menos 4 veces al año\n")
        f.write("(Estaciones) mejora la eficiencia en un 15-20%.\n")
        
    print(f"\n✅ ¡Reporte guardado con éxito como '{nombre_archivo}'!")

def main():
    print("--- SIMULADOR DE OPTIMIZACIÓN SOLAR (INGENIERÍA) ---")
    print("Este programa calcula la inclinación ideal de paneles fotovoltaicos.")
    
    try:
        latitud = float(input("Introduce la latitud de la ubicación (Ej: 19.43 para CDMX, -34.60 para Buenos Aires): "))
        if not (-90 <= latitud <= 90):
            print("❌ Error: La latitud debe estar entre -90 y 90 grados.")
            return
            
        print("\nProcesando datos geográficos...")
        angulos_mes = optimizar_angulos(latitud)
        
        print("\n--- RESULTADOS RECOMENDADOS ---")
        for mes, angulo in angulos_mes.items():
            print(f"📌 {mes:<12}: {angulo}°")
            
        generar_reporte(latitud, angulos_mes)
        
    except ValueError:
        print("❌ Error: Por favor introduce un número válido para la latitud.")

if __name__ == "__main__":
    main()
