let cities = document.querySelector('.cities')
let cities_img = document.querySelector('.cities_img')
let advertisements = document.querySelector('.advertisements')
let find_advertisement = document.querySelector('#find_advertisement')
let companies = document.querySelector('.companies')
let companies_img = document.querySelector('.companies_img')
let findCompanies = document.querySelector('.findCompanies')
let find_company = document.getElementById('find_company')

let categories = []
let inputs_city = cities.getElementsByTagName('input')
let inputs_companies = companies.getElementsByTagName('input')

function cities_img_checks(){
    if (cities.style.display === 'block'){
        cities.style.display = 'none'
        cities_img.style.display = 'block'
    }else{
        cities.style.display = 'block'
        cities_img.style.display = 'none'
    }
}

function companies_img_checks(){
    if (findCompanies.style.display === 'block'){
        findCompanies.style.display = 'none'
        companies_img.style.display = 'block'
    }else{
        findCompanies.style.display = 'block'
        companies_img.style.display = 'none'
    }
}

function AvertisementFilter(){
    let params = "find_on_text="+find_advertisement.value

    for (let i = inputs_city.length-1; i>=0; i--){
        if (inputs_city[i].checked){
            params+="&cities="+inputs_city[i].value
        }
    }

    for (let i = inputs_companies.length-1; i>=0; i--){
        if (inputs_companies[i].checked){
            params+="&companies="+inputs_companies[i].value
        }
    }



    for (let i = categories.length-1; i>=0; i--){
        params+="&categories="+categories[i].id.replace('category_','')
    }

    let xhttp = new XMLHttpRequest()

    xhttp.open("GET", avertisementFilter+"?"+params, true);
    xhttp.onload = (e) => {
        advertisements.innerHTML = e.currentTarget.response
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

function CompanyFilter(){
    let xhttp = new XMLHttpRequest()
    let params = "find_on_name="+find_company.value

    xhttp.open("GET", companiesFilter+"?"+params, true);
    xhttp.onload = (e) => {
        companies.innerHTML = e.currentTarget.response
    }
    xhttp.onerror = () => {
        console.log('error')
    }
    xhttp.send()
}

AvertisementFilter()
CompanyFilter()

