#!/usr/bin/env python3
"""Lê tools/itens/*.txt, valida e gera:
   itens/<categoria>.json   (um arquivo por categoria, baixado só quando a categoria é sorteada)
   itens/categorias.js      (lista de categorias com nome, emoji, grupo de perguntas e contagem)
Uso: python3 tools/gerar_itens.py"""
import glob, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'itens')
OUT = os.path.join(ROOT, 'itens')
NIVEIS = {'f', 'm', 'd'}
GRUPOS = {'geral', 'vivo', 'comida', 'objeto', 'pessoa', 'lugar', 'obra', 'personagem'}

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\b(o|a|os|as|um|uma|de|do|da|dos|das|e)\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

cats, erros, avisos = {}, [], []
ordem = []
for path in sorted(glob.glob(os.path.join(SRC, '*.txt'))):
    atual = None
    for ln, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        if not line: continue
        if line.startswith('#'):
            parts = [p.strip() for p in line[1:].split('|')]
            if len(parts) == 4 and re.fullmatch(r'[a-z]+', parts[0]):
                key, label, emoji, grupo = parts
                if grupo not in GRUPOS: erros.append(f'{path}:{ln} grupo inválido {grupo}')
                atual = cats.setdefault(key, {'label': label, 'emoji': emoji, 'q': grupo, 'items': []})
                ordem.append(key)
            continue
        if atual is None: erros.append(f'{path}:{ln} item fora de categoria'); continue
        p = [x.strip() for x in line.split('|')]
        if len(p) not in (6, 7): erros.append(f'{path}:{ln} esperado 6 ou 7 campos, veio {len(p)}: {line[:60]}'); continue
        nome, nivel, *hints = p[:6]
        alias = [a.strip() for a in p[6].split(';')] if len(p) == 7 and p[6] else []
        if nivel not in NIVEIS: erros.append(f'{path}:{ln} nível inválido "{nivel}"')
        if any(not h for h in hints): erros.append(f'{path}:{ln} dica vazia')
        n = norm(nome)
        for h in hints:
            if n and len(n) > 2 and re.search(r'\b' + re.escape(n) + r'\b', norm(h)):
                erros.append(f'{path}:{ln} a dica entrega o nome "{nome}": {h}')
        if len(set(norm(h) for h in hints)) < 4: erros.append(f'{path}:{ln} dicas repetidas em {nome}')
        item = {'n': nome, 'd': nivel, 'h': hints}
        alias = [a for a in alias if norm(a) and norm(a) != n]
        if alias: item['a'] = alias
        atual['items'].append(item)

for key, c in cats.items():
    nomes = [norm(i['n']) for i in c['items']]
    dup = {x for x in nomes if nomes.count(x) > 1}
    if dup: erros.append(f'{key}: nomes repetidos {dup}')
    niveis = {lv: sum(1 for i in c['items'] if i['d'] == lv) for lv in 'fmd'}
    if niveis['f'] < 6: avisos.append(f'{key}: poucos itens fáceis ({niveis["f"]})')

if erros:
    print('ERROS:'); [print(' -', e) for e in erros]; sys.exit(1)

os.makedirs(OUT, exist_ok=True)
for key, c in cats.items():
    with open(os.path.join(OUT, key + '.json'), 'w', encoding='utf-8') as f:
        json.dump(c['items'], f, ensure_ascii=False, separators=(',', ':'))
meta = {k: {'label': cats[k]['label'], 'emoji': cats[k]['emoji'], 'q': cats[k]['q'],
            'count': len(cats[k]['items']),
            'f': sum(1 for i in cats[k]['items'] if i['d'] == 'f'),
            'm': sum(1 for i in cats[k]['items'] if i['d'] == 'm'),
            'dd': sum(1 for i in cats[k]['items'] if i['d'] == 'd')} for k in ordem}
with open(os.path.join(OUT, 'categorias.js'), 'w', encoding='utf-8') as f:
    f.write('/* Gerado por tools/gerar_itens.py: não edite à mão. */\n')
    f.write('window.CATEGORIAS = ' + json.dumps(meta, ensure_ascii=False, indent=1) + ';\n')

total = sum(m['count'] for m in meta.values())
for k, m in meta.items(): print(f"{k:12s} {m['count']:4d}  (fácil {m['f']}, médio {m['m']}, difícil {m['dd']})")
print(f'TOTAL {total} itens em {len(meta)} categorias')
for a in avisos: print('aviso:', a)
