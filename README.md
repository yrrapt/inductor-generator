# Inductor Generator

A generalised inductor design and analysis toolset. It is largely a
collection of other freely available tools.

![Stackup](metal_stackup.svg)

## Tools

The tools supported are:

 - ASITIC - Berkeley RFIC inductor generator and analysis. Supports output to CIF file. As the program is very old (circa 2000) this is run in an i386 Docker image

  - OpenEMS - To be completed...

## File Formats

A generalised description of the Skywater 130nm stack up is provided
in the `sky130_stackup.yaml` file.

Python scripts convert this to the various formats required for tools such as:

 - ASITIC
 - OpenEMS