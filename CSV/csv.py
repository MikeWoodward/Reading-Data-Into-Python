import datetime
import csv

FILENAME = ("""RollingSystemDemand-2025-11-24"""
            """T21_30_00.000Z-2025-11-25"""
            """T21_30_00.000Z.csv""")

# Read data in
consumed = []
with open(FILENAME,
          'r') as csvfile:
    electric_csv = csv.DictReader(csvfile,
                                  fieldnames=['RecordType',
                                              'StartTime',
                                              'Demand'])
    # Read in every row
    for row in electric_csv:
        if row['RecordType'] == "VD":
            consumed.append({
                'time': (datetime
                         .datetime
                         .fromisoformat(row['StartTime'])),
                'demand': int(row['Demand'])}
            )

# Report max and min
c_max = max(consumed, key=lambda c: c['demand'])
c_min = min(consumed, key=lambda c: c['demand'])
print(f"Max at {c_max['time']} of {c_max['demand']}")
print(f"Min at {c_min['time']} of {c_min['demand']}")

# Output data
with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile,
                            fieldnames=['time', 'demand'],
                            delimiter='|')
    writer.writeheader()
    for row in consumed:
        writer.writerow(row)
