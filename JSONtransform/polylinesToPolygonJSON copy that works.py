import os
import json
import numpy as np
import copy

ROOT_DIR = os.path.abspath("../../")

def getRegion(imageV,type = 'Ring'):
	goodRegions = []
	orderX = []
	it = iter(imageV)
	for region in it:
		regAtt = region['region_attributes']
		shAtt = region['shape_attributes']
		if shAtt['name'] == 'polyline':
			for regk, regv in regAtt.items():
				if regv == type or regv == type:
					goodRegions.append(region)
					orderX.append(np.average(shAtt['all_points_x']))
	if not goodRegions:
		print("No data")
		return None
	return {'goodRegions':goodRegions, 'orderX':(np.argsort(orderX))}

def linesToPolygons(input = 'testJSON.json', output = 'testJSONresult.json'):
	
	newJ = {}
	shpAttrBase = {'name':'polygon'}
	with open(os.path.join(ROOT_DIR,'Mask_RCNN/JSONtransform/',input),'r') as json_file:
		dct = json.load(json_file)
		for image, imageAtt in dct.items():
			print("Which image:",' ',image)
			newJ[image] = {}
			for imageK, imageV in imageAtt.items():
				print("imageKeys:",' ',imageK)
				if imageK == 'regions':
					print("unsortedRegions:",' ',imageV)
					sortRegions = getRegion(imageV,type='Ring')
					if sortRegions == None:
						print("continue, no sortRegions")
						continue;
					print("sortRegions:",' ',sortRegions)
					print('orderX: ',sortRegions['orderX'])
					shpAtt = shpAttrBase.copy()
					newJ[image]['regions'] = []
					for i in range(len(sortRegions['orderX'])-1):
						print(i)
						firstRegion = sortRegions['goodRegions'][sortRegions['orderX'][i]]['shape_attributes']
						secondRegion = sortRegions['goodRegions'][sortRegions['orderX'][i+1]]['shape_attributes']
						print('firstRegion: ',firstRegion)
						print('secondRegion: ',secondRegion)
						shpAtt['all_points_x'] = firstRegion['all_points_x'] + secondRegion['all_points_x'][::-1]
						shpAtt['all_points_y'] = firstRegion['all_points_y'] + secondRegion['all_points_y'][::-1]
						print('newAtt: ',shpAtt)
						regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'RingBndy'}}
						newJ[image]['regions'].append(copy.deepcopy(regions))
				else:
					#print(imageV)
					try:
						newJ[image][imageK] = imageV
					except:
						print("can't append:",' ',imageK,",",imageV)
			with open(os.path.join(ROOT_DIR,'Mask_RCNN/JSONtransform/', output),'w') as outfile:
				json.dump(newJ, outfile,indent=4)
	return newJ
