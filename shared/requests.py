from dataclasses import dataclass

@dataclass
class PlayerAuthRequest:
  username: str
  password: str

@dataclass
class RconCommandRequest:
  rcon_command: str
  args: list

@dataclass
class RconAuthRequest:
  rcon_password: str

@dataclass
class Request:
  request: str
  data: object