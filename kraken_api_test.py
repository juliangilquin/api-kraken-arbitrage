#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""kraken_api_test.py, écrit par Julian Gilquin, le 01/06/2021.
Dernière mise à jour le 02/06/2021.
Récupérer les données de prix de devises et calculer des ratios pour obserer les opportunités d'arbitrage.
"""

import requests
import pprint
import json
import time
import datetime

# Definir les paires de devises qui m'intéressent
assets = [
("CURRENCY", "/EURO", "/BITCOIN", "/USDT", "/ETH"),
("TETHER", "USDTEUR", None, None, None),
("ETHEREUM","XETHZEUR", "XETHXXBT", "ETHUSDT", None), 
("BITCOIN", "XXBTZEUR", None, "XBTUSDT", None),
("RIPPLE", "XXRPZEUR", "XXRPXXBT", "XRPUSDT", "XRPETH"),
("UNISWAP", "UNIEUR", "UNIXBT", None, "UNIETH"),
("LITECOIN", "XLTCZEUR", "XLTCXXBT", "LTCUSDT", "LTCETH"),
("SIACOIN", "SCEUR", "SCXBT", None, "SCETH"),
("STELLAR", "XXLMZEUR", "XXLMXXBT", None, None),
("ALGORAND", "ALGOEUR", "ALGOXBT", None, "ALGOETH"),
("CARDANO", "ADAEUR", "ADAXBT", "ADAUSDT", "ADAETH")
]

assetpairs = []
for asset in assets[1:]:
	for item in asset[1:]:
		if item != None:
			assetpairs.append(item)
#print(assetpairs)

search_terms = ",".join(assetpairs)
#print(search_terms)

try:
	index_num = int(input("Entrer le numéro de la crypto à étudier:\n1.Tether\t2.Ethereum\t3.Bitcoin\t4.Ripple\t5.Uniswap\n6.Litecoin\t7.Siacoin\t8.Stellar\t9.Algorand\t10.Cardano\n"))
except ValueError:
	print("Rentrer un nombre entre 1 et 6. One more try.")
	index_num = input("Entrer le numéro de la crypto à étudier:\n1.Tether\t2.Ethereum\t3.Bitcoin\t4.Ripple\t5.Uniswap\n6.Litecoin\t7.Siacoin\t8.Stellar\t9.Algorand\t10.Cardano\n")

# La crypto qui m'intéresse. Changer le numero d'index pour etudier une autre
crypto = assets[index_num]

# Nb de secondes entre deux requetes d'API
sleepy_time = 2

# Definir les fonctions qui vont nous servir
def get_ratio(euro, crypto):
	the_ratio = float(euro)/float(crypto)
	return the_ratio

def percent_diff(check, base):
	percentage = (float(check)-float(base)) / float(base) * 100
	return (str(round(percentage, 2)) + "%")

#Loop de l'infini
try:
	while True:
		# Obtenir les données
		resp = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={search_terms}")
		data = json.loads(resp.text)
		#pprint.pprint(data)

		# Extraire les current prices
		now = datetime.datetime.today()
		print(now)
		current_prices = {k: v["c"][0] for k,v in data["result"].items()}
		if len(current_prices) != len(assetpairs):
			raise Exception("Missing data")
		#pprint.pprint(current_prices)

		# Attribuer les prix à des variables et calculer les ratios
		cusdteur = current_prices["USDTEUR"]
		cbtceur = current_prices["XXBTZEUR"]
		cetheur = current_prices["XETHZEUR"]

		name_crypto = crypto[0]
		current_crypto = current_prices[crypto[1]]
		try:
			crypto_par_btc = current_prices[crypto[2]]
			ratio_btc_crypto = get_ratio(current_crypto, crypto_par_btc)
			percent_diff_btc_crypto = percent_diff(ratio_btc_crypto, cbtceur)
		except:
			pass
		try:
			crypto_par_usdt = current_prices[crypto[3]]
			ratio_usdt_crypto = get_ratio(current_crypto, crypto_par_usdt)
			percent_diff_usdt_crypto = percent_diff(ratio_usdt_crypto, cusdteur)
		except:
			pass
		try:
			crypto_par_eth = current_prices[crypto[4]]
			ratio_eth_crypto = get_ratio(current_crypto, crypto_par_eth)
			percent_diff_eth_crypto = percent_diff(ratio_eth_crypto, cetheur)
		except:
			pass
		
		# Presentation des resultats
		print(f"{name_crypto}")
		print(f"Current (€): {current_crypto}")
		try:
			print(f"Current (BTC): {crypto_par_btc}")
			print(f"Ratio BTC: {ratio_btc_crypto}")
			print(f"% Diff BTC: {percent_diff_btc_crypto}")
		except:
			pass
		try:
			print(f"Current (USDT): {crypto_par_usdt}")
			print(f"Ratio USDT: {ratio_usdt_crypto}")
			print(f"% Diff USDT: {percent_diff_usdt_crypto}")
		except:
			pass
		try:
			print(f"Current (ETH): {crypto_par_eth}")
			print(f"Ratio ETH: {ratio_eth_crypto}")
			print(f"% Diff ETH: {percent_diff_eth_crypto}")
		except:
			pass
		print("\nCTRL + C pour stopper")
		print("___________________________________")

		# Temps d'attente avant que la boucle ne recommence
		time.sleep(sleepy_time)

except Exception as err:
	print("OOPS! Something went wrong\n", err)
except KeyboardInterrupt:
	print("Fin du Programme")