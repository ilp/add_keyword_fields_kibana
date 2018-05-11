# Script responsavel por adicionar .keyword nos atributos das visualizacoes importadas da versao do elk 5.
# AUTHOR: Iverson Luis Pereira
# CQS - NTI - UFPE - 2018
# ORGANIZATION: UFPE (Universidade Federal de Pernambuco) -  NTI (Nucleo de Tecnologia da Informacao)
# Todos os direitos reservados

import json
import sys

visualizations = []

#executar da seguinte forma python script_keyword.py export.json
#nao esquecer de passar o argumento 1 -> arquivo export.json obtido do kibana
with open(sys.argv[1]) as v:    
    visualizations = json.load(v)

print 'Conversao em andamento...'

for vis in range(len(visualizations)):
    _type = visualizations[vis]['_type']
    if _type == 'visualization':
        print "Convertendo: " + visualizations[vis]['_source']['title']
        vis_state = visualizations[vis]['_source']['visState']        
        vis_state_json = json.loads(vis_state)       
        print vis_state
        for i in range(len(vis_state_json['aggs'])):
            if "field" in vis_state_json['aggs'][i]['params']:
                vis_type = vis_state_json['aggs'][i]['type']
                if(vis_type == 'terms'):
                    field = vis_state_json['aggs'][i]['params']['field']
                    new_field = field + '.keyword'
                    vis_state_json['aggs'][i]['params']['field'] = new_field

        visualizations[vis]['_source']['visState'] = json.dumps(vis_state_json, indent=4, sort_keys=True)

print 'Concluido!'

with open('export_keyword.json', 'w') as outfile:
    json.dump(visualizations, outfile, indent=4)