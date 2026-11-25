# Regras de segurança comuns (todas as skills Treeunfe)

O MCP da Treeunfe opera **sempre em produção**. Toda gravação tem efeito fiscal real.

1. **Leitura é livre; escrita exige "sim" explícito** do usuário, depois de mostrar o antes e depois. Um "sim" vale só para o lote mostrado.
2. **Confirmações separadas por tipo de ação.** Corrigir cadastro, emitir nota, cancelar, inutilizar e enviar CC-e são aprovações distintas. Nunca encadeie duas ações de risco numa única aprovação.
3. **Ações irreversíveis** (`cancel_nfe`, `create_nfe_cce`, `create_nfe_inutilization`, `emit_nfe`) só com pedido claro do usuário para aquela nota e confirmação reforçada, repetindo número, destinatário e valor.
4. **Descubra antes de assumir.** A documentação do MCP não lista os parâmetros das ferramentas. Na primeira vez, leia um registro real (`get_customer`, `get_nfe`, etc.) e use os nomes de campos que ele devolver. Nunca invente campos.
5. **Altere o mínimo.** Em `update_*`, envie só os campos que mudam. Releia o registro depois para confirmar.
6. **Lotes pequenos.** Grave em blocos (ex.: 10), confira cada resposta e pare no primeiro erro, relatando o que já foi feito.
7. **Registro do que mudou.** Ao final, gere uma tabela (id, campo, antes, depois, resultado) e ofereça salvá-la em CSV local.
8. **Dados do cliente são privados.** Não envie CNPJ, nomes ou endereços a serviços externos sem o usuário aceitar. Consulta externa de CEP (ex.: ViaCEP) é opcional e fica desligada por padrão.
9. **Não afirme o que não verificou.** Se não souber onde um dado fica ou o que uma rejeição significa, diga e marque "Revisar com o contador/suporte".
10. **Nunca altere certificado, configurações da empresa (`update_settings_nfe`) ou webhooks** sem pedido explícito do usuário.
