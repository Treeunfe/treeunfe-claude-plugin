#!/usr/bin/env python3
"""Utilitarios de CEP para a skill corrigir-cep-clientes.

Uso:
  cep_utils.py CEP[:UF] ...            # ex.: 01310100:SP  13010-010:MG
  cep_utils.py --online CEP[:UF] ...   # tambem consulta o ViaCEP (envia o CEP a um servico externo!)
Saida: JSON. Verificacoes OFFLINE: formato (8 digitos, nao zerado) e coerencia da
UF com a faixa nacional de CEP. A faixa e indicativa: divergencia = "revisar",
nao prova de erro. Consulta online so com autorizacao do usuario.
"""
import json, re, sys, urllib.request

# Faixas de CEP por UF (prefixo de 5 digitos, inclusive).
FAIXAS = [
    ("SP", 1000, 19999), ("RJ", 20000, 28999), ("ES", 29000, 29999),
    ("MG", 30000, 39999), ("BA", 40000, 48999), ("SE", 49000, 49999),
    ("PE", 50000, 56999), ("AL", 57000, 57999), ("PB", 58000, 58999),
    ("RN", 59000, 59999), ("CE", 60000, 63999), ("PI", 64000, 64999),
    ("MA", 65000, 65999), ("PA", 66000, 68899), ("AP", 68900, 68999),
    ("AM", 69000, 69299), ("RR", 69300, 69399), ("AM", 69400, 69899),
    ("AC", 69900, 69999), ("DF", 70000, 72799), ("GO", 72800, 72999),
    ("DF", 73000, 73699), ("GO", 73700, 76799), ("RO", 76800, 76999),
    ("TO", 77000, 77995), ("MT", 78000, 78899), ("RO", 78900, 78999),
    ("MS", 79000, 79999), ("PR", 80000, 87999), ("SC", 88000, 89999),
    ("RS", 90000, 99999),
]


def uf_da_faixa(cep):
    p = int(cep[:5])
    for uf, a, b in FAIXAS:
        if a <= p <= b:
            return uf
    return None


def verificar(entrada, online=False):
    cep, _, uf = entrada.partition(":")
    bruto = cep
    cep = re.sub(r"\D", "", cep)
    uf = uf.strip().upper()
    r = {"entrada": bruto, "cep": cep, "problemas": []}
    if len(cep) == 7:  # zero a esquerda perdido (ex.: planilha)
        r["sugestao"] = cep.zfill(8)
        r["problemas"].append("7 digitos: provavel zero a esquerda perdido")
        cep = cep.zfill(8)
    if len(cep) != 8:
        r["problemas"].append("CEP deve ter 8 digitos")
        r["ok"] = False
        return r
    if cep == "0" * 8 or len(set(cep)) == 1:
        r["problemas"].append("CEP zerado ou repetido (placeholder)")
    esperado = uf_da_faixa(cep)
    r["uf_pela_faixa"] = esperado
    if esperado is None:
        r["problemas"].append("CEP fora das faixas nacionais")
    elif uf and uf != esperado:
        r["problemas"].append(f"UF informada ({uf}) diverge da faixa do CEP ({esperado})")
    if online:
        try:
            req = urllib.request.Request(f"https://viacep.com.br/ws/{cep}/json/",
                                         headers={"User-Agent": "treeunfe-skill/1.0"})
            with urllib.request.urlopen(req, timeout=15) as x:
                v = json.loads(x.read())
            if v.get("erro"):
                r["problemas"].append("CEP nao encontrado no ViaCEP")
            else:
                r["viacep"] = {k: v.get(k) for k in ("logradouro", "bairro", "localidade", "uf", "ibge")}
                if uf and v.get("uf") and uf != v["uf"]:
                    r["problemas"].append(f"UF informada ({uf}) diverge do ViaCEP ({v['uf']})")
        except Exception as e:
            r["problemas"].append(f"falha na consulta online: {e}")
    r["cep_formatado"] = f"{cep[:5]}-{cep[5:]}"
    r["ok"] = not r["problemas"]
    return r


if __name__ == "__main__":
    a = sys.argv[1:]
    online = "--online" in a
    a = [x for x in a if x != "--online"]
    if not a:
        sys.exit(__doc__)
    print(json.dumps([verificar(x, online) for x in a], ensure_ascii=False, indent=2))
