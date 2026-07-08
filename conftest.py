"""Configuración global de pytest para el backend del portafolio.

Fuerza SQLite en los tests independientemente de que el entorno defina
DATABASE_URL (settings.testing ya usa SQLite en memoria; esto es defensa en
profundidad para que la suite nunca golpee una base real).
"""
import os

os.environ.pop('DATABASE_URL', None)
