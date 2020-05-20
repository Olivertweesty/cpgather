#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pegar o arquivo .hosts, remover todos os resultados gerados pelo .massdns
# remover todos os CNAMES ?
# selecionar todos os hosts que nao resolvem nenhum ip
# gerar uma lista domain + unresolved
# pegar cada item dessa lista e forcar em cada ip valido desse dominio para descobrir onde o vhost esta instalado
# se conseguir descobrir, entao temos um vhost oculto e ainda acessivel.
# Podemos usar waybackmachine para encontrar mais detalhes desse vhost, google, github...
# podemos aplicar um patch no /etc/hosts
#
# buscar pelo vhost nos certificados encontrados




# procurar pelo codigo do google analytics UA-XXXXXXX
# procurar no google pelo codigo revela quais outros sites essa empresa possui
#
#
#
##

# ferramenta separada nova:
# crawler de 1 profundidade
# busca por variaveis
# forca variaveis por get e post
# injeta '' (duas x %27)
# inspeciona retorno para verificar injecao
# se injetar corretamente, indicativo de XSS
# reportar
#

# ferramenta separada nova:
# buscador de "interesting targets" usando bayes
# usuario configura parametros para oq ele entende como interessante, exemplo:
# - apache ou nginx desatualizado
# - roda php, tem links para arquivos php
# - tem composer
# - tem path específico
# - tem o diretorio /api/
# - o javascript tem alguma mençao de /api ou algum outro endpoint
#
#
#
#
#
#
#
#
#
#
#