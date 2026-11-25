#!/usr/bin/env python3
"""Consulta a base cClassTrib da Treeunfe (fonte: Receita Federal, calculadora RTC).

Uso:
  consulta_ncm.py 10063021 22030000 ...        # consulta por NCM (8 digitos)
  consulta_ncm.py --buscar arroz polido        # busca NCMs pela descricao
  consulta_ncm.py --lote ncms.txt              # um NCM por linha
  consulta_ncm.py --versao                     # versao da base em uso
Saida: JSON no stdout. A base e baixada uma vez e fica em cache (renovada se o
latest.json apontar outra versao).
"""
import json, os, re, sys, unicodedata, urllib.request

BASE_URL = "https://d1c2gtb75fe4co.cloudfront.net/cclasstrib/"
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "treeunfe-cclasstrib")


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "treeunfe-skill/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def carregar():
    os.makedirs(CACHE, exist_ok=True)
    try:
        ptr = json.loads(_get(BASE_URL + "latest.json"))
        arq = ptr["arquivo"]
    except Exception as e:  # offline: usa o que houver em cache
        cached = sorted(f for f in os.listdir(CACHE) if f.startswith("ncm-cclasstrib-"))
        if not cached:
            sys.exit(f"Sem acesso a base e sem cache: {e}")
        arq = cached[-1]
    path = os.path.join(CACHE, arq)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(_get(BASE_URL + arq))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def nome_completo(db, ncm):
    partes = []
    for n in (2, 4, 5, 6, 7):
        t = db["hier"].get(ncm[:n])
        if t:
            partes.append(t.rstrip("."))
    d = db["ncm"].get(ncm, {}).get("d", "")
    if d:
        partes.append(d.rstrip("."))
    return " > ".join(partes)


def consultar(db, ncm):
    ncm = re.sub(r"\D", "", ncm)
    if len(ncm) != 8:
        return {"ncm": ncm, "valido": False, "motivo": "NCM deve ter 8 digitos"}
    e = db["ncm"].get(ncm)
    if e is None:
        return {"ncm": ncm, "valido": False,
                "motivo": "NCM inexistente ou nao vigente na data de referencia da base"}
    out = {"ncm": ncm, "valido": True, "descricao": nome_completo(db, ncm),
           "imposto_seletivo": bool(e.get("is")), "candidatas": []}
    for opc in e.get("c", []):
        cod, itens = (opc, []) if isinstance(opc, str) else (opc[0], opc[1:])
        cc = db["cclass"].get(cod, {})
        out["candidatas"].append({
            "cClassTrib": cod, "CST": cc.get("cst"), "cstDesc": cc.get("cstDesc"),
            "descricao": cc.get("desc"), "reducao": cc.get("red"),
            "artigo": (cc.get("fund") or {}).get("art"),
            "itens_anexo": [{"item": i, "texto": db["anexos"].get(i)} for i in itens],
        })
    if not out["candidatas"]:
        out["regra_geral"] = {"CST": "000", "cClassTrib": "000001",
                              "descricao": "Tributacao integral (regra geral)"}
    return out


def buscar(db, termos, limite=40):
    alvo = [norm(t) for t in termos]
    achados = []
    for ncm in db["ncm"]:
        txt = norm(nome_completo(db, ncm))
        if all(t in txt for t in alvo):
            achados.append({"ncm": ncm, "descricao": nome_completo(db, ncm),
                            "opcoes": len(db["ncm"][ncm].get("c", []))})
            if len(achados) >= limite:
                break
    return achados


def main(a):
    if not a:
        sys.exit(__doc__)
    db = carregar()
    if a[0] == "--versao":
        r = {"versao": db["versaoBase"], "dataReferencia": db["dataReferencia"]}
    elif a[0] == "--buscar":
        r = buscar(db, a[1:])
    elif a[0] == "--lote":
        with open(a[1]) as f:
            r = [consultar(db, l.strip()) for l in f if l.strip()]
    else:
        r = [consultar(db, x) for x in a]
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
