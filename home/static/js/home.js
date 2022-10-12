let cities = document.querySelector('.cities')
let cities_img = document.querySelector('.cities_img')
function findOnCategory(e){

}

function cities_img_checks(){
    if (cities.style.display === 'block'){
        cities.style.display = 'none'
        cities_img.style.display = 'block'
    }else{
        cities.style.display = 'block'
        cities_img.style.display = 'none'
    }
}