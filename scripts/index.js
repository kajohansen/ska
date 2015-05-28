var socket = null;
var isopen = false;

var smbResult = document.getElementById("smbResult");
var execForm = document.getElementById("execForm");

window.onload = function() {
	
	socket = new WebSocket("ws://euserve.kajohansen.com:9000");
	socket.binaryType = "arraybuffer";
	
	socket.onopen = function() {
		console.log("Connected!");
		isopen = true;
	}
	
	socket.onmessage = function(e) {
		
		if (typeof e.data == "string") {
			
			// console.log("Text message received: " + e.data);
			
			var userData = JSON.parse(e.data);

			for(var i = 0; i < userData.length; i++) {
				smbResult.innerHTML += userData[i] + "<br>";
			}

		} else {
			console.warn("Did not receive s string.. ");
		}
	}
	
	socket.onclose = function(e) {
		console.log("Connection closed.");
		socket = null;
		isopen = false;
	}
};

execForm.onchange = function(event) {
	var i = event.target.options.selectedIndex;
	var action = event.target.options[i].value;
	
	if (action == "list-users" && isopen) {
		socket.send("list-users");
		console.info("Sendt action " + action);
	}
}

