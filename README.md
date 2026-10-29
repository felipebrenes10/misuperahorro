# MiSúperAhorro — actualización diaria gratuita

La web se alimenta de `data/prices.json`, generado por GitHub Actions a partir del CSV público de bajadas de CholloSúper. **Solo contiene bajadas del día**, no todo el catálogo. Los precios son de referencia; **no se han verificado en Brenes**. DIA usa una zona de Cataluña según CholloSúper. Fuente: https://chollosuper.com/datos (CC BY 4.0).

## Ponerlo en marcha, sin pagar

1. Crea una cuenta en https://github.com si no tienes una.
2. Haz clic en **New repository**; nómbralo `misuperahorro` y elige **Public**. No marques la opción de crear README (ya lo incluye el ZIP).
3. Abre el repositorio y elige **Add file > Upload files**. Sube el contenido **de la carpeta** `MiSuperAhorro_Automatico` (incluye `index.html`, `data/prices.json`, `scripts/actualizar.py` y `.github/workflows/actualizar-precios.yml`). **Atención:** al subir archivos desde el navegador, GitHub puede no mantener carpetas ocultas correctamente: comprueba que se ha subido exactamente `.github/workflows/actualizar-precios.yml`. La alternativa más fiable es usar GitHub Desktop para publicar la carpeta completa.
4. En **Settings > Pages**, selecciona **Deploy from a branch**, rama `main` y carpeta `/(root)`; pulsa **Save**. La web estará en `https://TUUSUARIO.github.io/misuperahorro/` tras la publicación.
5. En **Actions > Actualizar precios CholloSúper**, pulsa **Run workflow** para la primera descarga. Si no aparece, revisa que el archivo YAML esté en `.github/workflows/` y que Actions estén habilitadas.
6. Abre `https://TUUSUARIO.github.io/misuperahorro/data/prices.json` y comprueba que `items` tiene elementos y `updated_at` una fecha. Recarga la web: verás un mensaje con la cantidad de precios cargados.
7. La tarea se programa a las **10:20 UTC cada día** (GitHub Actions puede retrasarla). Si la descarga falla, se conserva el último archivo y tendrás que revisar la pestaña **Actions**.

## Importante

- Un HTML abierto directamente con doble clic **no puede leer automáticamente** el archivo como si fuese una web publicada; prueba la versión publicada en GitHub Pages o usa un servidor local (`python -m http.server 8000`).
- Las ofertas del CSV de bajadas no son un catálogo completo ni garantizan stock o promociones locales en Brenes.
- En `data/prices.json` se publica un archivo inicial **vacío** hasta la primera ejecución satisfactoria.
- Los precios añadidos manualmente siguen siendo locales a tu navegador; para una administración común necesitaríamos una base de datos/autenticación.
- Los repositorios públicos de GitHub y las páginas públicas no son adecuados para datos privados.
- Si la sección **Actions** pide activar permisos de escritura: **Settings > Actions > General > Workflow permissions > Read and write permissions**. GitHub Pages gratuito depende de la disponibilidad del plan y de las condiciones vigentes de GitHub.
