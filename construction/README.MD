# Construction

The construction is split up in many subassemblies and groups, which are featured and explained below.

## General information

### Naming system

In order to keep the project clean, the filesystem for the construction has a strict naming scheme. 

- Assemblies are referenced with an "a" prefix. Depending on the type of assembly a number can be added:
  - The main assembly has no number (e.g. "a_drake")
  - Subassemblies have a number attached to them (e.g. "a1_frame")
  - There can be subassemblies of subassemblies (e.g. "a1.1_frame_base")
- Standard parts have an "n{part-number}_" prefix
  - They are placed in a "standard" directory
- Modified parts (standard parts with modifications) have an "m{part-number}_" prefix
  - They are placed in a "modified" directory
- Custom parts just have their part number as prefix "{part-number}_"
  - They are placed into the assembies root

### Orientation



## Subassemblies

The important rule about subassemblies is, that they should always work on their own. This can of course mean that standard parts can be found multiple times in a construction.
The user interface has been kept as simple as possible, a button to start the process and an emergency-halt in case something goes wrong.

- [[A1] Frame](./a1_frame/): Base aluminium frame
- [[A2] Y-Axis](./a2_yaxis/): Y-Axis without the drawing head
- [[A3] Sideaxis](./a3_sideaxis/): Sideaxes used to move the `Y-Axis` in Z direction
- [[A4] Drawing Table](./a4_paper/): Drawing table with servos and clamps
- [[A5] Head](./a5_head/): A simple head used to track the user while drawing for more interaction
- [[A6] Arm](./a6_arm/): Both arms, one equipped with a camera
- [[A7] Pen mount](./a7_pen_mount/): Drawing head with pen mount
- [[A8] User terminal](./a8_user_terminal/): User terminal with buttons to interact with the machine
- [[A9] Trunk](./a9_trunk/): Trunk with the electronics inside

## Groups

- [[C1] Front cover](./c1_cover_front/): Cover parts used in the front
- [[C2] Octagon cover](./c2_cover_octagon/): Cover parts placed around the octagon

## [Misc](./m_misc/)

Remaining parts that do not fit in a group or subassembly