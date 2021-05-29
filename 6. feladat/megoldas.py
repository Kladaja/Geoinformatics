
project = QgsProject.instance()
telepulesek = project.mapLayersByName('tolna_megye_telepulesek')[0]
konyvtarak = project.mapLayersByName('konyvtarak')[0]


# uj mezo hozzaadasa
telepulesek.startEditing() 
telepulesek.addAttribute(QgsField('konyvtarak', QVariant.Int, 'int', 10))
telepulesek.updateFields()
telepulesek.commitChanges()
iface.vectorLayerTools().stopEditing(telepulesek)


# telepulesek teruletere eso konyvtarak
with edit(telepulesek):
	for telepules in telepulesek.getFeatures():
		konyvtar_counter = 0
		for konyvtar in konyvtarak.getFeatures():
			if telepules.geometry().contains(konyvtar.geometry()):
				konyvtar_counter += 1
				print(konyvtar['name'])
		print(telepules['NAME_2'], konyvtar_counter)
		telepules['konyvtarak'] = konyvtar_counter
		telepulesek.updateFeature(telepules)


# szabaly alapu megjelenes
epuletek = project.mapLayersByName("epuletek")[0]
renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()	

# szabaly letrehozasa a megyeszekhelyhez
rule1 = root_rule.children()[0].clone()
rule1.setLabel('Szekszárdi könyvtárak')
rule1.setFilterExpression('addr_city = \'Szekszárd\' AND amenity = \'library\'')
props1 = epuletek.renderer().symbol().symbolLayer(0).properties()
props1['color'] = 'blue'
props1['size'] = '10'
props1['name'] = 'diamond'
rule1.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props1)));
root_rule.appendChild(rule1)

rule2 = root_rule.children()[0].clone()
rule2.setLabel('Szekszárdi mozik')
rule2.setFilterExpression('addr_city = \'Szekszárd\' AND amenity = \'cinema\'')
props2 = epuletek.renderer().symbol().symbolLayer(0).properties()
props2['color'] = 'green'
props2['size'] = '10'
props2['name'] = 'square'
rule2.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props2)));
root_rule.appendChild(rule2)

rule3 = root_rule.children()[0].clone()
rule3.setLabel('Szekszárdi színházak')
rule3.setFilterExpression('addr_city = \'Szekszárd\'  AND amenity = \'theatre\'')
props3 = epuletek.renderer().symbol().symbolLayer(0).properties()
props3['color'] = 'purple'
props3['size'] = '10'
props3['name'] = 'star'
rule3.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props3)));
root_rule.appendChild(rule3)

rule4 = root_rule.children()[0].clone()
rule4.setLabel('Egyéb')
rule4.setFilterExpression('addr_city <> \'Szekszárd\'')
props4 = epuletek.renderer().symbol().symbolLayer(0).properties()
props4['color'] = 'red'
props4['size'] = '7'
rule4.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props4)));
root_rule.appendChild(rule4)

root_rule.removeChildAt(0) 

epuletek.setRenderer(renderer)
epuletek.triggerRepaint()
