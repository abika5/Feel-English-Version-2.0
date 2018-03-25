var tabURL ="";

chrome.runtime.onMessage.addListener(function(request,sender,sendResponse){

	chrome.tabs.query({active: true, currentWindow: true}, 
     function(arrayOfTabs) {
       var activeTab = arrayOfTabs[0];
       tabURL = activeTab.url;
     });
	console.log(request.data['content']);
	var username = tabURL.slice(tabURL.length-3,tabURL.length);
	request.data["username"]=username; 
	console.log(request.data["username"]);
	console.log(JSON.stringify(request.data))
	if (request.action == "xhttp") {
        var xhttprequest = new XMLHttpRequest();
        var method = request.method ? request.method.toUpperCase() : 'GET';
        xhttprequest.onload = function() {
            callback(xhttprequest.responseText);
        };
        xhttprequest.onerror = function() {
            callback();
        };
        xhttprequest.open(method, request.url, true);
        if (method == 'POST') {
            xhttprequest.setRequestHeader('Content-Type', 'application/json');
        }
        xhttprequest.send(JSON.stringify(request.data));
        return true;
    }
})