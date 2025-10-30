#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Standard imports
import os
import json

# Third-party imports
import cv2
import numpy as np
from typing import Dict, List, Optional
from ultralytics.solutions.solutions import BaseSolution
from ultralytics.utils.plotting import Annotator


# In[2]:


class ParkingDetector(BaseSolution):
    """
    A class to detect parking occupancy status using predefined parking regions.
    - Inherit from BaseSolution for YOLO model support
    """
    def __init__(self, model, source, json_file):
        super().__init__(model=model, source=source) # initialize YOLO model via BaseSolution
        self.json_file = json_file
        self.line_width = 2

        # initialize parking regions(bboxes), target parking status, and color for bbox status visualization
        self.bboxes = self._load_bboxes()
        # print(os.path.exists('yolo11s.pt'))     # for debugging porpose
        # print(f"Loaded bboxes: {self.bboxes}")  # for debugging purpose

        self.target_status = self._init_target_status()
        self.colors = {
            'available': (0, 255, 0),   # green
            'occupied': (0, 0, 255),    # red
            'detection': (255, 0, 189)  # purple
        }

    def _load_bboxes(self) -> List[Dict]:
        try:
            with open(self.json_file) as f:
                spaces = json.load(f)
                if not isinstance(spaces, list):
                    raise ValueError("Invalid JSON format: Expected list of spaces")
                if len(spaces) == 0:
                    raise ValueError("No parking spaces found in JSON")
                return spaces
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {self.json_file}")

    def _init_target_status(self) -> Dict[str, int]:
        return {
            'occupied': 0, 
            'available': len(self.bboxes)
        }

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        self.target_status = self._init_target_status()
        results = self.model.predict(frame, verbose=False)
        detections = results[0].boxes.data.tolist()
        # print(f"Detection: {detections}") # for debugging purpose
        annotator = Annotator(frame, self.line_width)

        for bbox in self.bboxes:
            pts = np.array(bbox['points'], dtype=np.int32)
            occupied = self._is_occupied(frame, pts, detections, annotator)
            color = self.colors['occupied'] if occupied else self.colors['available']
            cv2.drawContours(frame, [pts], -1, color, 2)

            if occupied:
                self.target_status['occupied'] += 1
                # print(f"Occupied space at {pts}")  # for debugging purpose

        self.target_status['available'] = len(self.bboxes) - self.target_status['occupied']
        self._draw_analytics(frame)
        return frame        

    def _is_occupied(self, frame: np.ndarray, polygon: np.ndarray, detections: List, annotator) -> bool:
        """Check if any detection occupies the parking space"""
        for *xyxy, conf, cls in detections:              
            xc, yc = int((xyxy[0] + xyxy[2])/2), int((xyxy[1] + xyxy[3])/2)
            if cv2.pointPolygonTest(polygon, (xc, yc), False) >= 0: # +1 means the detection is inside the contour(bbox)
                cv2.circle(frame, (xc, yc), self.line_width*4, self.colors['detection'], -1)
                label = f"{self.model.names[int(cls)]} {conf:.2f}"
                annotator.box_label([xyxy[0], xyxy[1], xyxy[2], xyxy[3]], label, color=self.colors['detection'])                
                return True
        return False

    def _draw_analytics(self, frame: np.ndarray): # draw parking status on frame
        status_text = (f"Occupied: {self.target_status['occupied']} | "
                      f"Available: {self.target_status['available']}")
        cv2.putText(frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                   (0, 0, 0), 2)

