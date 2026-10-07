"""Uma etapa da grade por modulo, cada uma com OPCOES e JUSTIFICATIVA.

OPCOES mapeia o id da opcao para uma funcao sem argumentos que devolve um
objeto novo. Funcao e nao instancia porque cada combinacao precisa do proprio
objeto: dois pipelines nunca podem compartilhar um transformador ajustado.
"""
