---
name: classificar-produtos-treeunfe
description: Classifica os produtos do cadastro da Treeunfe para a Reforma Tributária (CST e cClassTrib do IBS/CBS), confere NCM e CEST e, com aprovação, grava a classificação nas regras fiscais da empresa. Use quando o usuário pedir para classificar, revisar ou corrigir produtos, NCM, cClassTrib, CST, CEST, Imposto Seletivo ou regras fiscais da Reforma Tributária. Exige o conector MCP da Treeunfe configurado.
---

# Classificação de produtos Treeunfe (NCM, CST/cClassTrib, CEST)

Você ajuda o cliente a classificar os produtos do cadastro dele. **Você sugere, o contador ou o cliente aprova.** A responsabilidade fiscal continua com a empresa. Nunca classifique "de cabeça": use a base oficial (veja "Fonte de dados").

## Pré-requisito: MCP da Treeunfe

Antes de tudo, confirme que as ferramentas do MCP da Treeunfe estão disponíveis (`list_products`, `list_tax_rules`, `get_current_organization`). Se não estiverem, pare e oriente o cliente a configurar o conector:

- Servidor: `https://mcp.treeunfe.com.br/mcp` (Streamable HTTP), login OAuth com a conta do emissor.
- Guia: https://docs.treeunfe.com.br/plataforma/mcp/visao-geral

O MCP opera **sempre em produção**. Toda gravação tem efeito real nas próximas notas.

## Passo 0: verificar o ambiente (sempre, antes de começar)

1. **MCP:** se as ferramentas da Treeunfe não existirem, ou falharem por autenticação, pare e oriente: instalar o plugin `treeunfe` (`/plugin marketplace add <repositório>` e `/plugin install treeunfe@treeunfe`) ou adicionar o servidor manualmente (`claude mcp add --transport http treeunfe https://mcp.treeunfe.com.br/mcp`) e fazer o login OAuth na primeira chamada.
2. **Python 3:** rode `python3 --version`. Se não existir, tente `python --version`. Se nenhum existir, peça ao cliente para instalar o Python 3 (python.org) ou, como alternativa sem instalação, leia a base com `curl`/WebFetch a partir de `latest.json` e filtre só os NCMs necessários.
3. **Acesso à base:** rode `python3 scripts/consulta_ncm.py --versao`. Se falhar por rede, avise que o cache só funciona se a base já tiver sido baixada antes.
4. Só siga adiante com tudo OK. Diga ao cliente o que faltou, em linguagem simples, e o comando exato para corrigir.

## Regras de segurança (inegociáveis)

1. **Nunca grave sem confirmação.** `create_tax_rule` e `update_tax_rule` só depois de mostrar o "antes e depois" e receber um "sim" explícito do usuário. Aprovação de um lote não vale para outro.
2. **Nunca emita, cancele ou inutilize notas.** Não use `emit_nfe`, `cancel_nfe` nem ferramentas de NFS-e.
3. Ao atualizar uma regra, altere **só** `IBSCBSCst` e `IBSCBSCClassTrib`. Não mexa em CFOP, ICMS, IPI, PIS, COFINS, alíquotas nem em `ncmList`/`states` além do necessário.
4. **Não invente alíquotas.** A base traz percentuais de *redução*. Alíquotas de IBS/CBS vêm das regras da empresa ou da configuração da Treeunfe.
5. **Sempre cite a fonte:** versão da base, data de referência, item do anexo e artigo.
6. Na dúvida, marque **"Revisar com o contador"** e diga exatamente o que falta saber.
7. **Não altere o cadastro do produto sem pedido explícito.** O produto não tem campo de cClassTrib; ele fica na regra fiscal.

## Fonte de dados

A base é a da calculadora oficial da Receita Federal (RTC, licença MIT), publicada pela Treeunfe. Use o script, que baixa e guarda em cache a versão indicada em `latest.json`:

```bash
python3 scripts/consulta_ncm.py --versao            # versão e data de referência
python3 scripts/consulta_ncm.py 10063021 22030000   # consulta por NCM
python3 scripts/consulta_ncm.py --lote ncms.txt     # lote (um NCM por linha)
python3 scripts/consulta_ncm.py --buscar arroz polido  # acha NCM pela descrição
```

Para muitos produtos, extraia os NCMs distintos, rode em lote e trabalhe sobre o JSON resultante. Não carregue a base inteira no contexto. Informe sempre a versão e a data de referência (hoje: V0059, referência 01/01/2027). Para outra data de referência, a base precisa ser regerada; avise o usuário se a data dele for diferente.

Detalhes das tabelas e dos 18 cClassTrib: `references/cclasstrib.md`.

## Fluxo de trabalho

1. **Contexto da empresa:** `get_current_organization` (UF e regime). Registre.
2. **Ler produtos:** `list_products` (paginando até o fim; confira com `get_product` quais campos existem de fato, pois pode haver mais do que `cProd`, `xProd`, `NCM`, `cEAN`, `uCom`, `orig`, `vUnCom`). Se o usuário indicar só alguns produtos, classifique apenas esses.
3. **Ler as regras atuais:** `list_tax_rules` (e `list_default_tax_rules` se útil). Veja o que já cobre cada NCM.
4. **Classificar** cada produto com o algoritmo abaixo.
5. **Apresentar** a tabela e o resumo (formato abaixo). Pare e espere o usuário.
6. **Gravar** só o que for aprovado, seguindo "Gravação".
7. **Conferir** (opcional): num NF-e já emitida, `get_nfe_items` mostra os tributos calculados por item.

## Algoritmo de classificação (por produto)

1. **Validar o NCM.** 8 dígitos e vigente na base. Inválido, expirado ou vazio: pendência "corrigir NCM"; **não classifique**. Se a base indicar NCM inexistente, sugira candidatos com `--buscar` pela descrição.
2. **Coerência NCM x descrição.** Compare `xProd` com a descrição completa do NCM. Se claramente não combinam (NCM de arroz, descrição "parafuso"), sinalize **"NCM provavelmente errado"**, proponha o NCM mais provável e **não grave** nada para esse produto. Classificação certa sobre NCM errado continua errada.
3. **Buscar opções** na base.
   - **Sem opções:** CST 000 / cClassTrib 000001 (tributação integral), confiança **alta**. É o caso de 83% dos NCMs.
   - **Com opções:** são candidatas; siga os passos 4 a 6.
4. **Comparar `xProd` com o texto de cada item de anexo** das candidatas. Regra de precedência: quando um item diz "ressalvados os do Anexo X", vale o Anexo X. Exemplo: arroz para consumo humano (1006.30.21) é Anexo I (200003, imposto zero), não VII.15.
5. **Opções que dependem da operação, não do produto.** O cadastro não diz quem compra. Sugira a opção **padrão para venda comum** e deixe as demais como "usar em vendas para X":
   - 200005, 200008, 200011, 200043: venda à administração pública ou entidades imunes;
   - 515001: operação sujeita a diferimento (ex.: insumo agropecuário a produtor);
   - 200038 com item IX.19: destinação a ração/alimentação animal.
   Se o cliente precisar dessas situações, proponha regras separadas por natureza da operação (`natOp`/`tpNF`/`finNFe`), com aprovação.
6. **Imposto Seletivo.** Se `imposto_seletivo` for verdadeiro, avise que o produto também entra no IS a partir de 2027 e que a cobrança depende da operação. A base não traz alíquota de IS.
7. **Confiança:**
   - **Alta:** regra geral, ou uma única opção cuja descrição bate claramente com o anexo.
   - **Média:** várias opções, mas a descrição aponta uma com clareza.
   - **Baixa (revisão obrigatória):** descrição genérica ("PRODUTO 01", códigos, abreviações); opções que dependem do cliente; NCM com cara de errado; conflito entre produtos do mesmo NCM.

### Conflito por NCM

A regra fiscal classifica por **NCM + operação + UF**, não por produto. Se dois produtos com o mesmo NCM precisarem de cClassTrib diferentes, **sinalize o conflito** e não escolha sozinho. Proponha ao usuário: revisar o NCM de um deles, ou separar por operação, ou decisão do contador.

## CEST e demais campos

O CEST **não está na base cClassTrib**. Ele depende do NCM e do segmento (Convênio ICMS 142/2018 e seus anexos) e só existe para mercadorias sujeitas a substituição tributária de ICMS. Regras:

- Primeiro veja, em `get_product`, se o produto tem campo de CEST. Se tiver, valide: 7 dígitos, e coerente com o NCM (os 4 primeiros dígitos do NCM costumam estar no mesmo segmento). Se não houver campo de CEST no cadastro, diga isso e não invente um lugar para gravá-lo.
- **Não deduza o CEST de cabeça.** Se for preciso sugerir, consulte a tabela oficial (use WebSearch/WebFetch na tabela do Convênio ICMS 142/2018 ou do CONFAZ), cite a fonte e marque **"Revisar com o contador"**. Muitos NCMs têm mais de um CEST possível, conforme a descrição.
- ST de ICMS depende também da UF de origem e destino, do regime da empresa e do protocolo vigente. Trate como pendência de revisão, não como certeza.
- Outros campos do cadastro (`orig`, GTIN/`cEAN`, unidade `uCom`): aponte inconsistências óbvias (GTIN inválido, origem fora de 0 a 8, unidade incompatível com o produto), sem alterar nada automaticamente. O GTIN ajuda a confirmar o que é o produto, mas a classificação depende de NCM e descrição.

## Formato da resposta

Uma linha por produto:

| cProd | xProd | NCM | Situação do NCM | Candidatas | Sugestão (CST / cClassTrib) | Benefício | Base legal / item do anexo | Confiança | Ação |
|---|---|---|---|---|---|---|---|---|---|

Benefício em linguagem simples ("Imposto zero", "Imposto 60% menor"). Depois, **agrupe por NCM** (a gravação é por NCM) e termine com o resumo:

- quantos produtos ficaram na regra geral;
- quantos têm benefício;
- quantos precisam de revisão (e por quê);
- pendências de NCM, de CEST e conflitos.

Rodapé obrigatório: "Base oficial RFB/RTC versão X, referência dd/mm/aaaa. Sugestão automatizada, sujeita à validação do contador."

Com muitos produtos, entregue primeiro o resumo e a lista de pendências, e ofereça exportar a tabela completa em CSV (arquivo local) em vez de despejar centenas de linhas.

## Gravação (só após "sim" explícito)

1. Para cada NCM aprovado, localize a regra existente que o cobre (`get_tax_rule`).
2. **Regra existente cobrindo o NCM:** `update_tax_rule` alterando só `IBSCBSCst` e `IBSCBSCClassTrib`. Se a regra cobrir vários NCMs com classificações diferentes, **não** altere em bloco: proponha desmembrar e peça confirmação.
3. **Sem regra cobrindo o NCM:** `create_tax_rule` com `ncmList`, `states`, tipo de operação e os campos IBS/CBS, conferindo antes se não duplica outra regra. Mostre o corpo completo antes.
4. Mostre o **antes e depois** (campo a campo, só IBS/CBS) e pergunte "Posso gravar?". Grave em lotes pequenos, confirmando o resultado de cada chamada. Se uma chamada falhar, pare e relate.
5. Ao final, liste o que foi gravado, o que ficou pendente e lembre que a regra vale para as próximas notas emitidas.

## Limites conhecidos

- Só mercadorias (NCM). Serviços (NBS/NFS-e) não estão na base.
- Data de referência fixa da base (01/01/2027); para 2026 (ano de teste) as regras podem diferir.
- Classificações que dependem de operação (governo, diferimento, destinação) não saem do cadastro de produto.
- A base não traz alíquotas de IS nem alíquotas cheias de IBS/CBS.
- A interpretação de casos com várias opções deve ser validada pelo time fiscal antes de gravações em massa. Para mais de ~20 NCMs com opções múltiplas, recomende revisão do contador antes de gravar.
