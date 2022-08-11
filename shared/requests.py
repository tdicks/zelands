import jsons

class BaseRequest(object):
  def __init__(self):
    self.type = type(self).__name__

  def toJson(self):
    return jsons.dump(self)

  @staticmethod
  def fromJson(jsonstr):
    return jsons.load(jsonstr, type(self))

@dataclass
class PlayerAuthRequest(BaseRequest):
  username: str
  password: str

@dataclass
class RconCommandRequest(BaseRequest):
  command: str
  args: list

@dataclass
class RconAuthRequest(BaseRequest):
  password: str
