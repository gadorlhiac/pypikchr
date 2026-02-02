# pypikchr
pypikchr is a small Python wrapper for the Pikchr diagramming language. It allows you to embed Pikchr diagrams within Python applications.

The goal is to eventually support the range of features available in pikchr, in a "Pythonic" way. See the [pikchr](https://pikchr.org/home/doc/trunk/doc/examples.md) docs for more information and examples.

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**. You can freely use, modify, and distribute the software under the terms of this license, but any modification must also be shared under the same license, and the source code must be made available to users interacting with the software over the network.

## Third-Party Dependencies

This project uses code from the following third-party libraries:

- **Pikchr**: Uses code from the Pikchr diagramming tool, which is licensed under the **Zero-Clause BSD License**.
- **LEMON**: Uses code from the LEMON parser generator, which is in the **public domain**.

### Third-Party Licenses

- **Pikchr** is licensed under the Zero-Clause BSD License, which allows you to freely use, modify, and distribute the software with no restrictions.
- **LEMON** is in the public domain, meaning there are no restrictions on its use.


## Installation
Install using pip:
```bash
pip install . [--prefix="/path/to/installation"]
```

## Basic Usage
Example for usage after installation.

### Construct basic sequences
```py
from pypikchr.diagram import *

# Create a diagram
d = Diagram(direction=Direction.down)

# Create some objects - the input string is the text you see in the shape
# Provide a label so it is easy to refer to it when chaining together
# Be careful! Labels must be capital letters!
b1: Box = Box("Box 1").label("B1")

# Can also adjust fill
c1: Circle = Circle("Circle 1").label("C1").fill("orange")

# Add shapes into the diagram
d.add(b1)
d.add(c1)

# Link shapes together
d.add(Arrow().from_pos(b1.s).to_pos(c1.n).dashed())

# Generated markdown
print(d.md)

# Generated SVG HTML
print(d)
```

The above script will print the following to console:
```
B1: box "Box 1";
C1: circle "Circle 1" fill orange;
arrow from b1.s to c1.n dashed
<svg xmlns='http://www.w3.org/2000/svg' class="" viewBox="0 0 112.32 148.32">
<path d="M2.16,74.16L110.16,74.16L110.16,2.16L2.16,2.16Z"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="56.16" y="38.16" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Box 1</text>
<circle cx="56.16" cy="110.16" r="36"  style="fill:rgb(255,165,0);stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="56.16" y="110.16" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Circle 1</text>
<path d="M56.16,74.16L56.16,74.16"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);stroke-dasharray:7.2,7.2;" />
</svg>

```


### Shapes

### Modifying Attributes







