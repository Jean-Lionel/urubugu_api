var socket = new WebSocket(`http://10.42.0.253:8765/`);
socket.onopen = function(e) {
    console.log("[open] Connection established");
};
socket.onmessage = function(event) {
    console.log(event)

};
socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        console.log('[close] Connection died');
        console.log(`[close] ${JSON.stringify(event)}`);
    }
};
socket.onerror = function(error) {
    console.log(`[error] ${JSON.stringify(error)}`);
};
