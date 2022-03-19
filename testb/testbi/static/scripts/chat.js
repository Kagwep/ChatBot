// Collapsible
let loc = window.location
let wsStart = 'ws://'

if(loc.protocol == 'https'){
    wsStart = 'wss://'
}

let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)


var coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "How's it going?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}


firstBotMessage();

function getBotResponse(input) {
    let message = input;

    let data = {
        'message' : message
    }
    data = JSON.stringify(data)
    socket.send(data)
   
    res = '';
    if (res == res) {
        return res;
    }
 
}
// Retrieves the response
function getHardResponse(userText) {
    let botResponse = getBotResponse(userText);
    socket.onmessage = async function(e){
        console.log('message', e)
        let data = JSON.parse(e.data)
        let message1 = data['message']
        myGlobalVar = message1;
        botResponse = myGlobalVar;
        let botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';
        $("#chatbox").append(botHtml);
    
        document.getElementById("chat-bar-bottom").scrollIntoView(true);
        
    }

}

//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();
    console.log(userText);

    if (userText == "") {
        userText = "I love Code Palace!";
    }

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    setTimeout(() => {
        getHardResponse(userText);
    }, 1000)

}

// Handles sending text via button clicks
function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    //Uncomment this if you want the bot to respond to this buttonSendText event
    // setTimeout(() => {
    //     getHardResponse(sampleText);
    // }, 1000)
}

function sendButton() {
    getResponse();
    
}

function heartButton() {
    buttonSendText("Heart clicked!")
}
socket.onopen =  async function(e){
    console.log('open', e)
    $("#textInput").keypress(function (e) {
        if (e.which == 13) {
            getResponse();
        }
    });
}


socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}
// Press enter to send a message
