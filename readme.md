# Proyecto: Practica 2 Grupo 7

Este proyecto incluye pruebas unitarias utilizando `unittest` y reportes de cobertura con `coverage` para Python.

---

## Instrucciones para Python

### 1. Instalación de dependencias coverage


Para ejecutar las pruebas y obtener reportes de cobertura, necesitas instalar las siguientes herramientas utilizando `pip`:

pip install coverage
### 2. Importación de Unittest
unittest es el módulo de pruebas unitarias integrado en Python, por lo que no requiere instalación adicional. Solo necesitas importarlo en tu código para empezar a escribir y ejecutar las pruebas.
 import unittest

### 3. Ejecutar pruebas con unittest
Para ejecutar las pruebas definidas en el archivo tests/test_AgenteBot.py, utiliza el siguiente comando:
### python -m unittest tests/test_AgenteBot.py

### Ejecutar pruebas con coverage.py
Para ejecutar pruebas con cobertura usando coverage
### coverage run -m unittest tests/test_AgenteBot.py

### Generar Reporte
Para ver los resultados de la cobertura en la terminal
### coverage report
### Generar un reporte de cobertura en HTML
### coverage html

