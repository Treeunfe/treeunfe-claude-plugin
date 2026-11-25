---
name: checklist-pre-emissao
description: Confere se a empresa e a nota estão prontas antes de emitir uma NF-e (checklist da empresa, regra fiscal do NCM, destinatário, itens) e só emite depois da confirmação do usuário. Use quando o usuário quiser emitir uma nota com mais segurança ou perguntar se está pronto para emitir. Exige o MCP da Treeunfe.
---

# Checklist antes de emitir NF-e

Siga `../_compartilhado/seguranca.md`. `emit_nfe` tem valor fiscal e é irreversível.

## Fluxo (conforme o fluxo recomendado na documentação do MCP)
1. `get_nfe_checklist`: certificado, séries/numeração, regras fiscais. Se algo estiver pendente, explique em linguagem simples e **não emita**.
2. **Destinatário:** `get_customer` (ou `lookup_cnpj_rfb` para PJ não cadastrado). Valide CPF/CNPJ e CEP (`../corrigir-cep-clientes/scripts/cep_utils.py`). Corrija **só com aprovação**.
3. **Itens:** `get_product` de cada item; confira NCM (base da skill `classificar-produtos-treeunfe`), unidade e valor.
4. **Regra fiscal:** para cada NCM e a UF do destinatário, `list_tax_rules`/`get_tax_rule`. Sem regra que cubra, avise que o cálculo pode falhar e ofereça criar/ajustar a regra (aprovação separada).
5. **Resumo para conferência:** destinatário, itens, CFOP, tributos calculados e total. Mostre também série e próximo número.
6. **Confirmação explícita:** "Posso emitir esta nota?". Só então `emit_nfe` com `calculateTaxes: true`.
7. **Depois:** `get_nfe` para a situação; se autorizada, chave e `get_nfe_danfe_url`; se rejeitada, `diagnosticar-rejeicao`.

Para testes sem valor fiscal, lembre que o MCP é produção; homologação exige a API Key de homologação no programa, fora do MCP.
