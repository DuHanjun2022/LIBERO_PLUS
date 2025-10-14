from dataclasses import dataclass, field

from typing import List, Union, Tuple, Optional
import pprint


import numpy as np
import os
from libero.libero.envs.objects import get_object_dict, get_object_fn
from libero.libero.envs.predicates import get_predicate_fn_dict, get_predicate_fn
from libero.libero.utils.bddl_generation_utils import get_xy_region_kwargs_list_from_regions_info
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import register_task_info, get_task_info, generate_bddl_from_task_info


BDDL_FILE_PATH = "/home/leisongao/LIBERO/libero/libero/bddl_files/"


@dataclass
class Distribution:
    centroid: List[float]  # (x_min, y_min, x_max, y_max) in bddl
    loc_bounds: List[float]
    # rot: float = 0.0  # TODO: should we change the rotation to mutliple axes? currenlty LIBERO only supports yaw rotation
    rot_bounds: Tuple[float, float] = field(default_factory=lambda: (0, 2 * np.pi))


@dataclass
class DestInitState:
    name: Union[str, List[str]]
    init_state: Optional[Distribution] = None
    idx: int = None


# TODO: do we need to handle duplicates of objects?
@dataclass
class ObjectInitState:
    name: Union[str, List[str]]
    init_state: Optional[Distribution] = None
    dest: Optional[DestInitState] = None
    idx: int = None


@dataclass
class BackgroundInitState:
    name: Union[str, List[str]]
    # TODO: can we also modify lighting or other attributes?


@dataclass
class TableInitState:
    name: Union[str, List[str]]
    init_state: Optional[Distribution] = None


@dataclass
class GrabberInitState:
    name: Union[str, List[str]]
    # TODO: any other modifications?


@dataclass
class TaskInitState:
    name: str
    language_instruction: str
    task_suite: str
    goal_type: str
    dests: List[DestInitState]
    objs: List[ObjectInitState]
    background: BackgroundInitState
    default_dist: Distribution
    # table: TableInitState
    # grabber: GrabberInitState


# TODO: do we need to add host (named :target in bddl) object/location in the config?


def generate_task_bddl(task_init_state: TaskInitState, task_id: int):

    target_objs = []
    for obj in task_init_state.objs:
        if obj.dest:
            target_objs.append(obj)
    target_objs = sorted(target_objs, key=lambda obj: obj.name)  # sorted to avoid aliasing


    scene_name = f"{task_init_state.background.name}_{task_init_state.name}_scene{task_id}"


    class_name = f"{task_init_state.background.name.capitalize()}_{''.join(task_init_state.name)}Scene{task_id}"

    language = task_init_state.language_instruction


    if task_init_state.background.name == "floor":
        workspace = "floor"
    else:
        workspace = task_init_state.background.name + "_table"

    print(f"scene: {scene_name}")
    print(f"class: {class_name}")
    print(f"lang: {language}")

    @register_mu(scene_type=task_init_state.background.name, name_override=class_name)
    class DummyClass(InitialSceneTemplates):
        def __init__(self):
            fixture_num_info = {
                workspace: 1,
            }

            object_num_info = {}

            self.obj_list = task_init_state.dests + task_init_state.objs # + init_state.distractor_obj

            for obj in self.obj_list:
                if obj.name in object_num_info:
                    object_num_info[obj.name] += 1
                else:
                    object_num_info[obj.name] = 1
                
                obj.idx = object_num_info[obj.name]

            # pprint.pprint(self.obj_list)

            super().__init__(
                workspace_name=workspace,
                fixture_num_info=fixture_num_info,
                object_num_info=object_num_info
            )

        def define_regions(self):

            for obj in self.obj_list:
                if not obj.init_state:
                    obj.init_state = task_init_state.default_dist
                self.regions.update(
                    self.get_region_dict(region_centroid_xy=obj.init_state.centroid,
                                        region_name=f"{obj.name}_{obj.idx}_init_region", 
                                        target_name=self.workspace_name, 
                                        region_half_width=obj.init_state.loc_bounds[0],
                                        region_half_len=obj.init_state.loc_bounds[1],
                                        yaw_rotation=obj.init_state.rot_bounds)
                )
            
            self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)

        @property
        def init_states(self):
            states = []
            
            for obj in self.obj_list:
                obj_tup = ("On", f"{obj.name}_{obj.idx}", f"{workspace}_{obj.name}_{obj.idx}_init_region")
                states.append(obj_tup)
            
            return states
        

    goal_states = []

    # replicate code in class
    object_num_info = {}
    
    for obj in task_init_state.dests + task_init_state.objs:
        if obj.name in object_num_info:
            object_num_info[obj.name] += 1
        else:
            object_num_info[obj.name] = 1
        
        obj.idx = object_num_info[obj.name]
        

    for obj in target_objs:
        if task_init_state.goal_type == "On":
            obj_tup = (task_init_state.goal_type, f"{obj.name}_{obj.idx}", f"{obj.dest.name}_{obj.dest.idx}")
        else:
            obj_tup = (task_init_state.goal_type, f"{obj.name}_{obj.idx}", f"{obj.dest.name}_{obj.dest.idx}_contain_region")
        goal_states.append(obj_tup)

    # TODO: does obj of interest actually matter ... maybe it is for better sim
    # objs_of_interest = []

    # pprint.pprint(target_objs)

    # for obj in target_objs:
    #     objs_of_interest.append(obj.name + "_" + obj.idx)

    # for obj in task_init_state.dests:
    #     objs_of_interest.append(obj.name + "_" + obj.idx)

    register_task_info(language,
                       scene_name=scene_name,
                       objects_of_interest=[obj.name + "_1" for obj in target_objs],
                       goal_states=goal_states
    )

    folder = os.path.join(BDDL_FILE_PATH, task_init_state.task_suite)
    bddl_file_names, failures = generate_bddl_from_task_info(folder=folder)

    pprint.pprint(bddl_file_names)

    print("Encountered some failures: ", failures)

