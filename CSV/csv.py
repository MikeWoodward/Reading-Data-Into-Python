import datetime
import csv

FILENAME = ("""RollingSystemDemand-2025-01-13"""
            """T15_30_00.000Z-2025-01-14"""
            """T15_30_00.000Z.csv""")

# Read data in
consumed = []
with open(FILENAME,
          'r') as csvfile:
  electric_csv = csv.DictReader(
    csvfile,
    fieldnames=['code',
                'timestamp',
                'demand'])
  # Process every row
  for row in electric_csv:
    if row['code'] == "VD":
      consumed.append(
        {'time': (
          datetime
          .datetime
          .fromisoformat(row['timestamp'])),
        'demand': int(row['demand'])})

# Report max and min
c_max = max(consumed, key=lambda c: c['demand'])
c_min = min(consumed, key=lambda c: c['demand'])
print(f"Max at {c_max['time']} of {c_max['demand']}")
print(f"Min at {c_min['time']} of {c_min['demand']}")

# Output data
with open('output.csv', 'w') as csvfile:
  writer = csv.DictWriter(
    csvfile,
    fieldnames=['time', 'demand'],
    delimiter='|')
  writer.writeheader()
  for row in consumed:
    writer.writerow(row)
