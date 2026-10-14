with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazamos los fondos y acentos oscuros/grises por los tonos azules corporativos originales
# Fondo principal de negro/gris oscuro a azul marino profundo (#0f172a / #1e293b / #0284c7)
html = html.replace('bg-slate-900 text-slate-100', 'bg-[#0b192c] text-white')
html = html.replace('bg-slate-950', 'bg-[#06111e]')
html = html.replace('bg-slate-850', 'bg-[#1e3e62]')
html = html.replace('bg-slate-800', 'bg-[#1e3e62]')
html = html.replace('bg-slate-900/60', 'bg-[#132f4c]')
html = html.replace('border-slate-800', 'border-blue-900/50')
html = html.replace('border-slate-700', 'border-blue-800/40')
html = html.replace('hover:border-slate-600', 'hover:border-blue-500')
html = html.replace('text-amber-500', 'text-blue-400')
html = html.replace('text-amber-400', 'text-blue-300')
html = html.replace('bg-amber-500', 'bg-[#007acc]')
html = html.replace('hover:bg-amber-400', 'hover:bg-[#0062a3]')
html = html.replace('focus:ring-amber-400', 'focus:ring-blue-400')
html = html.replace('border-amber-500', 'border-blue-500')

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Diseño original en tonos azules restaurado con éxito en el frontend!")
