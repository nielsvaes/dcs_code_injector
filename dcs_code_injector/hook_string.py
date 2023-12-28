hook_string = r"""
package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"
socket = require("socket")

DCSCI = {}
DCSCI.host = "*"
DCSCI.port = 45221
DCSCI.mission_load_complete = false

DCSCI.server = socket.bind(DCSCI.host, DCSCI.port)
DCSCI.server:settimeout(0)

local function init()
    log.write("DCS Code Injector", log.INFO, "Starting...")

    local handler = {}

    function handler.onMissionLoadEnd()
        log.write("DCS Code Injector -->", log.INFO, "Mission load complete, Code Injector Loaded")
        DCSCI.mission_load_complete = true
    end

    function handler.onSimulationFrame()
        if not DCSCI.mission_load_complete then
            return
        end
        local code_injector_client = DCSCI.server:accept()

        if code_injector_client then
            code_injector_client:settimeout(0)

            local chunk, err, partial
            local response = ""
            repeat
                chunk, err, partial = code_injector_client:receive()
                response = response .. (chunk or partial) .. "\n"
            until err or chunk == nil

            if response:len() > 1 then
                -- thanks for this, trampi
                local mission_string =
                [[
                    local ok, err = pcall(a_do_script(
                            [=[
                            ]]
                            .. response ..
                            [[
                            ]=]
                    ))
                    if not ok then
                        log.write("DCS Code Injector", log.ERROR, err)
                    end
                ]]

                net.dostring_in('mission', mission_string)
            end
        else
            return
        end
    end

    function handler.onSimulationStop()
        log.write("DCS Code Injector", log.INFO, "Simulation stopped, closing connection")
    end

    DCS.setUserCallbacks(handler)
    log.write("DCS Code Injector", log.INFO, "Load OK!")
end

local ok, err = pcall(init)
if not ok then
    log.write("DCS Code Injector", log.ERROR, "Error loading Code Injector: " .. tostring(err))
end
"""