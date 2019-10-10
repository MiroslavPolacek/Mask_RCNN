import json
import os
ROOT_DIR = os.path.abspath("../../")
#path = "/home/miroslav/Dropbox/Python/Mask_RCNN/JSONtransform"

#Create json test file
TJ = {"Figure_1.jpg123":{"filename":"Figure_1.jpg","size":1234,"regions":[{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,100)), "all_points_y":list(range(100,200))},"region_attributes":{"Ring":""}},{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(10)), "all_points_y":list(range(10))},"region_attributes":{"type":"Ring"}},{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,20)), "all_points_y":list(range(20,40))},"region_attributes":{"notRing":"",}},{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(10)), "all_points_y":list(range(10))},"region_attributes":{"type":"Ring"}},{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,10)), "all_points_y":list(range(10,20))},"region_attributes":{"type":"Ring"}}],"file_attributes":{}},
"Figure_2.jpg123":{"filename":"Figure_2.jpg","size":23456,"regions":[{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(10)), "all_points_y":list(range(10))},"region_attributes":{"Ring":"","type":"Ring"}},{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(20)), "all_points_y":list(range(20))},"region_attributes":{"Ring":""}},{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(10)), "all_points_y":list(range(10))},"region_attributes":{"type":"Ring"}}],"file_attributes":{}},
"Figure_3.jpg123":{"filename":"Figure_3.jpg","size":345,"regions":[{
	"shape_attributes":{"name":"polygon","all_points_x":list(range(20)), "all_points_y":list(range(20))},"region_attributes":{"Ring":"","type":"Ring"}},{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,10)), "all_points_y":list(range(10,20))},"region_attributes":{"Ring":""}},{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,20)), "all_points_y":list(range(20,40))},"region_attributes":{"Ring":""}},{
	"shape_attributes":{"name":"polyline","all_points_x":list(range(0,30)), "all_points_y":list(range(30,60))},"region_attributes":{"Ring":""}}],"file_attributes":{}}
}

##With 3 figures and 2 (Figure_1 and 3)containing polylines
##Some othe kind of shapes (polygon)
##Some other kind of object not containing "Ring"

with open(os.path.join(ROOT_DIR,'Mask_RCNN/JSONtransform/testJSON.json'), 'w') as outfile:
	json.dump(TJ, outfile, indent = 4)

#Test JSON
import polylinesToPolygonJSON

def test_linesToPolygons():
	newJ = polylinesToPolygonJSON.linesToPolygons()
	#if the type is dictionary
	assert type(newJ) is dict
	#if contains 3 figures
	assert len(newJ.items()) == 3
	#figure 1 should have one polygone and figure 2 none and figure 3 two


	#the first object in the first figure should be polygon...may be all should be polygon
	assert newJ['Figure_1.jpg123']['regions'][0]['shape_attributes']['name'] == 'polygon'
	#check expected lengths of all_points_x
	allxCounts = []
	for figure, figureAtt in newJ.items():
		try:
			for i in range(len(newJ[figure]['regions'])):
				number = len(newJ[figure]['regions'][i]['shape_attributes']['all_points_x'])
				allxCounts.append(number)
		except:
			pass
	assert allxCounts ==[110,30,50]
	
	#all_points_x should have the same length as corresponding all_points_y
	allyCounts = []
	for figure, figureAtt in newJ.items():
		try:
			for i in range(len(newJ[figure]['regions'])):
				number = len(newJ[figure]['regions'][i]['shape_attributes']['all_points_y'])
				allyCounts.append(number)
		except:
			pass		
	assert allxCounts == allyCounts
	
	#check number of expected polygons
	polygonCounts = []
	for figure, figureAtt in newJ.items():
		try:
			number = len(newJ[figure]['regions'])
		except:
			number = 0
			pass
		polygonCounts.append(number)
	assert polygonCounts == [1,0,2]