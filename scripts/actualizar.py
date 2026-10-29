#!/usr/bin/env python3
"""Importa el CSV abierto de CholloSúper para publicar bajadas recientes."""
import csv
import io
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen, Request

SOURCE = 'https://chollosuper.com/datos/bajadas.csv'
OUTPUT = Path(__file__).resolve().parents[1] / 'data' / 'prices.json'

def parse(content):
    content=content.lstrip('\ufeff')
    delimiter=';' if content.partition('\n')[0].count(';') > content.partition('\n')[0].count(',') else ','
    reader=csv.DictReader(io.StringIO(content), delimiter=delimiter)
    if not reader.fieldnames: raise ValueError('CSV sin encabezados')
    names={x.lower().strip().replace(' ','').replace('_',''):x for x in reader.fieldnames}
    def get(row,*keys):
        for k in keys:
            if k in names:return (row.get(names[k]) or '').strip()
        return ''
    out={}
    for row in reader:
        raw=get(row,'cadena','supermercado')
        store='Mercadona' if 'mercadona' in raw.casefold() else 'DIA' if raw.strip().casefold() in ('dia','día') else None
        if not store:continue
        product=get(row,'producto','nombre')
        size=get(row,'tamano','formato','cantidad') or 'Formato no especificado'
        raw_price=get(row,'precioeur','precio','precionuevo')
        try:price=float(raw_price.replace('€','').replace(' ','').replace(',','.'))
        except ValueError:continue
        if not (0<price<=10000 and 0<len(product)<160 and len(size)<100):continue
        date=get(row,'dia','fecha')
        try: date=datetime.strptime(date[:10],'%Y-%m-%d').date().isoformat()
        except ValueError:continue
        # bajadas.csv is a daily snapshot: never silently assert local availability.
        url=get(row,'url','enlace')
        key=(product.casefold(),size.casefold(),store)
        out[key]={'id':f'chollo-{len(out)+1}', 'name':product,'size':size,'store':store,'price':price,
                  'date':date,'type':'regular','end':'','demo':False,'source':'CholloSúper (CC BY 4.0) · referencia no verificada en Brenes',
                  'product_url':url,'region':'Referencia online; DIA: Granollers/Cataluña por defecto','origin':'chollosuper'}
    return list(out.values())

def main():
    fixture=os.environ.get('CHOLLO_CSV_FILE')
    if fixture: csv_text=Path(fixture).read_text(encoding='utf-8-sig')
    else:
        req=Request(SOURCE,headers={'User-Agent':'MiSuperAhorro/1.0 (CSV público; atribución en web)','Accept':'text/csv,*/*'})
        with urlopen(req,timeout=30) as resp:csv_text=resp.read().decode('utf-8-sig')
    items=parse(csv_text)
    if not items:raise RuntimeError('No hay registros válidos de DIA ni Mercadona; se conserva el último fichero.')
    dates={p['date'] for p in items}
    today=datetime.now(timezone.utc).date()
    newest=max(datetime.fromisoformat(d).date() for d in dates)
    if (today-newest).days > 3:raise RuntimeError('CSV demasiado antiguo; no se sobrescriben precios existentes.')
    payload={'source':'CholloSúper','source_url':'https://chollosuper.com/datos','license':'CC BY 4.0',
             'updated_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'price_date':newest.isoformat(),
             'scope':'Precios de referencia, no comprobados en Brenes. DIA: Granollers/Cataluña por defecto.',
             'kind':'bajadas_del_dia_no_catalogo_completo','items':items}
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Escritos {len(items)} precios de referencia ({newest}) en {OUTPUT}')

if __name__=='__main__':main()
