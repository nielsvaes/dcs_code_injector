package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"

DCSCI = {}
DCSCI.host = "localhost"
DCSCI.port = 40322
DCSCI.time = 0
DCSCI.closed = true
DCSCI.wait = 0.25
DCSCI.mission_load_complete = false


local function reinit_client()
    if DCSCI.client ~= nil then
        DCSCI.client:close()
    end
    DCSCI.client = socket.tcp()
    DCSCI.client:settimeout(0.0001)
    local success, err = DCSCI.client:connect(DCSCI.host, DCSCI.port)
    if success ~= nil then
        DCSCI.closed = false
    end
end

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

        if DCSCI.time + DCSCI.wait  < DCS.getModelTime() then
            if DCSCI.closed then
                reinit_client()
            end

            -- poke the server, let it know we want some data
            local total_bytes_sent, err, index_last_byte_sent = DCSCI.client:send('{"connection": "active"}')
            if total_bytes_sent == nil then --
                if err == "closed" or err == "timeout" or err == "Socket is not connected" then
                    DCSCI.closed = true
                end
            end

            local response = ""
            local chunk, err, partial
            repeat
                chunk, err, partial = DCSCI.client:receive()
                response = response .. (chunk or partial) .. "\n"
            until err or chunk == nil

            if response:len() > 1 then
                -- thanks for this, trampi
                local mission_string =
                [[
                    local ok, err = pcall(a_do_script(
                            [=[
                                --<SCRIPT>
                            ]=]
                    ))
                    if not ok then
                        log.write("DCS Code Injector", log.ERROR, err)
                    end
                ]]

                net.dostring_in('mission', mission_string:gsub("--<SCRIPT>", response))
            else
                if err == "closed" then
                    DCSCI.closed = true
                end
            end

            DCSCI.dcsci_time = DCS.getModelTime()
        end
    end

    function handler.onSimulationStop()
        log.write("DCS Code Injector", log.INFO, "Simulation stopped, closing connection")
        DCSCI.client:send('{"connection": "not_active"}')
        DCSCI.client:close()
        DCSCI.closed = true
    end

    DCS.setUserCallbacks(handler)
    log.write("DCS Code Injector", log.INFO, "Load OK!")
end

local ok, err = pcall(init)
if not ok then
    log.write("DCS Code Injector", log.ERROR, "Error loading Code Injector: " .. tostring(err))
end

