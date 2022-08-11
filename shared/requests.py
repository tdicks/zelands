import json
import jsonpickle

class BaseRequest(object):
  def __init__(self):
    self.type = type(self).__name__
    self.data = {}
    self.message = ""

  def toJson(self):
    return json.dumps(jsonpickle.encode(self))
  
  @staticmethod
  def fromJson(jsonstr):
    return jsonpickle.decode(jsonstr)
    
  
class PlayerAuthRequest(BaseRequest):
  def __init__(self):
    self.data = {
      "username": "",
      "password": ""
    }
    
class RconCommandRequest(BaseRequest):
  def __init__(self):
    self.data = {
      "command": "",
      "args": []
    }

class RconAuthRequest(BaseRequest):
  self __init__(self):
    self.data = {
      "password": ""
    }

