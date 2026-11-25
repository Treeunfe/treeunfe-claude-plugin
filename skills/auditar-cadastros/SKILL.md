---
name: auditar-cadastros
description: Varre clientes, produtos e regras fiscais da empresa atrás de erros que vão gerar rejeição de NF-e (CEP, CNPJ/CPF, IE, NCM, GTIN, unidade, UF sem regra fiscal) e entrega um relatório priorizado. Use para prevenção, revisão de cadastro ou antes de uma emissão grande. Exige o MCP da Treeunfe.
---

# Auditar cadastros (prevenção de rejeição)

Somente leitura; correções só com aprovação, pelas skills específicas. Siga `../_compartilhado/seguranca.md`.

## Fluxo
1. **Escopo.** Pergunte o que auditar (clientes, produtos, regras ou tudo) e se há filtro (UF, período, só os usados nos últimos N meses via `list_nfe`).
2. **Descobrir campos.** Leia um `get_customer` e um `get_product` reais e use os nomes devolvidos.
3. **Ler tudo** com `list_customers`, `list_products` e `list_tax_rules` (paginando até o fim).
4. **Checagens (só sobre dados que existem):**
   - **Cliente:** CPF/CNPJ com dígito verificador válido; CEP pelo `python3 ../corrigir-cep-clientes/scripts/cep_utils.py`; UF e município preenchidos; IE vazia ou em formato incompatível com o indicador; campos obrigatórios em branco. Para PJ, compare com `lookup_cnpj_rfb` quando o usuário autorizar a amostra.
   - **Produto:** NCM com 8 dígitos e existente na base (use `consulta_ncm.py` da skill `classificar-produtos-treeunfe`); GTIN com dígito verificador válido ou "SEM GTIN"; origem de 0 a 8; unidade preenchida; valor unitário maior que zero; descrição genérica.
   - **Regras fiscais:** NCMs usados em produtos sem regra que os cubra; regras duplicadas ou sobrepostas; UFs de clientes sem regra.
5. **Priorizar por impacto:** primeiro o que bloqueia emissão (documento inválido, NCM inexistente), depois o que provavelmente rejeita (CEP incompatível, IE), depois o que é qualidade.
6. **Relatório:** resumo (totais e % com problema) e tabela id/nome/problema/gravidade/correção sugerida. Com centenas de linhas, entregue o resumo e ofereça CSV local.
7. **Encaminhar:** CEP → `corrigir-cep-clientes`; NCM/cClassTrib → `classificar-produtos-treeunfe`; notas já rejeitadas → `diagnosticar-rejeicao`.

Não corrija nada nesta skill. Sinalize, nunca presuma: "inválido" só quando a regra for objetiva (dígito verificador, tamanho); o restante é "suspeito, revisar".
