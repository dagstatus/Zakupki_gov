import requests
import sqlite3

def kol_pages(total,perpag):   #send total and perpage and return need kol pages to for
		
	if total%perpag>0 :
		return(total//perpag+1)
	else:
		return(total//perpag)


DATA_RANGE_PARSE='01.01.2015-31.12.2018'
STAGE_contr='EC'
API_URL = 'http://openapi.clearspending.ru/restapi/v3/contracts/select/'
bd_name='BD.db'

# data = {
# 	'customerregion': '05',
# 	'daterange': DATA_RANGE_PARSE,
# 	'currentstage': STAGE_contr,
# 	'page': 1,
# }

# r = requests.get(url=API_URL, params=data).json()

# pages_total=int(r['contracts']['total'])
# per_page=int(r['contracts']['perpage'])
# need_pages=kol_pages(pages_total,per_page)
# print('Количество страниц в заданном периоде - ',need_pages)


def kol_pp(date_rang,stage):#Считаем количество страниц для парса
	data = {
	'customerregion': '05',
	'daterange': date_rang,
	'currentstage': stage,
	'page': 1,
		}

	r = requests.get(url=API_URL, params=data).json()

	pages_total=int(r['contracts']['total'])
	per_page=int(r['contracts']['perpage'])
	need_pages=kol_pages(pages_total,per_page)
	print('Количество страниц в заданном периоде - ',need_pages)
	return(need_pages)


conn=sqlite3.connect(bd_name)
cursor = conn.cursor()





def parse_contract(num_page):   #num_page листаю страницы в цикле
	data = {
		'customerregion': '05',
		'daterange': DATA_RANGE_PARSE,
		'currentstage': STAGE_contr,
		'page': num_page,
			}

	r = requests.get(url=API_URL, params=data).json()

	contracts_dct = {}
	for contract in r['contracts']['data']:
		contracts_dct[int(contract['id'])] =	{
											'ID': str(contract['id']),
											# 'price': float(contract['price']),
											'regNum':str(contract['regNum']),
											'signDate':str(contract['signDate']),
											# 'currentContractStage':str(contract['currentContractStage']),
											# 'contractUrl':str(contract['contractUrl']),
											'customer_inn':str(contract['customer']['inn']),
											'customer_kpp':str(contract['customer']['kpp']),
											# 'customer_regNum':str(contract['customer']['regNum']),
											'customer_fullName':str(contract['customer']['fullName']),
											# 'customer_postalAddress':str(contract['customer']['postalAddress']),
											# 'supplier_inn':str(contract['suppliers'][0]['inn']),										
											'supplier_organizationName':str(contract['suppliers'][0]['organizationName'])
											#'supplier_factualAddress':str(contract['suppliers'][0]['factualAddress']),									
										

												}
		okpd_or_okpd2=''
		supl_kpp=''
		customer_postalAddr=''
		price_s=0.0
		supl_inn=''

		try:
			contr_url=str(contract['contractUrl'])
		except:
			contr_url=''
		try:
			customer_regnum_try=str(contract['customer']['regNum'])
		except:
			customer_regnum_try=''





		try:
			currentContractStage=str(contract['currentContractStage'])
		except:
			currentContractStage=''


		try:
			price_s=float(contract['price'])
		except:
			price_s=0,0
		try:
			customer_postalAddr=str(contract['customer']['postalAddress'])
		except:
			customer_postalAddr=''
		try:
			supl_inn=str(contract['suppliers'][0]['inn'])
		except:
			supl_inn=''
		try:
			supl_kpp=str(contract['suppliers'][0]['kpp'])
		except:
			supl_kpp=''
			#print('no kpp suppliers')
		
		try:
			okpd_or_okpd2=str(contract['products'][0]['OKPD2']['code'])
		except :
			pass
		try:
			okpd_or_okpd2=str(contract['products'][0]['OKPD']['code'])
		except :
			pass
		
		contracts_dct[int(contract['id'])].update({'OKPD2':okpd_or_okpd2,'supplier_inn':supl_inn,'supplier_kpp':supl_kpp,'customer_postalAddress':customer_postalAddr,'price':price_s,'currentContractStage':currentContractStage,'contractUrl':contr_url,'customer_regNum':customer_regnum_try})

	return(contracts_dct)

		


def add_to_db_date(contracts_dct):
	for x in contracts_dct:	
		for y in contracts_dct[x]:
			ID=(contracts_dct[x]['ID'])
			price=(contracts_dct[x]['price'])
			regNum=(contracts_dct[x]['regNum'])
			signDate=(contracts_dct[x]['signDate'])
			currentstage=(contracts_dct[x]['currentContractStage'])
			contractUrl=(contracts_dct[x]['contractUrl'])
			customer_inn=(contracts_dct[x]['customer_inn'])
			customer_kpp=(contracts_dct[x]['customer_kpp'])
			customer_regNum=(contracts_dct[x]['customer_regNum'])
			customer_fullName=(contracts_dct[x]['customer_fullName'])
			customer_postalAddress=(contracts_dct[x]['customer_postalAddress'])
			supplier_inn=(contracts_dct[x]['supplier_inn'])
			supplier_organizationName=(contracts_dct[x]['supplier_organizationName'])
			OKPD2=(contracts_dct[x]['OKPD2'])
			supplier_kpp=(contracts_dct[x]['supplier_kpp'])
			# print(contracts_dct[x]['ID'])
			# print(y,'-',contracts_dct[x][y])




		regNum= regNum.replace('\'', '')
		signDate= signDate.replace('\'', '')
		contractUrl= contractUrl.replace('\'', '')
		customer_inn= customer_inn.replace('\'', '')
		customer_kpp= customer_kpp.replace('\'', '')
		customer_regNum= customer_regNum.replace('\'', '')
		customer_fullName= customer_fullName.replace('\'', '')
		customer_postalAddress= customer_postalAddress.replace('\'', '')
		supplier_inn= supplier_inn.replace('\'', '')
		supplier_organizationName= supplier_organizationName.replace('\'', '')
		OKPD2= OKPD2.replace('\'', '')
		supplier_kpp= supplier_kpp.replace('\'', '')

		cursor.execute("INSERT INTO contracts (ID,price,regNum,signDate,currentstage,contractUrl,customer_inn,customer_kpp,customer_regNum,customer_fullName,customer_postalAddress,supplier_inn,supplier_organizationName,OKPD2,supplier_kpp) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
							%(ID,price,regNum,signDate,currentstage,contractUrl,customer_inn,customer_kpp,customer_regNum,customer_fullName,customer_postalAddress,supplier_inn,supplier_organizationName,OKPD2,supplier_kpp))

	conn.commit()
	

need_pages=kol_pp(DATA_RANGE_PARSE,'EC')

for x in range(1,need_pages+1):
	add_to_db_date(parse_contract(x))
	print('Добавленно в базу ',x,' страниц из ',kol_pp(DATA_RANGE_PARSE,'EC'))

STAGE_contr='E'
need_pages=kol_pp(DATA_RANGE_PARSE,'E')

for x in range(1,need_pages+1):
	add_to_db_date(parse_contract(x))
	print('Добавленно в базу ',x,' страниц из ',kol_pp(DATA_RANGE_PARSE,'E'))


# print(parse_contract(17))   need_pages+1




#ЗАКРЫВАЕМ БАЗУ
cursor.close()
conn.close()





# # find by id
# contract_id = 38952093
# for contract in r['contracts']['data']:
# 	if contract['id'] == contract_id:
# 		print(contract)