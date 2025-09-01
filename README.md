# 2D-and-3D-Floor-Planner
Using BSP Allocation, this code generates 2D and 3D floorplans from user input. Enter total house size and room sizes in natural language; the program automatically allocates rooms and draws labeled 2D and 3D floorplans with doors. Ideal for architects, students, and design enthusiasts to visualize layouts quickly. 

## Features

- Input **total house size** in sqft.
- Input **individual room sizes** in natural language.
- Automatically allocate rooms proportionally using BSP.
- Generate **2D floorplan** with labeled rooms and doors.
- Generate **3D floorplan** with labeled rooms and doors.
- Fully interactive: prompts user for room sizes at runtime.

---

## Installation

Make sure you have Python 3 installed. Then, install the required packages: 
```
pip install matplotlib
```

## Usage

1. Clone the repository:
```
git clone <your-repo-url>
cd <your-repo-folder>
``` 
2. Run the main script:
```
python main.py
```
3. Enter the total house size in sqft when prompted.

4. Describe your rooms in natural language (e.g., `2 bedrooms, 1 kitchen, 1 bathroom, 1 living room`).

5. Enter the size for each room when prompted.

6. The script will display:

   - A **2D floorplan** with labeled rooms and doors.
   - A **3D floorplan** with labeled rooms and doors.

---

## Example

```
Enter total house size in sqft: 1200
Describe rooms (e.g., '2 bedrooms, 1 kitchen, 1 bathroom, 1 living room'): 2 bedrooms, 1 kitchen, 1 bathroom, 1 living room
Enter size in sqft for Bedroom 1: 250
Enter size in sqft for Bedroom 2: 250
Enter size in sqft for Kitchen: 200
Enter size in sqft for Bathroom: 150
Enter size in sqft for Living Room: 350
```


The program will generate visual floorplans accordingly.

---

## Future Enhancements

- Add **windows and roofs** to 3D floorplans.
- Automatically detect **exterior walls** for window placement.
- Support for **furniture icons** in 2D/3D plans.
- Export floorplans as **images or PDFs**.

---

## License

MIT License 
