with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazamos los fondos oscuros por fondos blancos/grises muy claros
html = html.replace('bg-[#0b192c] text-white', 'bg-white text-slate-800')
html = html.replace('bg-[#06111e]', 'bg-slate-100')
html = html.replace('bg-[#1e3e62]', 'bg-white shadow-md')
html = html.replace('bg-[#132f4c]', 'bg-slate-50')
html = html.replace('border-blue-900/50', 'border-slate-200')
html = html.replace('border-blue-800/40', 'border-slate-200')
html = html.replace('hover:border-blue-500', 'hover:border-blue-400')
html = html.replace('text-blue-400', 'text-blue-600')
html = html.replace('text-blue-300', 'text-blue-600')
html = html.replace('bg-[#007acc]', 'bg-blue-600 text-white')
html = html.replace('hover:bg-[#0062a3]', 'hover:bg-blue-700')
html = html.replace('focus:ring-blue-400', 'focus:ring-blue-500')
html = html.replace('border-blue-500', 'border-blue-500')

# Ajustes generales para textos que antes eran blancos y ahora deben ser oscuros sobre fondo blanco
html = html.replace('text-white', 'text-slate-900')
html = html.replace('text-slate-100', 'text-slate-800')
html = html.replace('text-slate-300', 'text-slate-600')
html = html.replace('text-slate-400', 'text-slate-500')

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Fondo del frontend cambiado a blanco con éxito!")
