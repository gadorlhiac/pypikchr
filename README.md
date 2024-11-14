# pypikchr

## Installation
Install using the provide setup file using pip or directly:
```bash
#pip install .
python setup.py install
```

## Basic Usage
Example for usage after installation.

### Construct basic sequences
```py
from pypikchr.diagram import *

d: Diagram = Diagram(shape=Box("")>>Dot()>>Box(""))
print(d)
```

Above will output:
```bash
<svg xmlns='http://www.w3.org/2000/svg' class="" viewBox="0 0 220.32 76.32">
<path d="M2.16,74.16L110.16,74.16L110.16,2.16L2.16,2.16Z"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="56.16" y="38.16" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central"></text>
<path d="M110.16,74.16L218.16,74.16L218.16,2.16L110.16,2.16Z"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="164.16" y="38.16" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central"></text>
</svg>
```

### Shapes

### Modifying Attributes
