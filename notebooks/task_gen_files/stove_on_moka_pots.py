from gen_utils import generate_task_bddl
from gen_utils import ObjectInitState, TaskInitState, DestInitState, BackgroundInitState, Distribution

from pprint import pprint
"""
This is the tasks with moka pots

KITCHEN_SCENE8_put_both_moka_pots_on_the_stove
KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it

We extend the difficulty by modifying the receptacle location, and adding distractor objects

Eval set uses held out mug that has not been manipulated before

"""

# create separate task suite for eval set?
task_name = "mug_plate"
train_backgrounds = ["living_room", "kitchen", "floor"]
eval_backgrounds = ["study"]

train_objs = ["porcelain_mug", "white_yellow_mug"]
distractor_objs = ["cookies", "chocolate_pudding"]
eval_objs = ["porcelain_mug", "white_yellow_mug", "red_coffee_mug"]

plate_locs = [
    (
        ([-0.025, 0.15], [0.175, 0.15]), 
        ([-0.025, -0.15], [0.175, 0.15]),
        "left", 
        "right"
    ), # left right
    (
        ([-0.1, 0.0], [0.1, 0.3]), 
        ([0.075, 0.0], [0.075, 0.3]), 
        "close", 
        "far"
    ) # far close
]





id_task_mapping = {}

train = True

if train:
    task_suite = "libero_10_random_temp"
    objects = train_objs
    backgrounds = train_backgrounds
else:
    task_suite = "custom_eval_easy_temp"
    objects = eval_objs
    backgrounds = train_backgrounds + eval_backgrounds

for background_idx, background in enumerate(backgrounds):
    for loc_idx, (plate_1_loc, plate_2_loc, plate_1_nl, plate_2_nl) in enumerate(plate_locs):
        for obj_1_idx in range(len(objects)):
            for obj_2_idx in range(len(objects)):
                if obj_1_idx <= obj_2_idx:
                    continue
                    

                task_id =  10_000 * (2 - int(train)) + loc_idx * 1_000 + background_idx * 100 + obj_1_idx * 10 + obj_2_idx
                # we create task id 10_000 is for train task suite, 20_000 for easy_eval, 30_000 for hard_eval
                # 1_000 is for different task setups
                # 100 for background, 10 for obj_1, 1 for obj_2 idx

                obj_1 = objects[obj_1_idx]
                obj_2 = objects[obj_2_idx]

                id_task_mapping[task_id] = f"{background}_{task_name}_{obj_1}_{obj_2}"

                objs = []
                all_objs = objects + distractor_objs

                plate_1 = DestInitState(name="plate", 
                                    init_state=Distribution(
                                        plate_1_loc[0],
                                        plate_1_loc[1],
                                    ))
            
                plate_2 = DestInitState(name="plate", 
                                    init_state=Distribution(
                                        plate_2_loc[0],
                                        plate_2_loc[1],
                                    ))

                for obj in all_objs:
                    obj_dest = None
                    if obj == obj_1:
                        obj_dest = plate_1
                    elif obj == obj_2:
                        obj_dest = plate_2

                    objs.append(ObjectInitState(name=obj, dest=obj_dest))

                target_phrases = []

                lang = f"put the {obj_1.replace('_', ' ')} on the {plate_1_nl} plate and the {obj_2.replace('_', ' ')} on the {plate_2_nl} plate"

                task = TaskInitState(
                    name=task_name,
                    language_instruction=lang,
                    task_suite=task_suite,
                    goal_type="On",
                    dests=[
                        plate_1,
                        plate_2,
                    ],
                    objs=objs,
                    background=BackgroundInitState(name=background),
                    default_dist=Distribution([-0.025, 0.0], [0.175, 0.3])
                )
                
                
                generate_task_bddl(task, task_id)



pprint(f"\nTask ID mapping:\n{id_task_mapping}")


########### TRAIN
# ['/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/LIVING_ROOM_MUG_PLATE_SCENE10010_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/LIVING_ROOM_MUG_PLATE_SCENE11010_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/KITCHEN_MUG_PLATE_SCENE10110_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/KITCHEN_MUG_PLATE_SCENE11110_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/FLOOR_MUG_PLATE_SCENE10210_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random_temp/FLOOR_MUG_PLATE_SCENE11210_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl']
# Encountered some failures:  []
# ('\n'
#  'Task ID mapping:\n'
#  "{10010: 'living_room_mug_plate_white_yellow_mug_porcelain_mug', 11010: "
#  "'living_room_mug_plate_white_yellow_mug_porcelain_mug', 10110: "
#  "'kitchen_mug_plate_white_yellow_mug_porcelain_mug', 11110: "
#  "'kitchen_mug_plate_white_yellow_mug_porcelain_mug', 10210: "
#  "'floor_mug_plate_white_yellow_mug_porcelain_mug', 11210: "
#  "'floor_mug_plate_white_yellow_mug_porcelain_mug'}")



############## EVAL
# ['/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE20010_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE20020_put_the_red_coffee_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE20021_put_the_red_coffee_mug_on_the_left_plate_and_the_white_yellow_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE21010_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE21020_put_the_red_coffee_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/LIVING_ROOM_MUG_PLATE_SCENE21021_put_the_red_coffee_mug_on_the_close_plate_and_the_white_yellow_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE20110_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE20120_put_the_red_coffee_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE20121_put_the_red_coffee_mug_on_the_left_plate_and_the_white_yellow_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE21110_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE21120_put_the_red_coffee_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/KITCHEN_MUG_PLATE_SCENE21121_put_the_red_coffee_mug_on_the_close_plate_and_the_white_yellow_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE20210_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE20220_put_the_red_coffee_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE20221_put_the_red_coffee_mug_on_the_left_plate_and_the_white_yellow_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE21210_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE21220_put_the_red_coffee_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/FLOOR_MUG_PLATE_SCENE21221_put_the_red_coffee_mug_on_the_close_plate_and_the_white_yellow_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE20310_put_the_white_yellow_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE20320_put_the_red_coffee_mug_on_the_left_plate_and_the_porcelain_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE20321_put_the_red_coffee_mug_on_the_left_plate_and_the_white_yellow_mug_on_the_right_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE21310_put_the_white_yellow_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE21320_put_the_red_coffee_mug_on_the_close_plate_and_the_porcelain_mug_on_the_far_plate.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/custom_eval_easy_temp/STUDY_MUG_PLATE_SCENE21321_put_the_red_coffee_mug_on_the_close_plate_and_the_white_yellow_mug_on_the_far_plate.bddl']
# Encountered some failures:  []
# ('\n'
#  'Task ID mapping:\n'
#  "{20010: 'living_room_mug_plate_white_yellow_mug_porcelain_mug', 20020: "
#  "'living_room_mug_plate_red_coffee_mug_porcelain_mug', 20021: "
#  "'living_room_mug_plate_red_coffee_mug_white_yellow_mug', 21010: "
#  "'living_room_mug_plate_white_yellow_mug_porcelain_mug', 21020: "
#  "'living_room_mug_plate_red_coffee_mug_porcelain_mug', 21021: "
#  "'living_room_mug_plate_red_coffee_mug_white_yellow_mug', 20110: "
#  "'kitchen_mug_plate_white_yellow_mug_porcelain_mug', 20120: "
#  "'kitchen_mug_plate_red_coffee_mug_porcelain_mug', 20121: "
#  "'kitchen_mug_plate_red_coffee_mug_white_yellow_mug', 21110: "
#  "'kitchen_mug_plate_white_yellow_mug_porcelain_mug', 21120: "
#  "'kitchen_mug_plate_red_coffee_mug_porcelain_mug', 21121: "
#  "'kitchen_mug_plate_red_coffee_mug_white_yellow_mug', 20210: "
#  "'floor_mug_plate_white_yellow_mug_porcelain_mug', 20220: "
#  "'floor_mug_plate_red_coffee_mug_porcelain_mug', 20221: "
#  "'floor_mug_plate_red_coffee_mug_white_yellow_mug', 21210: "
#  "'floor_mug_plate_white_yellow_mug_porcelain_mug', 21220: "
#  "'floor_mug_plate_red_coffee_mug_porcelain_mug', 21221: "
#  "'floor_mug_plate_red_coffee_mug_white_yellow_mug', 20310: "
#  "'study_mug_plate_white_yellow_mug_porcelain_mug', 20320: "
#  "'study_mug_plate_red_coffee_mug_porcelain_mug', 20321: "
#  "'study_mug_plate_red_coffee_mug_white_yellow_mug', 21310: "
#  "'study_mug_plate_white_yellow_mug_porcelain_mug', 21320: "
#  "'study_mug_plate_red_coffee_mug_porcelain_mug', 21321: "
#  "'study_mug_plate_red_coffee_mug_white_yellow_mug'}")