from escpos.printer import Win32Raw
 # para convertir fecha si usas timezone



printer = Win32Raw("POS")
          # Cerrar la impresora antes de abrirla de nuevo

printer.text("\n\n\n\n\n\nhikavhhvhvhvhvhvhvhvhvhvhvhvhv")
printer.cashdraw(2)
printer.close()  # Cerrar la impresora
print("Factura impresa exitosamente.")

