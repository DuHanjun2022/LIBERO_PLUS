import itertools
from pprint import pprint
from gen_utils import generate_task_bddl
from gen_utils import ObjectInitState, TaskInitState, DestInitState, BackgroundInitState, Distribution


################################################################################
## 1. HIGH-LEVEL CONFIGURATION
################################################################################

# Define all possible components here
TASK_COMPONENTS = {
    "task_name": "moka_pots",
    "backgrounds": {
        "train": ["living_room", "kitchen", "floor"],
        "eval": ["study"],
    },
    "objects": {
        "pot": "moka_pot",
        "mug_distractor": "white_yellow_mug",
    },
    "locations": {
        "left":   {"coords": ([-0.025, 0.2], [0.175, 0.1]), "nl": "left"},
        "middle": {"coords": ([-0.025, 0.0], [0.175, 0.1]), "nl": "middle"},
        "right":  {"coords": ([-0.025, -0.2], [0.175, 0.1]), "nl": "right"},
    },
    "default_dist": Distribution([-0.025, 0.0], [0.175, 0.3]),
}

# Define the scenarios using the components above
# This is where you describe your task suites at a high level.
SCENARIOS = [
    { 
        "name": "train_2_pots_1_distractor",
        "task_suite": "libero_10_random_temp",
        "base_id": 10000,
        "backgrounds": TASK_COMPONENTS["backgrounds"]["train"],
        "objects_to_place": [TASK_COMPONENTS["objects"]["pot"]] * 2,
        "distractors": [TASK_COMPONENTS["objects"]["mug_distractor"]],
        # Generate all unique combinations of 2 locations
        "location_placements": list(itertools.combinations(TASK_COMPONENTS["locations"].keys(), 2)),
        "language_template": "put both moka pots on the stove",
    },
    { # spatial reasoning with distractor pot
        "name": "train_3_pots",
        "task_suite": "custom_eval_easy_temp",
        "base_id": 20000,
        "backgrounds": TASK_COMPONENTS["backgrounds"]["train"] + TASK_COMPONENTS["backgrounds"]["eval"],
        "objects_to_place": [TASK_COMPONENTS["objects"]["pot"]] * 3,
        "distractors": [],
        # Specify exact location pairings for this evaluation task
        "location_placements": [
            ("left", "right"),
            ("middle", "left"),
        ],
        "language_template": "put the {obj_1} on the {loc_1_nl} plate and the {obj_2} on the {loc_2_nl} plate",
    },
    { # spatial reasoning with distractor pot (eval uses middle, right combination)
        "name": "eval_3_pots",
        "task_suite": "custom_eval_easy_temp",
        "base_id": 20000,
        "backgrounds": TASK_COMPONENTS["backgrounds"]["train"] + TASK_COMPONENTS["backgrounds"]["eval"],
        "objects_to_place": [TASK_COMPONENTS["objects"]["pot"]] * 3,
        "distractors": [],
        # Specify exact location pairings for this evaluation task
        "location_placements": [
            ("middle", "right"),
        ],
        "language_template": "put the {obj_1} on the {loc_1_nl} plate and the {obj_2} on the {loc_2_nl} plate",
    }
]

################################################################################
## 2. TASK GENERATION LOGIC
################################################################################

def generate_tasks_from_scenarios(scenarios, components):
    """
    Generates all tasks based on a list of scenarios and a components dictionary.
    """
    id_task_mapping = {}
    
    # Use itertools.combinations to get all unique pairs of objects to place
    for scenario in scenarios:
        print(f"Processing Scenario: {scenario['name']}...")
        
        objects_to_place = scenario["objects_to_place"]
        all_available_objects = objects_to_place + scenario["distractors"]
        
        # Get all unique pairs of indices from the objects we need to place
        object_index_pairs = list(itertools.combinations(range(len(objects_to_place)), 2))

        # This outer loop handles different sets of placements, e.g., ("left", "right")
        for loc_placement_idx, loc_names in enumerate(scenario["location_placements"]):
            loc_1_name, loc_2_name = loc_names
            loc_1_data = components["locations"][loc_1_name]
            loc_2_data = components["locations"][loc_2_name]
            
            plate_1 = DestInitState(
                name="plate", 
                init_state=Distribution(loc_1_data["coords"][0], loc_1_data["coords"][1])
            )
            plate_2 = DestInitState(
                name="plate", 
                init_state=Distribution(loc_2_data["coords"][0], loc_2_data["coords"][1])
            )

            for bg_idx, background in enumerate(scenario["backgrounds"]):
                for obj_pair_indices in object_index_pairs:
                    obj_1_idx, obj_2_idx = obj_pair_indices
                    
                    # Generate a unique task ID
                    task_id = (scenario['base_id'] +
                               loc_placement_idx * 1000 +
                               bg_idx * 100 +
                               obj_1_idx * 10 +
                               obj_2_idx)
                    
                    obj_1_name = objects_to_place[obj_1_idx]
                    obj_2_name = objects_to_place[obj_2_idx]
                    
                    # Create the list of all ObjectInitState instances for this task
                    task_objects = []
                    for i, obj_name in enumerate(all_available_objects):
                        dest = None
                        if i == obj_1_idx:
                            dest = plate_1
                        elif i == obj_2_idx:
                            dest = plate_2
                        task_objects.append(ObjectInitState(name=obj_name, dest=dest))
                        
                    # Format the natural language instruction
                    lang = scenario["language_template"].format(
                        obj_1=obj_1_name.replace('_', ' '),
                        loc_1_nl=loc_1_data["nl"],
                        obj_2=obj_2_name.replace('_', ' '),
                        loc_2_nl=loc_2_data["nl"],
                    )

                    # Create the final task object
                    task = TaskInitState(
                        name=components["task_name"],
                        language_instruction=lang,
                        task_suite=scenario["task_suite"],
                        goal_type="On",
                        dests=[plate_1, plate_2],
                        objs=task_objects,
                        background=BackgroundInitState(name=background),
                        default_dist=components["default_dist"]
                    )
                    
                    # Generate BDDL and update mapping
                    generate_task_bddl(task, task_id)
                    id_task_mapping[task_id] = f"{background}_{components['task_name']}_{obj_1_name}_{obj_2_name}_on_{loc_1_name}_and_{loc_2_name}"

    return id_task_mapping


################################################################################
## 3. EXECUTION
################################################################################

if __name__ == "__main__":
    final_task_mapping = generate_tasks_from_scenarios(SCENARIOS, TASK_COMPONENTS)
    print("\n" + "="*50)
    print("Generated Task ID Mapping:")
    print("="*50)
    pprint(final_task_mapping)