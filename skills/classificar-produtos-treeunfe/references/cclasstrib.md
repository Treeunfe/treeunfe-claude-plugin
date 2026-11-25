# Referência: base cClassTrib (V0059, referência 01/01/2027)

Fonte: ReceitaFederal/calculadora-rtc-regime-regular (MIT). Publicada em
`https://d1c2gtb75fe4co.cloudfront.net/cclasstrib/latest.json` (aponta o arquivo da versão).
Consulta pública: https://www.treeunfe.com.br/consulta-ncm-cclasstrib

## Números

- 10.515 NCMs de 8 dígitos vigentes; 8.731 (83%) só regra geral; 1.784 (17%) com tratamento especial; 116 também no Imposto Seletivo.
- Opções por NCM: 0 → 8.731; 1 → 514; 2 → 950; 3 → 225; 4 → 92; 5 → 3.

## Os 18 cClassTrib

| cClassTrib | CST | Redução | Situação | Base legal |
|---|---|---|---|---|
| 000001 | 000 | — | Tributação integral (regra geral) | LC 214/2025 |
| 200003 | 200 | 100% | Cesta Básica Nacional, Anexo I | Art. 125 |
| 200004 | 200 | 100% | Dispositivos médicos (Anexo XII) | Art. 144, I |
| 200005 | 200 | 100% | Dispositivos médicos, administração pública e entidades de saúde imunes | Art. 144, II |
| 200007 | 200 | 100% | Acessibilidade PcD (Anexo XIII) | Art. 145, I |
| 200008 | 200 | 100% | Acessibilidade PcD, compra por órgãos públicos | Art. 145, II |
| 200011 | 200 | 100% | Nutrição enteral/parenteral para órgãos públicos | Art. 146, § 2º |
| 200014 | 200 | 100% | Hortícolas, frutas e ovos (Anexo XV) | Art. 148 |
| 200030 | 200 | 60% | Dispositivos médicos (Anexo IV) | Art. 131 |
| 200031 | 200 | 60% | Acessibilidade PcD (Anexo V) | Art. 132 |
| 200033 | 200 | 60% | Nutrição enteral/parenteral (Anexo VI) | Art. 133, § 1º |
| 200034 | 200 | 60% | Alimentos para consumo humano (Anexo VII) | Art. 135 |
| 200035 | 200 | 60% | Higiene pessoal e limpeza (Anexo VIII) | Art. 136 |
| 200038 | 200 | 60% | Insumos agropecuários e aquícolas (Anexo IX) | Art. 138 |
| 200039 | 200 | 60% | Produções artísticas, culturais, de eventos | Art. 139 |
| 200043 | 200 | 60% | Bens de soberania, administração pública (Anexo XI) | Art. 142, I |
| 200044 | 200 | 60% | Segurança da informação e cibernética | Art. 142, II |
| 515001 | 515 | 60% + diferimento | Insumos do Anexo IX com diferimento | Art. 138, § 2º |

## Como a base casa NCM e regra

1. Só NCMs de 8 dígitos vigentes na data de referência.
2. Um NCM casa com todas as regras cujo código seja prefixo dele, menos as exceções.
3. Classificações do Imposto Seletivo têm os mesmos códigos e viram só a marca `is`.
4. NCM sem opção: regra geral CST 000 / cClassTrib 000001.

## Formato do JSON (para quem for ler direto)

`ncm.<8d>.d` descrição (pode ser "Outros": use `hier`); `ncm.<8d>.c` opções, cada uma um código ou `[código, itens de anexo...]`; `ncm.<8d>.is` marca IS; `cclass.<cod>` com `cst`, `desc`, `red`, `fund`; `anexos.<item>` texto do item; `hier.<prefixo>` níveis acima do NCM.

## Atualizar a base (equipe Treeunfe, não o cliente)

1. `git clone --depth 1 https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git repo`
2. `node scripts/1-gerar-banco.mjs` (Node 22+)
3. `node scripts/2-gerar-json.mjs 2027-01-01`
4. Subir o JSON no S3 e depois atualizar o `latest.json`.
