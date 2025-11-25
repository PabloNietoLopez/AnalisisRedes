from estructura import analizador
from informe import generar_informe


def main():
    analizador.analizar_estructura()
    generar_informe.generar_informe_completo()


if __name__ == "__main__":
    main()
