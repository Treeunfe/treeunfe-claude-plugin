---
name: corrigir-e-reemitir
description: Executa o plano de correção de NF-e rejeitadas (corrige cadastro de cliente, produto ou regra fiscal) e, com aprovação separada, reemite as notas e confere o resultado. Use depois do diagnóstico, ou quando o usuário pedir para corrigir e reenviar notas rejeitadas. Exige o MCP da Treeunfe.
---

# Corrigir e reemitir notas rejeitadas

Siga `../_compartilhado/seguranca.md`. O MCP **não tem** ferramenta de "reenviar nota rejeitada": o caminho é **corrigir a origem do erro** e **emitir de novo** (`emit_nfe`). A emissão tem valor fiscal e é irreversível; trate com o máximo de cuidado.

## Fluxo
1. **Diagnóstico primeiro.** Se ainda não houver diagnóstico, rode a skill `diagnosticar-rejeicao`. Só prossiga com causas que você associa com segurança a um campo de cadastro.
2. **Plano.** Liste por grupo: nota(s), causa, ferramenta de correção (`update_customer`, `update_product`, `update_tax_rule`...), valor antes e depois. Notas de causa não corrigível por cadastro (uso denegado, certificado, emitente) ficam fora e vão para "Revisar com o contador/suporte".
3. **Aprovação 1: correção dos cadastros.** Mostre antes e depois; grave só após "sim", só os campos alterados, em lotes, relendo cada registro. Em regra fiscal, altere apenas os campos necessários; para IBS/CBS use a skill de classificação.
4. **Checar antes de reemitir.** Para cada nota: `get_nfe` para confirmar que a original **não foi autorizada** (se foi, não reemita). Rode `get_nfe_checklist`. Confira se o número a usar está livre; não reaproveite número sem entender o motivo da rejeição (duplicidade, por exemplo).
5. **Aprovação 2: reemissão.** Mostre, nota a nota, destinatário, itens, CFOP, total e série/número. Peça "Posso emitir estas N notas?". Reconstrua os dados da nota original a partir de `get_nfe`/`get_nfe_items`; **não altere valores, itens ou destinatário além da correção aprovada**.
6. **Emitir** com `emit_nfe` (com `calculateTaxes: true`, como orienta a documentação), uma por vez ou em lotes pequenos, parando no primeiro erro inesperado.
7. **Conferir.** `get_nfe` para a situação de cada nota. Autorizada: informe chave e link do DANFE (`get_nfe_danfe_url`). Rejeitada de novo: volte ao diagnóstico, sem repetir às cegas.
8. **Fechamento:** tabela nota original → nova nota → situação, e o que ficou pendente. Se sobraram números sem nota, **ofereça** inutilização (`create_nfe_inutilization`) apenas se o usuário quiser; é outra aprovação.

Nunca cancele nota nem envie CC-e por conta própria. Se o usuário pedir, siga a regra de ação irreversível.
