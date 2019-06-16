# mgt2-inventory-generator
A simple script that generates the inventory for a trade supplier in Mongoose Traveller 2E, that can optionally take a broker modifier to provide prices.

```python inventorygen.py X62723A-8 16```

The inventory generator requires two arguments:

### The World Profile. 
This is the 9-character code described on page 217 of the core rulebook that has the following format:
```<1234567-8>```
The code must be entered in this format (including the hyphen). The program uses this to determine the available trade goods on the planet, as well as any relevant purchase modifiers.

### The Broker Roll
This is the modified broker roll described on page 211. Players should make this roll by doing the following:
- Rolling 3d6 and summing the result
- Adding the player's (or local broker's) Broker skill to the result (or -3 + jack of all trades if no one has it)
- Adding or subtracting a DM from the supplier
The purchase DM and sale for each good is applied by the program.

## Output

The program outputs the available goods for purchase into a CSV (using comma as separator) with a name e.g. tradegoods_X62723A-8.csv. The quantity of available goods and the price to purchase and to sell is calculated.  It also determines the 'random' inventory (1-6 trade goods that don't appear on that planet), so the program can be executed multiple times if multiple inventories are desired. The command line will output the names of the random goods.

From there, put the output into a spreadsheet program and use that for any further calculations!