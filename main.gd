extends Node

class_name Main

signal http_completed

var field_size = 8
var field
var hitboxes_container
var selected_cell
var hitboxes: Array[Array]

var selected_entity: Entity

var not_selected = Color("dark gray", 0.06)
var selected = Color("yellow", 0.3)
var movable = Color("blue", 0.3)

var testing = true

var internet_enabled = false

var url: String = "http://127.0.0.1:8000" + "/api/v1"

var json: JSON

var http_request: HTTPRequest

var result
var response_code
var headers
var body

var availible_moves: Array[Array]

var positions: Array[Array]

var scale: Vector3

var game: Game

var TEAMS_NEUTRAL_ID = "neutral"

var label: Node

enum GameStates {
	BEFORE_START,
	IN_PROGRESS,
	FINISHED,
}

class Map:
	var sectors: Array 
	var entities: Dictionary 
	var influence: Array 
	
	func _init():
		sectors = []
		entities = {}
		influence = []
	
	func setFromJSON(data):
		sectors = data["sectors"]
		for key in data["entities"].keys():
			var entity = Entity.new()
			entity.setFromJSON(data["entities"][key])
			entities[key] = entity
			#print()
			#print(data["entities"].keys())
			#print()
			#print(entities[key])
			#print(data["entities"][key])
			#print()
		#entities = data["entities"]
		#print(data["entities"])
		#print()
		#print("ents")
		#print(entities)
		influence = data["influence"]
		#print(influence)
		

class Game:
	var id: String
	var map: Map
	var teams: Dictionary 
	var state: GameStates
	var activeTeamId: String
	var winningTeamId: String
	
	func _init():
		var TEAMS_NEUTRAL_ID = "neutral"
		activeTeamId = TEAMS_NEUTRAL_ID
		winningTeamId = TEAMS_NEUTRAL_ID
		map = Map.new()
		teams = {}
		state = GameStates.BEFORE_START
		
	func setFromJSON(data):
		id = data["id"]
		map.setFromJSON(data["map"])
		teams = {}
		for i in data["teams"].keys():
			var team = Team.new()
			team.setFromJSON(data["teams"][i])
			teams[i] = team
		state = GameStates.get(data["state"].to_upper())
		activeTeamId = data["activeTeamId"]
		winningTeamId = data["winningTeamId"]
		
		if true:
			map = Map.new()
			map.setFromJSON(JSON.parse_string('{"sectors":[[[{"id":"1c83c71f-f051-40ba-b591-183e040addd6","position":{"x":0,"y":0},"teamId":"34214631246321463123","type":"Capital","namespace":"buildings"}, {"id":"78e34539-dc79-41c0-99c1-591294f6a9bc","position":{"x":0,"y":0},"teamId":"4532164312","type":"Worker","namespace":"units","health":5,"armor":0,"damage":0,"movementRange":1,"attackRange":0}],[],[],[{"id":"58eb376a-ed8b-4084-be05-0c4c646e23c3","position":{"x":0,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"eda37701-ab8c-4ffc-8365-4952db04768b","position":{"x":1,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"eb19e8af-97c9-447c-8c20-ad44c578c254","position":{"x":2,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"9f5979f8-b27f-41dd-b2fe-4e4ea20bdf3b","position":{"x":3,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"b84c0038-cfd5-4f89-80b7-cf8135cc9a2b","position":{"x":4,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"af948946-2b96-4aca-91a9-867388fe1164","position":{"x":5,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[{"id":"1d2ce34c-a969-41e1-a284-d9b6b439a598","position":{"x":6,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}],[],[],[],[]],[[],[],[],[],[],[],[],[{"id":"9b7ac6e1-0b0a-407e-9bb5-42ebf3773fcf","position":{"x":7,"y":7},"teamId":"91463216425320541230","type":"Capital","namespace":"buildings"}]]],"entities":{"1c83c71f-f051-40ba-b591-183e040addd6":{"id":"1c83c71f-f051-40ba-b591-183e040addd6","position":{"x":0,"y":0},"teamId":"34214631246321463123","type":"Capital","namespace":"buildings"},"9b7ac6e1-0b0a-407e-9bb5-42ebf3773fcf":{"id":"9b7ac6e1-0b0a-407e-9bb5-42ebf3773fcf","position":{"x":7,"y":7},"teamId":"91463216425320541230","type":"Capital","namespace":"buildings"},"58eb376a-ed8b-4084-be05-0c4c646e23c3":{"id":"58eb376a-ed8b-4084-be05-0c4c646e23c3","position":{"x":0,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"eda37701-ab8c-4ffc-8365-4952db04768b":{"id":"eda37701-ab8c-4ffc-8365-4952db04768b","position":{"x":1,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"eb19e8af-97c9-447c-8c20-ad44c578c254":{"id":"eb19e8af-97c9-447c-8c20-ad44c578c254","position":{"x":2,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"9f5979f8-b27f-41dd-b2fe-4e4ea20bdf3b":{"id":"9f5979f8-b27f-41dd-b2fe-4e4ea20bdf3b","position":{"x":3,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"b84c0038-cfd5-4f89-80b7-cf8135cc9a2b":{"id":"b84c0038-cfd5-4f89-80b7-cf8135cc9a2b","position":{"x":4,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"af948946-2b96-4aca-91a9-867388fe1164":{"id":"af948946-2b96-4aca-91a9-867388fe1164","position":{"x":5,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"},"1d2ce34c-a969-41e1-a284-d9b6b439a598":{"id":"1d2ce34c-a969-41e1-a284-d9b6b439a598","position":{"x":6,"y":3},"teamId":"neutral","type":"Mountain","namespace":"obstacles"}},"influence":[["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"],["neutral","neutral","neutral","neutral","neutral","neutral","neutral","neutral"]]}'))
		
		#print(id)
		#print(map)
		#print(teams)
		#print(state)
		#print(activeTeamId)
		#print(winningTeamId)
		

class Resources:
	var food: int = 0
	var wood: int = 0
	var minerals: int = 0
	
	func _init():
		food = 0
		wood = 0
		minerals = 0
	
	func setFromJSON(data):
		food = data["food"]
		wood = data["wood"]
		minerals = data["minerals"]
		

class Team:
	var id: String
	var name: String
	var visible_area: Array[Vector2i]
	var resources: Resources
	
	func _init():
		visible_area = []
		resources = Resources.new()
	
	func setFromJSON(data):
		id = data["id"]
		name = data["name"]
		#print(data["visibleArea"])
		for value in data["visibleArea"]:
			visible_area.append(Vector2i(value["x"], value["y"]))
		#visible_area = data["visibleArea"]
		resources.setFromJSON(data["resources"])
	
class Entity:
	var id: String
	var position: Vector2i
	var teamId: String
	var type: String
	var ns: String
	var unit: Node = null
	
	func _init():
		unit = null
	
	func setFromJSON(data):
		id = data["id"]
		position = Vector2i(data["position"]["x"], data["position"]["y"])
		teamId = data["teamId"]
		type = data["type"]
		ns = data["namespace"]
		#print(id)
		#print(ns)
	
var unitInfo = [
	 'units/AdvancedSoldier', null, null, null, null,
	 'units/Soldier', "res://assets/VO-entiteti/soldier/scene.gltf", Vector3(0,0,0), Vector3(0,0,0), Vector3(0.5,0.5,0.5),
	 'units/Worker', "res://assets/VO-entiteti/soldier/scene.gltf", Vector3(0,0,0), Vector3(0,0,0), Vector3(0.5,0.5,0.5), #null, null, null, null,
	 'units/Tank', "res://assets/VO-entiteti/tank/tank.glb", Vector3(0,0,0), Vector3(0,0,0), Vector3(0.4,0.4,0.4),
	 'units/Calvary', null, null, null, null,
	 'units/AdvancedRanged', null, null, null, null,
	 'units/Scout', null, null, null, null,
	 'units/AdvancedTank', "res://assets/VO-entiteti/advanced_tank/advanced_tank.gltf", Vector3(0,0,0), Vector3(0,0,0), Vector3(0.2,0.2,0.2),
	 'units/Ranged', null, null, null, null,
	 'buildings/UnitUpgrader', null, null, null, null,
	 'buildings/Capital', "res://assets/VO-entiteti/main_city/scene.gltf", Vector3(0,0.12,0), Vector3(0,0,0), Vector3(0.1,0.1,0.1),
	 'buildings/Barracks', null, null, null, null,
	 'buildings/unit_generators/WorkerGenerator', "res://assets/VO-entiteti/worker_generator/worker_generator.glb", Vector3(0,0,0), Vector3(0,0,0), Vector3(0.004,0.004,0.004),
	 'buildings/unit_generators/SoldierGenerator', null, null, null, null,
	 'buildings/unit_generators/TankGenerator', null, null, null, null,
	 'buildings/unit_generators/RangedGenerator', null, null, null, null,
	 'buildings/unit_generators/ScoutGenerator', null, null, null, null,
	 'buildings/resource_collectors/Farm', "res://assets/VO-entiteti/farm/scene.gltf", Vector3(0,0.1,0), Vector3(0,0,0), Vector3(0.04,0.04,0.04),
	 'buildings/resource_collectors/Sawmill', "res://assets/VO-entiteti/sawmill/scene.gltf", Vector3(0,0.05,0), Vector3(0,0,0), Vector3(0.02,0.02,0.02),
	 'buildings/resource_collectors/Miner', null, null, null, null,
	 'obstacles/Mountain', "res://assets/VO-entiteti/mountain/everest.gltf", Vector3(0,0.1,0), Vector3(0,0,0), Vector3(0.3,0.3,0.3),
	 'resources/Food', "res://assets/VO-entiteti/food/scene.gltf", Vector3(0,0.25,0), Vector3(0,0,0), Vector3(0.9,0.9,0.9),
	 'resources/Wood', "res://assets/VO-entiteti/wood/scene.gltf", Vector3(0,0.3,0), Vector3(0,0,0), Vector3(0.9,0.9,0.9),
	 'resources/Mineral', "res://assets/VO-entiteti/mineral/scene.gltf", Vector3(-1,3,1.22), Vector3(0,0,0), Vector3(0.2,0.2,0.2),
	]
	
var unit_data_count 
	
func unitsAllInfo():
	var types = []
	var paths = []
	var poss = []
	var rots = []
	var scales = []
	for i in range(len(unitInfo)):
		if i%5 ==0:
			types.append(unitInfo[i])
		elif i%5 ==1:
			paths.append(unitInfo[i])
		elif i%5 ==2:
			poss.append(unitInfo[i])
		elif i%5 ==3:
			rots.append(unitInfo[i])
		else:
			scales.append(unitInfo[i])
			
	return {"types": types, "paths": paths, "positions": poss, "rotations": rots, "scales": scales}

var units = {}

var unit_preloads = {
	'units/AdvancedSoldier': AdvancedSoldier_preload,
	'units/Soldier': Soldier_preload,
	'units/Worker': Worker_preload,
	'units/Tank': Tank_preload,
	'units/Calvary': Calvary_preload,
	'units/AdvancedRanged': AdvancedRanged_preload,
	'units/Scout': Scout_preload,
	'units/AdvancedTank': AdvancedTank_preload,
	'units/Ranged': Ranged_preload,
	'buildings/UnitUpgrader': UnitUpgrader_preload,
	'buildings/Capital': Capital_preload,
	'buildings/Barracks': Barracks_preload,
	'buildings/unit_generators/WorkerGenerator': WorkerGenerator_preload,
	'buildings/unit_generators/SoldierGenerator': SoldierGenerator_preload,
	'buildings/unit_generators/TankGenerator': TankGenerator_preload,
	'buildings/unit_generators/RangedGenerator': RangedGenerator_preload,
	'buildings/unit_generators/ScoutGenerator': ScoutGenerator_preload,
	'buildings/resource_collectors/Farm': Farm_preload,
	'buildings/resource_collectors/Sawmill': Sawmill_preload,
	'buildings/resource_collectors/Miner': Miner_preload,
	'obstacles/Mountain': Mountain_preload,
	'resources/Food': Food_preload,
	'resources/Wood': Wood_preload,
	'resources/Mineral': Mineral_preload
}

var AdvancedSoldier_preload
var Soldier_preload
var Worker_preload
var Tank_preload
var Calvary_preload
var AdvancedRanged_preload
var Scout_preload
var AdvancedTank_preload
var Ranged_preload
var UnitUpgrader_preload
var Capital_preload
var Barracks_preload
var WorkerGenerator_preload
var SoldierGenerator_preload
var TankGenerator_preload
var RangedGenerator_preload
var ScoutGenerator_preload
var Farm_preload
var Sawmill_preload
var Miner_preload
var Mountain_preload
var Food_preload
var Wood_preload
var Mineral_preload

var basic_unit_preload

func prepareUnits():
	for type in unitsAllInfo()["types"]:
		units[type] = {"free": [], "used": []}
		
func getFreeUnit(nstype: String) -> Node:
	var dict = units[nstype]
	if dict["free"].size() == 0:
		var unit = makeNewUnit(nstype)
		dict["used"].append(unit)
		return unit
	else:
		var unit = dict["free"].pop_back()
		unit.set_visible(true)
		return unit

func freeUnit(entity: Entity):
	var nstype = entity.ns + "/" + entity.type
	var dict = units[nstype]
	var pos = dict["used"].find(entity.unit)
	if pos == -1:
		return
	var unit = dict["used"][pos]
	unit.set_visible(false)
	dict["free"].append(unit)
	
func makeNewUnit(nstype) -> Node:
	field = get_node("Field")
	var entities = field.get_node("Entities")
	
	var allInfo = unitsAllInfo()
	
	var pos = allInfo["types"].find(nstype)
	
	var instance
	
	if pos == -1:
		instance = basic_unit_preload.instantiate()
	else:
		var gltf_document_load = GLTFDocument.new()
		var gltf_state_load = GLTFState.new()
		var error = gltf_document_load.append_from_file(
				allInfo["paths"][pos], gltf_state_load)
		if error == OK:
			instance = gltf_document_load.generate_scene(gltf_state_load)
			instance.position = allInfo["positions"][pos]
			instance.rotation = allInfo["rotations"][pos]
			instance.scale = allInfo["scales"][pos]
		else:
			push_error("Couldn't load glTF scene (error code: %s)." % error_string(error))
	
	#print(instance.get_children().get_children())
	#instance.input_ray_pickable = false
	
	entities.add_child(instance)
	return instance
	
func freeAllUnitsFromEntities(entities):
	for key in entities.keys():
		var entity = entities[key]
		freeUnit(entity)
	
func loadUnits(entities):
	for key in entities.keys():
		var entity = entities[key]
		#print(entity)
		var nstype = entity.ns + "/" + entity.type
		entity.unit = getFreeUnit(nstype)
		entity.unit.position.x = positions[entity.position.x][entity.position.y].x
		#entity.unit.position.y = positions[entity.position.x][entity.position.y].y
		entity.unit.position.z = positions[entity.position.x][entity.position.y].z
		
var button_text = [
	"Unit Upgrader",
	"Barracks",
	"Worker Generator",
	"Soldier Generator",
	"Tank Generator",
	"Ranged Generator",
	"Scout Generator",
	"Farm",
	"Sawmill",
	"Miner",
]

var building_ns = [
	'buildings',
	'buildings',
	'buildings/unit_generators',
	'buildings/unit_generators',
	'buildings/unit_generators',
	'buildings/unit_generators',
	'buildings/unit_generators',
	'buildings/resource_collectors',
	'buildings/resource_collectors',
	'buildings/resource_collectors',
]

var building_types = [
	"UnitUpgrader",
	"Barracks",
	"WorkerGenerator",
	"SoldierGenerator",
	"TankGenerator",
	"RangedGenerator",
	"ScoutGenerator",
	"Farm",
	"Sawmill",
	"Miner",
]

func getSectorsAllEntities():
	var entities = {}
	for i in range(field_size):
		for j in range(field_size):
			var sector = game.map.sectors[i][j]
			for data in sector:
				var entity = Entity.new()
				entity.setFromJSON(data)
				entities[entity["id"]] = entity
	return entities

func resetMap(data):
	clearMap()
	loadSectors(data)
	loadUnits(getSectorsAllEntities())

func clearMap():
	freeAllUnitsFromEntities(game.map.entities)
	
func loadSectors(data):
	game.map.sectors = data

func _ready():
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
		
	json = JSON.new()
	
	label = get_node("UserInterface/Label")
	
	basic_unit_preload = preload("res://unit.tscn")
	
	var building_select = get_node("UserInterface/BuildingSelect")
	var buttons = building_select.get_children()
	
	for i in range(len(buttons)):
		if i != 0:
			buttons[i].text = button_text[i-1]	
		
	building_select.set_visible(false)
	
	field = get_node("Field")
	var hitbox_preload = preload("res://hitbox.tscn")
	hitboxes_container = field.get_node("Hitboxes")
	#print(hitboxes)
	#var instance = hitbox.instantiate()
	#hitboxes.add_child(instance)
	for i in range(field_size):
		hitboxes.append([]) 
		for j in range(field_size):
			hitboxes[i].append(null)
			
	for i in range(field_size):
		positions.append([]) 
		for j in range(field_size):
			positions[i].append(Vector3(-4+4.0/field_size+2*i*(4.0/field_size),0.5,
					-4+4.0/field_size+2*j*(4.0/field_size)))
	
	var scale_xyz = 8.0/field_size
	scale = Vector3(scale_xyz,scale_xyz,scale_xyz)
	
	for i in range(field_size):
		for j in range(field_size):
			var instance = hitbox_preload.instantiate()
			instance.name = "hitbox_" + str(i) + "_" + str(j)
			#instance.position = Vector3(-4 + 4.0/fieldSize + 7/(fieldSize-1)*i, \
				#0.5, -4 + 4.0/fieldSize + 7/(fieldSize-1)*j)
			instance.position = positions[i][j]
			instance.scale = scale
			#print(instance.position)
			#print((fieldSize-1))
			#print((fieldSize-1)/2)
			instance.location = Vector2i(i, j)
			
			
			var material = instance.get_node("MeshInstance3D").get_active_material(0)
			material = material.duplicate()
			material.albedo_color = not_selected
			instance.get_node("MeshInstance3D").set_surface_override_material(0, material)
			
			
			hitboxes_container.add_child(instance)
			hitboxes[i][j] = instance
			#print("test")
		
	#print(hitboxes.get_children())
	
	#for hitbox in hitboxes.get_children():
		#hitbox.input_event.connect(selectedCell)
		
	clearActions()
	
	prepareUnits()
	
	await startGame()
	#
	#print(json.data.keys())
	
	await getVisibleMap()
	
	if internet_enabled:
		#print(json.data.keys())
		
		var map_data = json.data["sectors"]
		
		resetMap(map_data)
	
	else:
		resetMap(game.map.sectors)
	
	#var gltf_document_load = GLTFDocument.new()
	#var gltf_state_load = GLTFState.new()
	#var error = gltf_document_load.append_from_file(
			#"res://assets/VO-entiteti/worker_generator/worker_generator.glb", gltf_state_load)
	#if error == OK:
		#var gltf_scene_root_node = gltf_document_load.generate_scene(gltf_state_load)
		#add_child(gltf_scene_root_node)
	#else:
		#push_error("Couldn't load glTF scene (error code: %s)." % error_string(error))

func colorObject(object, color):
	var material = object.get_node("MeshInstance3D").get_active_material(0)
	material = material.duplicate()
	material.albedo_color = color
	object.get_node("MeshInstance3D").set_surface_override_material(0, material)
	
func getSelectedEntity(location: Vector2i) -> Entity:
	var top_unit = null
	
	#print(game.map.sectors)
	#print()
	#print(game.map.sectors[location.x][location.y])
	
	for unit in game.map.sectors[location.x][location.y]:
		if top_unit == null:
			top_unit = unit
		elif top_unit["namespace"] == "buildings":
			top_unit = unit
			
	if top_unit == null || top_unit["namespace"] != "units":
		return null
		
	var sector_entitites = getSectorsAllEntities()
	
	return sector_entitites[top_unit["id"]]
	
func selectedCell(location: Vector2i) -> void:
	if (availible_moves[location.x][location.y] != null):
		if internet_enabled:
			await move(location)
		return

	if (selected_cell == null || selected_cell.location != location):
		clearActions()
		#cancelAction()
		
	selected_cell = hitboxes[location.x][location.y]
	colorObject(selected_cell, selected)
	#print(location)
	
	selected_entity = getSelectedEntity(location)
	
	print(selected_entity)
	
	if selected_entity == null:
		return
	
	if internet_enabled:
		var name = "selectedCell"
		
		var error = send_request("/game/"+ game.id +"/team/" + game.activeTeamId
			 + "/end-unit/" + selected_entity.id + "/build/available-buildings", 
			[], HTTPClient.METHOD_POST, JSON.stringify({}))
		
		if error != OK:
			push_error(name + " sendRequest available")
		
		await http_completed
		
		getJson(name, body)
		
		var available_buldings = json.data["availableBuildings"]
		
		var building_select = get_node("UserInterface/BuildingSelect")
		
		if available_buldings != []:
			building_select.set_visible(true)
		
		var buttons = building_select.get_children()
		
		for i in range(len(buttons)):
			if i != 0:
				buttons[i].set_visible(false)
		
		for ns_type in available_buldings:
			var pos = building_types.find(ns_type["type"])
			buttons[pos+1].set_visible(true)
			
		
		error = send_request("/game/"+ game.id +"/team/" + game.activeTeamId
			 + "/end-unit/" + selected_entity.id + "/move/reachable-sectors", 
			[], HTTPClient.METHOD_POST, JSON.stringify({}))
		
		if error != OK:
			push_error(name + " sendRequest available")
		
		await http_completed
		
		getJson(name, body)
		
		var reachable_sectors = json.data["sectors"]
		
		setAvailableMoves(reachable_sectors)
		
		colorAvailableMoves(movable)
		
	else:
		var available_buldings = [["buildings", "UnitUpgrader"], ["buildings", "Capital"], ["buildings", "Barracks"], ["buildings/unit_generators", "WorkerGenerator"], ["buildings/unit_generators", "SoldierGenerator"], ["buildings/unit_generators", "TankGenerator"], ["buildings/unit_generators", "RangedGenerator"], ["buildings/unit_generators", "ScoutGenerator"]]
		
		var building_select = get_node("UserInterface/BuildingSelect")
		
		if available_buldings != []:
			building_select.set_visible(true)
		
		var buttons = building_select.get_children()
		
		for i in range(len(buttons)):
			if i != 0:
				buttons[i].set_visible(false)
		
		for ns_type in available_buldings:
			var pos = building_types.find(ns_type[1])
			buttons[pos+1].set_visible(true)
		
		var reachable_sectors = [
			{"x":0, "y":1},
			{"x":1, "y":0},
			]
			
		setAvailableMoves(reachable_sectors)
			
		colorAvailableMoves(movable)
	
		
	
	# work with results -> result, response_code, headers, body

func setAvailableMoves(reachable_sectors):
	for pos in reachable_sectors:
		availible_moves[pos["x"]][pos["y"]] = 1
		
func colorAvailableMoves(color):
	for i in range(field_size):
		for j in range(field_size):
			if availible_moves[i][j] != null:
				selected_cell = hitboxes[i][j]
				colorObject(selected_cell, color)


func clearActions():
	for i in range(field_size):
		availible_moves.append([]) 
		for j in range(field_size):
			availible_moves[i].append(null)
			
	var building_select = get_node("UserInterface/BuildingSelect")
	var buttons = building_select.get_children()
	
	building_select.set_visible(false)
	
	for i in range(len(buttons)):
		if i != 0:
			buttons[i].set_visible(false)
			
	colorAvailableMoves(not_selected)
	
	if (selected_cell != null):
		colorObject(selected_cell, not_selected)
		
	#print(selected_cell.location)
	
# TODO
func move(location):
	var error = send_request("/bruhendpoiunt" , [], HTTPClient.METHOD_POST, 
		str(selected_cell.location) + " " + str(location) + "idk upit il nes")
	
	await http_completed
	
	
	clearActions()
	
	
	
func getJson(where, body):
	var error = json.parse(body)
	
	if error != OK:
		push_error(where + " json")
		push_error("JSON Parse Error: " + json.get_error_message() + " in " + body + 
			" at line " + json.get_error_line())

func getVisibleMap():
	if internet_enabled:
		var name = "getVisibleMap"
		var error = send_request("/game/"+ game.id +"/team/" + game.activeTeamId
			 + "/visible-map" , [], HTTPClient.METHOD_POST, JSON.stringify({}))
		
		if error != OK:
			push_error(name + " getVisibleMap")
		
		print("awaiting")
		await http_completed
		
		print("awaited")
		
		getJson(name, body)

func startGame():
	if internet_enabled:
		var name = "startGame"
		var error = send_request("/game" , [], HTTPClient.METHOD_POST, JSON.stringify({"mapName": "mapa"}))
		
		#print(error)
		
		if error != OK:
			push_error(name + " startGame")
		
		await http_completed
		
		print(response_code)
		print(body)
		print(json.parse(body))
		
		getJson(name, body)
		
	else:
		var body = '{
  "game": {
	"id": "string",
	"map": {
	  "sectors": [
		[
		  [
			{
			  "id": "string",
			  "position": {
				"x": 0,
				"y": 0
			  },
			  "teamId": "string",
			  "type": "string",
			  "namespace": "string",
			  "additionalProp1": {}
			}
		  ]
		]
	  ],
	  "entities": {
		"additionalProp1": {
		  "id": "string",
		  "position": {
			"x": 0,
			"y": 0
		  },
		  "teamId": "string",
		  "type": "string",
		  "namespace": "string",
		  "additionalProp1": {}
		},
		"additionalProp2": {
		  "id": "string",
		  "position": {
			"x": 0,
			"y": 0
		  },
		  "teamId": "string",
		  "type": "string",
		  "namespace": "string",
		  "additionalProp1": {}
		},
		"additionalProp3": {
		  "id": "string",
		  "position": {
			"x": 0,
			"y": 0
		  },
		  "teamId": "string",
		  "type": "string",
		  "namespace": "string",
		  "additionalProp1": {}
		}
	  },
	  "influence": [
		[
		  "string"
		]
	  ]
	},
	"teams": {
	  "additionalProp1": {
		"id": "string",
		"name": "string",
		"visibleArea": [
		  {
			"x": 0,
			"y": 0
		  }
		],
		"resources": {
		  "food": 0,
		  "wood": 0,
		  "minerals": 0
		}
	  },
	  "additionalProp2": {
		"id": "string",
		"name": "string",
		"visibleArea": [
		  {
			"x": 0,
			"y": 0
		  }
		],
		"resources": {
		  "food": 0,
		  "wood": 0,
		  "minerals": 0
		}
	  },
	  "additionalProp3": {
		"id": "string",
		"name": "string",
		"visibleArea": [
		  {
			"x": 0,
			"y": 0
		  }
		],
		"resources": {
		  "food": 0,
		  "wood": 0,
		  "minerals": 0
		}
	  }
	},
	"history": {
	  "actions": [],
	  "mapStates": []
	},
	"state": "before_start",
	"activeTeamId": "neutral",
	"winningTeamId": "neutral"
  }
}'
		getJson(name, body)
		
	game = Game.new()
	game.setFromJSON(json.data["game"])
	
func buildingSelected(event: InputEvent, extra_arg_0: String) -> void:
	if (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		print(extra_arg_0)
		var pos = building_types.find(extra_arg_0)
		if internet_enabled:
			var name = "buildingSelected"
			var error = send_request("/game/"+ game.id +"/team/" + game.activeTeamId
				 + "/unit/" + selected_entity.id + "/build" , [], HTTPClient.METHOD_POST, 
				JSON.stringify({
					"buildingType": building_types[pos],
					"buildingNamespace": building_ns[pos]
				}))
			
			if error != OK:
				push_error(name + " buildingSelected")
			
			await http_completed
			
			getJson(name, body)
	
func newTurnPressed():
	if internet_enabled:
		var name = "newTurnPressed"
		var error = send_request("/game/"+ game.id +"/team/" + game.activeTeamId
			 + "/end-turn" , [], HTTPClient.METHOD_POST, JSON.stringify({}))
		
		if error != OK:
			push_error(name + " newTurnPressed")
		
		await http_completed
		
		getJson(name, body)
	
func cancelAction():
	if (selected_cell != null):
		colorObject(selected_cell, not_selected)
		
	
	var resources: Resources
	if label.resources == null:
		resources = Resources.new()
	else:
		resources = label.resources
	
	resources.food += 1
	resources.wood += 1
	resources.minerals += 1
	
	label.updateResources(resources)
	
func _input(event: InputEvent) -> void:
	
	if (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT):
		clearActions()

func send_request(endpoint: String, headers: PackedStringArray, method: HTTPClient.Method, data: String):
	var error = http_request.request(url+endpoint, headers, method, data)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
	
	print("requestted http")	
	print(url+endpoint, headers, method, data)
	
	return error
	
func _http_request_completed(_result, _response_code, _headers, _body):
	print("_http_request_completed start")
	
	if _result != HTTPRequest.RESULT_SUCCESS:
		push_error("HTTP request unsuccessful.")
	
	result = _result
	response_code = _response_code
	headers = _headers
	body = _body
	
	print("_http_request_completed")
	
	http_completed.emit()
