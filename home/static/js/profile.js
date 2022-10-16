let advertisements = document.querySelector('.advertisements')

function AdvertisementUser(){
    let xhttp = new XMLHttpRequest()

    xhttp.open("GET", advertisementUser, true);
    xhttp.onload = (e) => {
        advertisements.innerHTML += e.srcElement.response
    }
    xhttp.onerror = (ev) => {
        console.log(ev)
    }
    xhttp.send()
}

AdvertisementUser()