import io
import re
import glob
import pandas as pd 
import numpy as np

def print_errors(corpus):
	err = corpus.loc[corpus['pos'] == 'E']
	print('err: ' + str(len(err)))

def get_part_number(path):
	return path.split('/')[-1].split('-')[0]

def clean_cell_content(corpus):
	corpus = corpus.replace(to_replace='JE_REMPLACE_LE_POINT_VIRGULE_CAR_C_EST_LE_SEPARATEUR_CSV', value=';', regex=True)
	corpus = corpus.replace(to_replace='_0_', value=',', regex=True) # Zero match
	corpus = corpus.replace(to_replace='(.*)(.*)', value='\\1Œ\\2', regex=True)
	corpus['pos'] = corpus['pos'].replace(to_replace='Aq', value='Ag', regex=True)
	corpus['pos'] = corpus['pos'].replace(to_replace='Z(.*)', value='M\\1', regex=True)
	corpus['pos'] = corpus['pos'].replace(to_replace='PAG(.*)', value='G\\1', regex=True)
	# debut --> surement incorrects
	corpus['pos'] = corpus['pos'].replace(to_replace='Ai', value='Ag', regex=True)
	corpus['pos'] = corpus['pos'].replace(to_replace='Ao', value='Mo', regex=True)
	corpus.loc[corpus['lemma'] == 'EN', 'pos'] = 'Rg'
	# fin
	for char in '()[]-':
		corpus.loc[corpus['form'] == char, 'pos'] = 'Fo'
		corpus.loc[corpus['form'] == char, 'Variante de lemme'] = char
		corpus.loc[corpus['form'] == char, 'lemma'] = char
	corpus['form'] = corpus['form'].replace(to_replace='\\*(.*)', value='\\1', regex=True)

	# [form=/[Aa]utres/ pos="E"] -> [form={$w1_form_0} lemma="AUTRE" pos="Ag"]
	corpus.loc[corpus.form.str.match('(A|a)utre(s?)$') & corpus.pos.str.match('E'), 'pos'] = "Ag" 
	# [form=/[Tt]elz/ pos="E"] -> [form={$w1_form_0} lemma="TEL" pos="Ag"]
	corpus.loc[corpus.form.str.match('(T|t)elz$') & corpus.pos.str.match('E'), 'pos'] = "Ag"

	return corpus

def split1(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne à deux éléments
		cpt += 1
		corpus.loc[id_ + 0.2] = [to_split.loc[id_][0], '-', '-', '-', 'Fo', to_split.loc[id_][5]] # Ajout de la ligne ponctuation
		token = to_split.loc[id_]['form'].split('-')[-1]
		# 'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles'
		if to_split.loc[id_]['pos'] == 'Pp' or token.lower() in ['je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles']:
			corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token, 'IL', 'IL', 'Pp', to_split.loc[id_][5]]
		# là
		elif token == 'là':
			corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token, 'LÀ', 'LÀ', 'Rg', to_split.loc[id_][5]]
		# ce (fût-ce ...)
		elif token.lower() == 'ce':
			corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token, 'CELUI', 'CELUI', 'Pd', to_split.loc[id_][5]]
		# moi, toi, lui, en, le, la, leur (les, leurs... mais pas dans corpus)
		elif token.lower() in ['moi', 'toi', 'lui', 'en', 'le', 'la', 'leur', 'les', 'leurs']:
			corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token, 'LE', 'LE', 'Pp', to_split.loc[id_][5]]
		else: # effet de bords
			corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token, 'E', 'E', 'E', to_split.loc[id_][5]]
	print('Split 1 : ' + str(cpt))
	return corpus

def split2(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		if len(to_split.loc[id_]['form'].split('-')) == 2:
			token1, token2 = to_split.loc[id_]['form'].split('-')
			if token2.lower() in ['je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles']:
				# token1 in : avez, trouvez, voyez, sçauriez, sçavez, pouvez, veux, pourroit, voudrois, puis, verray
				pos = ''
				if token1.lower() == 'avez': 
					pos, lemma = ('Vuc', 'AVOIR')
				elif token1.lower() == 'trouvez':
					pos, lemma = ('Vvc', 'TROUVER')
				elif token1.lower() == 'voyez':
					pos, lemma = ('Vvc', 'VOIR')
				elif token1.lower() == 'sçauriez':
					pos, lemma = ('Vvc', 'SAVOIR')
				elif token1.lower() == 'pouvez':
					pos, lemma = ('Vvc', 'POUVOIR')
				elif token1.lower() == 'veux':
					pos, lemma = ('Vvc', 'VOULOIR')
				elif token1.lower() == 'pourroit':
					pos, lemma = ('Vvc', 'POUVOIR')
				elif token1.lower() == 'pourrois':
					pos, lemma = ('Vvc', 'POUVOIR')
				elif token1.lower() == 'voudrois':
					pos, lemma = ('Vvc', 'VOULOIR')
				elif token1.lower() == 'puis':
					pos, lemma = ('Vvc', 'POUVOIR')
				elif token1.lower() == 'verray':
					pos, lemma = ('Vvc', 'VOIR')
				elif token1.lower() == 'sçavez':
					pos, lemma = ('Vvc', 'SAVOIR')
				else:
					pos, lemma = ('E', 'E')

				corpus = corpus.drop([id_], axis=0) # Suppression de la ligne à deux éléments
				corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, lemma, lemma, pos, to_split.loc[id_][5]]
				corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
				corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, 'IL', 'IL', 'Pp', to_split.loc[id_][5]]
				cpt += 1
			elif token2 in ['moi', 'toi', 'lui', 'en', 'le', 'la', 'leur', 'les', 'leurs']:
				if token1.lower() == 'poussez': 
					pos, lemma = ('Vuc', 'POUSSER')
				elif token1.lower() == 'permettez':
					pos, lemma = ('Vvc', 'PERMETTRE')
				else:
					pos, lemma = ('E', 'E')
				corpus = corpus.drop([id_], axis=0) # Suppression de la ligne à deux éléments
				corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, lemma, lemma, pos, to_split.loc[id_][5]]
				corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
				corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, 'LE', 'LE', 'Pp', to_split.loc[id_][5]]
				cpt += 1
			else:
				if 'dessus' in token2.lower():
					vlemma1, vlemma2 = ('PAR', 'DESSUS')
					lemma1, lemma2 = ('PAR', 'DESSUS')
					pos1, pos2 = ('S', 'Rg')
					corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
					corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
					corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
					corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
					cpt += 1
				elif 'même' in token2.lower():
					vlemma1, vlemma2 = ('IL', 'MÊME')
					lemma1, lemma2 = ('IL', 'MÊME')
					pos1, pos2 = ('Pp', 'Rg')
					corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
					corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
					corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
					corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
					cpt += 1
				elif 'dessous' in token2.lower():
					vlemma1, vlemma2 = ('PAR', 'DESSOUS')
					lemma1, lemma2 = ('PAR', 'DESSOUS')
					pos1, pos2 = ('S', 'Rg')
					corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
					corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
					corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
					corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
					cpt += 1
				else:
					"""
					petit-maître
					par-là
					avant-hier
					au-delà
					temps-là
					peut-être
					"""
					print('', end='')
		else:
			# en lower() : 'continua-t-il', 'tout-à-coup', 'a-t-il'
			print('', end='')
	print('Split 2 : ' + str(cpt))
	return corpus

def split_tresgrand(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((T|t)r(e|é|è)s)(.+)', '\\1 \\4', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		vlemma1, vlemma2 = to_split.loc[id_]['Variante de lemme'].split(' ')
		lemma1, lemma2 = to_split.loc[id_]['lemma'].split(' ')
		pos1, pos2 = ('R', 'Ag')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('Très grand : ' + str(cpt))
	return corpus

def split_aumoins(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((A|a)u)(moins)', '\\1 \\3', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		vlemma1, vlemma2 = ('À+LE', 'MOINS')
		lemma1, lemma2 = ('À+LE', 'MOINS')
		pos1, pos2 = ('S+Da', 'Rg')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('Au moins : ' + str(cpt))
	return corpus

def split_lon(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((L|l)\'?)(on)', '\\1 \\3', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		if '\'' in token1:
			vlemma1, vlemma2 = ('L\'', 'IL')
			lemma1, lemma2 = ('L\'', 'IL')
			pos1, pos2 = ('Xi', 'Pp')
		else:
			vlemma1, vlemma2 = ('L', 'IL')
			lemma1, lemma2 = ('L', 'IL')
			pos1, pos2 = ('Xi', 'Pp')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('L\'on : ' + str(cpt))
	return corpus

def split_pource(corpus_before, to_split):
	cpt = 0
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((P|p)our)(ce)', '\\1 \\3', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		vlemma1, vlemma2 = ('POUR', 'CE')
		lemma1, lemma2 = ('POUR', 'CE')
		pos1, pos2 = ('S', 'Dd')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('Pour ce : ' + str(cpt))
	return corpus

def split_puisje(corpus_before, to_split):
	cpt = 0 
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((P|p)uis)(je)', '\\1 \\3', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		vlemma1, vlemma2 = ('POUVOIR', 'JE')
		lemma1, lemma2 = ('POUVOIR', 'JE')
		pos1, pos2 = ('Vvc', 'Pp')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('Puis je : ' + str(cpt))
	return corpus

def split_cellecy_n_co(corpus_before, to_split):
	cpt = 0 
	corpus = corpus_before
	for id_ in to_split.index:
		token1, token2 = re.sub('((C|c)elle(s?)|(C|c)eux|(C|c)elu(i|y))-(c(i|y))', '\\1 \\7', to_split.loc[id_]['form']).split(' ') # J'ajoute une espace pour pouvoir faire le split
		vlemma1, vlemma2 = ('CE', 'CI')
		lemma1, lemma2 = ('CE', 'CI')
		pos1, pos2 = ('Dd', 'Rg')
		corpus = corpus.drop([id_], axis=0) # Suppression de la ligne
		corpus.loc[id_ + 0.2] = [to_split.loc[id_]['Mot n°'], token1, vlemma1, lemma1, pos1, to_split.loc[id_][5]]
		corpus.loc[id_ + 0.5] = [to_split.loc[id_]['Mot n°'], '-', '-', '-', 'Fo', to_split.loc[id_][5]]
		corpus.loc[id_ + 0.7] = [to_split.loc[id_]['Mot n°'], token2, vlemma2, lemma2, pos2, to_split.loc[id_][5]]
		cpt += 1
	print('Celle-ci & co : ' + str(cpt))
	return corpus


def clean_segmentation(corpus):
	
	# Enlever les commentaires de changement de partie textuelle - [form=/#.*/]
	indexes_comments = corpus[corpus.form.str.match('(#.*)')].index
	corpus = corpus.drop(indexes_comments)

	# -(je|tu|il|on|elle|nous|vous|ils|elles)
	to_split = corpus.loc[((corpus['pos'] == 'Pp') | (corpus['pos'] == 'E')) & (corpus.form.str.match('^-(.+)'))]
	corpus = split1(corpus, to_split)
	
	# (.+)-(je|tu|il|on|elle|nous|vous|ils|elles)
	to_split = corpus.loc[((corpus['pos'] == 'Pp') | (corpus['pos'] == 'Vvc') | (corpus['pos'] == 'E')) & (corpus.form.str.match('(.+)-(.+)'))]
	corpus = split2(corpus, to_split)
	
	# tresgrand -> tres grand
	to_split = corpus.loc[corpus.form.str.match('(T|t)r(e|é|è)s(.+)') & corpus.lemma.str.match('TRÈS (.*)') & corpus.pos.str.match('E')]
	corpus = split_tresgrand(corpus, to_split)

	# Aumoins	E	À LE MOINS
	to_split = corpus.loc[corpus.form.str.match('(A|a)umoins') & corpus.lemma.str.match('À LE MOINS') & corpus.pos.str.match('E')]
	corpus = split_aumoins(corpus, to_split)

	# lon et l'on
	to_split = corpus.loc[corpus.form.str.match('(L|l)\'?on') & corpus.pos.str.match('E')]
	corpus = split_lon(corpus, to_split)

	# Pource
	to_split = corpus.loc[corpus.form.str.match('(P|p)ource') & corpus.lemma.str.match('POUR CE') & corpus.pos.str.match('E')]
	corpus = split_pource(corpus, to_split)
	
	
	# [form=/([Pp]uis)je/ pos="E"] -> [form={$w1_form_1} lemma="POUVOIR" pos="Vvc"] [form="je" lemma="JE" pos="Pp"]
	to_split = corpus.loc[corpus.form.str.match('(P|p)uisje') & corpus.pos.str.match('E')]
	corpus = split_puisje(corpus, to_split)
	
	#[form=/([Cc]elle|[Cc]eux|[Cc]elu[iy])-(c[iy])/ pos="E"] -> [form={$w1_form_1} lemma="CE" pos="Dd"] [form={$w1_form_2} lemma="CI" pos="Rg"]
	to_split = corpus.loc[corpus.form.str.match('((C|c)elle(s?)|(C|c)eux|(C|c)elu(i|y))-(c(i|y))') & corpus.pos.str.match('E')]
	corpus = split_cellecy_n_co(corpus, to_split)
	
	corpus = corpus.sort_index(axis=0)  # On remet tout dans l'ordre car les idx ajoutés le sont à la fin...

	return corpus

def convert_into_cattex09(corpus):
	#print('-----> début de la convertion de Multext en Cattex')
	pos = list(corpus['pos'].values)
	dic_pos = {}
	for p in set(pos):
		dic_pos[p] = pos.count(p)

	print('-------------------------')
	for pos, val in dic_pos.items():
		print(str(pos) + '\t' + str(val))
	print('-------------------------')
	#print('-----> fin de la convertion de Multext en Cattex')
	return corpus

path_presto = './Reference/'
path_CSVs = glob.glob(path_presto + '*csv')

data = []

for path in path_CSVs:
	part_nb = get_part_number(path) # numéro de la partition
	presto_part = pd.read_csv(path, sep='\t', low_memory=False) # lecture du csv
	head = presto_part.columns[:5].to_numpy() # on récupère l'en-tête
	head = np.append(head, 'part') # on ajoute la colonne 'part'
	presto_part = presto_part.to_numpy() # on transforme en array
	part_data = presto_part[1:len(presto_part),:5] # on récupère les données (line:à partir line1, col:jusque col5)
	part_data = np.append(part_data, [[part_nb] for _ in range(len(part_data))], axis=1) # on ajout les données de la colonne 'part'
	data = part_data if data == [] else np.append(data, part_data, axis=0) # ajout du sous corpus au corpus total (on fait attention à initialisation de corpus)


corpus = pd.DataFrame(data=data, columns=head) 
#print_errors(corpus)
corpus = clean_cell_content(corpus)
corpus = clean_segmentation(corpus)
corpus = convert_into_cattex09(corpus)
#print_errors(corpus)

corpus.to_csv('presto_all_parts_net.csv', index=True, sep='\t')