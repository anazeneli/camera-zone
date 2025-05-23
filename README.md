# Module camera-zone 

Provide a description of the purpose of the module and any relevant information.

## Model azeneli:camera-zone:zone

Provide a description of the model and any relevant information.

### Configuration
The following attribute template can be used to configure this model:

```json
{
  "camera_name": "<string>",
  "zones": {
    "<ZONE_NAME_1>": [[<int>, <int>], [<int>, <int>], ...],
    "<ZONE_NAME_2>": [[<int>, <int>], [<int>, <int>], ...],
    ...
  },
  "zone_colors": {
    "<ZONE_NAME_1>": [<int>, <int>, <int>],
    "<ZONE_NAME_2>": [<int>, <int>, <int>],
    ...
  }
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `camera_name` | str    | Required  | Camera component name.     |
| `zones`       | dict   | Required  |A dictionary where each key is a string representing the zone name (e.g., "WAIT"). The value is a list of coordinates [[x1, y1], [x2, y2], ...] defining the vertices of the polygon for that zone. Each coordinate is a list of two integers [x, y]. |
| `zone_colors` | dict   | Required  | A dictionary where each key is a string representing the zone name (must match names in zones). The value is a list of three integers [R, G, B] representing the RGB color for that zone (e.g., [255, 0, 0] for red).


#### Example Configuration

```json
{
  "camera_name": "camera-1",
  "zones": {
    "WAIT": [
      [443, 590], [908, 480], [1405, 674], [1097, 811], [796, 842], [442, 591]
    ],
    "SUCCESS": [
      [889, 473], [994, 425], [1867, 705], [1607, 952], [1349, 797], [1406, 673], [899, 473]
    ],
    "ABANDON": [
      [406, 582], [98, 660], [336, 1053], [1628, 1062], [1767, 945], [1374, 770], [1106, 843], [800, 874], [407, 584]
    ],
    "ENTER": [
      [750, 899], [755, 791], [1108, 773], [1142, 897], [749, 913]
    ]
  },
  "zone_colors": {
    "SUCCESS": [0, 255, 0],
    "ABANDON": [255, 0, 0],
    "ENTER": [0, 0, 255],
    "WAIT": [255, 255, 0]
  }
}
```

### GetImage

Returns a Viam Image with the zones drawn on mapped to the colors in zone_colors 

