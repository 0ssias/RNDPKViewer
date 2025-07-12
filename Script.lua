local socket = require("socket.core")
local host, port = "127.0.0.1", 5000
local client = assert(socket.connect(host, port))
client:settimeout(0)

emu.registerafter(function()
  local species = memory.readwordunsigned(0x0229688C)
  client:send(string.format("%d\n", species))
end)