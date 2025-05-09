const unitInfo = {
    // Units
    'units/Worker': {
        name: 'Worker',
        description: 'A unit that gathers resources and constructs buildings.',
        image: 'static/icons/units/worker.png',
        scale: 1.0,
    },
    'units/Soldier': {
        name: 'Soldier',
        description: 'A basic infantry unit.',
        image: 'static/icons/units/soldier.png',
        scale: 1.0,
    },
    'units/AdvancedSoldier': {
        name: 'Advanced Soldier',
        description: 'A highly trained soldier with advanced combat skills.',
        image: 'static/icons/units/advanced_soldier.png',
        scale: 1.0,
    },
    'units/Tank': {
        name: 'Tank',
        description: 'A heavily armored unit with high firepower.',
        image: 'static/icons/units/tank.png',
        scale: 1.0,
    },
    'units/AdvancedTank': {
        name: 'Advanced Tank',
        description: 'An upgraded version of the tank with enhanced capabilities.',
        image: 'static/icons/units/advanced_tank.png',
        scale: 1.0,
    },
    'units/Scout': {
        name: 'Scout',
        description: 'A fast unit used for reconnaissance.',
        image: 'static/icons/units/scout.png',
        scale: 1.0,
    },
    'units/Cavalry': {
        name: 'Cavalry',
        description: 'A fast-moving unit that can traverse rough terrain.',
        image: 'static/icons/units/cavalry.png',
        scale: 1.0,
    },
    'units/Ranged': {
        name: 'Ranged',
        description: 'A unit equipped with ranged weapons.',
        image: 'static/icons/units/ranged.png',
        scale: 1.0,
    },
    'units/AdvancedRanged': {
        name: 'Advanced Ranged',
        description: 'A ranged unit with advanced targeting systems.',
        image: 'static/icons/units/advanced_ranged.png',
        scale: 1.0,
    },

    // Buildings
    'buildings/Capital': {
        name: 'Capital',
        description: 'The main building of a team. Destroying it will eliminate the team.',
        image: 'static/icons/buildings/capital.png',
        scale: 1.0,
    },
    'buildings/Barracks': {
        name: 'Barracks',
        description: 'Increases maximum unit capacity.',
        image: 'static/icons/buildings/barracks.png',
        scale: 1.0,
    },
    'buildings/UnitUpgrader': {
        name: 'Unit Upgrader',
        description: 'Allows for the upgrade of units. Place a unit in the building to upgrade it.',
        image: 'static/icons/buildings/unit_upgrader.png',
        scale: 1.0,
    },
    'buildings/unit_generators/WorkerGenerator': {
        name: 'Worker Generator',
        description: 'Generates worker units every turn.',
        image: 'static/icons/buildings/worker_generator.png',
        scale: 1.0,
    },
    'buildings/unit_generators/SoldierGenerator': {
        name: 'Soldier Generator',
        description: 'Place a worker unit in the building to turn it into a soldier.',
        image: 'static/icons/buildings/soldier_generator.png',
        scale: 1.0,
    },
    'buildings/unit_generators/TankGenerator': {
        name: 'Tank Generator',
        description: 'Place a worker unit in the building to turn it into a tank.',
        image: 'static/icons/buildings/tank_generator.png',
        scale: 1.0,
    },
    'buildings/unit_generators/RangedGenerator': {
        name: 'Ranged Generator',
        description: 'Place a worker unit in the building to turn it into a ranged unit.',
        image: 'static/icons/buildings/ranged_generator.png',
        scale: 1.0,
    },
    'buildings/unit_generators/ScoutGenerator': {
        name: 'Scout Generator',
        description: 'Place a worker unit in the building to turn it into a scout.',
        image: 'static/icons/buildings/scout_generator.png',
        scale: 1.0,
    },

    // Resource Collectors
    'buildings/resource_collectors/Farm': {
        name: 'Farm',
        description: 'Generates food resources every turn.',
        image: 'static/icons/buildings/farm.png',
        scale: 1.0,
    },
    'buildings/resource_collectors/Sawmill': {
        name: 'Sawmill',
        description: 'Generates wood resources every turn.',
        image: 'static/icons/buildings/sawmill.png',
        scale: 1.0,
    },
    'buildings/resource_collectors/Miner': {
        name: 'Miner',
        description: 'Generates mineral resources every turn.',
        image: 'static/icons/buildings/miner.png',
        scale: 1.0,
    },

    // Obstacles
    'obstacles/Mountain': {
        name: 'Mountain',
        description: 'A large obstacle that blocks movement.',
        image: 'static/icons/obstacles/mountain.png',
        scale: 1.0,
    },

    // Resources
    'resources/Food': {
        name: 'Food',
        description: 'Place a farm on this resource to start collecting it.',
        image: 'static/icons/resources/food.png',
        scale: 1.0,
    },
    'resources/Wood': {
        name: 'Wood',
        description: 'Place a sawmill on this resource to start collecting it.',
        image: 'static/icons/resources/wood.png',
        scale: 1.0,
    },
    'resources/Mineral': {
        name: 'Mineral',
        description: 'Place a miner on this resource to start collecting it.',
        image: 'static/icons/resources/mineral.png',
        scale: 1.0,
    },
}

export default unitInfo;
