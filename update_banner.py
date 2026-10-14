with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazamos el texto antiguo de Chubb por un mensaje de movilidad eléctrica
old_banner = "Agrega Chubb Travel Care+ y Participa para ganar un pase doble para la carrera automovilística más importante del año"
new_banner = "⚡ Descubre el futuro de la movilidad eléctrica: cero emisiones, autonomía superior y la mejor experiencia en renta de autos sustentables."

html = html.replace(old_banner, new_banner)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Banner actualizado con éxito!")
