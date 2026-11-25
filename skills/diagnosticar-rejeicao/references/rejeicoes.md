# Rejeições comuns da NF-e (guia de apoio)

**Use o `xMotivo` devolvido pela SEFAZ como fonte principal.** A tabela abaixo ajuda a interpretar e a escolher a correção, mas a lista oficial é o Manual de Orientação do Contribuinte (MOC) da NF-e. Os códigos marcados com ✔ são os que conheço com segurança; para os demais, procure pela **palavra-chave** do motivo e confirme no MOC.

| Sinal (cStat / palavras do motivo) | Significa | Onde corrigir | Reemitir? |
|---|---|---|---|
| 204 / 539 — "Duplicidade de NF-e" ✔ | Número/série já usado (ou mesma chave com dados diferentes) | Usar número ainda não utilizado; checar se a nota original já foi autorizada | Sim, com novo número, **depois de conferir se a original não foi autorizada** |
| 225 — "Falha no Schema XML" ✔ | XML fora do layout (campo obrigatório vazio, formato errado) | Campo apontado no motivo (cadastro do cliente/produto ou dado da emissão) | Sim |
| 233 — "IE do destinatário não cadastrada" ✔ | Inscrição Estadual não existe na UF | Cadastro do cliente (IE ou indicador de IE) | Sim |
| 778 — "NCM inexistente" ✔ | NCM do item não existe | Cadastro do produto (use a skill `classificar-produtos-treeunfe`) | Sim |
| 301 / 302 — "Uso denegado" ✔ | Irregularidade fiscal do emitente ou destinatário | Não é erro de cadastro; falar com o contador | Não até resolver |
| 108 / 109 — "Serviço paralisado" ✔ | SEFAZ indisponível | Aguardar | Sim, depois |
| "CEP" (inválido, não pertence ao município/UF, ausente) | CEP incompatível com cidade/UF ou mal formatado | Cadastro do cliente (use `corrigir-cep-clientes`) | Sim |
| "CNPJ"/"CPF" do destinatário ou emitente | Documento inválido | Cadastro do cliente; para o emitente, falar com o suporte | Sim |
| "IE do emitente" | IE da empresa incorreta | Configuração da empresa (suporte Treeunfe) | Sim, depois de corrigir |
| "CFOP" | CFOP incompatível com a operação/UF/destinatário | Regra fiscal (`get_tax_rule`) ou dado da operação | Sim |
| "CEST" | CEST ausente ou incompatível com o NCM | Cadastro do produto; revisão do contador | Sim |
| "Certificado" (vencido, inválido) | Problema no certificado digital | `get_current_certificate`; suporte | Sim, depois |
| "Valor"/"Total" não confere | Soma dos itens/tributos difere do total | Regra fiscal ou dado dos itens | Sim |
| "Município" / "código do município" | Código IBGE incorreto | Cadastro do cliente | Sim |

## Regra de numeração

Nota **rejeitada** normalmente não fica autorizada, mas a regra de reaproveitar ou não o número varia conforme o motivo (por exemplo, duplicidade). Antes de reemitir, confirme a situação da nota original com `get_nfe` e, se houver dúvida, oriente o cliente a consultar o contador. Se um número ficar sem nota, a saída correta é inutilização (`create_nfe_inutilization`), só com pedido do usuário.

## Quando NÃO corrigir sozinho

Uso denegado, problemas de certificado, IE ou CNPJ do emitente e qualquer motivo que você não consiga associar com segurança a um campo de cadastro: apenas explique e encaminhe.
