---
name: diagnosticar-rejeicao
description: Explica por que NF-e foram rejeitadas pela SEFAZ e indica o que corrigir (cliente, produto, regra fiscal ou emissão), sem alterar nada. Use quando o usuário perguntar o motivo de uma rejeição, pedir para analisar notas rejeitadas ou entender um cStat/xMotivo. Exige o MCP da Treeunfe.
---

# Diagnosticar rejeição de NF-e

Skill **somente de leitura**. Explica a causa e propõe a correção; quem corrige é a skill `corrigir-e-reemitir` (ou outra), com aprovação. Siga `../_compartilhado/seguranca.md`.

## Pré-requisito
Ferramentas do MCP da Treeunfe disponíveis (`list_nfe`, `get_nfe`). Se faltarem, oriente a instalar o plugin `treeunfe` e fazer o login (veja o README).

## Fluxo
1. **Localizar as notas.** Uma nota específica (número, chave ou id): `get_nfe`. "A última" ou "as rejeitadas de hoje/da semana": `list_nfe` e filtre pela situação rejeitada. Paginando se necessário.
2. **Descobrir onde está o motivo.** A documentação não diz em que campo vem o `cStat`/`xMotivo`. Leia o retorno real de um `get_nfe` e use o que ele trouxer (situação, código e mensagem). Se o motivo não vier, diga isso e, se útil, veja `get_nfe_xml` e `get_nfe_items`.
3. **Interpretar** com `references/rejeicoes.md`. O `xMotivo` da SEFAZ é a fonte principal; a tabela ajuda a classificar a causa e escolher a ferramenta de correção.
4. **Achar a origem do dado errado.** Cruze com o cadastro: `get_customer` (destinatário), `get_product` (item/NCM), `get_tax_rule`/`list_tax_rules` (CFOP, tributos), `get_current_organization` (emitente).
5. **Agrupar.** Com muitas notas, agrupe por causa e por cliente/produto: dez notas rejeitadas pelo mesmo CEP são **um** cadastro a corrigir.

## Resposta
Para cada grupo:

| Notas | Motivo (código e texto da SEFAZ) | Causa provável | Onde corrigir | Ação sugerida | Confiança |
|---|---|---|---|---|---|

Termine com: quantas notas, quantas causas distintas, o que dá para resolver por cadastro e o que precisa do contador ou do suporte. Para CEP, indique `corrigir-cep-clientes`; para NCM/classificação, `classificar-produtos-treeunfe`; para o plano de correção e reemissão, `corrigir-e-reemitir`.

Não prometa que a correção resolve. Diga "provável causa" quando não houver certeza e não invente códigos de rejeição.
