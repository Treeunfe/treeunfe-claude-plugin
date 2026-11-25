# Treeunfe para Claude

Plugin com o **conector MCP da Treeunfe** e a skill **classificar-produtos-treeunfe**, que ajuda a classificar os produtos do seu cadastro na Reforma Tributária (CST e cClassTrib do IBS/CBS), conferir NCM e CEST e, com a sua aprovação, gravar a classificação nas regras fiscais da empresa.

> A skill **sugere**; o contador **aprova**. A responsabilidade fiscal continua com a empresa. O MCP opera sempre em **produção**: toda gravação tem efeito real nas próximas notas.

## Instalação no Claude Code

```bash
/plugin marketplace add Treeunfe/treeunfe-claude-plugin
```

```bash
/plugin install treeunfe@treeunfe
```

Na primeira chamada ao MCP, faça o login com a conta do seu emissor (nfe.treeunfe.com.br). O acesso vale só para a sua empresa.

Requisito: Python 3 (a skill usa só a biblioteca padrão). Sem Python, ela lê a base por `curl`.

## Instalação no Claude Desktop ou claude.ai

1. Em **Conectores**, adicione o servidor MCP `https://mcp.treeunfe.com.br/mcp` e faça o login.
2. Baixe `classificar-produtos-treeunfe.zip` na página de [Releases](../../releases) e envie em **Configurações > Capacidades > Skills**.

## Como usar

Peça, por exemplo:

- "Classifique os produtos da minha empresa para o IBS/CBS."
- "Confira o NCM e o cClassTrib dos produtos de bebidas."
- "Quais produtos meus têm Imposto Seletivo?"

A skill lista os produtos, compara com a base oficial, mostra a sugestão com confiança e base legal, e **só grava com o seu "sim" explícito**. Ela nunca emite, cancela nem inutiliza notas.

## Fonte de dados

Base oficial da Receita Federal, [ReceitaFederal/calculadora-rtc-regime-regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) (MIT), publicada pela Treeunfe. Consulta pública: https://www.treeunfe.com.br/consulta-ncm-cclasstrib

## Limites

Só mercadorias (NCM); serviços (NBS/NFS-e) não estão na base. A data de referência da base é 01/01/2027. A base não traz alíquotas de Imposto Seletivo nem alíquotas cheias de IBS/CBS. CEST não faz parte da base e é sempre tratado como revisão.

Documentação do MCP: https://docs.treeunfe.com.br/plataforma/mcp/visao-geral
