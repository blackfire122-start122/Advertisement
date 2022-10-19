let img_advertisement = document.querySelector('#img_advertisement')
let advertisement_images = document.getElementsByClassName('img_advertisement')

let len_advertisement_images = advertisement_images.length

if (advertisement_images[0].complete){
    img_advertisement.src = advertisement_images[0].getAttribute('src')
    img_advertisement.value = 0
}else {
    advertisement_images[0].onload = () => {
        img_advertisement.src = advertisement_images[0].getAttribute('src')
        advertisement_images[0].onload = null
        img_advertisement.value = 0
    }
}

function previous_img(){
    if (0 < img_advertisement.value) {
        img_advertisement.value -= 1
        img_advertisement.src = advertisement_images[img_advertisement.value].getAttribute('src')
    }
}

function next_img(){
    if (len_advertisement_images-1 >= img_advertisement.value+1){
        img_advertisement.value += 1
        img_advertisement.src = advertisement_images[img_advertisement.value].getAttribute('src')

    }
}