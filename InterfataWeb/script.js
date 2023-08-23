function displayResultsTemp(res) {
    document.querySelector('pre.response1').innerHTML = JSON.stringify(`Temperatură: ${res.temperature}°C Umiditate: ${res.humidity}%`).slice(1,-1)
} 

function displayResultsHum(res) {
    document.querySelector('pre.response1').innerHTML = JSON.stringify(res.humidity)
} 

function displayResultsCarbon(res) {
    document.querySelector('pre.response2').innerHTML = JSON.stringify(res).slice(1,-1)
}

function moverRight(res){
    document.querySelector('pre.response3').innerHTML = JSON.stringify(res.message).slice(1,-1)
}

function moverLeft(res){
    document.querySelector('pre.response4').innerHTML = JSON.stringify(res.message).slice(1,-1)
}


function displayInformationTemp(){
    fetch('http://192.168.174.227:8000/api/v1.0/temp')
        .then(response => response.json())
        .then(json => displayResultsTemp(json))
}


function displayInformationCarbon(){
    fetch('http://192.168.174.227:8000/api/v1.0/carbon')
        .then(response => response.json())
        .then(json => displayResultsCarbon(json))
}

function moveMotorR(){
    fetch('http://192.168.174.227:8000/api/v1.0/motor')
        .then(response => response.json())
		.then(json => moverRight(json))
}

function moveMotorL(){
    fetch('http://192.168.174.227:8000/api/v1.0/motor-l')
        .then(response => response.json())
        .then(json => moverLeft(json))
}

