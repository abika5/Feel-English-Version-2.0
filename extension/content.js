//Detecting the click of java,nullpointerexception
links = document.getElementsByClassName("post-tag");
for (i = 0; i < links.length; i++)
{
  	links[i].addEventListener("click", function(e)
  	{
	chrome.runtime.sendMessage({
		method: 'POST',
		action: 'xhttp',
		url: 'http://127.0.0.1:5000/logactions',
		data: {content:e.target.href,action:"tag interaction"}
	});
});
}
//Detecting the search tab 
var inputs = document.getElementsByName('q');
for (i = 0; i < inputs.length; i++)
{
  inputs[i].addEventListener('input', function(e)
  {
	chrome.runtime.sendMessage({
		method: 'POST',
		action: 'xhttp',
		url: 'http://127.0.0.1:5000/logactions',
		data: {content:"search tab interaction",action:"search tab interaction"}
	});
});
}
//Job Search interaction
var someButton=document.getElementById("nav-jobs");
someButton.addEventListener("click",function(button){
	chrome.runtime.sendMessage({
    method: 'POST',
    action: 'xhttp',
    url: 'http://127.0.0.1:5000/logactions',
    data: {content:button.target.href,action:"Job search interaction"}
});
})
//Detecting Asking a question interaction
data = document.getElementsByClassName("btn-outlined");
for (i = 0; i < data.length; i++)
{
  	data[i].addEventListener("click", function(e)
  	{
	chrome.runtime.sendMessage({
		method: 'POST',
		action: 'xhttp',
		url: 'http://127.0.0.1:5000/logactions',
		data: {content:e.target.href,action:"Ask question interaction"}
	});
});
}
//Detecting question click
questionlinks = document.getElementsByClassName("question-hyperlink");
for (i = 0; i < questionlinks.length; i++)
{
  	questionlinks[i].addEventListener("click", function(e)
  	{
	chrome.runtime.sendMessage({
		method: 'POST',
		action: 'xhttp',
		url: 'http://127.0.0.1:5000/logactions',
		data: {content:e.target.href,action:"view question interaction"}
	});
});
}