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

let startAdvertisement = 0
let endAdvertisement = MaxGetAjax

let startCompany = 0
let endCompany = MaxGetAjax

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

function createAdvertisements(data){
    let a = document.createElement('a')
    let img = document.createElement('img')
    let h2 = document.createElement('h2')

    a.className = 'advertisement'
    a.href = data['href']
    img.src = data['image']
    img.alt = data['header']
    h2.textContent = data['header'].slice(0,25)

    a.append(img)
    a.append(h2)

    advertisements.append(a)
}

function createCompanyElement(data){
    let div = document.createElement('div')
    let input = document.createElement('input')
    let img = document.createElement('img')
    let h4 = document.createElement('h4')

    div.className = 'company_check'
    input.type = "checkbox"
    input.value = data['pk']
    input.onchange = AdvertisementFilter

    img.src = data['logo']
    img.className = 'img_company'
    img.alt = 'img '+data['name']

    h4.textContent = data['name']

    div.append(input)
    div.append(img)
    div.append(h4)

    companies.append(div)
}

function AdvertisementGet(paramsAdd=''){
    let params = '?'
    params+="start="+startAdvertisement
    params+="&end="+endAdvertisement
    params+=paramsAdd

    let xhttp = new XMLHttpRequest()

    xhttp.open("GET", avertisementFilter+params, true);
    xhttp.onload = (e) => {
        let jsonData = JSON.parse(e.currentTarget.response)
        for (let i = jsonData.length-1; i >= 0 ; i--) {
            createAdvertisements(jsonData[i])
        }
        startAdvertisement += MaxGetAjax
        endAdvertisement += MaxGetAjax
    }
    xhttp.onerror = () => {
        console.log('error')
    }
    xhttp.send()
}

function AdvertisementFilter(clear=false){
    if (clear) {
        advertisements.innerHTML = ''
        get_or_filter_s = 'filter'
        startAdvertisement = 0
        endAdvertisement = MaxGetAjax
    }

    let params = "&find_on_text="+find_advertisement.value

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

    AdvertisementGet(params)
}

function AdvertisementFilterOnCategory(e){
    if (categories.includes(e)){
        e.style.backgroundColor = ""
        categories.splice(categories.indexOf(e),1)
    }else{
        e.style.backgroundColor = "beige"
        categories.push(e)
    }
    AdvertisementFilter(true)
}

function CompanyFilter(){
    let xhttp = new XMLHttpRequest()
    let params = "find_on_name="+find_company.value
    params+="&start="+startCompany
    params+="&end="+endCompany

    xhttp.open("GET", companiesFilter+"?"+params, true);
    xhttp.onload = (e) => {
        let jsonData = JSON.parse(e.currentTarget.response)
        for (let i = jsonData.length-1; i >= 0 ; i--) {
            createCompanyElement(jsonData[i])
        }
        startCompany += MaxGetAjax
        endCompany += MaxGetAjax
    }
    xhttp.onerror = () => {
        console.log('error')
    }
    xhttp.send()
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.addEventListener('scroll',scroll_advertisement)
companies.addEventListener('scroll',scroll_company)

let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

async function scroll_advertisement() {
	if (get_can){
	    if (window.scrollY+ window.innerHeight>=document.body.scrollHeight-500) {
            get_or_filter()
            get_can = false
            get_can_true()
        }
	}
}

async function scroll_company() {
	if (get_can){
	    if (companies.scrollTop+companies.clientHeight>=companies.scrollHeight-30) {
            CompanyFilter()
            get_can = false
            get_can_true()
        }
	}
}

let get_or_filter_s = 'get'

function get_or_filter(){
    if (get_or_filter_s === 'get'){
        AdvertisementGet()
    }else if (get_or_filter_s === 'filter'){
        AdvertisementFilter()
    }
}

get_or_filter()
CompanyFilter()
