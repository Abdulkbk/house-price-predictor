// Getting the form values
const form = document.querySelector('#form')

const bedrooms = document.querySelector('#bedrooms')
const bathrooms = document.querySelector('#bathrooms')
const toilets = document.querySelector('#toilets')
const parking_space = document.querySelector('#space')
const title = document.querySelector('#title')
const town = document.querySelector('#town')
const state_ = document.querySelector('#state')

const close_btn = document.querySelector('.close')
const price_box = document.querySelector('#price')
close_btn.addEventListener('click', handleClose)

// Getting the displayed data
let price_tag = document.querySelector('#price-val')

let n_bedrooms = document.querySelector('#d_bedrooms')
let n_bathrooms = document.querySelector('#d_bathrooms')
let n_toilets = document.querySelector('#d_toilets')
let n_parking_space = document.querySelector('#d_parking')
let n_title = document.querySelector('#d_title')
let n_town = document.querySelector('#d_town')
let n_state_ = document.querySelector('#d_state')

// Restricting refresh
form.addEventListener('submit', e => {
    e.preventDefault()
    handleDisplay()

    sendReq('/predict').then(data => {
        const abs_price = Math.abs(data.price) / 10
        let price = Intl.NumberFormat('en-US').format(abs_price)

        price_tag.innerHTML = `NGN ${price}`

        price_box.className = 'price'
    })
})

function handleDisplay() {
    n_bedrooms.innerHTML = bedrooms.value
    n_bathrooms.innerHTML = bathrooms.value
    n_toilets.innerHTML = toilets.value
    n_parking_space.innerHTML = parking_space.value
    n_title.innerHTML = title.value
    n_town.innerHTML = town.value
    n_state_.innerHTML = state_.value
}

function handleClose() {
    price_box.className = 'hidden'
}

url = "/predict"

async function sendReq(url = "", data = {}) {

    // sending form data using fetch
    data = {
        'bedrooms': bedrooms.value,
        'bathrooms': bathrooms.value,
        'toilets': toilets.value,
        'parking_space': parking_space.value,
        'title': title.value,
        'town': town.value,
        'state': state_.value
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    return response.json()
}

