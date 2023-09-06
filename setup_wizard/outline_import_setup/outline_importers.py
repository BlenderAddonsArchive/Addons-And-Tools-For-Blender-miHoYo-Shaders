# Author: michael-gh1

import os
import bpy

from abc import ABC, abstractmethod
from bpy.types import Operator, Context

from setup_wizard.outline_import_setup.outline_node_groups import OutlineNodeGroupNames
from setup_wizard.import_order import FESTIVITY_OUTLINES_FILE_PATH, NYA222_HONKAI_STAR_RAIL_OUTLINES_FILE_PATH, \
    NextStepInvoker, cache_using_cache_key, get_cache
from setup_wizard.domain.game_types import GameType


class GameOutlineImporterFactory:
    def create(game_type: GameType, blender_operator: Operator, context: Context):
        if game_type == GameType.GENSHIN_IMPACT.name:
            return GenshinImpactOutlineNodeGroupImporter(blender_operator, context)
        elif game_type == GameType.HONKAI_STAR_RAIL.name:
            return HonkaiStarRailOutlineNodeGroupImporter(blender_operator, context)
        else:
            raise Exception(f'Unknown {GameType}: {game_type}')


class GameOutlineNodeGroupImporter(ABC):
    @abstractmethod
    def import_outline_node_group(self):
        raise NotImplementedError


class GenshinImpactOutlineNodeGroupImporter(GameOutlineNodeGroupImporter):
    def __init__(self, blender_operator, context):
        self.blender_operator = blender_operator
        self.context = context

    def import_outline_node_group(self):
        if not bpy.data.node_groups.get(OutlineNodeGroupNames.FESTIVITY_GENSHIN_OUTLINES):
            outlines_file_path = FESTIVITY_OUTLINES_FILE_PATH
            cache_enabled = self.context.window_manager.cache_enabled
            inner_path = 'NodeTree'
            object_name = OutlineNodeGroupNames.FESTIVITY_GENSHIN_OUTLINES
            filepath = get_cache(cache_enabled).get(outlines_file_path) or self.blender_operator.filepath

            if not filepath:
                bpy.ops.genshin.import_outlines(
                    'INVOKE_DEFAULT',
                    next_step_idx=self.blender_operator.next_step_idx, 
                    file_directory=self.blender_operator.file_directory,
                    invoker_type=self.blender_operator.invoker_type,
                    high_level_step_name=self.blender_operator.high_level_step_name,
                    game_type=self.blender_operator.game_type,
                )
                return {'FINISHED'}
            bpy.ops.wm.append(
                filepath=os.path.join(filepath, inner_path, object_name),
                directory=os.path.join(filepath, inner_path),
                filename=object_name
            )
            if cache_enabled and filepath:
                cache_using_cache_key(get_cache(cache_enabled), outlines_file_path, filepath)
            
            NextStepInvoker().invoke(
                self.blender_operator.next_step_idx, 
                self.blender_operator.invoker_type,
                high_level_step_name=self.blender_operator.high_level_step_name,
                game_type=self.blender_operator.game_type,
            )

class HonkaiStarRailOutlineNodeGroupImporter(GameOutlineNodeGroupImporter):
    def __init__(self, blender_operator, context):
        self.blender_operator = blender_operator
        self.context = context

    def import_outline_node_group(self):
        if not bpy.data.node_groups.get(OutlineNodeGroupNames.NYA222_HSR_OUTLINES):
            outlines_file_path = NYA222_HONKAI_STAR_RAIL_OUTLINES_FILE_PATH
            cache_enabled = self.context.window_manager.cache_enabled
            inner_path = 'NodeTree'
            object_name = OutlineNodeGroupNames.NYA222_HSR_OUTLINES
            filepath = get_cache(cache_enabled).get(outlines_file_path) or self.blender_operator.filepath

            if not filepath:
                bpy.ops.genshin.import_outlines(
                    'INVOKE_DEFAULT',
                    next_step_idx=self.blender_operator.next_step_idx, 
                    file_directory=self.blender_operator.file_directory,
                    invoker_type=self.blender_operator.invoker_type,
                    high_level_step_name=self.blender_operator.high_level_step_name,
                    game_type=self.blender_operator.game_type,
                )
                return {'FINISHED'}
            bpy.ops.wm.append(
                filepath=os.path.join(filepath, inner_path, object_name),
                directory=os.path.join(filepath, inner_path),
                filename=object_name
            )
            if cache_enabled and filepath:
                cache_using_cache_key(get_cache(cache_enabled), outlines_file_path, filepath)

            NextStepInvoker().invoke(
                self.blender_operator.next_step_idx, 
                self.blender_operator.invoker_type,
                high_level_step_name=self.blender_operator.high_level_step_name,
                game_type=self.blender_operator.game_type,
            )