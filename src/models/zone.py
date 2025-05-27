import sys
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple, cast)

from typing_extensions import Self
from viam.components.camera import Camera   
from viam.media.video import NamedImage, ViamImage
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName, ResponseMetadata
from viam.proto.component.camera import GetPropertiesResponse
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes, struct_to_dict
from viam.media.utils.pil import viam_to_pil_image, pil_to_viam_image

import cv2 
import numpy as np
from PIL import Image


class Zone(Camera, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("azeneli", "camera-zone"), "zone")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Camera component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any required dependencies or optional dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Tuple[Sequence[str], Sequence[str]]: A tuple where the
                first element is a list of required dependencies and the
                second element is a list of optional dependencies
        """
        attrs = struct_to_dict(config.attributes)
        
        # Validate camera name
        if "camera_name" not in attrs or not isinstance(attrs["camera_name"], str):
            raise ValueError("camera is required and must be a string")
        
        # Validate user-defined field (zones)
        if "zones" not in attrs or not isinstance(attrs["zones"], dict):
            raise ValueError("zones is required and must be a dictionary of polygon list coordinates")
        
        # Validate user-defined field (zones)
        if "zone_colors" not in attrs or not isinstance(attrs["zones"], dict):
            raise ValueError("zone_colors is required and must be a dictionary of zone color lists of (r,g,b)")
        

        # Return implicit dependencies
        implicit_dependencies = [attrs["camera_name"]]

        return implicit_dependencies, [] 


    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        # self.config = config
        
        # Define the zones for detections
        # ["zone1": [[x,y],[x,y]...], "zone2": [..]
        attrs = struct_to_dict(config.attributes)

        # Safe to access zones directly since validate_config already checked it        
        self.zones = self.prepare_zones(attrs["zones"])       
        self.zone_colors = attrs["zone_colors"]   

        self.dependencies = dependencies
        config_dict = struct_to_dict(config.attributes)
        self.base_camera_name = config_dict["camera_name"] 


        return super().reconfigure(config, dependencies)


    def prepare_zones(self, zones):
        """
            Prepare and process zone data.

            Args:
                zones (dict): A dictionary where keys are zone names (str) and values are numpy arrays representing polygons.

            Returns:
                dict: Processed zones with the same structure.
        """ 
        # convert to numpy arrays
        for zone_name, polygon in zones.items():            
            zones[zone_name] = np.array(polygon)

        return zones


    async def draw_zones(self, frame: np.ndarray) -> np.ndarray:
        """ 
        Draw polygons specified in zones attribute.

        Args:
            frame (np.ndarray): The frame on which to draw the polygons.

        Returns:
            np.ndarray: The frame with the polygons drawn.
        """
        for zone_name, polygon in self.zones.items():
            color = self.zone_colors.get(zone_name, (255, 255, 255))  # Default to white if color not found
            cv2.polylines(frame, [polygon.astype(np.int32)], isClosed=True, color=color, thickness=2)
        return frame


    async def get_image(
        self,
        mime_type: str = "",
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> ViamImage:
        self.logger.error("`get_image` is not implemented")

        zone_camera = self.dependencies[Camera.get_resource_name(self.base_camera_name)]
        camera = cast(Camera, zone_camera)

        frame = await camera.get_image() 

        # Store the original mime_type before conversion
        original_mime_type = frame.mime_type

        # Convert image to numpy for drawing 
        # Convert to PIL Image
        pil_frame = viam_to_pil_image(frame)

        # Convert PIL Image to numpy array
        np_frame = np.array(pil_frame)
        # opencv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # convert to PIL 
        zone_frame = await self.draw_zones(np_frame)
        # Convert numpy array back to PIL Image
        zone_frame_pil = Image.fromarray(zone_frame)
        zone_frame_viam = pil_to_viam_image(zone_frame_pil, original_mime_type) 

        return zone_frame_viam
    

    async def get_images(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Tuple[List[NamedImage], ResponseMetadata]:
        self.logger.error("`get_images` is not implemented")
        raise NotImplementedError()

    async def get_point_cloud(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Tuple[bytes, str]:
        self.logger.error("`get_point_cloud` is not implemented")
        raise NotImplementedError()

    async def get_properties(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Camera.Properties:
        self.logger.error("`get_properties` is not implemented")
        raise NotImplementedError()

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

