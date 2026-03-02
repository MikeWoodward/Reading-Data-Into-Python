import json
import numpy as np

if __name__ == "__main__":
    
  class DataEncoder(json.JSONEncoder):
    def default(self, obj):
      if isinstance(obj, np.ndarray):
        return obj.tolist()
      return json.JSONEncoder.default(
        self, obj)
    
  test_dict = {
    'name': 'James Bond',
    'age': 35,
    'code name': '007',
    'crypto index': np.array(
      [199, 45, 17, 11, 17])
    }
  with open('data.json', 'w') as file:
    json.dump(test_dict, 
              file, 
              cls=DataEncoder)
