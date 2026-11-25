---
name: corrigir-cep-clientes
description: Encontra e corrige CEP incorretos no cadastro de clientes (principalmente os que fazem a NF-e ser rejeitada), em lote e com aprovação, e oferece reemitir as notas. Use quando o usuário falar de CEP inválido, rejeição por CEP, endereço de cliente errado ou correção em massa de endereços. Exige o MCP da Treeunfe.
---

# Corrigir CEP de clientes em lote

Siga `../_compartilhado/seguranca.md`. Corrigir o cadastro e reemitir são **duas aprovações separadas**.

## Pré-requisito
MCP da Treeunfe (`list_nfe`, `get_nfe`, `list_customers`, `get_customer`, `update_customer`). Python 3 para `scripts/cep_utils.py`.

## Fluxo
1. **Descobrir os campos.** A documentação não traz a estrutura do cliente. Leia um `get_customer` real e identifique os campos de CEP, logradouro, número, município (nome e código IBGE) e UF. Use exatamente esses nomes. Se não achar o campo de CEP, pare e relate.
2. **Levantar os casos.** Duas origens, combine-as:
   - **Por rejeição:** `list_nfe` com notas rejeitadas cujo motivo cita CEP; leia o `get_nfe` de cada uma, identifique o destinatário e agrupe **por cliente** (vários erros costumam vir de um cadastro).
   - **Por varredura (opcional):** `list_customers` e valide todos os CEPs.
3. **Validar offline** com `python3 scripts/cep_utils.py CEP:UF ...` (formato de 8 dígitos, zero à esquerda perdido, CEP zerado, UF fora da faixa do CEP). Divergência de faixa é **indicativo**, não prova.
4. **Propor a correção.** Só proponha valor quando houver base:
   - zero à esquerda perdido (7 dígitos → 8): correção segura;
   - formatação (hífen, espaços): segura;
   - CEP que não bate com UF/município: **não adivinhe**. Marque "Revisar", mostre o endereço cadastrado e peça o CEP correto ao usuário.
   - Opcional: consulta ao ViaCEP (`--online`) para sugerir logradouro/município. **Pergunte antes**, pois envia o CEP a um serviço externo. Use `lookup_cnpj_rfb` para comparar com o endereço da Receita, quando o cliente for PJ.
5. **Mostrar antes e depois**, por cliente: id, nome, CEP atual, CEP novo, motivo da mudança, quantas notas rejeitadas dependem dele, confiança. Pergunte "Posso gravar estes N clientes?".
6. **Gravar** com `update_customer` enviando **só os campos alterados**, em lotes de ~10. Releia com `get_customer` e confirme. Pare no primeiro erro.
7. **Reemissão (segunda aprovação).** Ofereça reemitir as notas afetadas pela skill `corrigir-e-reemitir`. Não reemita sem novo "sim".
8. **Fechamento:** tabela id/antes/depois/resultado, pendências ("Revisar") e oferta de salvar CSV local.

Nunca altere outros campos do cliente (IE, CNPJ, nome) nesta skill.
