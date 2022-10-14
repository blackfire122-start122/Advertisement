let cities = document.querySelector('.cities')
let cities_img = document.querySelector('.cities_img')
let advertisements = document.querySelector('.advertisements')
let find_adversement = document.querySelector('#find_adversement')

let categories = []
let inputs_city = cities.getElementsByTagName('input')

function cities_img_checks(){
    if (cities.style.display === 'block'){
        cities.style.display = 'none'
        cities_img.style.display = 'block'
    }else{
        cities.style.display = 'block'
        cities_img.style.display = 'none'
    }
}

function AvertisementFilter(){
    let params = "find_on_text="+find_adversement.value

    for (let i = inputs_city.length-1; i>=0; i--){
        if (inputs_city[i].checked){
            params+="&cities="+inputs_city[i].value
        }
    }

    for (let i = categories.length-1; i>=0; i--){
        params+="&categories="+categories[i].id.replace('category_','')
    }

    let xhttp = new XMLHttpRequest()

    xhttp.open("GET", avertisementFilter+"?"+params, true);
    xhttp.onload = (e) => {
        advertisements.innerHTML = e.srcElement.response
    }
    xhttp.onerror = () => {
        console.log('error')
    }
    xhttp.send()
}

function AvertisementFilterOnCategory(e){
    if (categories.includes(e)){
        e.style.backgroundColor = ""
        categories.splice(categories.indexOf(e),1)
    }else{
        e.style.backgroundColor = "beige"
        categories.push(e)
    }
    AvertisementFilter()
}
